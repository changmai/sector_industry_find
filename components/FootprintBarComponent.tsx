import React, { useMemo } from 'react';
import { FootprintCandle, PriceLevelData } from '../types';
import { COLORS } from '../constants';
import { Magnet, Ban } from 'lucide-react';

interface FootprintBarProps {
  candle: FootprintCandle;
  isActive: boolean;
}

const FootprintBarComponent: React.FC<FootprintBarProps> = ({ candle, isActive }) => {
  // Max Volume for Heatmap & Profile within this specific bar
  const { maxTotalVolume, maxCellVolume } = useMemo(() => {
    let maxTotal = 0;
    let maxCell = 0;
    candle.priceLevels.forEach(d => {
      if (d.totalVolume > maxTotal) maxTotal = d.totalVolume;
      if (d.buyVolume > maxCell) maxCell = d.buyVolume;
      if (d.sellVolume > maxCell) maxCell = d.sellVolume;
    });
    return { maxTotalVolume: maxTotal || 1, maxCellVolume: maxCell || 1 };
  }, [candle]);

  return (
    <div className={`flex flex-col min-w-[220px] border-r border-border-color h-full ${isActive ? 'bg-gray-900/50' : 'bg-panel-bg'}`}>
      {/* Bar Header info */}
      <div className="text-[10px] text-center py-1 border-b border-gray-800 text-gray-500 font-mono">
        <div>{candle.startTime}</div>
        <div className={`font-bold ${candle.close > candle.open ? 'text-kr-red' : candle.close < candle.open ? 'text-kr-blue' : 'text-gray-400'}`}>
            Vol: {candle.totalVolume.toLocaleString()}
        </div>
        <div className="text-[9px] flex justify-center gap-1">
            <span>D: {candle.delta > 0 ? '+' : ''}{candle.delta}</span>
        </div>
      </div>

      {/* Candle Body (Ladder) */}
      <div className="flex-1 overflow-y-auto hide-scrollbar relative">
         {/* Render rows */}
         {candle.priceLevels.map((row, index) => (
            <Row 
                key={row.price} 
                row={row} 
                maxTotalVolume={maxTotalVolume} 
                maxCellVolume={maxCellVolume}
                isHigh={index === 0}
                isLow={index === candle.priceLevels.length - 1}
                isCurrent={isActive && row.price === candle.close}
            />
         ))}
      </div>
    </div>
  );
};

interface RowProps {
    row: PriceLevelData;
    maxTotalVolume: number;
    maxCellVolume: number;
    isHigh: boolean;
    isLow: boolean;
    isCurrent: boolean;
}

const Row: React.FC<RowProps> = ({ row, maxTotalVolume, maxCellVolume, isHigh, isLow, isCurrent }) => {
  // Profile Bar Width
  const profileWidth = (row.totalVolume / maxTotalVolume) * 100;

  // Heatmap Opacity
  const getOpacity = (vol: number) => {
      if (vol === 0) return 0;
      const ratio = vol / maxCellVolume;
      return Math.min(0.85, Math.max(0.05, Math.sqrt(ratio))); 
  };

  const sellOpacity = getOpacity(row.sellVolume);
  const buyOpacity = getOpacity(row.buyVolume);

  return (
    <div className={`grid grid-cols-12 gap-px text-[10px] font-mono leading-tight relative border-b border-gray-800/30 ${isCurrent ? 'bg-gray-700/30' : ''}`}>
      
      {/* Bid (Sell Side) */}
      <div 
        className={`col-span-4 px-1 text-right flex items-center justify-end text-gray-200 relative
            ${row.imbalanceSell ? 'border border-yellow-400 font-bold' : ''}
        `}
        style={{ backgroundColor: `rgba(77, 148, 255, ${sellOpacity})` }}
      >
        {row.stackedImbalanceSell && <div className="absolute inset-y-0 right-0 w-1 bg-kr-blue z-20"></div>}
        <span className="relative z-10">{row.sellVolume}</span>
      </div>

      {/* Price */}
      <div className={`col-span-4 flex items-center justify-center font-medium text-gray-400 relative border-x border-gray-800/30
        ${isCurrent ? 'text-white font-bold bg-gray-600' : ''}
      `}>
        {row.isPOC && (
            <div className={`absolute inset-0 border ${COLORS.POC_BORDER} pointer-events-none`}></div>
        )}
        
        {/* Unfinished / Zero Indicators */}
        {row.isUnfinished && (isHigh || isLow) && (
             <Magnet className="w-3 h-3 text-highlight absolute left-0 ml-0.5 opacity-70" />
        )}
        {!row.isUnfinished && (isHigh || isLow) && (
             <Ban className="w-3 h-3 text-gray-600 absolute left-0 ml-0.5 opacity-70" />
        )}

        {row.price.toLocaleString()}
      </div>

      {/* Ask (Buy Side) */}
      <div 
        className={`col-span-4 px-1 text-left flex items-center justify-start text-gray-200 relative
            ${row.imbalanceBuy ? 'border border-yellow-400 font-bold' : ''}
        `}
        style={{ backgroundColor: `rgba(255, 77, 77, ${buyOpacity})` }}
      >
        {row.stackedImbalanceBuy && <div className="absolute inset-y-0 left-0 w-1 bg-kr-red z-20"></div>}
        <span className="relative z-10">{row.buyVolume}</span>
      </div>

      {/* Volume Profile Overlay (Background) */}
      <div 
        className={`absolute top-0 bottom-0 left-0 opacity-10 pointer-events-none z-0 ${row.delta > 0 ? 'bg-kr-red' : 'bg-kr-blue'}`}
        style={{ width: `${profileWidth}%` }}
      ></div>
    </div>
  );
};

export default FootprintBarComponent;
