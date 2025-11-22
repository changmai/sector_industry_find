
import React from 'react';
import { Tick, Side } from '../types';
import { COLORS } from '../constants';

interface TickListProps {
  ticks: Tick[];
}

const TickList: React.FC<TickListProps> = ({ ticks }) => {
  return (
    <div className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color overflow-hidden">
        <div className="px-2 py-1 border-b border-border-color bg-gray-900">
            <h3 className="text-[11px] font-bold text-white uppercase tracking-wider">Tape</h3>
        </div>
        
        {/* Header - Ultra Tight Layout */}
        {/* Grid: Time(50px) | Price(60px) | Side(26px) | Vol(52px) */}
        <div className="grid grid-cols-[50px_60px_26px_52px] gap-1 text-[9px] text-gray-500 px-1 py-0.5 border-b border-border-color items-center">
            <div className="text-center">Time</div>
            <div className="text-right">Price</div>
            <div className="text-center">Sd</div>
            <div className="text-right pr-2">Vol</div>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
            {ticks.map((tick) => (
                <div key={tick.id} className="grid grid-cols-[50px_60px_26px_52px] gap-1 text-[10px] px-1 py-0.5 border-b border-gray-800/30 hover:bg-gray-800/50 font-mono animate-fade-in leading-none items-center">
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
            ))}
        </div>
    </div>
  );
};

export default TickList;
