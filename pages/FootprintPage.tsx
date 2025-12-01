
import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import Header from '../components/Header';
import FootprintTable from '../components/FootprintTable';
import TickList from '../components/TickList';
import StockCodeChangeDialog from '../components/StockCodeChangeDialog';
import RawDataFileDialog from '../components/RawDataFileDialog';
import CVDChart, { CVDChartHandle } from '../components/CVDChart';
import SimulationControls, { PlaybackSpeed } from '../components/SimulationControls';
import { generateTick } from '../services/mockDataService';
import { loadRawData, parseRawDataFile, extractStockCodeFromFilename } from '../services/rawDataService';
import { connectWebSocket, changeTargetCode, fetchHistoricalData, fetchStockInfo } from '../services/websocketDataService';
import { Tick, PriceLevelData, FootprintStats, Side, FootprintCandle, CVDCandle } from '../types';
import { CONFIG, ZOOM_LEVELS, ZoomLevel, DEFAULT_ZOOM, BAR_WIDTH } from '../constants';
import { calculateFootprintIndicators } from '../utils';
import { groupPriceLevel, PRICE_GROUPING_OPTIONS, PriceGroupingOption } from '../utils/priceGrouping';
import { Clock, BarChart2, MoveVertical, Layers, ZoomIn, ZoomOut } from 'lucide-react';
import { useWebSocket } from '../contexts/WebSocketContext';

type RotationMode = 'VOLUME' | 'TIME' | 'RANGE';
type DataSource = 'mock' | 'raw' | 'websocket';

