
import React, { useMemo } from 'react';
import { FootprintCandle, PriceLevelData } from '../types';
import { COLORS, ROW_HEIGHT } from '../constants';
import { Magnet, Ban } from 'lucide-react';

interface FootprintBarProps {
  candle: FootprintCandle;
  isActive: boolean;
  priceRows: number[];
}

const FootprintBarComponent: React.FC<FootprintBarProps> = ({ candle, isActive, priceRows }) => {
  // Create a quick lookup map for this bar's data
  const priceDataMap = useMemo(() => {
      const map = new Map<number, PriceLevelData>();
      candle.priceLevels.forEach(level => map.set(level.price, level));
      return map;
  }, [candle]);

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

  // --- OHLC Strip Calculations ---
  const isBullish = candle.close >= candle.open;
  const stripColor = isBullish ? 'bg-kr-red' : 'bg-kr-blue';
  const wickColor = isBullish ? 'bg-kr-red/50' : 'bg-kr-blue/50';

  // Note: priceRows is sorted Descending (High to Low)
  // So Higher Price = Lower Index
  const highIndex = priceRows.indexOf(candle.high);
  const lowIndex = priceRows.indexOf(candle.low);
  
  // For body, we want the range between Open and Close
  // Since rows are descending, the "Top" visual is the Min Index (Higher Price)
  const openIndex = priceRows.indexOf(candle.open);
  const closeIndex = priceRows.indexOf(candle.close);
  
  // Safe checks in case price is out of view (though global sync handles this)
  const hasValidIndices = highIndex !== -1 && lowIndex !== -1 && openIndex !== -1 && closeIndex !== -1;
  
  const bodyTopIndex = Math.min(openIndex, closeIndex);
  const bodyBottomIndex = Math.max(openIndex, closeIndex);
  
  // Update: Wick now covers the FULL height of the High row down to the Bottom of the Low row
  const wickTop = highIndex * ROW_HEIGHT;
  const wickHeight = (lowIndex - highIndex + 1) * ROW_HEIGHT;
  
  const bodyTop = bodyTopIndex * ROW_HEIGHT;
  const bodyHeight = (bodyBottomIndex - bodyTopIndex + 1) * ROW_HEIGHT;

  return (
    // Reduced min-width and added flex-row to accommodate OHLC strip
    <div className={`flex flex-col min-w-[140px] border-r border-border-color shrink-0 ${isActive ? 'bg-gray-900/50' : 'bg-panel-bg'}`}>
      
      {/* Header Info */}
      <div className="sticky top-0 z-20 bg-inherit border-b border-gray-800 text-[10px] text-center py-1 text-gray-500 font-mono shadow-sm">
        <div>{candle.startTime}</div>
        <div className={`font-bold ${candle.close > candle.open ? 'text-kr-red' : candle.close < candle.open ? 'text-kr-blue' : 'text-gray-400'}`}>
            Vol: {candle.totalVolume.toLocaleString()}
        </div>
        <div className="text-[9px] flex justify-center gap-1">
            <span>D: {candle.delta > 0 ? '+' : ''}{candle.delta}</span>
        </div>
      </div>

      {/* Main Content Area: OHLC Strip + Footprint Rows */}
      <div className="flex flex-row relative">
          
          {/* OHLC Strip Column (12px) */}
          <div className="w-[12px] border-r border-gray-800/30 relative shrink-0 bg-gray-900/20">
             {hasValidIndices && (
                 <>
                    {/* Wick */}
                    <div 
                        className={`absolute left-1/2 -translate-x-1/2 w-[1px] ${wickColor}`}
                        style={{ top: wickTop, height: wickHeight }}
                    ></div>
                    {/* Body */}
                    <div 
                        className={`absolute left-[2px] right-[2px] ${stripColor} rounded-[1px] z-10`}
                        style={{ top: bodyTop, height: bodyHeight }}
                    ></div>
                 </>
             )}
          </div>

          {/* Footprint Rows Container */}
          <div className="flex flex-col pb-4 flex-1">
            {priceRows.map((price) => {
                const rowData = priceDataMap.get(price);
                
                if (!rowData) {
                    return <EmptyRow key={price} price={price} />;
                }

                return (
                    <Row 
                        key={price} 
                        row={rowData} 
                        maxTotalVolume={maxTotalVolume} 
                        maxCellVolume={maxCellVolume}
                        isHigh={price === candle.high}
                        isLow={price === candle.low}
                        isCurrent={isActive && price === candle.close}
                    />
                );
            })}
          </div>
      </div>
    </div>
  );
};

