
import React, { useRef, useEffect, useMemo } from 'react';
import { FootprintCandle } from '../types';
import FootprintBarComponent from './FootprintBarComponent';
import { Magnet, Ban } from 'lucide-react';
import { CONFIG } from '../constants';

interface FootprintTableProps {
  bars: FootprintCandle[];
  activeBar: FootprintCandle | null;
  globalHigh: number;
  globalLow: number;
}

const FootprintTable: React.FC<FootprintTableProps> = ({ bars, activeBar, globalHigh, globalLow }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const isAutoScrollEnabled = useRef<boolean>(true);

  // Generate Master Price List for Synchronization
  const priceRows = useMemo(() => {
      const rows: number[] = [];
      for (let p = globalHigh; p >= globalLow; p -= CONFIG.PRICE_STEP) {
          rows.push(p);
      }
      return rows;
  }, [globalHigh, globalLow]);

  // Detect user scroll interaction
  const handleScroll = () => {
      if (containerRef.current) {
          const { scrollLeft, scrollWidth, clientWidth } = containerRef.current;
          // If the user is within 50px of the right edge, enable auto-scroll
          // otherwise, assume they are viewing history and disable it.
          const isAtRightEdge = Math.abs(scrollWidth - clientWidth - scrollLeft) < 50;
          isAutoScrollEnabled.current = isAtRightEdge;
      }
  };

  // Auto-scroll to right when new bars are added, ONLY if enabled
  useEffect(() => {
    if (containerRef.current && isAutoScrollEnabled.current) {
      containerRef.current.scrollLeft = containerRef.current.scrollWidth;
    }
  }, [bars.length, activeBar, globalHigh, globalLow]); 

  return (
    <div className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color shadow-xl relative overflow-hidden">
      
      {/* 
        Dual-Axis Scroll Container 
        - Horizontal for Bars
        - Vertical for Price Depth
      */}
      <div 
        ref={containerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-auto custom-scrollbar relative"
      >
         <div className="flex h-full items-stretch min-h-min">
            {bars.length === 0 && !activeBar && (
                <div className="absolute inset-0 flex items-center justify-center text-gray-600 sticky left-0">
                    Waiting for market data...
                </div>
            )}

            {/* Render Historical Bars */}
            {bars.map((bar) => (
                <FootprintBarComponent 
                    key={bar.id} 
                    candle={bar} 
                    isActive={false} 
                    priceRows={priceRows}
                />
            ))}

            {/* Render Active Bar */}
            {activeBar && (
                <FootprintBarComponent 
                    candle={activeBar} 
                    isActive={true} 
                    priceRows={priceRows}
                />
            )}
            
            {/* Spacer for comfortable viewing on right */}
            <div className="min-w-[50px] shrink-0"></div>
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
         </div>
      </div>
    </div>
  );
};

export default FootprintTable;
