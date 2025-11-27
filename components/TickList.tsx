
import React, { useRef, useState, useEffect, useMemo, useCallback } from 'react';
import { Tick, Side } from '../types';
import { COLORS } from '../constants';

interface TickListProps {
  ticks: Tick[];
}

const TICK_ROW_HEIGHT = 20;
const OVERSCAN = 5;

// Memoized row component
const TickRow = React.memo(({ tick, style }: { tick: Tick; style: React.CSSProperties }) => (
  <div
    style={style}
    className="tick-row grid grid-cols-[50px_60px_26px_52px] gap-1 text-[10px] px-1 border-b border-gray-800/30 hover:bg-gray-800/50 font-mono leading-none items-center"
  >
    <div className="text-gray-500 text-center tracking-tighter">{tick.time}</div>
    <div className={`text-right font-bold tracking-tight ${tick.side === Side.Buy ? COLORS.BUY_TEXT : COLORS.SELL_TEXT}`}>
      {tick.price.toLocaleString()}
    </div>
    <div className={`text-center text-[9px] uppercase ${tick.side === Side.Buy ? COLORS.BUY_TEXT : COLORS.SELL_TEXT}`}>
      {tick.side === Side.Buy ? 'B' : 'S'}
    </div>
    <div className={`text-right pr-2 ${tick.volume >= 100 ? 'text-yellow-400 font-bold' : 'text-gray-300'}`}>
      {tick.volume.toLocaleString()}
    </div>
  </div>
));

TickRow.displayName = 'TickRow';

const TickList: React.FC<TickListProps> = React.memo(({ ticks }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [listHeight, setListHeight] = useState(400);
  const [scrollTop, setScrollTop] = useState(0);

  // Calculate available height for the list
  useEffect(() => {
    const updateHeight = () => {
      if (containerRef.current) {
        const availableHeight = containerRef.current.clientHeight - 52;
        setListHeight(Math.max(100, availableHeight));
      }
    };

    updateHeight();

    const resizeObserver = new ResizeObserver(updateHeight);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => resizeObserver.disconnect();
  }, []);

  // Handle scroll
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  // Calculate visible range
  const visibleRange = useMemo(() => {
    const startIdx = Math.max(0, Math.floor(scrollTop / TICK_ROW_HEIGHT) - OVERSCAN);
    const visibleCount = Math.ceil(listHeight / TICK_ROW_HEIGHT) + OVERSCAN * 2;
    const endIdx = Math.min(ticks.length, startIdx + visibleCount);
    return { startIdx, endIdx };
  }, [scrollTop, listHeight, ticks.length]);

  // Render visible rows only
  const renderedRows = useMemo(() => {
    const elements: React.ReactNode[] = [];
    const { startIdx, endIdx } = visibleRange;

    for (let i = startIdx; i < endIdx; i++) {
      const tick = ticks[i];
      if (!tick) continue;

      elements.push(
        <TickRow
          key={tick.id}
          tick={tick}
          style={{
            position: 'absolute',
            top: i * TICK_ROW_HEIGHT,
            left: 0,
            right: 0,
            height: TICK_ROW_HEIGHT,
          }}
        />
      );
    }

    return elements;
  }, [visibleRange, ticks]);

  const totalHeight = ticks.length * TICK_ROW_HEIGHT;

  return (
    <div
      ref={containerRef}
      className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color overflow-hidden"
    >
      <div className="px-2 py-1 border-b border-border-color bg-gray-900">
        <h3 className="text-[11px] font-bold text-white uppercase tracking-wider">Tape</h3>
      </div>

      {/* Header */}
      <div className="grid grid-cols-[50px_60px_26px_52px] gap-1 text-[9px] text-gray-500 px-1 py-0.5 border-b border-border-color items-center">
        <div className="text-center">Time</div>
        <div className="text-right">Price</div>
        <div className="text-center">Sd</div>
        <div className="text-right pr-2">Vol</div>
      </div>

      {/* Virtualized List */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto custom-scrollbar gpu-accelerated"
        style={{ height: listHeight }}
        onScroll={handleScroll}
      >
        <div style={{ position: 'relative', height: totalHeight, minHeight: totalHeight }}>
          {renderedRows}
        </div>
      </div>
    </div>
  );
});

TickList.displayName = 'TickList';

export default TickList;