const FootprintPage: React.FC = () => {
  // WebSocket Context for connection status sync
  const { setConnected } = useWebSocket();

  const [ticks, setTicks] = useState<Tick[]>([]);
  const [currentPrice, setCurrentPrice] = useState(CONFIG.INITIAL_PRICE);

  // --- Stock Code Management ---
  const [targetCode, setTargetCode] = useState(CONFIG.TARGET_CODE);
  const [targetName, setTargetName] = useState(CONFIG.TARGET_NAME);
  const [showStockChangeDialog, setShowStockChangeDialog] = useState(false);

  // --- Raw Data File Selection ---
  const [showRawDataDialog, setShowRawDataDialog] = useState(false);
  const [rawDataFileName, setRawDataFileName] = useState<string | null>(null);

  // --- Simulation State (Raw Data Mode) ---
  const [simIsPlaying, setSimIsPlaying] = useState(false);
  const [simSpeed, setSimSpeed] = useState<PlaybackSpeed>(1);
  const [simCurrentTime, setSimCurrentTime] = useState(0);
  const [simStartTime, setSimStartTime] = useState(0);
  const [simEndTime, setSimEndTime] = useState(0);
  const [simCurrentTickIdx, setSimCurrentTickIdx] = useState(0);
  const simTimerRef = useRef<NodeJS.Timeout | null>(null);
  const [simDataLoaded, setSimDataLoaded] = useState(false);

  // 시간 기반 시뮬레이션을 위한 ref
  const simLastRealTimeRef = useRef(0);  // 마지막 렌더링의 실제 시간
  const simLastSimTimeRef = useRef(0);   // 마지막 렌더링의 시뮬레이션 시간
  const simProcessedIdxRef = useRef(0);  // 이미 처리된 틱 인덱스

  // --- Data Source Selection ---
  const [dataSource, setDataSource] = useState<DataSource>('websocket');
  const [wsStatus, setWsStatus] = useState<string>('준비');
  const rawTicksRef = useRef<Tick[]>([]);
  const rawTickIndexRef = useRef(0);
  const wsRef = useRef<WebSocket | null>(null);
  const cvdChartRef = useRef<CVDChartHandle>(null);

  // --- Rotation Settings ---
  const [rotationMode, setRotationMode] = useState<RotationMode>('RANGE');

  // Thresholds for each mode
  const [thresholds, setThresholds] = useState({
    VOLUME: 50000,
    TIME: 600, // seconds (10 minutes)
    RANGE: 10 // ticks (e.g., 10 * 100 = 1000 price range)
  });

  // Temp input state for UI
  const [tempInput, setTempInput] = useState<string>("10");

  // --- Price Grouping Settings ---
  const [priceGrouping, setPriceGrouping] = useState<PriceGroupingOption>(1000);

  // --- Zoom Settings ---
  const [zoomLevel, setZoomLevel] = useState<ZoomLevel>(DEFAULT_ZOOM as ZoomLevel);

  // --- CVD Chart Height (resizable) ---
  const [cvdHeight, setCvdHeight] = useState(120);
  const isResizingRef = useRef(false);
  const resizeStartYRef = useRef(0);
  const resizeStartHeightRef = useRef(0);

  const handleZoomIn = useCallback(() => {
    const currentIdx = ZOOM_LEVELS.indexOf(zoomLevel);
    if (currentIdx < ZOOM_LEVELS.length - 1) {
      setZoomLevel(ZOOM_LEVELS[currentIdx + 1]);
    }
  }, [zoomLevel]);

  const handleZoomOut = useCallback(() => {
    const currentIdx = ZOOM_LEVELS.indexOf(zoomLevel);
    if (currentIdx > 0) {
      setZoomLevel(ZOOM_LEVELS[currentIdx - 1]);
    }
  }, [zoomLevel]);

  // --- Sequential Footprint State ---
  const [historyBars, setHistoryBars] = useState<FootprintCandle[]>([]);
  const activeBarMap = useRef<Map<number, PriceLevelData>>(new Map());
  const barIdCounter = useRef<number>(1);

  // Store ALL ticks for recalculation when rotation mode changes
  // Memory management: limit to MAX_TICKS_HISTORY to prevent unbounded growth
  const MAX_TICKS_HISTORY = 50000; // ~10MB at 200 bytes/tick
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

    // 종목 변경 시 즉시 초기화 (데이터 로드 전) - 이전 종목 데이터 잔존 방지
    setHistoryBars([]);
    setTicks([]);
    activeBarMap.current = new Map();
    allTicksHistory.current = [];

    // WebSocket 모드인 경우: 과거 데이터 먼저 로드
    if (dataSource === 'websocket') {
      console.log('📥 Loading historical data for', newCode);

      // watchlist 확인 (서버에서 구독 중인지)
      try {
        const serverInfo = await fetch(`${window.location.protocol}//${'localhost'}:8000/`).then(r => r.json());
        const watchlist = serverInfo.watchlist || [];
        if (!watchlist.includes(newCode)) {
          console.warn(`⚠️ ${newCode} is not in server watchlist. Real-time data will not be available.`);
          console.warn(`💡 Add "${newCode}" to backend/watchlist.json and restart server for live data.`);
        }
      } catch (err) {
        console.error('Failed to check watchlist:', err);
      }

      // 1. 과거 데이터 fetch
      const historicalTicks = await fetchHistoricalData(newCode);

      // 2. 상태 초기화 (과거 데이터로)
      if (historicalTicks.length > 0) {
        console.log(`✅ Loaded ${historicalTicks.length} historical ticks`);
        allTicksHistory.current = historicalTicks;

        // TickList 표시용으로 최근 200개만
        setTicks(historicalTicks.slice(0, 200));

        // 과거 데이터로 차트 재계산
        recalculateBars(rotationMode, thresholds[rotationMode], priceGrouping);

        // 최신 틱으로 현재가 설정
        const latestTick = historicalTicks[0]; // 최신 데이터가 앞에 있다고 가정
        setCurrentPrice(latestTick.price);
      } else {
        console.log('⚠️ No historical data found, starting fresh');
        // 데이터 없으면 초기화
        allTicksHistory.current = [];
        setHistoryBars([]);
        setTicks([]);
        activeBarMap.current = new Map();
        barIdCounter.current = 1;

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
      }
    } else {
      // Mock/Raw 모드인 경우: 기존대로 초기화
      setTicks([]);
      setHistoryBars([]);
      setCurrentPrice(CONFIG.INITIAL_PRICE);
      allTicksHistory.current = [];
      activeBarMap.current = new Map();
      barIdCounter.current = 1;
      rawTickIndexRef.current = 0;

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
    }

    // Update stock info
    setTargetCode(newCode);
    setTargetName(newName);

    // WebSocket은 이미 모든 종목을 구독 중이므로 changeTargetCode 불필요
    // (Frontend에서 filterCode만 변경하면 됨)

    // Close dialog
    setShowStockChangeDialog(false);
  }, [dataSource, rotationMode, thresholds, priceGrouping]);

  // Show Raw Data file dialog when mode is enabled
  useEffect(() => {
    if (dataSource === 'raw' && rawTicksRef.current.length === 0) {
      // 파일이 선택되지 않았으면 다이얼로그 표시
      setShowRawDataDialog(true);
    }
  }, [dataSource]);

  // Handle Raw Data file selection
  const handleRawDataFileSelect = useCallback(async (file: File) => {
    console.log('📥 Loading raw data from file:', file.name);
    try {
      const ticks = await parseRawDataFile(file);
      if (ticks.length === 0) {
        console.error('❌ No valid ticks found in file');
        return;
      }

      rawTicksRef.current = ticks;
      rawTickIndexRef.current = 0;
      setRawDataFileName(file.name);

      // 파일명에서 종목 코드 추출 및 종목명 조회
      const extractedCode = extractStockCodeFromFilename(file.name);
      if (extractedCode) {
        console.log(`📊 Extracted stock code from filename: ${extractedCode}`);
        setTargetCode(extractedCode);

        // 종목명 조회 (백엔드 API)
        try {
          const stockInfo = await fetchStockInfo(extractedCode);
          setTargetName(stockInfo.name);
          console.log(`📊 Stock info: ${extractedCode} - ${stockInfo.name}`);
        } catch (err) {
          // API 실패 시 코드만 표시
          setTargetName(`종목 ${extractedCode}`);
          console.warn(`⚠️ Failed to fetch stock name for ${extractedCode}`);
        }
      }

      // 차트 초기화
      setTicks([]);
      setHistoryBars([]);
      allTicksHistory.current = [];
      activeBarMap.current = new Map();
      barIdCounter.current = 1;

      // 첫 번째 틱의 가격으로 초기화
      const firstTick = ticks[0];
      const lastTick = ticks[ticks.length - 1];
      setCurrentPrice(firstTick.price);

      // 시뮬레이션 시간 범위 설정
      setSimStartTime(firstTick.timestamp);
      setSimEndTime(lastTick.timestamp);
      setSimCurrentTime(firstTick.timestamp);
      setSimCurrentTickIdx(0);
      setSimIsPlaying(false);
      setSimSpeed(1);
      setSimDataLoaded(true);

      // ref 초기화
      simProcessedIdxRef.current = 0;
      simLastSimTimeRef.current = firstTick.timestamp;
      simLastRealTimeRef.current = Date.now();

      setActiveBarStats({
        id: barIdCounter.current++,
        startTime: new Date().toTimeString().split(' ')[0],
        timestamp: Date.now(),
        open: firstTick.price,
        high: firstTick.price,
        low: firstTick.price,
        totalVolume: 0,
        currentDelta: 0,
        maxDelta: 0,
        minDelta: 0
      });

      console.log(`✅ Raw data loaded: ${ticks.length} ticks ready`);
      console.log(`📊 Time range: ${new Date(firstTick.timestamp).toTimeString()} ~ ${new Date(lastTick.timestamp).toTimeString()}`);
      setShowRawDataDialog(false);
    } catch (err) {
      console.error('❌ Failed to load raw data:', err);
    }
  }, []);

  // Load Historical Data when switching to WebSocket mode (only once on mount)
  const initialLoadDone = useRef(false);

  useEffect(() => {
    if (dataSource === 'websocket' && !initialLoadDone.current) {
      initialLoadDone.current = true;
      console.log('📥 Loading historical data for initial load:', targetCode);
      fetchHistoricalData(targetCode).then(historicalTicks => {
        if (historicalTicks.length > 0) {
          console.log(`✅ Initial load: ${historicalTicks.length} historical ticks`);
          allTicksHistory.current = historicalTicks;
          setTicks(historicalTicks.slice(0, 200));
          recalculateBars(rotationMode, thresholds[rotationMode], priceGrouping);
          setCurrentPrice(historicalTicks[0].price);
        } else {
          console.log('⚠️ No historical data for initial load');
        }
      }).catch(err => {
        console.error('❌ Failed to load historical data:', err);
      });
    }

    // dataSource가 변경되면 reset
    if (dataSource !== 'websocket') {
      initialLoadDone.current = false;
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
        isUnfinished: false,
        isVA: false,
        isVAH: false,
        isVAL: false,
        isLVN: false
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

  // --- Derived Stats for Header (optimized: split into two memos) ---
  // Tick-based stats: only recalculates when ticks array changes
  const tickBasedStats = useMemo(() => {
     if (ticks.length === 0) return { totalVolume: 0, cvd: 0, high: 0, low: 0, open: 0 };

     // Single pass through ticks array
     let totalVol = 0;
     let buyVol = 0;
     let high = ticks[0].price;
     let low = ticks[0].price;

     for (const t of ticks) {
       totalVol += t.volume;
       if (t.side === Side.Buy) buyVol += t.volume;
       if (t.price > high) high = t.price;
       if (t.price < low) low = t.price;
     }

     return {
         totalVolume: totalVol,
         cvd: buyVol - (totalVol - buyVol), // buyVol - sellVol
         high,
         low,
         open: ticks[ticks.length - 1].price,
     };
  }, [ticks]);

  // Final header stats: combines tick stats with current price (minimal computation)
  const headerStats: FootprintStats = useMemo(() => ({
    ...tickBasedStats,
    close: currentPrice
  }), [tickBasedStats, currentPrice]);

  // --- Calculate Global Y-Axis Range (Optimized: single pass, no temp arrays) ---
  // Cache history bars range separately to avoid recalculation on active bar updates
  const historyRange = useMemo(() => {
    if (historyBars.length === 0) {
      return { high: -Infinity, low: Infinity };
    }

    let high = historyBars[0].high;
    let low = historyBars[0].low;

    for (let i = 1; i < historyBars.length; i++) {
      const bar = historyBars[i];
      if (bar.high > high) high = bar.high;
      if (bar.low < low) low = bar.low;
    }

    return { high, low };
  }, [historyBars]);

  const { globalHigh, globalLow } = useMemo(() => {
    let max = historyRange.high;
    let min = historyRange.low;

    // Include active bar if it has data
    if (activeBarStats.totalVolume > 0) {
      if (activeBarStats.high > max) max = activeBarStats.high;
      if (activeBarStats.low < min) min = activeBarStats.low;
    }

    // Fallback if no data
    if (max === -Infinity || min === Infinity) {
      return {
        globalHigh: CONFIG.INITIAL_PRICE + CONFIG.PRICE_STEP * 5,
        globalLow: CONFIG.INITIAL_PRICE - CONFIG.PRICE_STEP * 5
      };
    }

    return {
      globalHigh: max + (CONFIG.PRICE_STEP * 2),
      globalLow: min - (CONFIG.PRICE_STEP * 2)
    };
  }, [historyRange, activeBarStats.high, activeBarStats.low, activeBarStats.totalVolume]);


  // --- Refs for stable access in processTick (avoid callback recreation) ---
  const rotationModeRef = useRef(rotationMode);
  const thresholdsRef = useRef(thresholds);
  const priceGroupingRef = useRef(priceGrouping);

  // Keep refs in sync
  useEffect(() => {
    rotationModeRef.current = rotationMode;
    thresholdsRef.current = thresholds;
    priceGroupingRef.current = priceGrouping;
  }, [rotationMode, thresholds, priceGrouping]);

  // --- Tick Processing Function (used by both interval and WebSocket) ---
  // Optimized: Uses refs to avoid recreation on settings change
  const processTick = useCallback((newTick: Tick) => {
    const now = Date.now();
    const nowStr = new Date(now).toTimeString().split(' ')[0];
    const currentPriceGrouping = priceGroupingRef.current;
    const currentRotationMode = rotationModeRef.current;
    const currentThresholds = thresholdsRef.current;
    const groupedPrice = groupPriceLevel(newTick.price, currentPriceGrouping);

    setCurrentPrice(newTick.price);

    // Store tick in full history for recalculation (with memory limit)
    allTicksHistory.current.push(newTick);
    // Trim if exceeds limit (keep recent ticks)
    if (allTicksHistory.current.length > MAX_TICKS_HISTORY) {
      allTicksHistory.current = allTicksHistory.current.slice(-MAX_TICKS_HISTORY);
    }

    // Optimized: Avoid spread operator, use functional update with efficient slicing
    setTicks(prevTicks => {
      // If already at max capacity, just shift and add
      if (prevTicks.length >= 200) {
        const updated = [newTick, ...prevTicks.slice(0, 199)];
        return updated;
      }
      return [newTick, ...prevTicks];
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

      if (currentRotationMode === 'VOLUME') {
          if (potentialTotalVol >= currentThresholds.VOLUME) shouldRotate = true;
      }
      else if (currentRotationMode === 'TIME') {
          const elapsedSec = (now - prev.timestamp) / 1000;
          if (elapsedSec >= currentThresholds.TIME) shouldRotate = true;
      }
      else if (currentRotationMode === 'RANGE') {
          const rangeTicks = (potentialHigh - potentialLow) / currentPriceGrouping;
          if (rangeTicks >= currentThresholds.RANGE) shouldRotate = true;
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
               isUnfinished: false,
               isVA: false,
               isVAH: false,
               isVAL: false,
               isLVN: false
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

           // Optimized: Use concat instead of spread for better performance
           setHistoryBars(prevHistory => prevHistory.concat(finishedBar));

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
          isUnfinished: false,
          isVA: false,
          isVAH: false,
          isVAL: false,
          isLVN: false
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
  }, []); // Optimized: No dependencies - uses refs for settings access

  // --- WebSocket Connection (separate from tick processing) ---
  // filterCode를 ref로 관리하여 재연결 없이 필터만 변경
  const filterCodeRef = useRef(targetCode);
  const processTickRef = useRef(processTick);

  // Throttle: 틱을 버퍼에 모았다가 일정 간격으로 처리
  const tickBufferRef = useRef<Tick[]>([]);
  const throttleIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const THROTTLE_MS = 50; // 50ms마다 렌더링 (초당 20회)

  // processTick ref 업데이트 (재연결 없이)
  useEffect(() => {
    processTickRef.current = processTick;
  }, [processTick]);

  useEffect(() => {
    filterCodeRef.current = targetCode;
  }, [targetCode]);

  // Throttled tick processing - uses requestAnimationFrame for smoother rendering
  useEffect(() => {
    let rafId: number | null = null;
    let lastProcessTime = 0;

    const processBuffer = (timestamp: number) => {
      // Only process if enough time has passed (throttle)
      if (timestamp - lastProcessTime >= THROTTLE_MS) {
        const buffer = tickBufferRef.current;
        if (buffer.length > 0) {
          // Process all buffered ticks
          for (const tick of buffer) {
            processTickRef.current(tick);
          }
          // Clear buffer
          tickBufferRef.current = [];
        }
        lastProcessTime = timestamp;
      }

      // Schedule next frame
      rafId = requestAnimationFrame(processBuffer);
    };

    // Start the loop
    rafId = requestAnimationFrame(processBuffer);

    return () => {
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
      }
    };
  }, []);

  useEffect(() => {
    if (dataSource === 'websocket') {
      const ws = connectWebSocket(
        (tick: any) => {
          // 종목코드로 필터링 (Backend가 모든 종목 데이터를 브로드캐스트하므로)
          if (tick.code && tick.code === filterCodeRef.current) {
            // Throttle: 바로 처리하지 않고 버퍼에 추가
            tickBufferRef.current.push(tick);
          } else if (!tick.code) {
            // code 필드가 없으면 그냥 버퍼에 추가 (Legacy 호환)
            tickBufferRef.current.push(tick);
          }
        },
        (error) => {
          console.error('WebSocket Error:', error);
          setWsStatus('연결 오류');
          setConnected(false); // Context 연결 상태 업데이트
        },
        (status) => {
          setWsStatus(status);
          // Context 연결 상태 업데이트
          setConnected(status === '연결됨' || status === '구독 완료');
        },
        targetCode  // 초기 filterCode 전달 (참고용)
      );

      wsRef.current = ws;

      return () => {
        // Properly cleanup WebSocket to prevent memory leaks
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
        // Clear event handlers to prevent memory leaks
        ws.onmessage = null;
        ws.onerror = null;
        ws.onclose = null;
        ws.onopen = null;
        wsRef.current = null;
        setConnected(false); // 연결 해제 시 Context 업데이트
      };
    } else {
      // WebSocket 모드가 아닐 때는 연결 해제 상태로 표시
      setConnected(false);
    }
  }, [dataSource, setConnected]); // processTick 제거: 재연결 방지

  // --- Simulation Control Handlers ---
  const handleSimPlay = useCallback(() => {
    setSimIsPlaying(true);
  }, []);

  const handleSimPause = useCallback(() => {
    setSimIsPlaying(false);
  }, []);

  const handleSimSeek = useCallback((targetTime: number) => {
    // Clamp to valid range
    const clampedTime = Math.max(simStartTime, Math.min(simEndTime, targetTime));

    // Find the tick index for this time using binary search
    const ticks = rawTicksRef.current;
    if (ticks.length === 0) return;

    let left = 0;
    let right = ticks.length - 1;

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (ticks[mid].timestamp < clampedTime) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }

    // Reset chart state
    setTicks([]);
    setHistoryBars([]);
    allTicksHistory.current = [];
    activeBarMap.current = new Map();
    barIdCounter.current = 1;

    // Process all ticks up to the target index
    const ticksToProcess = ticks.slice(0, left);
    if (ticksToProcess.length > 0) {
      // Bulk recalculate bars
      allTicksHistory.current = ticksToProcess;
      recalculateBars(rotationModeRef.current, thresholdsRef.current[rotationModeRef.current], priceGroupingRef.current);

      // Update tick list with recent ticks
      setTicks(ticksToProcess.slice(-200).reverse());

      // Update current price
      const lastTick = ticksToProcess[ticksToProcess.length - 1];
      setCurrentPrice(lastTick.price);
    } else {
      // Reset to initial state
      const firstTick = ticks[0];
      setCurrentPrice(firstTick.price);
      setActiveBarStats({
        id: barIdCounter.current++,
        startTime: new Date(firstTick.timestamp).toTimeString().split(' ')[0],
        timestamp: firstTick.timestamp,
        open: firstTick.price,
        high: firstTick.price,
        low: firstTick.price,
        totalVolume: 0,
        currentDelta: 0,
        maxDelta: 0,
        minDelta: 0
      });
    }

    // ref도 함께 업데이트
    simProcessedIdxRef.current = left;
    simLastSimTimeRef.current = clampedTime;
    simLastRealTimeRef.current = Date.now();

    setSimCurrentTickIdx(left);
    setSimCurrentTime(clampedTime);
  }, [simStartTime, simEndTime]);

  const handleSimSpeedChange = useCallback((speed: PlaybackSpeed) => {
    setSimSpeed(speed);
  }, []);

  const handleSimSkipBack = useCallback(() => {
    handleSimSeek(simStartTime);
    setSimIsPlaying(false);
  }, [simStartTime, handleSimSeek]);

  const handleSimSkipForward = useCallback(() => {
    handleSimSeek(simEndTime);
    setSimIsPlaying(false);
  }, [simEndTime, handleSimSeek]);

  // --- Raw Data Simulation Timer (시간 기반 + 10fps 고정 렌더링) ---
  useEffect(() => {
    if (dataSource !== 'raw' || !simIsPlaying) {
      if (simTimerRef.current) {
        clearInterval(simTimerRef.current);
        simTimerRef.current = null;
      }
      return;
    }

    const ticks = rawTicksRef.current;
    if (ticks.length === 0) return;

    // 고정 렌더링 간격: 100ms = 10fps (배속과 무관)
    const RENDER_INTERVAL_MS = 100;

    // 시뮬레이션 시작 시 기준 시간 설정
    const realStartTime = Date.now();
    const simStartTimeLocal = simCurrentTime || simStartTime;

    // ref 초기화
    simLastRealTimeRef.current = realStartTime;
    simLastSimTimeRef.current = simStartTimeLocal;

    // 현재 시뮬레이션 시간에 해당하는 틱 인덱스 찾기
    let currentIdx = simProcessedIdxRef.current;

    // 성능 로깅용
    let tickCounter = 0;
    let lastLogTime = Date.now();

    simTimerRef.current = setInterval(() => {
      const now = Date.now();
      const realElapsed = now - simLastRealTimeRef.current;

      // 시뮬레이션 시간 계산 (실제 경과 시간 × 배속)
      const simElapsed = realElapsed * simSpeed;
      const newSimTime = simLastSimTimeRef.current + simElapsed;

      // 종료 체크
      if (newSimTime >= simEndTime || currentIdx >= ticks.length) {
        setSimIsPlaying(false);
        setSimCurrentTime(simEndTime);
        console.log('⏹️ Simulation finished');
        return;
      }

      // 현재 시뮬레이션 시간까지의 모든 틱 처리 (버퍼링)
      let processedCount = 0;
      while (currentIdx < ticks.length && ticks[currentIdx].timestamp <= newSimTime) {
        processTick(ticks[currentIdx]);
        currentIdx++;
        processedCount++;
        tickCounter++;
      }

      // 상태 업데이트 (렌더링 트리거)
      simProcessedIdxRef.current = currentIdx;
      setSimCurrentTickIdx(currentIdx);
      setSimCurrentTime(newSimTime);

      // 다음 프레임을 위한 기준 시간 갱신
      simLastRealTimeRef.current = now;
      simLastSimTimeRef.current = newSimTime;

      // 성능 로깅 (1초마다)
      if (now - lastLogTime >= 1000) {
        console.log(`📊 Ticks processed: ${tickCounter}/sec, Renders: 10fps, Speed: ${simSpeed}x`);
        tickCounter = 0;
        lastLogTime = now;
      }
    }, RENDER_INTERVAL_MS);

    return () => {
      if (simTimerRef.current) {
        clearInterval(simTimerRef.current);
        simTimerRef.current = null;
      }
    };
  }, [dataSource, simIsPlaying, simSpeed, processTick, simStartTime, simEndTime]);

  // --- Mock Data Tick Loop ---
  useEffect(() => {
    // Only for mock mode
    if (dataSource !== 'mock') {
      return;
    }

    console.log(`▶️ Starting mock data playback`);

    const interval = setInterval(() => {
      const newTick = generateTick();
      processTick(newTick);
    }, CONFIG.TICK_RATE_MS);

    return () => clearInterval(interval);
  }, [dataSource, processTick]);

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

  // --- CVD (Cumulative Volume Delta) Data Transformation ---
  // Optimized: Cache history CVD and only recalculate when historyBars changes
  // Active bar CVD is computed separately to avoid full recalculation on every tick

  // Cache for history bars CVD (only recalculates when historyBars changes)
  const historyCvdData = useMemo(() => {
    const result: CVDCandle[] = [];
    let cumulativeDelta = 0;

    for (let i = 0; i < historyBars.length; i++) {
      const bar = historyBars[i];
      const cvdOpen = cumulativeDelta;
      const cvdClose = cvdOpen + bar.delta;
      const cvdHigh = cvdOpen + bar.maxDelta;
      const cvdLow = cvdOpen + bar.minDelta;

      result.push({
        time: i,
        open: cvdOpen,
        high: Math.max(cvdHigh, cvdOpen, cvdClose),
        low: Math.min(cvdLow, cvdOpen, cvdClose),
        close: cvdClose,
      });

      cumulativeDelta = cvdClose;
    }

    return { data: result, lastCumulativeDelta: cumulativeDelta };
  }, [historyBars]);

  // Final CVD data: history + active bar (only active bar recalculates on tick)
  const cvdData: CVDCandle[] = useMemo(() => {
    const { data: historyData, lastCumulativeDelta } = historyCvdData;

    if (activeBarStats.totalVolume === 0) {
      return historyData;
    }

    // Only compute active bar CVD
    const cvdOpen = lastCumulativeDelta;
    const cvdClose = cvdOpen + activeBarStats.currentDelta;
    const cvdHigh = cvdOpen + activeBarStats.maxDelta;
    const cvdLow = cvdOpen + activeBarStats.minDelta;

    const activeBarCvd: CVDCandle = {
      time: historyBars.length,
      open: cvdOpen,
      high: Math.max(cvdHigh, cvdOpen, cvdClose),
      low: Math.min(cvdLow, cvdOpen, cvdClose),
      close: cvdClose,
    };

    // Return new array with active bar appended (shallow copy of history)
    return [...historyData, activeBarCvd];
  }, [historyCvdData, historyBars.length, activeBarStats.currentDelta, activeBarStats.maxDelta, activeBarStats.minDelta, activeBarStats.totalVolume]);

  // Handle scroll sync between FootprintTable and CVDChart
  const handleFootprintScroll = useCallback((visibleBarIndex: number) => {
    if (cvdChartRef.current) {
      cvdChartRef.current.scrollToBar(visibleBarIndex);
    }
  }, []);

  // Handle CVD chart resize
  const handleResizeStart = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    isResizingRef.current = true;
    resizeStartYRef.current = e.clientY;
    resizeStartHeightRef.current = cvdHeight;
    document.body.style.cursor = 'ns-resize';
    document.body.style.userSelect = 'none';
  }, [cvdHeight]);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizingRef.current) return;
      const deltaY = resizeStartYRef.current - e.clientY;
      const newHeight = Math.max(60, Math.min(400, resizeStartHeightRef.current + deltaY));
      setCvdHeight(newHeight);
    };

    const handleMouseUp = () => {
      if (isResizingRef.current) {
        isResizingRef.current = false;
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
      }
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

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
    <div className="h-screen w-screen bg-dark-bg text-white flex flex-col font-sans selection:bg-gray-700 overflow-hidden">
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

                    <div className="h-4 w-px bg-gray-700"></div>

                    {/* Zoom Controls */}
                    <div className="flex items-center space-x-1 text-[10px]">
                        <button
                            onClick={handleZoomOut}
                            disabled={zoomLevel === ZOOM_LEVELS[0]}
                            className="p-1 rounded bg-gray-800 border border-gray-600 hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed"
                            title="Zoom Out"
                        >
                            <ZoomOut className="w-3 h-3 text-gray-300" />
                        </button>
                        <span className="text-gray-300 font-mono w-10 text-center">{zoomLevel}%</span>
                        <button
                            onClick={handleZoomIn}
                            disabled={zoomLevel === ZOOM_LEVELS[ZOOM_LEVELS.length - 1]}
                            className="p-1 rounded bg-gray-800 border border-gray-600 hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed"
                            title="Zoom In"
                        >
                            <ZoomIn className="w-3 h-3 text-gray-300" />
                        </button>
                    </div>
                </div>

                <div className="flex space-x-2 items-center">
                    <select
                        value={dataSource}
                        onChange={(e) => {
                            const newSource = e.target.value as DataSource;
                            setDataSource(newSource);
                            // Reset raw data when switching to raw mode (prompt file selection)
                            if (newSource === 'raw') {
                                rawTicksRef.current = [];
                                rawTickIndexRef.current = 0;
                                setRawDataFileName(null);
                                setSimDataLoaded(false);
                                setSimIsPlaying(false);
                            } else {
                                // Reset simulation state when switching away from raw mode
                                setSimDataLoaded(false);
                                setSimIsPlaying(false);
                            }
                        }}
                        className="text-[10px] px-3 py-1 rounded font-semibold transition-colors border bg-gray-700 text-gray-300 hover:bg-gray-600 border-gray-600 cursor-pointer"
                    >
                        <option value="mock">🎲 Mock Data</option>
                        <option value="raw">📊 Raw Data</option>
                        <option value="websocket">🔴 Live WebSocket</option>
                    </select>
                    {dataSource === 'raw' && rawDataFileName && (
                        <button
                            onClick={() => setShowRawDataDialog(true)}
                            className="text-[10px] text-orange-400 bg-gray-800 px-2 py-0.5 rounded border border-gray-700 font-mono hover:bg-gray-700 cursor-pointer"
                            title="다른 파일 선택"
                        >
                            📁 {rawDataFileName.length > 20 ? rawDataFileName.slice(0, 17) + '...' : rawDataFileName}
                        </button>
                    )}
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

            <div className="flex-1 min-h-0 overflow-hidden">
                <FootprintTable
                    bars={historyBars}
                    activeBar={activeBarCandle}
                    globalHigh={globalHigh}
                    globalLow={globalLow}
                    priceStep={priceGrouping}
                    zoomLevel={zoomLevel}
                    onScrollChange={handleFootprintScroll}
                />
            </div>

            {/* Resize Handle */}
            <div
              className="h-2 bg-gray-800 hover:bg-highlight cursor-ns-resize flex items-center justify-center shrink-0 transition-colors border-y border-gray-700"
              onMouseDown={handleResizeStart}
            >
              <div className="w-10 h-0.5 bg-gray-600 rounded-full"></div>
            </div>

            {/* CVD Chart - Below FootprintTable */}
            <div className="shrink-0">
                <CVDChart
                  ref={cvdChartRef}
                  data={cvdData}
                  height={cvdHeight}
                  barWidth={Math.round(BAR_WIDTH * (zoomLevel / 100) * (zoomLevel >= 75 ? 1 : 0.6))}
                />
            </div>

            {/* Simulation Controls - Only for Raw Data Mode */}
            {dataSource === 'raw' && simDataLoaded && (
              <div className="shrink-0 mt-1">
                <SimulationControls
                  isPlaying={simIsPlaying}
                  currentTime={simCurrentTime}
                  startTime={simStartTime}
                  endTime={simEndTime}
                  speed={simSpeed}
                  onPlay={handleSimPlay}
                  onPause={handleSimPause}
                  onSeek={handleSimSeek}
                  onSpeedChange={handleSimSpeedChange}
                  onSkipBack={handleSimSkipBack}
                  onSkipForward={handleSimSkipForward}
                  tickCount={rawTicksRef.current.length}
                  currentTickIndex={simCurrentTickIdx}
                />
              </div>
            )}
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
        dataSource={dataSource}
      />

      {/* Raw Data File Selection Dialog */}
      <RawDataFileDialog
        isOpen={showRawDataDialog}
        onClose={() => {
          setShowRawDataDialog(false);
          // 파일 선택 취소 시 mock 모드로 돌아감
          if (rawTicksRef.current.length === 0) {
            setDataSource('mock');
          }
        }}
        onApply={handleRawDataFileSelect}
      />
    </div>
  );
};

export default FootprintPage;
