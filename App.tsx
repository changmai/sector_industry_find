
import React, { useState, useEffect, useMemo, useRef } from 'react';
import Header from './components/Header';
import FootprintTable from './components/FootprintTable';
import TickList from './components/TickList';
import { generateTick } from './services/mockDataService';
import { Tick, PriceLevelData, FootprintStats, Side, FootprintCandle } from './types';
import { CONFIG } from './constants';
import { calculateFootprintIndicators } from './utils';
import { Clock, BarChart2, MoveVertical } from 'lucide-react';

type RotationMode = 'VOLUME' | 'TIME' | 'RANGE';

const App: React.FC = () => {
  const [ticks, setTicks] = useState<Tick[]>([]);
  const [currentPrice, setCurrentPrice] = useState(CONFIG.INITIAL_PRICE);
  
  // --- Rotation Settings ---
  const [rotationMode, setRotationMode] = useState<RotationMode>('VOLUME');
  
  // Thresholds for each mode
  const [thresholds, setThresholds] = useState({
    VOLUME: 2000,
    TIME: 30, // seconds
    RANGE: 10 // ticks (e.g., 10 * 100 = 1000 price range)
  });
  
  // Temp input state for UI
  const [tempInput, setTempInput] = useState<string>("2000");

  // --- Sequential Footprint State ---
  const [historyBars, setHistoryBars] = useState<FootprintCandle[]>([]);
  const activeBarMap = useRef<Map<number, PriceLevelData>>(new Map());
  
  // Metadata for the active bar
  const [activeBarStats, setActiveBarStats] = useState<{
    id: number;
    startTime: string;
    timestamp: number; // Creation timestamp (ms) for Time-based rotation
    open: number;
    high: number;
    low: number;
    totalVolume: number;
    currentDelta: number;
    maxDelta: number;
    minDelta: number;
  }>({
    id: Date.now(),
    startTime: new Date().toTimeString().split(' ')[0],
    timestamp: Date.now(),
    open: CONFIG.INITIAL_PRICE,
    high: CONFIG.INITIAL_PRICE,
    low: CONFIG.INITIAL_PRICE,
    totalVolume: 0,
    currentDelta: 0,
    maxDelta: 0,
    minDelta: 0
  });

  // Update temp input when mode changes
  useEffect(() => {
    setTempInput(thresholds[rotationMode].toString());
  }, [rotationMode]);

  // --- Derived Stats for Header ---
  const headerStats: FootprintStats = useMemo(() => {
     if (ticks.length === 0) return { totalVolume: 0, cvd: 0, high: 0, low: 0, open: 0, close: 0 };
     const totalVol = ticks.reduce((acc, t) => acc + t.volume, 0);
     const buyVol = ticks.filter(t => t.side === Side.Buy).reduce((acc, t) => acc + t.volume, 0);
     const sellVol = ticks.filter(t => t.side === Side.Sell).reduce((acc, t) => acc + t.volume, 0);
     
     return {
         totalVolume: totalVol,
         cvd: buyVol - sellVol,
         high: Math.max(...ticks.map(t => t.price)),
         low: Math.min(...ticks.map(t => t.price)),
         open: ticks[ticks.length - 1].price, 
         close: currentPrice
     };
  }, [ticks, currentPrice]);

  // --- Calculate Global Y-Axis Range ---
  const { globalHigh, globalLow } = useMemo(() => {
    let highs: number[] = [];
    let lows: number[] = [];

    if (historyBars.length > 0) {
        highs.push(...historyBars.map(b => b.high));
        lows.push(...historyBars.map(b => b.low));
    }
    
    if (activeBarStats.totalVolume > 0) {
        highs.push(activeBarStats.high);
        lows.push(activeBarStats.low);
    }

    if (highs.length === 0) {
        return { globalHigh: CONFIG.INITIAL_PRICE + CONFIG.PRICE_STEP * 5, globalLow: CONFIG.INITIAL_PRICE - CONFIG.PRICE_STEP * 5 };
    }

    const max = Math.max(...highs);
    const min = Math.min(...lows);

    return {
        globalHigh: max + (CONFIG.PRICE_STEP * 2),
        globalLow: min - (CONFIG.PRICE_STEP * 2)
    };
  }, [historyBars, activeBarStats.high, activeBarStats.low]);


  // --- Main Tick Loop ---
  useEffect(() => {
    const interval = setInterval(() => {
      const newTick = generateTick();
      const now = Date.now();
      const nowStr = new Date(now).toTimeString().split(' ')[0];

      setCurrentPrice(newTick.price);
      
      setTicks(prevTicks => {
        const updated = [newTick, ...prevTicks];
        return updated.slice(0, 200); 
      });

      // --- Footprint Bar Logic ---
      
      // 1. Update Active Bar Map
      const currentMap = activeBarMap.current;
      const level: PriceLevelData = currentMap.get(newTick.price) || {
          price: newTick.price,
          buyVolume: 0,
          sellVolume: 0,
          totalVolume: 0,
          delta: 0,
          imbalanceBuy: false,
          imbalanceSell: false,
          stackedImbalanceBuy: false,
          stackedImbalanceSell: false,
          isPOC: false,
          isUnfinished: false
      };

      if (newTick.side === Side.Buy) level.buyVolume += newTick.volume;
      else level.sellVolume += newTick.volume;
      
      level.totalVolume += newTick.volume;
      level.delta = level.buyVolume - level.sellVolume;
      currentMap.set(newTick.price, level);

      // 2. Update Stats & Check Rotation
      const tickDelta = newTick.side === Side.Buy ? newTick.volume : -newTick.volume;

      setActiveBarStats(prev => {
        const newTotalVol = prev.totalVolume + newTick.volume;
        const newHigh = Math.max(prev.high, newTick.price);
        const newLow = Math.min(prev.low, newTick.price);
        
        const newCurrentDelta = prev.currentDelta + tickDelta;
        const newMaxDelta = Math.max(prev.maxDelta, newCurrentDelta);
        const newMinDelta = Math.min(prev.minDelta, newCurrentDelta);

        // --- ROTATION LOGIC ---
        let shouldRotate = false;

        if (rotationMode === 'VOLUME') {
            if (newTotalVol >= thresholds.VOLUME) shouldRotate = true;
        } 
        else if (rotationMode === 'TIME') {
            const elapsedSec = (now - prev.timestamp) / 1000;
            if (elapsedSec >= thresholds.TIME) shouldRotate = true;
        }
        else if (rotationMode === 'RANGE') {
            const rangeTicks = (newHigh - newLow) / CONFIG.PRICE_STEP;
            if (rangeTicks >= thresholds.RANGE) shouldRotate = true;
        }

        if (shouldRotate) {
             // Finalize Bar
             const processedLevels = calculateFootprintIndicators(currentMap);
             const finishedBar: FootprintCandle = {
                 id: prev.id,
                 startTime: prev.startTime,
                 endTime: nowStr,
                 open: prev.open,
                 close: newTick.price,
                 high: newHigh,
                 low: newLow,
                 totalVolume: newTotalVol,
                 delta: newCurrentDelta,
                 maxDelta: newMaxDelta,
                 minDelta: newMinDelta,
                 priceLevels: processedLevels
             };

             setHistoryBars(prevHistory => {
                 const newHistory = [...prevHistory, finishedBar];
                 return newHistory.slice(-20); 
             });

             activeBarMap.current = new Map(); // Clear
             
             // Reset
             return {
                 id: now,
                 startTime: nowStr,
                 timestamp: now,
                 open: newTick.price,
                 high: newTick.price,
                 low: newTick.price,
                 totalVolume: 0,
                 currentDelta: 0,
                 maxDelta: 0,
                 minDelta: 0
             };
        }

        return {
            ...prev,
            high: newHigh,
            low: newLow,
            totalVolume: newTotalVol,
            currentDelta: newCurrentDelta,
            maxDelta: newMaxDelta,
            minDelta: newMinDelta
        };
      });

    }, CONFIG.TICK_RATE_MS);

    return () => clearInterval(interval);
  }, [rotationMode, thresholds]); // Re-bind when mode/thresholds change

  const activeBarCandle: FootprintCandle | null = useMemo(() => {
      if (activeBarStats.totalVolume === 0 && activeBarMap.current.size === 0) return null;
      const processed = calculateFootprintIndicators(activeBarMap.current);
      return {
          id: activeBarStats.id,
          startTime: activeBarStats.startTime,
          open: activeBarStats.open,
          close: currentPrice,
          high: activeBarStats.high,
          low: activeBarStats.low,
          totalVolume: activeBarStats.totalVolume,
          delta: activeBarStats.currentDelta,
          maxDelta: activeBarStats.maxDelta,
          minDelta: activeBarStats.minDelta,
          priceLevels: processed
      };
  }, [activeBarStats, currentPrice]); 

  const handleThresholdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setTempInput(e.target.value);
  };
  
  const applySettings = () => {
      const val = parseInt(tempInput, 10);
      if (!isNaN(val) && val > 0) {
          setThresholds(prev => ({
              ...prev,
              [rotationMode]: val
          }));
      }
  };

  // Helper to get label and icon for current mode
  const getModeMeta = () => {
      switch (rotationMode) {
          case 'VOLUME': return { icon: <BarChart2 className="w-3 h-3 mr-1 text-kr-blue" />, label: 'Volume', unit: 'Vol' };
          case 'TIME': return { icon: <Clock className="w-3 h-3 mr-1 text-highlight" />, label: 'Time', unit: 'Sec' };
          case 'RANGE': return { icon: <MoveVertical className="w-3 h-3 mr-1 text-kr-red" />, label: 'Range', unit: 'Ticks' };
      }
  };
  const meta = getModeMeta();

  return (
    <div className="h-screen w-screen bg-dark-bg text-white flex flex-col overflow-hidden font-sans selection:bg-gray-700">
      <Header stats={headerStats} />
      
      <main className="flex-1 flex overflow-hidden p-1 gap-1">
        {/* Left Panel */}
        <div className="flex-[1] flex flex-col min-w-0">
            {/* Settings Toolbar */}
            <div className="flex items-center justify-between mb-1 px-2 bg-panel-bg py-1 rounded border border-border-color shrink-0">
                <div className="flex items-center space-x-4">
                    <div className="flex items-center">
                        <span className="w-2 h-2 rounded-full bg-kr-red mr-2 animate-pulse"></span>
                        <h2 className="text-xs font-bold text-gray-300">Footprint</h2>
                    </div>
                    
                    <div className="h-4 w-px bg-gray-700"></div>

                    {/* Rotation Controls */}
                    <div className="flex items-center space-x-2 text-[10px]">
                        <span className="text-gray-400 font-semibold">Type:</span>
                        <select 
                            value={rotationMode}
                            onChange={(e) => setRotationMode(e.target.value as RotationMode)}
                            className="bg-gray-800 border border-gray-600 text-white text-[10px] px-1 py-0.5 rounded outline-none focus:border-highlight cursor-pointer"
                        >
                            <option value="VOLUME">Volume</option>
                            <option value="TIME">Time</option>
                            <option value="RANGE">Range</option>
                        </select>

                        <div className="flex items-center pl-2">
                            {meta.icon}
                            <span className="text-gray-400 mr-1">{meta.label}:</span>
                            <input 
                                type="number" 
                                value={tempInput}
                                onChange={handleThresholdChange}
                                className="bg-gray-800 border border-gray-600 text-white px-1 py-0.5 rounded w-12 text-center focus:border-kr-blue outline-none"
                            />
                            <span className="text-gray-500 ml-1 mr-2">{meta.unit}</span>
                            <button 
                                onClick={applySettings}
                                className="bg-gray-700 hover:bg-gray-600 text-gray-200 px-2 py-0.5 rounded transition-colors border border-gray-600"
                            >
                                Set
                            </button>
                        </div>
                    </div>
                </div>

                <div className="flex space-x-2">
                    <span className="text-[10px] text-gray-500 bg-gray-800 px-2 py-0.5 rounded border border-gray-700 font-mono">
                        History: {historyBars.length}/20
                    </span>
                </div>
            </div>
            
            <FootprintTable 
                bars={historyBars} 
                activeBar={activeBarCandle}
                globalHigh={globalHigh}
                globalLow={globalLow}
            />
        </div>

        {/* Right Panel: Tick List */}
        <div className="w-[200px] flex flex-col min-w-0 flex-none border-l border-border-color">
            <TickList ticks={ticks} />
        </div>
      </main>
    </div>
  );
};

export default App;