// Adjusted Grid: 2 (Bid) - 8 (Price) - 2 (Ask)
const EmptyRow: React.FC<{ price: number }> = ({ price }) => (
    <div 
        className="grid grid-cols-12 gap-px text-[10px] font-mono border-b border-gray-800/10 opacity-20"
        style={{ height: ROW_HEIGHT }}
    >
        <div className="col-span-2"></div>
        <div className="col-span-8 text-center text-gray-700 flex items-center justify-center">{price}</div>
        <div className="col-span-2"></div>
    </div>
);

interface RowProps {
    row: PriceLevelData;
    maxTotalVolume: number;
    maxCellVolume: number;
    isHigh: boolean;
    isLow: boolean;
    isCurrent: boolean;
}

const Row: React.FC<RowProps> = ({ row, maxTotalVolume, maxCellVolume, isHigh, isLow, isCurrent }) => {
  const profileWidth = (row.totalVolume / maxTotalVolume) * 100;

  const getOpacity = (vol: number) => {
      if (vol === 0) return 0;
      const ratio = vol / maxCellVolume;
      return Math.min(0.85, Math.max(0.05, Math.sqrt(ratio))); 
  };

  const sellOpacity = getOpacity(row.sellVolume);
  const buyOpacity = getOpacity(row.buyVolume);

  return (
    <div 
        className={`grid grid-cols-12 gap-px text-[10px] font-mono leading-tight relative border-b border-gray-800/30 items-center ${isCurrent ? 'bg-gray-700/30' : ''}`}
        style={{ height: ROW_HEIGHT }}
    >
      
      {/* Bid (Sell Side) - Reduced to col-span-2 (approx 16%) */}
      <div 
        className={`col-span-2 px-1 h-full text-right flex items-center justify-end text-gray-200 relative
            ${row.imbalanceSell ? 'border border-yellow-400 font-bold' : ''}
        `}
        style={{ backgroundColor: `rgba(77, 148, 255, ${sellOpacity})` }}
      >
        {row.stackedImbalanceSell && <div className="absolute inset-y-0 right-0 w-1 bg-kr-blue z-20"></div>}
        <span className="relative z-10 scale-90 origin-right">{row.sellVolume > 0 ? row.sellVolume : ''}</span>
      </div>

      {/* Price & Profile - Expanded to col-span-8 (approx 66%) */}
      <div className={`col-span-8 h-full flex items-center justify-center font-medium text-gray-400 relative border-x border-gray-800/30 overflow-hidden
        ${isCurrent ? 'text-white font-bold bg-gray-600' : ''}
      `}>
        {/* Volume Profile Overlay */}
        <div 
            className={`absolute top-0 bottom-0 left-0 opacity-30 pointer-events-none z-0 ${row.delta > 0 ? 'bg-kr-red' : 'bg-kr-blue'}`}
            style={{ width: `${profileWidth}%` }}
        ></div>

        {row.isPOC && (
            <div className={`absolute inset-0 border ${COLORS.POC_BORDER} pointer-events-none z-10`}></div>
        )}
        
        {row.isUnfinished && (isHigh || isLow) && (
             <Magnet className="w-3 h-3 text-highlight absolute left-0 ml-0.5 opacity-90 z-20" />
        )}
        {!row.isUnfinished && (isHigh || isLow) && (
             <Ban className="w-3 h-3 text-gray-600 absolute left-0 ml-0.5 opacity-90 z-20" />
        )}

        <span className="relative z-10">{row.price.toLocaleString()}</span>
      </div>

      {/* Ask (Buy Side) - Reduced to col-span-2 (approx 16%) */}
      <div 
        className={`col-span-2 px-1 h-full text-left flex items-center justify-start text-gray-200 relative
            ${row.imbalanceBuy ? 'border border-yellow-400 font-bold' : ''}
        `}
        style={{ backgroundColor: `rgba(255, 77, 77, ${buyOpacity})` }}
      >
        {row.stackedImbalanceBuy && <div className="absolute inset-y-0 left-0 w-1 bg-kr-red z-20"></div>}
        <span className="relative z-10 scale-90 origin-left">{row.buyVolume > 0 ? row.buyVolume : ''}</span>
      </div>
    </div>
  );
};

export default FootprintBarComponent;
