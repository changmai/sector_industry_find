
import React, { useRef, useEffect, useMemo, useCallback, useState } from 'react';
import { FootprintCandle } from '../types';
import FootprintBarComponent from './FootprintBarComponent';
import { Magnet, Ban } from 'lucide-react';
import { ROW_HEIGHT } from '../constants';

interface FootprintTableProps {
  bars: FootprintCandle[];
  activeBar: FootprintCandle | null;
  globalHigh: number;
  globalLow: number;
  priceStep: number;
}

// Constants for virtualization
const BAR_WIDTH = 130;
const HEADER_HEIGHT = 35;
const OVERSCAN = 2; // Extra bars to render outside viewport

const FootprintTable: React.FC<FootprintTableProps> = ({ bars, activeBar, globalHigh, globalLow, priceStep }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const isAutoScrollEnabled = useRef<boolean>(true);
  const prevBarsLengthRef = useRef<number>(0);
  const prevPriceStepRef = useRef<number>(priceStep);

  // Ref for stable access to bars (avoids renderedBars dependency on entire array)
  const barsRef = useRef(bars);
  barsRef.current = bars;

  // Container dimensions
  const [containerWidth, setContainerWidth] = useState(800);
  const [scrollLeft, setScrollLeft] = useState(0);

  // Generate Master Price List - stabilized to prevent unnecessary re-renders
  const priceRowsRef = useRef<number[]>([]);
  const prevRangeRef = useRef({ high: 0, low: 0, step: 0 });

  const priceRows = useMemo(() => {
    const alignedHigh = Math.ceil(globalHigh / priceStep) * priceStep;
    const alignedLow = Math.floor(globalLow / priceStep) * priceStep;

    // Only regenerate if range actually changed significantly
    const prev = prevRangeRef.current;
    if (
      prev.high === alignedHigh &&
      prev.low === alignedLow &&
      prev.step === priceStep &&
      priceRowsRef.current.length > 0
    ) {
      return priceRowsRef.current;
    }

    const rows: number[] = [];
    for (let p = alignedHigh; p >= alignedLow; p -= priceStep) {
      rows.push(p);
    }

    prevRangeRef.current = { high: alignedHigh, low: alignedLow, step: priceStep };
    priceRowsRef.current = rows;
    return rows;
  }, [globalHigh, globalLow, priceStep]);

  // Calculate heights
  const chartBodyHeight = priceRows.length * ROW_HEIGHT;
  const STATS_HEIGHT = ROW_HEIGHT * 4;
  const totalRowHeight = HEADER_HEIGHT + chartBodyHeight + STATS_HEIGHT;

  // Total content width
  const totalBars = bars.length + (activeBar ? 1 : 0);
  const totalContentWidth = totalBars * BAR_WIDTH;

  // Calculate visible range (direct virtualization)
  const visibleRange = useMemo(() => {
    const startIdx = Math.max(0, Math.floor(scrollLeft / BAR_WIDTH) - OVERSCAN);
    const visibleCount = Math.ceil(containerWidth / BAR_WIDTH) + OVERSCAN * 2;
    const endIdx = Math.min(totalBars, startIdx + visibleCount);
    return { startIdx, endIdx };
  }, [scrollLeft, containerWidth, totalBars]);

  // Handle scroll
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    setScrollLeft(target.scrollLeft);

    // Auto-scroll detection
    const { scrollWidth, clientWidth } = target;
    isAutoScrollEnabled.current = scrollWidth - clientWidth - target.scrollLeft < 100;
  }, []);

  // Auto-scroll to right when new bars are added
  useEffect(() => {
    if (scrollContainerRef.current && isAutoScrollEnabled.current) {
      const newLength = bars.length + (activeBar ? 1 : 0);
      if (newLength > prevBarsLengthRef.current || newLength === prevBarsLengthRef.current) {
        scrollContainerRef.current.scrollLeft = totalContentWidth;
      }
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
        const targetScrollTop = (rowIndex * ROW_HEIGHT) - (scrollContainerRef.current.clientHeight / 2) + HEADER_HEIGHT;

        // Apply scroll with bounds check
        scrollContainerRef.current.scrollTop = Math.max(0, targetScrollTop);
      }

      prevPriceStepRef.current = priceStep;
    }
  }, [priceStep, globalHigh, activeBar, bars]);

  // Render visible bars only
  // Optimized: Uses barsRef to avoid dependency on entire bars array
  const barsLength = bars.length;
  const renderedBars = useMemo(() => {
    const elements: React.ReactNode[] = [];
    const { startIdx, endIdx } = visibleRange;
    const currentBars = barsRef.current;

    for (let i = startIdx; i < endIdx; i++) {
      const isActiveBarIndex = i === barsLength && activeBar;
      const bar = isActiveBarIndex ? activeBar : currentBars[i];

      if (!bar) continue;

      elements.push(
        <div
          key={bar.id}
          style={{
            position: 'absolute',
            left: i * BAR_WIDTH,
            top: 0,
            width: BAR_WIDTH,
            height: totalRowHeight,
          }}
        >
          <FootprintBarComponent
            candle={bar}
            isActive={!!isActiveBarIndex}
            priceRows={priceRows}
          />
        </div>
      );
    }

    return elements;
  }, [visibleRange, barsLength, activeBar, priceRows, totalRowHeight]);

  return (
    <div
      ref={containerRef}
      className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color shadow-xl relative overflow-hidden"
    >
      <div className="flex-1 flex overflow-hidden">
        {/* Sticky Stats Label Column */}
        <div className="z-30 bg-panel-bg border-r border-border-color flex flex-col shrink-0 w-[70px] shadow-md">
          {/* Header Placeholder */}
          <div
            className="border-b border-gray-800 flex items-center justify-center text-[9px] text-gray-500 font-mono bg-panel-bg"
            style={{ height: HEADER_HEIGHT }}
          >
            Stats
          </div>

          {/* Body Spacer */}
          <div style={{ height: chartBodyHeight, minHeight: chartBodyHeight }}></div>

          {/* Stats Labels - Sticky Bottom */}
          <div className="mt-auto border-t border-gray-700 bg-panel-bg z-40 shadow-[0_-1px_2px_rgba(0,0,0,0.3)]">
            <StatLabelRow label="Delta" />
            <StatLabelRow label="Max Delta" />
            <StatLabelRow label="Min Delta" />
            <StatLabelRow label="Volume" />
          </div>
        </div>

        {/* Direct Virtualized Scroll Container */}
        <div
          ref={scrollContainerRef}
          className="flex-1 overflow-x-auto overflow-y-auto custom-scrollbar gpu-accelerated"
          onScroll={handleScroll}
          style={{ height: totalRowHeight + 20 }}
        >
          {totalBars === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-600">
              Waiting for market data...
            </div>
          ) : (
            <div
              style={{
                position: 'relative',
                width: totalContentWidth,
                height: totalRowHeight,
                minWidth: totalContentWidth,
              }}
            >
              {renderedBars}
            </div>
          )}
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

const StatLabelRow: React.FC<{ label: string }> = React.memo(({ label }) => (
  <div className="flex items-center justify-end pr-2 text-[9px] text-white font-bold font-mono border-b border-gray-800 last:border-b-0" style={{ height: ROW_HEIGHT }}>
    {label}
  </div>
));

StatLabelRow.displayName = 'StatLabelRow';

export default FootprintTable;
