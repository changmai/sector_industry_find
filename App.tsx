
import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import Header from './components/Header';
import FootprintTable from './components/FootprintTable';
import TickList from './components/TickList';
import StockCodeChangeDialog from './components/StockCodeChangeDialog';
import { generateTick } from './services/mockDataService';
import { loadRawData } from './services/rawDataService';
import { connectWebSocket, changeTargetCode } from './services/websocketDataService';
import { Tick, PriceLevelData, FootprintStats, Side, FootprintCandle } from './types';
import { CONFIG } from './constants';
import { calculateFootprintIndicators } from './utils';
import { groupPriceLevel, PRICE_GROUPING_OPTIONS, PriceGroupingOption } from './utils/priceGrouping';
import { Clock, BarChart2, MoveVertical, Layers } from 'lucide-react';

type RotationMode = 'VOLUME' | 'TIME' | 'RANGE';
type DataSource = 'mock' | 'raw' | 'websocket';

const App: React.FC = () => {
  const [ticks, setTicks] = useState<Tick[]>([]);
  const [currentPrice, setCurrentPrice] = useState(CONFIG.INITIAL_PRICE);

  // --- Stock Code Management ---
  const [targetCode, setTargetCode] = useState(CONFIG.TARGET_CODE);
  const [targetName, setTargetName] = useState(CONFIG.TARGET_NAME);
  const [showStockChangeDialog, setShowStockChangeDialog] = useState(false);

  // --- Data Source Selection ---
  const [dataSource, setDataSource] = useState<DataSource>('mock');
  const [wsStatus, setWsStatus] = useState<string>('준비');
  const rawTicksRef = useRef<Tick[]>([]);
  const rawTickIndexRef = useRef(0);
  const wsRef = useRef<WebSocket | null>(null);

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

  // --- Price Grouping Settings ---
  const [priceGrouping, setPriceGrouping] = useState<PriceGroupingOption>(100);

  // --- Sequential Footprint State ---
  const [historyBars, setHistoryBars] = useState<FootprintCandle[]>([]);
  const activeBarMap = useRef<Map<number, PriceLevelData>>(new Map());
  const barIdCounter = useRef<number>(1);

  // Store ALL ticks for recalculation when rotation mode changes
  const allTicksHistory = useRef<Tick[]>([]);

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
    id: barIdCounter.current++,
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

  // Handle stock code change
  const handleStockCodeChange = useCallback(async (newCode: string, newName: string) => {
    console.log(`📊 Changing stock to: ${newCode} - ${newName}`);

    // Clear existing data
    setTicks([]);
    setHistoryBars([]);
    setCurrentPrice(CONFIG.INITIAL_PRICE);
    allTicksHistory.current = [];
    activeBarMap.current = new Map();
    barIdCounter.current = 1;
    rawTickIndexRef.current = 0;

    // Reset active bar stats
    setActiveBarStats({
      id: barIdCounter.current++,
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

    // Update stock info
    setTargetCode(newCode);
    setTargetName(newName);

    // Send WebSocket message to backend if connected
    if (dataSource === 'websocket' && wsRef.current?.readyState === WebSocket.OPEN) {
      changeTargetCode(wsRef.current, newCode);
    }

    // Close dialog
    setShowStockChangeDialog(false);
  }, [dataSource]);

  // Load Raw Data when mode is enabled
  useEffect(() => {
    if (dataSource === 'raw' && rawTicksRef.current.length === 0) {
      console.log('📥 Loading raw data...');
      loadRawData().then(ticks => {
        rawTicksRef.current = ticks;
        rawTickIndexRef.current = 0;
        console.log(`✅ Raw data loaded: ${ticks.length} ticks ready`);
      }).catch(err => {
        console.error('❌ Failed to load raw data:', err);
      });
    }
  }, [dataSource]);

  // Recalculate all bars when rotation mode or thresholds change
  const recalculateBars = (mode: RotationMode, threshold: number, grouping: number) => {
    const allTicks = allTicksHistory.current;
    if (allTicks.length === 0) return;

    const newHistoryBars: FootprintCandle[] = [];
    let currentBarMap = new Map<number, PriceLevelData>();
    let barId = 1;
    let barStartTime = allTicks[0].time;
    let barTimestamp = allTicks[0].timestamp;
    let barOpen = groupPriceLevel(allTicks[0].price, grouping);
    let barHigh = groupPriceLevel(allTicks[0].price, grouping);
    let barLow = groupPriceLevel(allTicks[0].price, grouping);
    let barTotalVolume = 0;
    let barCurrentDelta = 0;
    let barMaxDelta = 0;
    let barMinDelta = 0;

    for (let i = 0; i < allTicks.length; i++) {
      const tick = allTicks[i];
      const groupedPrice = groupPriceLevel(tick.price, grouping);

      // Add tick to current bar (with grouped price)
      const level: PriceLevelData = currentBarMap.get(groupedPrice) || {
        price: groupedPrice,
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

      if (tick.side === Side.Buy) level.buyVolume += tick.volume;
      else level.sellVolume += tick.volume;

      level.totalVolume += tick.volume;
      level.delta = level.buyVolume - level.sellVolume;
      currentBarMap.set(groupedPrice, level);

      // Update bar stats
      const tickDelta = tick.side === Side.Buy ? tick.volume : -tick.volume;
      barTotalVolume += tick.volume;
      barHigh = Math.max(barHigh, groupedPrice);
      barLow = Math.min(barLow, groupedPrice);
      barCurrentDelta += tickDelta;
      barMaxDelta = Math.max(barMaxDelta, barCurrentDelta);
      barMinDelta = Math.min(barMinDelta, barCurrentDelta);

      // Check rotation
      let shouldRotate = false;

      if (mode === 'VOLUME') {
        if (barTotalVolume >= threshold) shouldRotate = true;
      } else if (mode === 'TIME') {
        const elapsedSec = (tick.timestamp - barTimestamp) / 1000;
        if (elapsedSec >= threshold) shouldRotate = true;
      } else if (mode === 'RANGE') {
        const rangeTicks = (barHigh - barLow) / grouping;
        if (rangeTicks >= threshold) shouldRotate = true;
      }

      // Finalize bar if rotation condition met
      if (shouldRotate) {
        const processedLevels = calculateFootprintIndicators(currentBarMap);
        const finishedBar: FootprintCandle = {
          id: barId++,
          startTime: barStartTime,
          endTime: tick.time,
          open: barOpen,
          close: tick.price,
          high: barHigh,
          low: barLow,
          totalVolume: barTotalVolume,
          delta: barCurrentDelta,
          maxDelta: barMaxDelta,
          minDelta: barMinDelta,
          priceLevels: processedLevels
        };

        newHistoryBars.push(finishedBar);

        // Reset for next bar
        currentBarMap = new Map();

        // Always reset stats for next bar (will be updated by next tick)
        if (i < allTicks.length - 1) {
          barStartTime = tick.time;
          barTimestamp = tick.timestamp;
          barOpen = groupedPrice;
          barHigh = groupedPrice;
          barLow = groupedPrice;
          barTotalVolume = 0;
          barCurrentDelta = 0;
          barMaxDelta = 0;
          barMinDelta = 0;
        }
      }
    }

    // Update state with recalculated bars
    setHistoryBars(newHistoryBars);

    // Reset active bar
    activeBarMap.current = currentBarMap;
    barIdCounter.current = barId;

    setActiveBarStats({
      id: barId,
      startTime: barStartTime,
      timestamp: barTimestamp,
      open: barOpen,
      high: barHigh,
      low: barLow,
      totalVolume: barTotalVolume,
      currentDelta: barCurrentDelta,
      maxDelta: barMaxDelta,
      minDelta: barMinDelta
    });
  };

  // Trigger recalculation when mode, threshold, or price grouping changes
  useEffect(() => {
    if (allTicksHistory.current.length > 0) {
      recalculateBars(rotationMode, thresholds[rotationMode], priceGrouping);
    }
  }, [rotationMode, thresholds, priceGrouping]);

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


  // --- Tick Processing Function (used by both interval and WebSocket) ---
  const processTick = useCallback((newTick: Tick) => {
    const now = Date.now();
    const nowStr = new Date(now).toTimeString().split(' ')[0];
    const groupedPrice = groupPriceLevel(newTick.price, priceGrouping);

    setCurrentPrice(newTick.price);

    // Store tick in full history for recalculation
    allTicksHistory.current.push(newTick);

    setTicks(prevTicks => {
      const updated = [newTick, ...prevTicks];
      return updated.slice(0, 200);
    });

    // --- Footprint Bar Logic ---

    // Check rotation BEFORE adding the tick
    setActiveBarStats(prev => {
        const potentialTotalVol = prev.totalVolume + newTick.volume;
        const potentialHigh = Math.max(prev.high, groupedPrice);
        const potentialLow = Math.min(prev.low, groupedPrice);

      const tickDelta = newTick.side === Side.Buy ? newTick.volume : -newTick.volume;
      const potentialCurrentDelta = prev.currentDelta + tickDelta;
      const potentialMaxDelta = Math.max(prev.maxDelta, potentialCurrentDelta);
      const potentialMinDelta = Math.min(prev.minDelta, potentialCurrentDelta);

      // --- ROTATION LOGIC ---
      let shouldRotate = false;

      if (rotationMode === 'VOLUME') {
          if (potentialTotalVol >= thresholds.VOLUME) shouldRotate = true;
      }
      else if (rotationMode === 'TIME') {
          const elapsedSec = (now - prev.timestamp) / 1000;
          if (elapsedSec >= thresholds.TIME) shouldRotate = true;
      }
      else if (rotationMode === 'RANGE') {
          const rangeTicks = (potentialHigh - potentialLow) / priceGrouping;
          if (rangeTicks >= thresholds.RANGE) shouldRotate = true;
      }

      if (shouldRotate) {
           // Add the current tick to the active bar map BEFORE finalizing
           const currentMap = activeBarMap.current;
           const level: PriceLevelData = currentMap.get(groupedPrice) || {
               price: groupedPrice,
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
           currentMap.set(groupedPrice, level);

           // Finalize Bar with the tick included
           const processedLevels = calculateFootprintIndicators(currentMap);
           const finishedBar: FootprintCandle = {
               id: prev.id,
               startTime: prev.startTime,
               endTime: nowStr,
               open: prev.open,
               close: groupedPrice,
               high: potentialHigh,
               low: potentialLow,
               totalVolume: potentialTotalVol,
               delta: potentialCurrentDelta,
               maxDelta: potentialMaxDelta,
               minDelta: potentialMinDelta,
               priceLevels: processedLevels
           };

           setHistoryBars(prevHistory => {
               const newHistory = [...prevHistory, finishedBar];
               return newHistory;
           });

           // Clear the map for new bar
           activeBarMap.current = new Map();

           // Reset with unique ID - new bar will start with next tick
           // CRITICAL: Use the LAST price (close of finished bar) as starting point
           return {
               id: barIdCounter.current++,
               startTime: nowStr,
               timestamp: now,
               open: groupedPrice, // Start new bar from the rotation tick's grouped price
               high: groupedPrice,
               low: groupedPrice,
               totalVolume: 0,
               currentDelta: 0,
               maxDelta: 0,
               minDelta: 0
           };
      }

      // No rotation - add tick to active bar
      const currentMap = activeBarMap.current;
      const level: PriceLevelData = currentMap.get(groupedPrice) || {
          price: groupedPrice,
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
      currentMap.set(groupedPrice, level);

      // Check if this is the first tick of a new bar
      const isFirstTick = prev.totalVolume === 0;

      return {
          ...prev,
          open: isFirstTick ? groupedPrice : prev.open,
          // CRITICAL FIX: For first tick, initialize high/low to current price
          // This ensures Range calculation starts fresh from 0
          high: isFirstTick ? groupedPrice : potentialHigh,
          low: isFirstTick ? groupedPrice : potentialLow,
          totalVolume: potentialTotalVol,
          currentDelta: potentialCurrentDelta,
          maxDelta: potentialMaxDelta,
          minDelta: potentialMinDelta
      };
    });
  }, [rotationMode, thresholds, priceGrouping]); // Dependencies: recreate when rotation settings or price grouping change

  // --- WebSocket Connection (separate from tick processing) ---
  useEffect(() => {
    if (dataSource === 'websocket') {
      const ws = connectWebSocket(
        (tick) => {
          processTick(tick);
        },
        (error) => {
          console.error('WebSocket Error:', error);
          setWsStatus('연결 오류');
        },
        (status) => {
          setWsStatus(status);
        }
      );

      wsRef.current = ws;

      return () => {
        ws.close();
        wsRef.current = null;
      };
    }
  }, [dataSource, processTick]); // Reconnect when data source changes or processTick updates

  // --- Mock/Raw Data Tick Loop ---
  useEffect(() => {
    // Skip if using WebSocket
    if (dataSource === 'websocket') {
      return;
    }

    const interval = setInterval(() => {
      let newTick: Tick;

      // Select data source
      if (dataSource === 'raw') {
        // Raw Data Mode: Sequential playback
        if (rawTickIndexRef.current >= rawTicksRef.current.length) {
          console.log('⏹️ Raw data playback finished');
          clearInterval(interval);
          return;
        }
        newTick = rawTicksRef.current[rawTickIndexRef.current++];
      } else {
        // Mock Data Mode: Generate random tick
        newTick = generateTick();
      }

      processTick(newTick);
    }, dataSource === 'raw' ? 100 : CONFIG.TICK_RATE_MS); // 100ms for Raw Data, 200ms for Mock Data

    return () => clearInterval(interval);
  }, [dataSource, processTick]); // Re-bind when data source or processTick changes

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
    <div className="h-screen w-screen bg-dark-bg text-white flex flex-col font-sans selection:bg-gray-700">
      <Header
        stats={headerStats}
        targetCode={targetCode}
        targetName={targetName}
        onSettingsClick={() => setShowStockChangeDialog(true)}
      />

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

                    <div className="h-4 w-px bg-gray-700"></div>

                    {/* Price Grouping Controls */}
                    <div className="flex items-center space-x-2 text-[10px]">
                        <Layers className="w-3 h-3 text-purple-400" />
                        <span className="text-gray-400 font-semibold">Price Step:</span>
                        <select
                            value={priceGrouping}
                            onChange={(e) => setPriceGrouping(Number(e.target.value) as PriceGroupingOption)}
                            className="bg-gray-800 border border-gray-600 text-white text-[10px] px-1 py-0.5 rounded outline-none focus:border-purple-400 cursor-pointer"
                        >
                            {PRICE_GROUPING_OPTIONS.map(option => (
                                <option key={option} value={option}>{option}</option>
                            ))}
                        </select>
                        <span className="text-gray-500 text-[9px]">원</span>
                    </div>
                </div>

                <div className="flex space-x-2 items-center">
                    <select
                        value={dataSource}
                        onChange={(e) => {
                            const newSource = e.target.value as DataSource;
                            setDataSource(newSource);
                            // Reset raw data index when switching to raw
                            if (newSource === 'raw') {
                                rawTickIndexRef.current = 0;
                            }
                        }}
                        className="text-[10px] px-3 py-1 rounded font-semibold transition-colors border bg-gray-700 text-gray-300 hover:bg-gray-600 border-gray-600 cursor-pointer"
                    >
                        <option value="mock">🎲 Mock Data</option>
                        <option value="raw">📊 Raw Data</option>
                        <option value="websocket">🔴 Live WebSocket</option>
                    </select>
                    {dataSource === 'websocket' && (
                        <span className="text-[10px] text-green-400 bg-gray-800 px-2 py-0.5 rounded border border-gray-700 font-mono">
                            {wsStatus}
                        </span>
                    )}
                    <span className="text-[10px] text-gray-500 bg-gray-800 px-2 py-0.5 rounded border border-gray-700 font-mono">
                        History: {historyBars.length}
                    </span>
                </div>
            </div>
            
            <FootprintTable
                bars={historyBars}
                activeBar={activeBarCandle}
                globalHigh={globalHigh}
                globalLow={globalLow}
                priceStep={priceGrouping}
            />
        </div>

        {/* Right Panel: Tick List */}
        <div className="w-[200px] flex flex-col min-w-0 flex-none border-l border-border-color">
            <TickList ticks={ticks} />
        </div>
      </main>

      {/* Stock Code Change Dialog */}
      <StockCodeChangeDialog
        isOpen={showStockChangeDialog}
        onClose={() => setShowStockChangeDialog(false)}
        onApply={handleStockCodeChange}
        initialCode={targetCode}
      />
    </div>
  );
};

export default App;
