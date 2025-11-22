
import React, { useState, useEffect, useMemo, useRef } from 'react';
import Header from './components/Header';
import FootprintTable from './components/FootprintTable';
import TickList from './components/TickList';
import { generateTick } from './services/mockDataService';
import { Tick, PriceLevelData, FootprintStats, Side, FootprintCandle } from './types';
import { CONFIG } from './constants';
import { calculateFootprintIndicators } from './utils';

const App: React.FC = () => {
  const [ticks, setTicks] = useState<Tick[]>([]);
  const [currentPrice, setCurrentPrice] = useState(CONFIG.INITIAL_PRICE);
  
  // --- Settings ---
  const [volumeThreshold, setVolumeThreshold] = useState<number>(2000);
  const [tempThreshold, setTempThreshold] = useState<string>("2000");

  // --- Sequential Footprint State ---
  const [historyBars, setHistoryBars] = useState<FootprintCandle[]>([]);
  // We store the active bar's raw map to allow fast O(1) updates
  const activeBarMap = useRef<Map<number, PriceLevelData>>(new Map());
  // We store the active bar's metadata separately to avoid re-rendering everything constantly
  const [activeBarStats, setActiveBarStats] = useState<{
    id: number;
    startTime: string;
    open: number;
    high: number;
    low: number;
    totalVolume: number;
  }>({
    id: Date.now(),
    startTime: new Date().toTimeString().split(' ')[0],
    open: CONFIG.INITIAL_PRICE,
    high: CONFIG.INITIAL_PRICE,
    low: CONFIG.INITIAL_PRICE,
    totalVolume: 0
  });

  // --- Derived Stats for Header ---
  const headerStats: FootprintStats = useMemo(() => {
     if (ticks.length === 0) return { totalVolume: 0, cvd: 0, high: 0, low: 0, open: 0, close: 0 };
     // Global stats for the session
     const totalVol = ticks.reduce((acc, t) => acc + t.volume, 0);
     const buyVol = ticks.filter(t => t.side === Side.Buy).reduce((acc, t) => acc + t.volume, 0);
     const sellVol = ticks.filter(t => t.side === Side.Sell).reduce((acc, t) => acc + t.volume, 0);
     
     return {
         totalVolume: totalVol,
         cvd: buyVol - sellVol,
         high: Math.max(...ticks.map(t => t.price)),
         low: Math.min(...ticks.map(t => t.price)),
         open: ticks[ticks.length - 1].price, // Oldest tick
         close: currentPrice
     };
  }, [ticks, currentPrice]);

  // --- Calculate Global Y-Axis Range (Synchronization) ---
  const { globalHigh, globalLow } = useMemo(() => {
    let highs: number[] = [];
    let lows: number[] = [];

    if (historyBars.length > 0) {
        highs.push(...historyBars.map(b => b.high));
        lows.push(...historyBars.map(b => b.low));
    }
    
    // Include active bar
    if (activeBarStats.totalVolume > 0) {
        highs.push(activeBarStats.high);
        lows.push(activeBarStats.low);
    }

    if (highs.length === 0) {
        return { globalHigh: CONFIG.INITIAL_PRICE + CONFIG.PRICE_STEP * 5, globalLow: CONFIG.INITIAL_PRICE - CONFIG.PRICE_STEP * 5 };
    }

    const max = Math.max(...highs);
    const min = Math.min(...lows);

    // Add Padding (2 steps)
    return {
        globalHigh: max + (CONFIG.PRICE_STEP * 2),
        globalLow: min - (CONFIG.PRICE_STEP * 2)
    };
  }, [historyBars, activeBarStats.high, activeBarStats.low]);


  // --- Main Tick Loop ---
  useEffect(() => {
    const interval = setInterval(() => {
      const newTick = generateTick();
      const nowStr = new Date().toTimeString().split(' ')[0];

      setCurrentPrice(newTick.price);
      
      // Update Tape
      setTicks(prevTicks => {
        const updated = [newTick, ...prevTicks];
        return updated.slice(0, 200); // Limit tape history
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

      // 2. Update Active Bar Stats & Check Rotation
      setActiveBarStats(prev => {
        const newTotalVol = prev.totalVolume + newTick.volume;
        const newHigh = Math.max(prev.high, newTick.price);
        const newLow = Math.min(prev.low, newTick.price);

        // --- ROTATION TRIGGER ---
        if (newTotalVol >= volumeThreshold) {
             // A. Finalize Current Bar
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
                 delta: processedLevels.reduce((acc, l) => acc + l.delta, 0),
                 priceLevels: processedLevels
             };

             // B. Push to History (Max 20)
             setHistoryBars(prevHistory => {
                 const newHistory = [...prevHistory, finishedBar];
                 return newHistory.slice(-20); // Keep last 20
             });

             // C. Reset for New Bar
             activeBarMap.current = new Map(); // Clear map
             
             // Initialize next bar with the SAME tick price as open (gapless in sim)
             return {
                 id: Date.now(),
                 startTime: nowStr,
                 open: newTick.price,
                 high: newTick.price,
                 low: newTick.price,
                 totalVolume: 0 
             };
        }

        // Continue current bar
        return {
            ...prev,
            high: newHigh,
            low: newLow,
            totalVolume: newTotalVol
        };
      });

    }, CONFIG.TICK_RATE_MS);

    return () => clearInterval(interval);
  }, [volumeThreshold]); // Re-create interval if threshold changes

  // Prepare Active Bar Object for Rendering
  const activeBarCandle: FootprintCandle | null = useMemo(() => {
      if (activeBarStats.totalVolume === 0 && activeBarMap.current.size === 0) return null;
      
      return {
          id: activeBarStats.id,
          startTime: activeBarStats.startTime,
          open: activeBarStats.open,
          close: currentPrice,
          high: activeBarStats.high,
          low: activeBarStats.low,
          totalVolume: activeBarStats.totalVolume,
          delta: Array.from(activeBarMap.current.values()).reduce((acc, v) => acc + v.delta, 0),
          // Calculate indicators on the fly for the active bar
          priceLevels: calculateFootprintIndicators(activeBarMap.current) 
      };
  }, [activeBarStats, currentPrice]); // Updates on every tick roughly

  // Handler for Threshold Input
  const handleThresholdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setTempThreshold(e.target.value);
  };
  
  const applyThreshold = () => {
      const val = parseInt(tempThreshold, 10);
      if (!isNaN(val) && val > 0) {
          setVolumeThreshold(val);
          // Optional: Force rotate or reset could go here, but we just let the next tick handle it
      }
  };

  return (
    <div className="h-screen w-screen bg-dark-bg text-white flex flex-col overflow-hidden font-sans selection:bg-gray-700">
      <Header stats={headerStats} />
      
      <main className="flex-1 flex overflow-hidden p-2 gap-2">
        {/* Left Panel: Footprint Analysis */}
        <div className="flex-[3] flex flex-col min-w-0">
            <div className="flex items-center justify-between mb-2 px-1 bg-panel-bg p-2 rounded border border-border-color">
                <div className="flex items-center">
                    <h2 className="text-sm font-bold text-gray-300 flex items-center mr-4">
                        <span className="w-2 h-2 rounded-full bg-kr-red mr-2"></span>
                        Sequential Footprint
                    </h2>
                    
                    {/* Volume Threshold Controls */}
                    <div className="flex items-center space-x-2 text-xs">
                        <span className="text-gray-400">Rotation Vol:</span>
                        <input 
                            type="number" 
                            value={tempThreshold}
                            onChange={handleThresholdChange}
                            className="bg-gray-800 border border-gray-600 text-white px-2 py-1 rounded w-20 text-center focus:border-kr-blue outline-none"
                        />
                        <button 
                            onClick={applyThreshold}
                            className="bg-gray-700 hover:bg-gray-600 text-gray-200 px-3 py-1 rounded transition-colors"
                        >
                            Apply
                        </button>
                        <span className="text-gray-500 ml-2">(Current: {volumeThreshold})</span>
                    </div>
                </div>

                <div className="flex space-x-2">
                    <span className="text-[10px] text-gray-500 bg-gray-800 px-2 py-0.5 rounded border border-gray-700">
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
        <div className="flex-[1.5] flex flex-col min-w-0">
             <div className="flex items-center justify-between mb-2 px-1 py-2 bg-panel-bg rounded border border-border-color">
                <h2 className="text-sm font-bold text-gray-300 flex items-center">
                   <span className="w-2 h-2 rounded-full bg-highlight mr-2"></span>
                   Tape
                </h2>
            </div>
            <TickList ticks={ticks} />
        </div>
      </main>
    </div>
  );
};

export default App;
