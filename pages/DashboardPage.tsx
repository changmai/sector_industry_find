import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, BarChart3, TrendingUp } from 'lucide-react';
import { useWebSocket } from '../contexts/WebSocketContext';
import ProgramDashboard from '../components/research/ProgramDashboard';

const DashboardPage: React.FC = () => {
  const { isConnected, todayEventCount } = useWebSocket();

  return (
    <div className="min-h-screen bg-dark-bg text-white">
      {/* Navigation Header */}
      <nav className="bg-panel-bg border-b border-border-color px-4 py-2 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center space-x-6">
          <div className="flex items-center">
            <BarChart3 className="w-5 h-5 text-kr-blue mr-2" />
            <span className="font-bold text-white">Footprint Chart</span>
          </div>

          <div className="flex items-center space-x-1">
            <Link
              to="/"
              className="px-3 py-1.5 rounded text-sm text-gray-400 hover:text-white hover:bg-gray-700 transition-colors flex items-center"
            >
              <Activity className="w-4 h-4 mr-1" />
              차트
            </Link>
            <span className="px-3 py-1.5 rounded text-sm bg-kr-blue text-white flex items-center">
              <TrendingUp className="w-4 h-4 mr-1" />
              연구
              {todayEventCount > 0 && (
                <span className="ml-1.5 px-1.5 py-0.5 text-[10px] bg-yellow-500/20 text-yellow-400 rounded-full font-mono">
                  {todayEventCount}
                </span>
              )}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-4 text-xs">
          {/* Today's event count */}
          <div className="flex items-center text-gray-400">
            <span className="mr-1">오늘 이벤트:</span>
            <span className={`font-mono ${todayEventCount > 0 ? 'text-yellow-400' : 'text-gray-500'}`}>
              {todayEventCount}
            </span>
          </div>

          {/* WebSocket connection status */}
          <div className="flex items-center">
            <span
              className={`w-2 h-2 rounded-full mr-2 ${
                isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
              }`}
            />
            <span className={isConnected ? 'text-green-400' : 'text-red-400'}>
              {isConnected ? '연결됨' : '연결 끊김'}
            </span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="p-6">
        <ProgramDashboard autoRefresh={true} refreshInterval={30000} />
      </main>
    </div>
  );
};

export default DashboardPage;
