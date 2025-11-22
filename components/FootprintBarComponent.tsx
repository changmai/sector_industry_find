
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

  const highIndex = priceRows.indexOf(candle.high);
  const lowIndex = priceRows.indexOf(candle.low);
  const openIndex = priceRows.indexOf(candle.open);
  const closeIndex = priceRows.indexOf(candle.close);
  
  const hasValidIndices = highIndex !== -1 && lowIndex !== -1 && openIndex !== -1 && closeIndex !== -1;
  
  const bodyTopIndex = Math.min(openIndex, closeIndex);
  const bodyBottomIndex = Math.max(openIndex, closeIndex);
  
  // Wick covers full height of High row to Bottom of Low row
  const wickTop = highIndex * ROW_HEIGHT;
  const wickHeight = (lowIndex - highIndex + 1) * ROW_HEIGHT;
  
  const bodyTop = bodyTopIndex * ROW_HEIGHT;
  const bodyHeight = (bodyBottomIndex - bodyTopIndex + 1) * ROW_HEIGHT;

  // Helper for heatmap style opacity
  const getDeltaStyle = (val: number) => {
      if (val === 0) return {};
      // Simple scaling for visualization
      const opacity = Math.min(0.8, Math.max(0.2, Math.abs(val) / 500));
      return { backgroundColor: val > 0 ? `rgba(255, 77, 77, ${opacity})` : `rgba(77, 148, 255, ${opacity})` };
  };

  // Calculate explicit height for the body area
  const chartBodyHeight = priceRows.length * ROW_HEIGHT;

  return (
    // Increased min-width to 120px, added margin-right for spacing
    <div className={`flex flex-col min-w-[120px] border-r border-border-color shrink-0 mr-1 h-fit min-h-full ${isActive ? 'bg-gray-900/50' : 'bg-panel-bg'}`}>
      
      {/* Header Info - Compact */}
      <div className="h-[35px] border-b border-gray-800 text-[9px] text-center flex flex-col justify-center text-gray-500 font-mono leading-tight shrink-0 bg-inherit z-10">
        <div>{candle.startTime}</div>
        <div className={`font-bold ${candle.close > candle.open ? 'text-kr-red' : candle.close < candle.open ? 'text-kr-blue' : 'text-gray-400'}`}>
            {candle.close.toLocaleString()}
        </div>
      </div>

      {/* Main Content Area - STRICT HEIGHT to match sticky column */}
      <div 
        className="flex flex-row relative shrink-0"
        style={{ height: chartBodyHeight }}
      >
          
          {/* OHLC Strip Column (8px) */}
          <div className="w-[8px] border-r border-gray-800/30 relative shrink-0 bg-gray-900/20 h-full">
             {hasValidIndices && (
                 <>
                    {/* Wick */}
                    <div 
                        className={`absolute left-1/2 -translate-x-1/2 w-[1px] ${wickColor}`}
                        style={{ top: wickTop, height: wickHeight }}
                    ></div>
                    {/* Body */}
                    <div 
                        className={`absolute left-[1px] right-[1px] ${stripColor} rounded-[1px] z-10`}
                        style={{ top: bodyTop, height: bodyHeight }}
                    ></div>
                 </>
             )}
          </div>

          {/* Footprint Rows Container */}
          <div className="flex flex-col flex-1">
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
      
      {/* Bottom Stats Table (Heatmap) - Sticky Bottom */}
      <div className={`sticky bottom-0 border-t border-gray-700 mt-auto shrink-0 z-20 shadow-[0_-1px_2px_rgba(0,0,0,0.3)] ${isActive ? 'bg-gray-900' : 'bg-panel-bg'}`}>
          <StatRow label="Delta" value={candle.delta} style={getDeltaStyle(candle.delta)} isDelta />
          <StatRow label="Max" value={candle.maxDelta} style={getDeltaStyle(candle.maxDelta)} isDelta />
          <StatRow label="Min" value={candle.minDelta} style={getDeltaStyle(candle.minDelta)} isDelta />
          <StatRow label="Vol" value={candle.totalVolume} style={{}} />
      </div>
    </div>
  );
};

