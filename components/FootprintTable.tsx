
import React, { useRef, useEffect, useMemo, useCallback } from 'react';
import { Grid, CellComponentProps, GridImperativeAPI } from 'react-window';
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
const BAR_WIDTH = 130; // Width of each bar (120px + margin)
const HEADER_HEIGHT = 35;

// Cell props type for react-window v2 (must NOT contain forbidden keys)
interface BarCellProps {
  allBars: FootprintCandle[];
  activeBar: FootprintCandle | null;
  priceRows: number[];
}

// Cell component for Grid - receives built-in props + custom cellProps
const BarCell = ({
  columnIndex,
  style,
  allBars,
  activeBar,
  priceRows
}: CellComponentProps<BarCellProps>) => {
  const bar = allBars[columnIndex];
  if (!bar) return <div style={style} />;

  const isActive = activeBar ? bar.id === activeBar.id : false;

  return (
    <div style={style}>
      <FootprintBarComponent
        candle={bar}
        isActive={isActive}
        priceRows={priceRows}
      />
    </div>
  );
};

const FootprintTable: React.FC<FootprintTableProps> = ({ bars, activeBar, globalHigh, globalLow, priceStep }) => {
  const gridRef = useRef<GridImperativeAPI>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const isAutoScrollEnabled = useRef<boolean>(true);

  // Generate Master Price List for Synchronization
  const priceRows = useMemo(() => {
      const alignedHigh = Math.ceil(globalHigh / priceStep) * priceStep;
      const alignedLow = Math.floor(globalLow / priceStep) * priceStep;

      const rows: number[] = [];
      for (let p = alignedHigh; p >= alignedLow; p -= priceStep) {
          rows.push(p);
      }
      return rows;
  }, [globalHigh, globalLow, priceStep]);

  // Combine bars and activeBar for rendering
  const allBars = useMemo(() => {
    const result = [...bars];
    if (activeBar) {
      result.push(activeBar);
    }
    return result;
  }, [bars, activeBar]);

  // Calculate exact heights for synchronization
  const chartBodyHeight = priceRows.length * ROW_HEIGHT;
  const STATS_HEIGHT = ROW_HEIGHT * 4;
  const totalRowHeight = HEADER_HEIGHT + chartBodyHeight + STATS_HEIGHT;

  // Auto-scroll to right when new bars are added
  useEffect(() => {
    if (gridRef.current && isAutoScrollEnabled.current && allBars.length > 0) {
      gridRef.current.scrollToColumn({
        index: allBars.length - 1,
        align: 'end',
        behavior: 'auto'
      });
    }
  }, [allBars.length, gridRef]);

  // Handle scroll to detect user interaction
  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    const { scrollLeft, scrollWidth, clientWidth } = target;
    // If user is within 100px of the right edge, enable auto-scroll
    isAutoScrollEnabled.current = scrollWidth - clientWidth - scrollLeft < 100;
  }, []);

  // Container dimensions - use ResizeObserver
  const [containerWidth, setContainerWidth] = React.useState(800);

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

  // Cell props for react-window (only custom props, not forbidden keys)
  const cellProps: BarCellProps = useMemo(() => ({
    allBars,
    activeBar,
    priceRows
  }), [allBars, activeBar, priceRows]);

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

        {/* Virtualized Bar Grid (1 row, N columns) */}
        <div className="flex-1 overflow-hidden" onScroll={handleScroll}>
          {allBars.length === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-600">
              Waiting for market data...
            </div>
          ) : (
            <Grid<BarCellProps>
              gridRef={gridRef}
              columnCount={allBars.length}
              columnWidth={BAR_WIDTH}
              rowCount={1}
              rowHeight={totalRowHeight}
              cellComponent={BarCell}
              cellProps={cellProps}
              overscanCount={3}
              className="custom-scrollbar"
              style={{
                overflowY: 'auto',
                width: containerWidth,
                height: totalRowHeight + 20
              }}
            />
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
          <span className="ml-4 text-gray-600">| Bars: {allBars.length} (Virtualized)</span>
        </div>
      </div>
    </div>
  );
};

const StatLabelRow: React.FC<{ label: string }> = ({ label }) => (
  <div className="flex items-center justify-end pr-2 text-[9px] text-white font-bold font-mono border-b border-gray-800 last:border-b-0" style={{ height: ROW_HEIGHT }}>
    {label}
  </div>
);

export default FootprintTable;
