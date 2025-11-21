import React, { useMemo, useRef, useEffect } from 'react';
import { PriceLevelData } from '../types';
import { COLORS } from '../constants';
import { ArrowUp, ArrowDown, Lock, Magnet, Ban } from 'lucide-react';

interface FootprintTableProps {
  data: PriceLevelData[];
  currentPrice: number;
}

const FootprintTable: React.FC<FootprintTableProps> = ({ data, currentPrice }) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const isAutoScroll = useRef(true);

  // Data is already sorted descending from App.tsx
  const sortedData = useMemo(() => {
    return [...data].sort((a, b) => b.price - a.price);
  }, [data]);

  // 1. Max Volume for Profile Bar (Total Volume)
  const maxTotalVolume = useMemo(() => {
    if (data.length === 0) return 1;
    return Math.max(...data.map(d => d.totalVolume));
  }, [data]);

  // 2. Max Volume for Heatmap (Single Cell Volume)
  // We find the largest single buy or sell volume in the visible range to scale the opacity.
  const maxCellVolume = useMemo(() => {
    if (data.length === 0) return 1;
    let max = 0;
    for (const d of data) {
        if (d.buyVolume > max) max = d.buyVolume;
        if (d.sellVolume > max) max = d.sellVolume;
    }
    return max;
  }, [data]);

  // Auto-scroll to current price on initial load
  useEffect(() => {
    if (scrollRef.current && isAutoScroll.current && sortedData.length > 0) {
      // Simplified auto-scroll logic could go here
    }
  }, [sortedData, currentPrice]);

  return (
    <div className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color overflow-hidden shadow-xl">
      {/* Table Header */}
      <div className="grid grid-cols-12 gap-px bg-gray-900 border-b border-border-color text-xs font-medium text-gray-400 py-2 sticky top-0 z-20 shadow-sm">
        <div className="col-span-3 text-center flex flex-col justify-center">
            <span>Bid Vol</span>
            <span className="text-[9px] text-kr-blue opacity-70">Selling</span>
        </div>
        <div className="col-span-2 text-center border-l border-r border-gray-800 flex flex-col justify-center">
            <span>Price</span>
        </div>
        <div className="col-span-3 text-center flex flex-col justify-center">
            <span>Ask Vol</span>
            <span className="text-[9px] text-kr-red opacity-70">Buying</span>
        </div>
        <div className="col-span-2 text-center border-l border-gray-800 flex flex-col justify-center">
            <span>Delta</span>
        </div>
        <div className="col-span-2 text-center border-l border-gray-800 flex flex-col justify-center">
            <span>Profile</span>
        </div>
      </div>

      {/* Table Body */}
      <div className="overflow-y-auto flex-1 relative bg-[#1a1a1a]" ref={scrollRef}>
        {sortedData.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center text-gray-600">
            Waiting for tick data...
          </div>
        )}
        
        {sortedData.map((row, index) => (
          <FootprintRow 
            key={row.price} 
            row={row} 
            isCurrent={row.price === currentPrice} 
            maxTotalVolume={maxTotalVolume}
            maxCellVolume={maxCellVolume}
            isHigh={index === 0}
            isLow={index === sortedData.length - 1}
          />
        ))}
      </div>
      
      <div className="h-6 bg-gray-900 border-t border-border-color flex items-center justify-between px-2 text-[10px] text-gray-500">
         <div className="flex space-x-3">
             <span className="flex items-center"><Magnet className="w-3 h-3 mr-1 text-gray-400" /> Unfinished</span>
             <span className="flex items-center"><Ban className="w-3 h-3 mr-1 text-gray-400" /> Zero Print</span>
         </div>
         <div className="flex space-x-3 items-center">
             <span className="flex items-center mr-2">
                <div className="w-2 h-2 border border-yellow-400 mr-1"></div> Imbalance
             </span>
             <span>Stacked: <span className="text-kr-red">Buy</span> / <span className="text-kr-blue">Sell</span></span>
         </div>
      </div>
    </div>
  );
};

interface RowProps {
    row: PriceLevelData;
    isCurrent: boolean;
    maxTotalVolume: number;
    maxCellVolume: number;
    isHigh: boolean;
    isLow: boolean;
}

