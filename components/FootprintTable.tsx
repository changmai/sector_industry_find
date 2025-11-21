import React, { useRef, useEffect } from 'react';
import { FootprintCandle } from '../types';
import FootprintBarComponent from './FootprintBarComponent';
import { Magnet, Ban } from 'lucide-react';

interface FootprintTableProps {
  bars: FootprintCandle[];
  activeBar: FootprintCandle | null;
}

const FootprintTable: React.FC<FootprintTableProps> = ({ bars, activeBar }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to right when new bars are added
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollLeft = containerRef.current.scrollWidth;
    }
  }, [bars.length, activeBar]); // Trigger on history change or active bar update

  return (
    <div className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color shadow-xl relative">
      
      {/* Horizontal Scroll Container */}
      <div 
        ref={containerRef}
        className="flex-1 overflow-x-auto overflow-y-hidden flex items-stretch relative custom-scrollbar"
      >
        {bars.length === 0 && !activeBar && (
            <div className="absolute inset-0 flex items-center justify-center text-gray-600">
                Waiting for market data...
            </div>
        )}

        {/* Render Historical Bars */}
        {bars.map((bar) => (
            <FootprintBarComponent key={bar.id} candle={bar} isActive={false} />
        ))}

        {/* Render Active Bar */}
        {activeBar && (
            <FootprintBarComponent candle={activeBar} isActive={true} />
        )}
        
        {/* Spacer for comfortable viewing on right */}
        <div className="min-w-[50px]"></div>
      </div>

      {/* Legend / Status Bar */}
      <div className="h-6 bg-gray-900 border-t border-border-color flex items-center justify-between px-2 text-[10px] text-gray-500 shrink-0">
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
