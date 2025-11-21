import React from 'react';
import { Activity, Wifi, Settings } from 'lucide-react';
import { CONFIG } from '../constants';
import { FootprintStats } from '../types';

interface HeaderProps {
  stats: FootprintStats;
}

const Header: React.FC<HeaderProps> = ({ stats }) => {
  return (
    <div className="h-14 bg-panel-bg border-b border-border-color flex items-center justify-between px-4 shrink-0">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className="bg-kr-red/10 p-1.5 rounded">
            <Activity className="w-5 h-5 text-kr-red" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white leading-none">{CONFIG.TARGET_NAME}</h1>
            <span className="text-xs text-gray-500 font-mono">{CONFIG.TARGET_CODE}</span>
          </div>
        </div>

        <div className="h-8 w-px bg-gray-700 mx-2"></div>

        <div className="flex space-x-6 text-sm">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-500 uppercase tracking-wider">Last Price</span>
            <span className={`font-mono font-bold ${stats.close > stats.open ? 'text-kr-red' : stats.close < stats.open ? 'text-kr-blue' : 'text-white'}`}>
              {stats.close.toLocaleString()}
            </span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-500 uppercase tracking-wider">Total Vol</span>
            <span className="font-mono text-white">{stats.totalVolume.toLocaleString()}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-500 uppercase tracking-wider">CVD</span>
            <span className={`font-mono font-bold ${stats.cvd > 0 ? 'text-kr-red' : 'text-kr-blue'}`}>
              {stats.cvd > 0 ? '+' : ''}{stats.cvd.toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="px-2 py-1 bg-gray-800 rounded border border-gray-700 flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-xs text-gray-300">Live Simulation</span>
        </div>
        <button className="p-2 hover:bg-gray-800 rounded text-gray-400 transition-colors">
            <Settings className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default Header;