const FootprintRow: React.FC<RowProps> = ({ row, isCurrent, maxTotalVolume, maxCellVolume, isHigh, isLow }) => {
  // Profile Bar Calculation
  const profileWidth = maxTotalVolume > 0 ? (row.totalVolume / maxTotalVolume) * 100 : 0;

  // Heatmap Opacity Calculation (Min 0.05 to see grid, Max 0.9 for text readability)
  // Using a slight curve (Math.sqrt) to make smaller volumes more visible
  const getOpacity = (vol: number) => {
      if (vol === 0) return 0;
      const ratio = vol / maxCellVolume;
      // Use square root to boost visibility of lower volumes, cap at 0.85
      return Math.min(0.85, Math.max(0.05, Math.sqrt(ratio))); 
  };

  const sellOpacity = getOpacity(row.sellVolume);
  const buyOpacity = getOpacity(row.buyVolume);

  return (
    <div className={`grid grid-cols-12 gap-px text-xs font-mono relative group hover:bg-gray-800/50 transition-colors ${isCurrent ? 'bg-gray-800' : ''}`}>
      
      {/* Bid Volume (Sell Side) - Heatmap Blue */}
      <div 
        className={`col-span-3 py-1 px-2 text-right relative flex items-center justify-end border-b border-gray-800/50 text-gray-200
            ${row.imbalanceSell ? 'border-2 border-yellow-400 font-black z-10' : ''}
        `}
        style={{ backgroundColor: `rgba(77, 148, 255, ${sellOpacity})` }} // Blue Heatmap
      >
        {/* Stacked Imbalance Indicator (Sell) */}
        {row.stackedImbalanceSell && (
            <div className="absolute inset-y-0 right-0 w-1.5 bg-kr-blue z-20 border-l border-white/20"></div>
        )}
        {row.imbalanceSell && <span className="absolute left-1 text-[8px] text-yellow-400 font-bold opacity-90">IMB</span>}
        <span className="relative z-10 drop-shadow-sm">{row.sellVolume.toLocaleString()}</span>
      </div>

      {/* Price */}
      <div className={`col-span-2 py-1 flex items-center justify-center font-bold border-x border-b border-gray-800/50 relative ${isCurrent ? 'text-white bg-gray-700' : 'text-gray-300'}`}>
        {isCurrent && (
           <div className="absolute inset-0 border-2 border-white/20 pointer-events-none"></div>
        )}
        {row.isPOC && (
            <div className={`absolute inset-0 border-2 ${COLORS.POC_BORDER} pointer-events-none flex items-start justify-start`}>
                <div className="bg-highlight text-black text-[8px] px-0.5 leading-none font-bold">POC</div>
            </div>
        )}
        
        {/* Auction Status Indicators (High/Low) */}
        {row.isUnfinished && (isHigh || isLow) && (
            <div className="absolute -right-6 top-0 bottom-0 flex items-center z-30">
                <div className="bg-gray-800 text-gray-300 border border-gray-500 text-[9px] px-1 rounded flex items-center whitespace-nowrap shadow-lg shadow-black/50">
                    <Magnet className="w-3 h-3 mr-1 text-highlight" /> Unfinished
                </div>
            </div>
        )}
        {!row.isUnfinished && (isHigh || isLow) && (
            <div className="absolute -right-6 top-0 bottom-0 flex items-center z-30">
                 <div className="bg-gray-800 text-gray-400 border border-gray-600 text-[9px] px-1 rounded flex items-center whitespace-nowrap shadow-lg">
                    <Ban className="w-3 h-3 mr-1" /> Zero Print
                </div>
            </div>
        )}

        {row.price.toLocaleString()}
      </div>

      {/* Ask Volume (Buy Side) - Heatmap Red */}
      <div 
        className={`col-span-3 py-1 px-2 text-left relative flex items-center justify-start border-b border-gray-800/50 text-gray-200
            ${row.imbalanceBuy ? 'border-2 border-yellow-400 font-black z-10' : ''}
        `}
        style={{ backgroundColor: `rgba(255, 77, 77, ${buyOpacity})` }} // Red Heatmap
      >
        {/* Stacked Imbalance Indicator (Buy) */}
        {row.stackedImbalanceBuy && (
            <div className="absolute inset-y-0 left-0 w-1.5 bg-kr-red z-20 border-r border-white/20"></div>
        )}
        <span className="relative z-10 drop-shadow-sm">{row.buyVolume.toLocaleString()}</span>
        {row.imbalanceBuy && <span className="absolute right-1 text-[8px] text-yellow-400 font-bold opacity-90">IMB</span>}
      </div>

      {/* Delta */}
      <div className={`col-span-2 py-1 px-2 text-right border-l border-b border-gray-800/50 ${row.delta > 0 ? COLORS.BUY_TEXT : row.delta < 0 ? COLORS.SELL_TEXT : COLORS.NEUTRAL}`}>
        {row.delta > 0 ? '+' : ''}{row.delta.toLocaleString()}
      </div>
      
      {/* Volume Profile (Relative to Total Max) */}
      <div className="col-span-2 relative border-l border-b border-gray-800/50 h-full min-h-[24px]">
        <div 
            className={`absolute top-1 bottom-1 left-0 opacity-30 ${row.delta > 0 ? 'bg-kr-red' : 'bg-kr-blue'}`}
            style={{ width: `${profileWidth}%` }}
        ></div>
        <span className="absolute right-1 top-1/2 -translate-y-1/2 text-[9px] text-gray-500 z-10">{row.totalVolume.toLocaleString()}</span>
      </div>

    </div>
  );
};

export default FootprintTable;