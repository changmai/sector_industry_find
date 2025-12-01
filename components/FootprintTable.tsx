
import React, { useRef, useEffect, useMemo, useCallback, useState, MouseEvent } from 'react';
import { FootprintCandle } from '../types';
import FootprintBarComponent, { StatRow, PercentDeltaRow, formatCompactNumber } from './FootprintBarComponent';
import { Magnet, Ban } from 'lucide-react';
import { ROW_HEIGHT, BAR_WIDTH, ZoomLevel, COLORS } from '../constants';

interface FootprintTableProps {
  bars: FootprintCandle[];
  activeBar: FootprintCandle | null;
  globalHigh: number;
  globalLow: number;
  priceStep: number;
  zoomLevel: ZoomLevel;
  onScrollChange?: (visibleBarIndex: number) => void; // Callback for scroll sync with CVD chart
}

// Constants for virtualization
const BASE_BAR_WIDTH = BAR_WIDTH;
const HEADER_HEIGHT = 35;
const OVERSCAN = 2; // Extra bars to render outside viewport
const RIGHT_MARGIN = 80; // Right margin to align with CVD chart's price scale

const FootprintTable: React.FC<FootprintTableProps> = ({ bars, activeBar, globalHigh, globalLow, priceStep, zoomLevel, onScrollChange }) => {
  // Calculate scaled dimensions based on zoom
  const scale = zoomLevel / 100;
  const scaledRowHeight = Math.round(ROW_HEIGHT * scale);

  // Hide Bid/Ask columns when zoom < 75%
  const showBidAsk = zoomLevel >= 75;

  // Bar width: 60% when Bid/Ask hidden
  const scaledBarWidth = showBidAsk
    ? Math.round(BASE_BAR_WIDTH * scale)
    : Math.round(BASE_BAR_WIDTH * scale * 0.6);
  const containerRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const isAutoScrollEnabled = useRef<boolean>(true);
  const prevBarsLengthRef = useRef<number>(0);
  const prevPriceStepRef = useRef<number>(priceStep);

  // Container dimensions
  const [containerWidth, setContainerWidth] = useState(800);
  const [scrollLeft, setScrollLeft] = useState(0);
  const [scrollTop, setScrollTop] = useState(0);

  // Ref for Stats Label Column scroll sync
  const statsColumnRef = useRef<HTMLDivElement>(null);

  // Hover state for crosshair
  const [hoverY, setHoverY] = useState<number | null>(null);
  const [hoverPrice, setHoverPrice] = useState<number | null>(null);

  // Generate Master Price List - FIXED: Always regenerate when deps change
  const priceRows = useMemo(() => {
    const alignedHigh = Math.ceil(globalHigh / priceStep) * priceStep;
    const alignedLow = Math.floor(globalLow / priceStep) * priceStep;

    const rows: number[] = [];
    for (let p = alignedHigh; p >= alignedLow; p -= priceStep) {
      rows.push(p);
    }

    return rows;
  }, [globalHigh, globalLow, priceStep]);

  // Calculate heights with scaled row height
  const chartBodyHeight = priceRows.length * scaledRowHeight;
  const STATS_HEIGHT = scaledRowHeight * 5; // Delta, Max, Min, %Delta, Vol
  const totalRowHeight = HEADER_HEIGHT + chartBodyHeight; // Stats는 별도 고정 레이어로 분리

  // Total content width with scaled bar width
  const totalBars = bars.length + (activeBar ? 1 : 0);
  const totalContentWidth = totalBars * scaledBarWidth;

  // Calculate visible range (direct virtualization)
  // Now calculated from the RIGHT edge since bars are rendered right-to-left
  const visibleRange = useMemo(() => {
    const effectiveBarWidth = scaledBarWidth || 1; // Prevent division by zero
    // Calculate how far scrolled from the right edge
    const scrollRight = Math.max(0, totalContentWidth - containerWidth - scrollLeft);
    // startIdx = 0 means rightmost bar (newest)
    const startIdx = Math.max(0, Math.floor(scrollRight / effectiveBarWidth) - OVERSCAN);
    const visibleCount = Math.ceil(containerWidth / effectiveBarWidth) + OVERSCAN * 2;
    const endIdx = Math.min(totalBars, startIdx + visibleCount);
    return { startIdx, endIdx };
  }, [scrollLeft, containerWidth, totalBars, scaledBarWidth, totalContentWidth]);

  // Handle scroll (both X and Y axis)
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    setScrollLeft(target.scrollLeft);
    setScrollTop(target.scrollTop);

    // Sync Stats Label Column Y scroll
    if (statsColumnRef.current) {
      statsColumnRef.current.scrollTop = target.scrollTop;
    }

    // Auto-scroll detection (X-axis) - now checks if scrolled to RIGHT edge
    const { scrollWidth, clientWidth } = target;
    isAutoScrollEnabled.current = scrollWidth - clientWidth - target.scrollLeft < 100;

    // Notify parent about scroll position for CVD chart sync
    if (onScrollChange && scaledBarWidth > 0) {
      // Calculate precise scroll position (with decimal) for smooth sync
      const scrollRight = Math.max(0, totalContentWidth - clientWidth - target.scrollLeft);
      const visibleBarPosition = scrollRight / scaledBarWidth;
      onScrollChange(visibleBarPosition);
    }
  }, [onScrollChange, scaledBarWidth, totalContentWidth]);

  // Keep scroll position at right edge (newest bar always visible on right)
  useEffect(() => {
    if (scrollContainerRef.current && isAutoScrollEnabled.current) {
      const newLength = bars.length + (activeBar ? 1 : 0);
      // FIXED: Always scroll to right when bars change (including recalculate)
      // Use setTimeout to ensure DOM has updated
      setTimeout(() => {
        if (scrollContainerRef.current) {
          const { scrollWidth, clientWidth } = scrollContainerRef.current;
          scrollContainerRef.current.scrollLeft = scrollWidth - clientWidth;
        }
      }, 0);
      prevBarsLengthRef.current = newLength;
    }
  }, [bars.length, activeBar, totalContentWidth]);

  // Container resize observer
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setContainerWidth(rect.width - 70); // Subtract stats label column width
      }
    };

    updateSize();

    const resizeObserver = new ResizeObserver(updateSize);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => resizeObserver.disconnect();
  }, []);

  // Initialize scroll position to right edge on mount
  useEffect(() => {
    if (scrollContainerRef.current) {
      const { scrollWidth, clientWidth } = scrollContainerRef.current;
      scrollContainerRef.current.scrollLeft = scrollWidth - clientWidth;
    }
  }, []);

  // FIXED: Reset scroll to right edge when bars array reference changes (after recalculate)
  const prevBarsRef = useRef(bars);
  useEffect(() => {
    // Detect if bars array reference changed (not just length)
    if (prevBarsRef.current !== bars && scrollContainerRef.current) {
      // Bars were recalculated, scroll to right
      setTimeout(() => {
        if (scrollContainerRef.current) {
          const { scrollWidth, clientWidth } = scrollContainerRef.current;
          scrollContainerRef.current.scrollLeft = scrollWidth - clientWidth;
        }
      }, 0);
    }
    prevBarsRef.current = bars;
  }, [bars]);

  // Handle mouse move for crosshair
  const handleMouseMove = useCallback((e: MouseEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    const rect = target.getBoundingClientRect();

    // Calculate Y position relative to scroll container (accounting for scroll and header)
    const relativeY = e.clientY - rect.top + target.scrollTop - HEADER_HEIGHT;

    // Only show crosshair within chart body area
    if (relativeY >= 0 && relativeY < chartBodyHeight) {
      // Calculate which row is being hovered
      const rowIndex = Math.floor(relativeY / scaledRowHeight);

      if (rowIndex >= 0 && rowIndex < priceRows.length) {
        const price = priceRows[rowIndex];
        // Calculate the Y position for the center of this row (relative to chart body)
        const rowCenterY = (rowIndex * scaledRowHeight) + (scaledRowHeight / 2);
        setHoverY(rowCenterY);
        setHoverPrice(price);
      }
    } else {
      setHoverY(null);
      setHoverPrice(null);
    }
  }, [chartBodyHeight, scaledRowHeight, priceRows]);

  const handleMouseLeave = useCallback(() => {
    setHoverY(null);
    setHoverPrice(null);
  }, []);

  // Auto-scroll Y-axis when priceStep changes to center on active data
  useEffect(() => {
    if (prevPriceStepRef.current !== priceStep && scrollContainerRef.current) {
      // Get the target price to center on (activeBar or last history bar)
      const targetBar = activeBar || (bars.length > 0 ? bars[bars.length - 1] : null);

      if (targetBar) {
        // Calculate center price of the target bar
        const centerPrice = (targetBar.high + targetBar.low) / 2;

        // Calculate aligned prices for current priceStep
        const alignedHigh = Math.ceil(globalHigh / priceStep) * priceStep;

        // Calculate row index for center price
        const rowIndex = Math.floor((alignedHigh - centerPrice) / priceStep);

        // Calculate scroll position to center this row in viewport
        const targetScrollTop = (rowIndex * scaledRowHeight) - (scrollContainerRef.current.clientHeight / 2) + HEADER_HEIGHT;

        // Apply scroll with bounds check
        scrollContainerRef.current.scrollTop = Math.max(0, targetScrollTop);
      }

      prevPriceStepRef.current = priceStep;
    }
  }, [priceStep, globalHigh, activeBar, bars]);

  // Render visible bars only
  // Bars are rendered right-to-left: newest bar (activeBar) is always on the right
  // Index 0 = rightmost (newest), higher index = further left (older)
  const barsLength = bars.length;

  // Optimized: Separate active bar ID tracking to minimize re-renders
  const activeBarId = activeBar?.id;

  const renderedBars = useMemo(() => {
    const elements: React.ReactNode[] = [];
    const { startIdx, endIdx } = visibleRange;
    // FIXED: Use bars directly instead of barsRef to ensure fresh data after recalculate
    const currentBars = bars;
    const currentActiveBar = activeBar; // Capture for closure
    const currentBarsLength = currentBars.length;

    for (let i = startIdx; i < endIdx; i++) {
      // Determine which bar to render based on index
      // If activeBar exists: i=0 is activeBar, i=1 is bars[barsLength-1], i=2 is bars[barsLength-2], etc.
      // If no activeBar: i=0 is bars[barsLength-1], i=1 is bars[barsLength-2], etc.

      let bar;
      let isActive = false;

      if (currentActiveBar) {
        if (i === 0) {
          bar = currentActiveBar;
          isActive = true;
        } else {
          const historyIndex = currentBarsLength - i;
          if (historyIndex >= 0 && historyIndex < currentBarsLength) {
            bar = currentBars[historyIndex];
          }
        }
      } else {
        // No active bar
        const historyIndex = currentBarsLength - 1 - i;
        if (historyIndex >= 0 && historyIndex < currentBarsLength) {
          bar = currentBars[historyIndex];
        }
      }

      if (!bar) continue;

      // Position from right: i=0 is rightmost
      const rightPosition = i * scaledBarWidth;

      elements.push(
        <div
          key={bar.id}
          style={{
            position: 'absolute',
            right: rightPosition,
            top: 0,
            width: scaledBarWidth,
            height: totalRowHeight,
          }}
        >
          <FootprintBarComponent
            candle={bar}
            isActive={isActive}
            priceRows={priceRows}
            zoomLevel={zoomLevel}
            hideStats={true}
          />
        </div>
      );
    }

    return elements;
  }, [visibleRange, bars, activeBarId, activeBar, priceRows, totalRowHeight, scaledBarWidth, zoomLevel]);

  // Generate visible bars data for stats rendering (memoized)
  const visibleBarsData = useMemo(() => {
    const result: { bar: FootprintCandle; isActive: boolean; rightPosition: number }[] = [];
    const { startIdx, endIdx } = visibleRange;

    for (let i = startIdx; i < endIdx; i++) {
      let bar: FootprintCandle | undefined;
      let isActive = false;

      if (activeBar) {
        if (i === 0) {
          bar = activeBar;
          isActive = true;
        } else {
          const historyIndex = bars.length - i;
          if (historyIndex >= 0 && historyIndex < bars.length) {
            bar = bars[historyIndex];
          }
        }
      } else {
        const historyIndex = bars.length - 1 - i;
        if (historyIndex >= 0 && historyIndex < bars.length) {
          bar = bars[historyIndex];
        }
      }

      if (bar) {
        result.push({ bar, isActive, rightPosition: i * scaledBarWidth });
      }
    }

    return result;
  }, [visibleRange, bars, activeBar, scaledBarWidth]);

  // Delta style helper
  const getDeltaStyle = useCallback((val: number): React.CSSProperties => {
    if (val === 0) return {};
    const opacity = Math.min(0.8, Math.max(0.2, Math.abs(val) / 500));
    return { backgroundColor: val > 0 ? `rgba(255, 77, 77, ${opacity})` : `rgba(77, 148, 255, ${opacity})` };
  }, []);

  return (
    <div
      ref={containerRef}
      className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color shadow-xl relative overflow-hidden"
    >
      {/* Main Chart Area */}
      <div className="flex-1 flex overflow-hidden min-h-0">
        {/* Left Label Column */}
        <div className="z-30 bg-panel-bg border-r border-border-color flex flex-col shrink-0 w-[70px] shadow-md overflow-hidden">
          {/* Header Placeholder - fixed at top */}
          <div
            className="border-b border-gray-800 flex items-center justify-center text-[9px] text-gray-500 font-mono bg-panel-bg shrink-0"
            style={{ height: HEADER_HEIGHT }}
          >
            Stats
          </div>

          {/* Scrollable body area (synced with main container) */}
          <div
            ref={statsColumnRef}
            className="flex-1 overflow-hidden"
            style={{ minHeight: 0 }}
          >
            <div style={{ height: chartBodyHeight, minHeight: chartBodyHeight }}></div>
          </div>
        </div>

        {/* Direct Virtualized Scroll Container */}
        <div
          ref={scrollContainerRef}
          className="flex-1 overflow-auto custom-scrollbar gpu-accelerated relative"
          onScroll={handleScroll}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          style={{ minHeight: 0 }}
        >
          {totalBars === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-600">
              Waiting for market data...
            </div>
          ) : (
            <div
              style={{
                display: 'flex',
                justifyContent: 'flex-end',
                width: Math.max(containerWidth, totalContentWidth),
                minWidth: Math.max(containerWidth, totalContentWidth),
                height: totalRowHeight,
                minHeight: totalRowHeight,
              }}
            >
              {/* Inner container for bars - positioned from right */}
              <div
                style={{
                  position: 'relative',
                  width: totalContentWidth,
                  minWidth: totalContentWidth,
                  height: totalRowHeight,
                  flexShrink: 0,
                }}
              >
                {renderedBars}

                {/* Crosshair horizontal line */}
                {hoverY !== null && (
                  <div
                    className="absolute pointer-events-none z-50"
                    style={{
                      top: HEADER_HEIGHT + hoverY,
                      left: 0,
                      right: 0,
                      height: 1,
                      backgroundColor: '#ffffff',
                      opacity: 0.6,
                    }}
                  />
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right Price Axis Column */}
        <div
          className="z-30 bg-panel-bg border-l border-border-color flex flex-col shrink-0 shadow-md overflow-hidden relative"
          style={{ width: RIGHT_MARGIN }}
        >
          {/* Header Placeholder */}
          <div
            className="border-b border-gray-800 flex items-center justify-center text-[9px] text-gray-500 font-mono bg-panel-bg shrink-0"
            style={{ height: HEADER_HEIGHT }}
          >
            Price
          </div>

          {/* Price Labels - Synced with vertical scroll */}
          <div
            className="flex-1 overflow-hidden relative"
            style={{ minHeight: 0 }}
          >
            <div
              style={{
                position: 'relative',
                height: chartBodyHeight,
                transform: `translateY(${-scrollTop}px)`,
              }}
            >
              {priceRows.map((price, idx) => (
                <div
                  key={price}
                  className="absolute w-full flex items-center justify-end pr-2 text-[9px] font-mono text-gray-400"
                  style={{
                    top: idx * scaledRowHeight,
                    height: scaledRowHeight,
                  }}
                >
                  {price.toLocaleString()}
                </div>
              ))}
            </div>

            {/* Hover Price Indicator */}
            {hoverY !== null && hoverPrice !== null && (
              <div
                className="absolute left-0 right-0 flex items-center justify-center bg-highlight text-black text-[10px] font-mono font-bold pointer-events-none z-50"
                style={{
                  top: hoverY - scrollTop,
                  height: scaledRowHeight,
                }}
              >
                {hoverPrice.toLocaleString()}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Stats Table - Fixed at bottom */}
      <div className="shrink-0 border-t border-gray-700 bg-panel-bg z-30 shadow-[0_-2px_4px_rgba(0,0,0,0.3)]" style={{ height: STATS_HEIGHT }}>
        <div className="flex h-full">
          {/* Stats Labels Column */}
          <div className="w-[70px] shrink-0 border-r border-border-color bg-panel-bg">
            <StatLabelRow label="Delta" scaledRowHeight={scaledRowHeight} />
            <StatLabelRow label="Max Delta" scaledRowHeight={scaledRowHeight} />
            <StatLabelRow label="Min Delta" scaledRowHeight={scaledRowHeight} />
            <StatLabelRow label="% Delta" scaledRowHeight={scaledRowHeight} />
            <StatLabelRow label="Volume" scaledRowHeight={scaledRowHeight} />
          </div>

          {/* Stats Values - Synced with horizontal scroll */}
          <div className="flex-1 overflow-hidden">
            <div
              style={{
                display: 'flex',
                justifyContent: 'flex-end',
                width: Math.max(containerWidth, totalContentWidth),
                minWidth: Math.max(containerWidth, totalContentWidth),
                transform: `translateX(${-scrollLeft}px)`,
              }}
            >
              <div
                style={{
                  position: 'relative',
                  width: totalContentWidth,
                  minWidth: totalContentWidth,
                  height: STATS_HEIGHT,
                }}
              >
                {visibleBarsData.map(({ bar, isActive, rightPosition }) => (
                  <div
                    key={`stats-${bar.id}`}
                    className={`absolute top-0 border-r border-border-color ${isActive ? 'bg-gray-900' : 'bg-panel-bg'}`}
                    style={{
                      right: rightPosition,
                      width: scaledBarWidth,
                      height: STATS_HEIGHT,
                    }}
                  >
                    <BarStats
                      candle={bar}
                      isActive={isActive}
                      scaledRowHeight={scaledRowHeight}
                      showBidAsk={showBidAsk}
                      getDeltaStyle={getDeltaStyle}
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Price Axis Spacer */}
          <div
            className="shrink-0 border-l border-border-color bg-panel-bg"
            style={{ width: RIGHT_MARGIN }}
          />
        </div>
      </div>

      {/* Legend / Status Bar */}
      <div className="h-6 bg-gray-900 border-t border-border-color flex items-center justify-between px-2 text-[10px] text-gray-500 shrink-0 z-20">
        <div className="flex space-x-3">
          <span className="flex items-center"><Magnet className="w-3 h-3 mr-1 text-highlight" /> Unfinished</span>
          <span className="flex items-center"><Ban className="w-3 h-3 mr-1 text-gray-500" /> Zero Print</span>
        </div>
        <div className="flex space-x-3 items-center">
          <span className="flex items-center mr-2">
            <div className="w-2 h-2 border border-yellow-400 mr-1"></div> Imbalance
          </span>
          <span>Stacked: <span className="text-kr-red">Buy</span> / <span className="text-kr-blue">Sell</span></span>
          <span className="ml-4 text-gray-600">| Bars: {totalBars} | Visible: {visibleRange.endIdx - visibleRange.startIdx}</span>
        </div>
      </div>
    </div>
  );
};

const StatLabelRow: React.FC<{ label: string; scaledRowHeight: number }> = React.memo(({ label, scaledRowHeight }) => (
  <div className="flex items-center justify-end pr-2 text-[9px] text-white font-bold font-mono border-b border-gray-800 last:border-b-0" style={{ height: scaledRowHeight }}>
    {label}
  </div>
));

// BarStats component for bottom stats area
interface BarStatsProps {
  candle: FootprintCandle;
  isActive: boolean;
  scaledRowHeight: number;
  showBidAsk: boolean;
  getDeltaStyle: (val: number) => React.CSSProperties;
}

const BarStats: React.FC<BarStatsProps> = React.memo(({ candle, isActive, scaledRowHeight, showBidAsk, getDeltaStyle }) => {
  const percentDelta = candle.totalVolume > 0 ? (candle.delta / candle.totalVolume) * 100 : 0;
  const isPositive = percentDelta > 0;
  const isNegative = percentDelta < 0;

  const percentDeltaBgStyle: React.CSSProperties = {};
  if (percentDelta !== 0) {
    const opacity = Math.min(0.6, Math.max(0.2, Math.abs(percentDelta) / 50));
    percentDeltaBgStyle.backgroundColor = isPositive ? `rgba(255, 77, 77, ${opacity})` : `rgba(77, 148, 255, ${opacity})`;
  }

  return (
    <div className={`h-full border-r border-border-color ${isActive ? 'bg-gray-900' : 'bg-panel-bg'}`}>
      <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800" style={{ height: scaledRowHeight, ...getDeltaStyle(candle.delta) }}>
        {showBidAsk && (
          <span className="font-bold text-white drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
            {formatCompactNumber(candle.delta)}
          </span>
        )}
      </div>
      <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800" style={{ height: scaledRowHeight, ...getDeltaStyle(candle.maxDelta) }}>
        {showBidAsk && (
          <span className="font-bold text-white drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
            {formatCompactNumber(candle.maxDelta)}
          </span>
        )}
      </div>
      <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800" style={{ height: scaledRowHeight, ...getDeltaStyle(candle.minDelta) }}>
        {showBidAsk && (
          <span className="font-bold text-white drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
            {formatCompactNumber(candle.minDelta)}
          </span>
        )}
      </div>
      <div className="flex items-center justify-center text-[10px] font-mono border-b border-gray-800" style={{ height: scaledRowHeight, ...percentDeltaBgStyle }}>
        {showBidAsk && (
          <span className={`font-bold drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)] ${isPositive ? 'text-kr-red' : isNegative ? 'text-kr-blue' : 'text-gray-400'}`}>
            {percentDelta > 0 ? '+' : ''}{percentDelta.toFixed(1)}%
          </span>
        )}
      </div>
      <div className="flex items-center justify-center text-[10px] font-mono" style={{ height: scaledRowHeight }}>
        {showBidAsk && (
          <span className="font-bold text-white drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
            {formatCompactNumber(candle.totalVolume)}
          </span>
        )}
      </div>
    </div>
  );
});
BarStats.displayName = 'BarStats';

StatLabelRow.displayName = 'StatLabelRow';

export default FootprintTable;
