import React from 'react';
import { Tick, Side } from '../types';
import { COLORS } from '../constants';

interface TickListProps {
  ticks: Tick[];
}

const TickList: React.FC<TickListProps> = ({ ticks }) => {
  return (
    <div className="flex flex-col h-full bg-panel-bg rounded-lg border border-border-color overflow-hidden">
        <div className="p-2 border-b border-border-color bg-gray-900">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">Real-time Ticks</h3>
        </div>
        
        {/* Header */}
        <div className="grid grid-cols-4 text-[10px] text-gray-500 px-2 py-1 border-b border-border-color">
            <div>Time</div>
            <div className="text-center">Price</div>
            <div className="text-center">Side</div>
            <div className="text-right">Vol</div>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
            {ticks.map((tick) => (
                <div key={tick.id} className="grid grid-cols-4 text-xs px-2 py-1 border-b border-gray-800/30 hover:bg-gray-800/50 font-mono animate-fade-in">
                    <div className="text-gray-400">{tick.time}</div>
                    <div className={`text-center font-bold ${tick.side === Side.Buy ? COLORS.BUY_TEXT : COLORS.SELL_TEXT}`}>
                        {tick.price.toLocaleString()}
                    </div>
                    <div className={`text-center ${tick.side === Side.Buy ? COLORS.BUY_TEXT : COLORS.SELL_TEXT}`}>
                        {tick.side === Side.Buy ? 'Buy' : 'Sell'}
                    </div>
                    <div className={`text-right ${tick.volume >= 100 ? 'text-yellow-400 font-bold' : 'text-gray-300'}`}>
                        {tick.volume.toLocaleString()}
                    </div>
                </div>
            ))}
        </div>
    </div>
  );
};

export default TickList;