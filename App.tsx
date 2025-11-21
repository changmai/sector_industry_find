import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Header from './components/Header';
import FootprintTable from './components/FootprintTable';
import TickList from './components/TickList';
import { generateTick } from './services/mockDataService';
import { Tick, PriceLevelData, FootprintStats, Side } from './types';
import { CONFIG } from './constants';

const App: React.FC = () => {
  const [ticks, setTicks] = useState<Tick[]>([]);
  const [currentPrice, setCurrentPrice] = useState(CONFIG.INITIAL_PRICE);
  
  // We store the accumulated volume data in a Map for O(1) access by price
  const [priceMap, setPriceMap] = useState<Map<number, PriceLevelData>>(new Map());

  // Derived Stats
  const stats: FootprintStats = useMemo(() => {
    if (ticks.length === 0) {
        return { totalVolume: 0, cvd: 0, high: CONFIG.INITIAL_PRICE, low: CONFIG.INITIAL_PRICE, open: CONFIG.INITIAL_PRICE, close: CONFIG.INITIAL_PRICE };
    }
    
    const totalVolume = ticks.reduce((acc, t) => acc + t.volume, 0);
    const buyVol = ticks.filter(t => t.side === Side.Buy).reduce((acc, t) => acc + t.volume, 0);
    const sellVol = ticks.filter(t => t.side === Side.Sell).reduce((acc, t) => acc + t.volume, 0);
    const prices = ticks.map(t => t.price);
    
    return {
        totalVolume,
        cvd: buyVol - sellVol,
        high: Math.max(...prices),
        low: Math.min(...prices),
        open: ticks[0].price,
        close: ticks[ticks.length - 1].price
    };
  }, [ticks]);

  // Core Data Processing Loop
  useEffect(() => {
    const interval = setInterval(() => {
      const newTick = generateTick();
      
      setCurrentPrice(newTick.price);
      
      setTicks(prevTicks => {
        const updated = [newTick, ...prevTicks];
        return updated.slice(0, 500); // Keep last 500 for the list
      });

      setPriceMap((prevMap: Map<number, PriceLevelData>) => {
        const newMap = new Map<number, PriceLevelData>(prevMap);
        const level: PriceLevelData = newMap.get(newTick.price) || {
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

        // Update Volumes
        if (newTick.side === Side.Buy) {
            level.buyVolume += newTick.volume;
        } else {
            level.sellVolume += newTick.volume;
        }
        level.totalVolume += newTick.volume;
        level.delta = level.buyVolume - level.sellVolume;
        
        newMap.set(newTick.price, level);
        return newMap;
      });

    }, CONFIG.TICK_RATE_MS);

    return () => clearInterval(interval);
  }, []);

  // Transformation for Rendering: Calculate POC, Imbalances, and Advanced Indicators
  const footprintData = useMemo(() => {
    const rawData: PriceLevelData[] = Array.from(priceMap.values());
    if (rawData.length === 0) return [];

    // 1. Find POC (Max Volume)
    const maxVol = Math.max(...rawData.map((d) => d.totalVolume));
    
    // 2. First Pass: Calculate Basic Diagonal Imbalances
    let processed = rawData.map((item) => {
        const priceStep = 100; 
        
        const bidAtP = item.sellVolume; 
        const askAtP = item.buyVolume;
        
        // Check for Sell Imbalance (Bid P vs Ask P+1)
        const levelAbove = priceMap.get(item.price + priceStep);
        const askAbove = levelAbove ? levelAbove.buyVolume : 0;
        const isSellImbalance = (askAbove > 0) && (bidAtP >= askAbove * CONFIG.IMBALANCE_RATIO);
        
        // Check for Buy Imbalance (Ask P vs Bid P-1)
        const levelBelow = priceMap.get(item.price - priceStep);
        const bidBelow = levelBelow ? levelBelow.sellVolume : 0;
        const isBuyImbalance = (bidBelow > 0) && (askAtP >= bidBelow * CONFIG.IMBALANCE_RATIO);

        return {
            ...item,
            isPOC: item.totalVolume === maxVol,
            imbalanceBuy: isBuyImbalance,
            imbalanceSell: isSellImbalance,
            // Reset advanced flags for second pass
            stackedImbalanceBuy: false,
            stackedImbalanceSell: false,
            isUnfinished: false
        };
    });

    // Sort by price descending (High to Low) for easier sequential checking
    processed.sort((a, b) => b.price - a.price);

    // 3. Second Pass: Stacked Imbalances & Unfinished Business
    for (let i = 0; i < processed.length; i++) {
        // --- Stacked Imbalance Logic (3+ consecutive) ---
        // Check Next 2 rows (since we sorted High to Low, "next" is "below" in price)
        if (i <= processed.length - 3) {
            // Check Buy Stack
            if (processed[i].imbalanceBuy && processed[i+1].imbalanceBuy && processed[i+2].imbalanceBuy) {
                processed[i].stackedImbalanceBuy = true;
                processed[i+1].stackedImbalanceBuy = true;
                processed[i+2].stackedImbalanceBuy = true;
            }
            // Check Sell Stack
            if (processed[i].imbalanceSell && processed[i+1].imbalanceSell && processed[i+2].imbalanceSell) {
                processed[i].stackedImbalanceSell = true;
                processed[i+1].stackedImbalanceSell = true;
                processed[i+2].stackedImbalanceSell = true;
            }
        }

        // --- Unfinished Business Logic (High/Low) ---
        // Check High (Index 0)
        if (i === 0) {
             // If both sides have volume, it's unfinished (magnet)
             if (processed[i].buyVolume > 0 && processed[i].sellVolume > 0) {
                 processed[i].isUnfinished = true;
             }
        }
        // Check Low (Last Index)
        if (i === processed.length - 1) {
             if (processed[i].buyVolume > 0 && processed[i].sellVolume > 0) {
                 processed[i].isUnfinished = true;
             }
        }
    }

    return processed;

  }, [priceMap]);

  return (
    <div className="h-screen w-screen bg-dark-bg text-white flex flex-col overflow-hidden font-sans selection:bg-gray-700">
      <Header stats={stats} />
      
      <main className="flex-1 flex overflow-hidden p-2 gap-2">
        {/* Left Panel: Footprint Analysis (60%) */}
        <div className="flex-[3] flex flex-col min-w-0">
            <div className="flex items-center justify-between mb-2 px-1">
                <h2 className="text-sm font-bold text-gray-300 flex items-center">
                   <span className="w-2 h-2 rounded-full bg-kr-red mr-2"></span>
                   Cumulative Footprint (Price Ladder)
                </h2>
                <div className="flex space-x-2">
                    <span className="text-[10px] text-gray-500 bg-gray-800 px-2 py-0.5 rounded border border-gray-700">
                        Imbalance: {CONFIG.IMBALANCE_RATIO * 100}%
                    </span>
                    <span className="text-[10px] text-kr-red bg-gray-800 px-2 py-0.5 rounded border border-gray-700 flex items-center">
                        <div className="w-1.5 h-1.5 bg-kr-red mr-1"></div> Buy Zone
                    </span>
                    <span className="text-[10px] text-kr-blue bg-gray-800 px-2 py-0.5 rounded border border-gray-700 flex items-center">
                        <div className="w-1.5 h-1.5 bg-kr-blue mr-1"></div> Sell Zone
                    </span>
                </div>
            </div>
            <FootprintTable data={footprintData} currentPrice={currentPrice} />
        </div>

        {/* Right Panel: Tick List (40%) */}
        <div className="flex-[2] flex flex-col min-w-0">
             <div className="flex items-center justify-between mb-2 px-1">
                <h2 className="text-sm font-bold text-gray-300 flex items-center">
                   <span className="w-2 h-2 rounded-full bg-highlight mr-2"></span>
                   Tape (Time & Sales)
                </h2>
            </div>
            <TickList ticks={ticks} />
        </div>
      </main>
    </div>
  );
};

export default App;