const StatRow: React.FC<{ label: string, value: number, style: React.CSSProperties, isDelta?: boolean }> = ({ label, value, style, isDelta }) => (
    <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800 last:border-b-0" style={{ height: ROW_HEIGHT, ...style }}>
        <span className={`font-bold ${isDelta ? (value > 0 ? 'text-kr-red' : value < 0 ? 'text-kr-blue' : 'text-gray-400') : 'text-white'}`}>
            {value.toLocaleString()}
        </span>
    </div>
);

// Custom Grid System: 3fr (Bid) | 4fr (Price) | 3fr (Ask)
const EmptyRow: React.FC<{ price: number }> = ({ price }) => (
    <div 
        className="grid grid-cols-[3fr_4fr_3fr] gap-px text-[9px] font-mono border-b border-gray-800/10 opacity-20"
        style={{ height: ROW_HEIGHT }}
    >
        <div></div>
        <div className="text-center text-gray-700 flex items-center justify-center tracking-tighter scale-75">{price}</div>
        <div></div>
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
      return Math.min(0.85, Math.max(0.1, Math.sqrt(ratio))); 
  };

  const sellOpacity = getOpacity(row.sellVolume);
  const buyOpacity = getOpacity(row.buyVolume);

  return (
    <div 
        className={`grid grid-cols-[3fr_4fr_3fr] gap-px text-[9px] font-mono leading-tight relative border-b border-gray-800/30 items-center ${isCurrent ? 'bg-gray-700/30' : ''}`}
        style={{ height: ROW_HEIGHT }}
    >
      
      {/* Bid (Sell Side) - Wider (30%) */}
      <div 
        className={`px-0.5 h-full text-right flex items-center justify-end text-gray-200 relative overflow-hidden
            ${row.imbalanceSell ? 'border border-yellow-400 font-bold' : ''}
        `}
        style={{ backgroundColor: `rgba(77, 148, 255, ${sellOpacity})` }}
      >
        {row.stackedImbalanceSell && <div className="absolute inset-y-0 right-0 w-0.5 bg-kr-blue z-20"></div>}
        {/* Scale increased to 90 for visibility */}
        <span className="relative z-10 scale-90 origin-right">{row.sellVolume > 0 ? row.sellVolume : ''}</span>
      </div>

      {/* Price & Profile - Narrower (40%) */}
      <div className={`h-full flex items-center justify-center font-medium text-gray-400 relative border-x border-gray-800/30 overflow-hidden
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
             <Magnet className="w-2.5 h-2.5 text-highlight absolute left-0 ml-0.5 opacity-90 z-20" />
        )}
        {!row.isUnfinished && (isHigh || isLow) && (
             <Ban className="w-2.5 h-2.5 text-gray-600 absolute left-0 ml-0.5 opacity-90 z-20" />
        )}

        {/* Price Text Scaled Down to fit narrower column */}
        <span className="relative z-10 tracking-tighter scale-75">{row.price.toLocaleString()}</span>
      </div>

      {/* Ask (Buy Side) - Wider (30%) */}
      <div 
        className={`px-0.5 h-full text-left flex items-center justify-start text-gray-200 relative overflow-hidden
            ${row.imbalanceBuy ? 'border border-yellow-400 font-bold' : ''}
        `}
        style={{ backgroundColor: `rgba(255, 77, 77, ${buyOpacity})` }}
      >
        {row.stackedImbalanceBuy && <div className="absolute inset-y-0 left-0 w-0.5 bg-kr-red z-20"></div>}
        {/* Scale increased to 90 for visibility */}
        <span className="relative z-10 scale-90 origin-left">{row.buyVolume > 0 ? row.buyVolume : ''}</span>
      </div>
    </div>
  );
};

export default FootprintBarComponent;
