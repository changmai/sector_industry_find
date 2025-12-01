
import React, { useMemo, useCallback } from 'react';
import { FootprintCandle, PriceLevelData } from '../types';
import { COLORS, ROW_HEIGHT, ZoomLevel } from '../constants';
import { Magnet, Ban } from 'lucide-react';

// Format large numbers with K suffix (e.g., 150 -> 0.1K, 1500 -> 1.5K)
const formatCompactNumber = (num: number): string => {
  const absNum = Math.abs(num);
  if (absNum >= 10000) {
    return (num / 1000).toFixed(0) + 'K';
  }
  if (absNum >= 100) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

interface FootprintBarProps {
  candle: FootprintCandle;
  isActive: boolean;
  priceRows: number[];
  zoomLevel: ZoomLevel;
  hideStats?: boolean; // Stats를 숨기고 별도 레이어에서 렌더링할 때 사용
}

const FootprintBarComponent: React.FC<FootprintBarProps> = React.memo(({ candle, isActive, priceRows, zoomLevel, hideStats = false }) => {
  // Calculate scaled row height based on zoom level
  const scale = zoomLevel / 100;
  const scaledRowHeight = Math.round(ROW_HEIGHT * scale);

  // Hide Bid/Ask columns when zoom < 75%
  const showBidAsk = zoomLevel >= 75;

  // Calculate min-width: when Bid/Ask hidden, reduce to 60% of original
  const baseMinWidth = 120; // Base min-width at 100%
  const scaledMinWidth = showBidAsk
    ? Math.round(baseMinWidth * scale)
    : Math.round(baseMinWidth * scale * 0.6); // 60% when Bid/Ask hidden

  // Create a quick lookup map for this bar's data
  const priceDataMap = useMemo(() => {
      const map = new Map<number, PriceLevelData>();
      candle.priceLevels.forEach(level => map.set(level.price, level));
      return map;
  }, [candle]);

  // Price to Index map - O(1) lookup instead of O(n) indexOf
  const priceIndexMap = useMemo(() => {
      const map = new Map<number, number>();
      priceRows.forEach((price, idx) => map.set(price, idx));
      return map;
  }, [priceRows]);

  // Helper function to find nearest price index when exact match not found
  // priceRows is sorted descending (high to low)
  const findNearestPriceIndex = useCallback((targetPrice: number): number => {
    // First try exact match
    const exactIdx = priceIndexMap.get(targetPrice);
    if (exactIdx !== undefined) return exactIdx;

    // If no exact match, find the nearest price in priceRows
    if (priceRows.length === 0) return -1;

    // priceRows is sorted descending, so binary search for nearest
    let left = 0;
    let right = priceRows.length - 1;

    // Handle edge cases
    if (targetPrice >= priceRows[0]) return 0;  // Above highest price
    if (targetPrice <= priceRows[right]) return right;  // Below lowest price

    // Binary search for the closest price
    while (left <= right) {
      const mid = Math.floor((left + right) / 2);
      if (priceRows[mid] === targetPrice) return mid;

      if (priceRows[mid] > targetPrice) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
    }

    // left is now the index of first price smaller than target
    // right is the index of first price larger than target
    // Return the closer one
    if (right < 0) return left;
    if (left >= priceRows.length) return right;

    const diffLeft = Math.abs(priceRows[left] - targetPrice);
    const diffRight = Math.abs(priceRows[right] - targetPrice);
    return diffLeft < diffRight ? left : right;
  }, [priceRows, priceIndexMap]);

  // Max Volume for Heatmap & Profile within this specific bar
  const { maxTotalVolume, maxCellVolume, maxAbsDelta } = useMemo(() => {
    let maxTotal = 0;
    let maxCell = 0;
    let maxAbsD = 0;
    candle.priceLevels.forEach(d => {
      if (d.totalVolume > maxTotal) maxTotal = d.totalVolume;
      if (d.buyVolume > maxCell) maxCell = d.buyVolume;
      if (d.sellVolume > maxCell) maxCell = d.sellVolume;
      if (Math.abs(d.delta) > maxAbsD) maxAbsD = Math.abs(d.delta);
    });
    return { maxTotalVolume: maxTotal || 1, maxCellVolume: maxCell || 1, maxAbsDelta: maxAbsD || 1 };
  }, [candle]);

  // --- OHLC Strip Calculations ---
  const isDoji = candle.open === candle.close;
  const isBullish = candle.close >= candle.open;
  const stripColor = isDoji ? 'bg-gray-300' : (isBullish ? 'bg-kr-red' : 'bg-kr-blue');
  const wickColor = isBullish ? 'bg-kr-red/50' : 'bg-kr-blue/50';

  // Use findNearestPriceIndex for robust OHLC index lookup
  const highIndex = findNearestPriceIndex(candle.high);
  const lowIndex = findNearestPriceIndex(candle.low);
  const openIndex = findNearestPriceIndex(candle.open);
  const closeIndex = findNearestPriceIndex(candle.close);

  // Always valid if priceRows has data
  const hasValidIndices = priceRows.length > 0 && highIndex !== -1 && lowIndex !== -1 && openIndex !== -1 && closeIndex !== -1;

  const bodyTopIndex = Math.min(openIndex, closeIndex);
  const bodyBottomIndex = Math.max(openIndex, closeIndex);

  // Wick covers full height of High row to Bottom of Low row
  const wickTop = highIndex * scaledRowHeight;
  const wickHeight = (lowIndex - highIndex + 1) * scaledRowHeight;

  // Doji candle: render as horizontal line at price level center
  let bodyTop: number;
  let bodyHeight: number;

  if (isDoji) {
    const DOJI_LINE_HEIGHT = 2;
    bodyTop = (openIndex * scaledRowHeight) + (scaledRowHeight / 2) - (DOJI_LINE_HEIGHT / 2);
    bodyHeight = DOJI_LINE_HEIGHT;
  } else {
    // Normal candle: full body from open to close
    bodyTop = bodyTopIndex * scaledRowHeight;
    bodyHeight = (bodyBottomIndex - bodyTopIndex + 1) * scaledRowHeight;
  }

  // Helper for heatmap style opacity - memoized to prevent recreation
  const getDeltaStyle = useCallback((val: number) => {
      if (val === 0) return {};
      // Simple scaling for visualization
      const opacity = Math.min(0.8, Math.max(0.2, Math.abs(val) / 500));
      return { backgroundColor: val > 0 ? `rgba(255, 77, 77, ${opacity})` : `rgba(77, 148, 255, ${opacity})` };
  }, []);

  // Calculate explicit height for the body area
  const chartBodyHeight = priceRows.length * scaledRowHeight;

  return (
    // Dynamic min-width based on zoom and showBidAsk
    // footprint-bar class for content-visibility optimization
    <div
      className={`footprint-bar flex flex-col border-r border-border-color shrink-0 mr-1 ${isActive ? 'bg-gray-900/50' : 'bg-panel-bg'}`}
      style={{ minWidth: scaledMinWidth, width: scaledMinWidth }}
    >
      
      {/* Header Info - Compact (hide numbers when zoom < 75%) */}
      <div className="h-[35px] border-b border-gray-800 text-[11px] text-center flex flex-col justify-center text-gray-500 font-mono leading-tight shrink-0 bg-inherit z-10">
        {showBidAsk ? (
          <>
            <div>{candle.startTime}</div>
            <div className={`font-bold ${candle.close > candle.open ? 'text-kr-red' : candle.close < candle.open ? 'text-kr-blue' : 'text-gray-400'}`}>
                {candle.close.toLocaleString()}
            </div>
          </>
        ) : (
          <div className={`w-full h-2 rounded ${candle.close > candle.open ? 'bg-kr-red' : candle.close < candle.open ? 'bg-kr-blue' : 'bg-gray-400'}`}></div>
        )}
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

          {/* Footprint Rows Container - Optimized: only render rows with data */}
          <div className="relative flex-1" style={{ height: priceRows.length * scaledRowHeight }}>
            {/* Background grid lines */}
            <div
              className="absolute inset-0 opacity-10"
              style={{
                backgroundImage: 'linear-gradient(to bottom, transparent calc(100% - 1px), #333 calc(100% - 1px))',
                backgroundSize: `100% ${scaledRowHeight}px`,
              }}
            />

            {/* Only render rows that have data */}
            {candle.priceLevels.map((levelData) => {
                const rowIndex = priceIndexMap.get(levelData.price);
                if (rowIndex === undefined) return null;

                return (
                    <div
                        key={levelData.price}
                        style={{
                            position: 'absolute',
                            top: rowIndex * scaledRowHeight,
                            left: 0,
                            right: 0,
                            height: scaledRowHeight,
                        }}
                    >
                        <Row
                            row={levelData}
                            maxTotalVolume={maxTotalVolume}
                            maxCellVolume={maxCellVolume}
                            maxAbsDelta={maxAbsDelta}
                            isHigh={levelData.price === candle.high}
                            isLow={levelData.price === candle.low}
                            isCurrent={isActive && levelData.price === candle.close}
                            showBidAsk={showBidAsk}
                            scaledRowHeight={scaledRowHeight}
                            showNumbers={showBidAsk}
                        />
                    </div>
                );
            })}
          </div>
      </div>
      
      {/* Bottom Stats Table (Heatmap) - Hidden when rendered separately */}
      {!hideStats && (
        <div className={`border-t border-gray-700 shrink-0 z-20 ${isActive ? 'bg-gray-900' : 'bg-panel-bg'}`}>
            <StatRow label="Delta" value={candle.delta} style={getDeltaStyle(candle.delta)} scaledRowHeight={scaledRowHeight} showNumbers={showBidAsk} />
            <StatRow label="Max" value={candle.maxDelta} style={getDeltaStyle(candle.maxDelta)} scaledRowHeight={scaledRowHeight} showNumbers={showBidAsk} />
            <StatRow label="Min" value={candle.minDelta} style={getDeltaStyle(candle.minDelta)} scaledRowHeight={scaledRowHeight} showNumbers={showBidAsk} />
            <PercentDeltaRow delta={candle.delta} totalVolume={candle.totalVolume} scaledRowHeight={scaledRowHeight} showNumbers={showBidAsk} />
            <StatRow label="Vol" value={candle.totalVolume} style={{}} scaledRowHeight={scaledRowHeight} showNumbers={showBidAsk} />
        </div>
      )}
    </div>
  );
});

const StatRow: React.FC<{ label: string, value: number, style: React.CSSProperties, scaledRowHeight: number, showNumbers: boolean }> = React.memo(({ label, value, style, scaledRowHeight, showNumbers }) => (
    <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800 last:border-b-0" style={{ height: scaledRowHeight, ...style }}>
        {showNumbers && (
          <span className="font-bold text-white drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
              {formatCompactNumber(value)}
          </span>
        )}
    </div>
));
StatRow.displayName = 'StatRow';

// % Delta Row: (Delta / Total Volume) * 100
const PercentDeltaRow: React.FC<{ delta: number, totalVolume: number, scaledRowHeight: number, showNumbers: boolean }> = React.memo(({ delta, totalVolume, scaledRowHeight, showNumbers }) => {
    const percentDelta = totalVolume > 0 ? (delta / totalVolume) * 100 : 0;
    const isPositive = percentDelta > 0;
    const isNegative = percentDelta < 0;

    // Background color based on value
    const bgStyle: React.CSSProperties = {};
    if (percentDelta !== 0) {
        const opacity = Math.min(0.6, Math.max(0.2, Math.abs(percentDelta) / 50));
        bgStyle.backgroundColor = isPositive ? `rgba(255, 77, 77, ${opacity})` : `rgba(77, 148, 255, ${opacity})`;
    }

    return (
        <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800" style={{ height: scaledRowHeight, ...bgStyle }}>
            {showNumbers && (
                <span className={`font-bold drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)] ${isPositive ? 'text-kr-red' : isNegative ? 'text-kr-blue' : 'text-gray-400'}`}>
                    {percentDelta > 0 ? '+' : ''}{percentDelta.toFixed(1)}%
                </span>
            )}
        </div>
    );
});
PercentDeltaRow.displayName = 'PercentDeltaRow';

// Custom Grid System: 2.5fr (Bid) | 3fr (Price) | 2.4fr (Delta) | 2.5fr (Ask)
const EmptyRow: React.FC<{ price: number }> = React.memo(({ price }) => (
    <div
        className="grid grid-cols-[2.5fr_3fr_2.4fr_2.5fr] gap-px text-[11px] font-mono border-b border-gray-800/10 opacity-20"
        style={{ height: ROW_HEIGHT }}
    >
        <div></div>
        <div className="text-center text-gray-700 flex items-center justify-center tracking-tighter scale-75">{price}</div>
        <div></div>
        <div></div>
    </div>
));

interface RowProps {
    row: PriceLevelData;
    maxTotalVolume: number;
    maxCellVolume: number;
    maxAbsDelta: number;
    isHigh: boolean;
    isLow: boolean;
    isCurrent: boolean;
    showBidAsk: boolean;
    scaledRowHeight: number;
    showNumbers: boolean; // Hide numbers when zoom < 75%
}

// Custom comparison function for Row - prevents re-render when row data hasn't changed
const areRowPropsEqual = (prevProps: RowProps, nextProps: RowProps): boolean => {
  return (
    prevProps.row.price === nextProps.row.price &&
    prevProps.row.buyVolume === nextProps.row.buyVolume &&
    prevProps.row.sellVolume === nextProps.row.sellVolume &&
    prevProps.row.totalVolume === nextProps.row.totalVolume &&
    prevProps.row.delta === nextProps.row.delta &&
    prevProps.row.isPOC === nextProps.row.isPOC &&
    prevProps.row.isVA === nextProps.row.isVA &&
    prevProps.row.isVAH === nextProps.row.isVAH &&
    prevProps.row.isVAL === nextProps.row.isVAL &&
    prevProps.row.isLVN === nextProps.row.isLVN &&
    prevProps.row.isUnfinished === nextProps.row.isUnfinished &&
    prevProps.row.imbalanceBuy === nextProps.row.imbalanceBuy &&
    prevProps.row.imbalanceSell === nextProps.row.imbalanceSell &&
    prevProps.row.stackedImbalanceBuy === nextProps.row.stackedImbalanceBuy &&
    prevProps.row.stackedImbalanceSell === nextProps.row.stackedImbalanceSell &&
    prevProps.maxTotalVolume === nextProps.maxTotalVolume &&
    prevProps.maxCellVolume === nextProps.maxCellVolume &&
    prevProps.maxAbsDelta === nextProps.maxAbsDelta &&
    prevProps.isHigh === nextProps.isHigh &&
    prevProps.isLow === nextProps.isLow &&
    prevProps.isCurrent === nextProps.isCurrent &&
    prevProps.showBidAsk === nextProps.showBidAsk &&
    prevProps.scaledRowHeight === nextProps.scaledRowHeight &&
    prevProps.showNumbers === nextProps.showNumbers
  );
};

const Row: React.FC<RowProps> = React.memo(({ row, maxTotalVolume, maxCellVolume, maxAbsDelta, isHigh, isLow, isCurrent, showBidAsk, scaledRowHeight, showNumbers }) => {
  const profileWidth = (row.totalVolume / maxTotalVolume) * 100;
  const deltaWidth = (Math.abs(row.delta) / maxAbsDelta) * 100;

  const getOpacity = (vol: number) => {
      if (vol === 0) return 0;
      const ratio = vol / maxCellVolume;
      return Math.min(0.85, Math.max(0.1, Math.sqrt(ratio)));
  };

  const sellOpacity = getOpacity(row.sellVolume);
  const buyOpacity = getOpacity(row.buyVolume);

  // Dynamic grid: hide Bid/Ask when showBidAsk is false
  const gridCols = showBidAsk
    ? 'grid-cols-[2.5fr_3fr_2.4fr_2.5fr]'
    : 'grid-cols-[3fr_2fr]';

  return (
    <div
        className={`grid ${gridCols} gap-px text-[11px] font-mono leading-tight relative border-b border-gray-800/30 items-center ${isCurrent ? 'bg-gray-700/30' : ''} ${row.isLVN ? COLORS.LVN_BG : ''}`}
        style={{ height: scaledRowHeight }}
    >

      {/* Bid (Sell Side) - Hidden when zoom < 75% */}
      {showBidAsk && (
        <div
          className={`px-0.5 h-full text-right flex items-center justify-end text-gray-200 relative overflow-hidden
              ${row.imbalanceSell ? `border ${COLORS.IMBALANCE_BORDER} font-bold` : ''}
          `}
          style={{ backgroundColor: `rgba(77, 148, 255, ${sellOpacity})` }}
        >
          {row.stackedImbalanceSell && <div className="absolute inset-y-0 right-0 w-0.5 bg-kr-blue z-20"></div>}
          <span className="relative z-10 origin-right">{row.sellVolume > 0 ? formatCompactNumber(row.sellVolume) : ''}</span>
        </div>
      )}

      {/* Price & Profile */}
      <div className={`h-full flex items-center justify-center font-medium text-gray-400 relative border-x border-gray-800/30 overflow-hidden
        ${isCurrent ? 'text-white font-bold bg-gray-600' : ''}
      `}>
        {/* VA Indicator - Left vertical line (thinner when zoomed out) */}
        {row.isVA && (
          <div
            className={`absolute left-0 top-0 bottom-0 z-20 ${showBidAsk ? 'w-[3px]' : 'w-[1px]'}`}
            style={{ backgroundColor: row.isVAH || row.isVAL ? '#00d3ff' : '#82e9ff' }}
          ></div>
        )}

        {/* Volume Profile Overlay - White color */}
        <div
            className="absolute top-0 bottom-0 left-0 opacity-40 pointer-events-none z-0 bg-white"
            style={{ width: `${profileWidth}%` }}
        ></div>

        {row.isPOC && (
            <div className={`absolute inset-0 ${showBidAsk ? 'border-2' : 'border'} ${COLORS.POC_BORDER} pointer-events-none z-10`}></div>
        )}

        {row.isUnfinished && (isHigh || isLow) && (
             <Magnet className="w-2.5 h-2.5 text-highlight absolute left-0 ml-0.5 opacity-90 z-20" />
        )}
        {!row.isUnfinished && (isHigh || isLow) && (
             <Ban className="w-2.5 h-2.5 text-gray-600 absolute left-0 ml-0.5 opacity-90 z-20" />
        )}

        {/* LVN indicator - dashed line */}
        {row.isLVN && (
          <div
            className="absolute inset-x-0 top-1/2 border-t-2 border-dashed z-10"
            style={{ borderColor: '#ffff00' }}
          ></div>
        )}

        {showNumbers && (
          <span className="relative z-10 tracking-tighter text-[9px] scale-75">{row.price.toLocaleString()}</span>
        )}
      </div>

      {/* Delta Bar Column */}
      <div className="h-full relative overflow-hidden flex items-center justify-center border-x border-gray-800/30">
        <div
          className={`absolute top-0 bottom-0 left-0 ${row.delta > 0 ? 'bg-kr-red' : 'bg-kr-blue'} opacity-40`}
          style={{ width: `${deltaWidth}%` }}
        />
        {showNumbers && (
          <span className={`relative z-10 ${row.delta > 0 ? 'text-kr-red' : row.delta < 0 ? 'text-kr-blue' : 'text-gray-500'}`}>
            {row.delta !== 0 ? (row.delta > 0 ? '+' : '') + formatCompactNumber(row.delta) : ''}
          </span>
        )}
      </div>

      {/* Ask (Buy Side) - Hidden when zoom < 75% */}
      {showBidAsk && (
        <div
          className={`px-0.5 h-full text-left flex items-center justify-start text-gray-200 relative overflow-hidden
              ${row.imbalanceBuy ? `border ${COLORS.IMBALANCE_BORDER} font-bold` : ''}
          `}
          style={{ backgroundColor: `rgba(255, 77, 77, ${buyOpacity})` }}
        >
          {row.stackedImbalanceBuy && <div className="absolute inset-y-0 left-0 w-0.5 bg-kr-red z-20"></div>}
          <span className="relative z-10 origin-left">{row.buyVolume > 0 ? formatCompactNumber(row.buyVolume) : ''}</span>
        </div>
      )}
    </div>
  );
}, areRowPropsEqual);

export default FootprintBarComponent;
export { StatRow, PercentDeltaRow, formatCompactNumber };
