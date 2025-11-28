import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Wifi, Settings, TrendingUp } from 'lucide-react';
import { FootprintStats } from '../types';
import { useWebSocket } from '../contexts/WebSocketContext';

interface HeaderProps {
  stats: FootprintStats;
  targetCode: string;
  targetName: string;
  onSettingsClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ stats, targetCode, targetName, onSettingsClick }) => {
  const { isConnected, todayEventCount } = useWebSocket();

  return (
    <div className="sticky top-0 z-50 h-14 bg-panel-bg border-b border-border-color flex items-center justify-between px-4 shrink-0">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className="bg-kr-red/10 p-1.5 rounded">
            <Activity className="w-5 h-5 text-kr-red" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white leading-none">{targetName}</h1>
            <span className="text-xs text-gray-500 font-mono">{targetCode}</span>
          </div>
        </div>

        <div className="h-8 w-px bg-gray-700 mx-2"></div>

        {/* Navigation Links */}
        <div className="flex items-center space-x-1">
          <span className="px-3 py-1.5 rounded text-sm bg-kr-blue text-white">
            차트
          </span>
          <Link
            to="/research"
            className="px-3 py-1.5 rounded text-sm text-gray-400 hover:text-white hover:bg-gray-700 transition-colors flex items-center"
          >
            <TrendingUp className="w-4 h-4 mr-1" />
            연구
            {todayEventCount > 0 && (
              <span className="ml-1.5 px-1.5 py-0.5 text-[10px] bg-yellow-500/20 text-yellow-400 rounded-full font-mono">
                {todayEventCount}
              </span>
            )}
          </Link>
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
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
          <span className={`text-xs ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
            {isConnected ? 'Live Connected' : 'Disconnected'}
          </span>
        </div>
        <button
          className="p-2 hover:bg-gray-800 rounded text-gray-400 hover:text-white transition-colors"
          onClick={onSettingsClick}
          title="종목 코드 변경"
        >
            <Settings className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default Header;