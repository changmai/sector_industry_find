import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Activity, BarChart3, TrendingUp, ArrowLeft, Clock, Layers } from 'lucide-react';
import { useWebSocket } from '../contexts/WebSocketContext';
import { StockDetailResponse, ResearchEvent, HourlyStats, DeltaRangeStats } from '../types/research';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import ErrorMessage from '../components/ui/ErrorMessage';
import EventDetailModal from '../components/research/EventDetailModal';

const StockDetailPage: React.FC = () => {
  const { code } = useParams<{ code: string }>();
  const { isConnected, todayEventCount } = useWebSocket();

  const [data, setData] = useState<StockDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal state
  const [selectedEventId, setSelectedEventId] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    if (code) {
      fetchStockDetail();
    }
  }, [code]);

  const fetchStockDetail = async () => {
    if (!code) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/research/stock/${code}/detail`);
      if (!response.ok) {
        throw new Error('종목 데이터를 불러오지 못했습니다');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류');
    } finally {
      setLoading(false);
    }
  };

  const handleEventClick = (eventId: number) => {
    setSelectedEventId(eventId);
    setIsModalOpen(true);
  };

  return (
    <div className="h-screen bg-dark-bg text-white flex flex-col overflow-hidden">
      {/* Navigation Header */}
      <nav className="bg-panel-bg border-b border-border-color px-4 py-2 flex items-center justify-between shrink-0">
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
            <Link
              to="/research"
              className="px-3 py-1.5 rounded text-sm bg-kr-blue text-white flex items-center"
            >
              <TrendingUp className="w-4 h-4 mr-1" />
              연구
            </Link>
          </div>
        </div>

        <div className="flex items-center space-x-4 text-xs">
          <div className="flex items-center text-gray-400">
            <span className="mr-1">오늘 이벤트:</span>
            <span className={`font-mono ${todayEventCount > 0 ? 'text-yellow-400' : 'text-gray-500'}`}>
              {todayEventCount}
            </span>
          </div>
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

      {/* Main Content - Scrollable */}
      <main className="flex-1 overflow-y-auto p-6 pb-12">
        {/* Back Link */}
        <Link
          to="/research"
          className="inline-flex items-center text-gray-400 hover:text-white mb-4 transition-colors text-sm"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          대시보드로 돌아가기
        </Link>

        {loading && (
          <div className="flex items-center justify-center h-64">
            <LoadingSpinner size="lg" />
          </div>
        )}

        {error && <ErrorMessage message={error} onRetry={fetchStockDetail} />}

        {data && !loading && (
          <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-white">{code}</h1>
                <p className="text-gray-400">종목 상세 통계</p>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-white">
                  {data.summary.total_events}
                </div>
                <div className="text-sm text-gray-400">전체 이벤트</div>
              </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
              <SummaryCard
                title="1분 수익률"
                value={data.summary.avg_return_1m !== null ? `${data.summary.avg_return_1m.toFixed(2)}%` : '-'}
                valueColor={data.summary.avg_return_1m && data.summary.avg_return_1m > 0 ? 'text-green-400' : 'text-red-400'}
              />
              <SummaryCard
                title="5분 수익률"
                value={data.summary.avg_return_5m !== null ? `${data.summary.avg_return_5m.toFixed(2)}%` : '-'}
                valueColor={data.summary.avg_return_5m && data.summary.avg_return_5m > 0 ? 'text-green-400' : 'text-red-400'}
              />
              <SummaryCard
                title="10분 수익률"
                value={data.summary.avg_return_10m !== null ? `${data.summary.avg_return_10m.toFixed(2)}%` : '-'}
                valueColor={data.summary.avg_return_10m && data.summary.avg_return_10m > 0 ? 'text-green-400' : 'text-red-400'}
              />
              <SummaryCard
                title="30분 수익률"
                value={data.summary.avg_return_30m !== null ? `${data.summary.avg_return_30m.toFixed(2)}%` : '-'}
                valueColor={data.summary.avg_return_30m && data.summary.avg_return_30m > 0 ? 'text-green-400' : 'text-red-400'}
              />
              <SummaryCard
                title="1분 승률"
                value={data.summary.win_rate_1m !== null ? `${data.summary.win_rate_1m.toFixed(1)}%` : '-'}
                valueColor={data.summary.win_rate_1m && data.summary.win_rate_1m >= 50 ? 'text-green-400' : 'text-red-400'}
              />
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* By Hour */}
              <div className="bg-panel-bg border border-border-color rounded-lg overflow-hidden">
                <div className="px-4 py-3 border-b border-border-color flex items-center">
                  <Clock className="w-4 h-4 mr-2 text-yellow-400" />
                  <h3 className="font-semibold text-white">시간대별 통계</h3>
                </div>
                <div className="p-4">
                  <HourlyStatsChart stats={data.by_hour} />
                </div>
              </div>

              {/* By Delta */}
              <div className="bg-panel-bg border border-border-color rounded-lg overflow-hidden">
                <div className="px-4 py-3 border-b border-border-color flex items-center">
                  <Layers className="w-4 h-4 mr-2 text-purple-400" />
                  <h3 className="font-semibold text-white">Delta 범위별 통계</h3>
                </div>
                <div className="p-4">
                  <DeltaStatsChart stats={data.by_delta} />
                </div>
              </div>
            </div>

            {/* Events Table */}
            <div className="bg-panel-bg border border-border-color rounded-lg overflow-hidden">
              <div className="px-4 py-3 border-b border-border-color flex items-center justify-between">
                <h3 className="font-semibold text-white">이벤트 목록</h3>
                <span className="text-xs text-gray-500">최근 100건</span>
              </div>
              <EventsTable events={data.events} onEventClick={handleEventClick} />
            </div>
          </div>
        )}
      </main>

      {/* Event Detail Modal */}
      <EventDetailModal
        eventId={selectedEventId}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

// Helper Components
const SummaryCard: React.FC<{
  title: string;
  value: string;
  valueColor?: string;
}> = ({ title, value, valueColor = 'text-white' }) => (
  <div className="bg-panel-bg border border-border-color rounded-lg p-4">
    <div className="text-xs text-gray-400 mb-2">{title}</div>
    <div className={`text-2xl font-bold ${valueColor}`}>{value}</div>
  </div>
);

const HourlyStatsChart: React.FC<{ stats: HourlyStats[] }> = ({ stats }) => {
  if (stats.length === 0) {
    return <div className="text-center text-gray-500 py-4">데이터가 없습니다</div>;
  }

  const maxCount = Math.max(...stats.map(s => s.count));

  return (
    <div className="space-y-2">
      {stats.map((stat) => (
        <div key={stat.hour} className="flex items-center space-x-3">
          <span className="w-12 text-xs text-gray-400">{stat.hour}:00</span>
          <div className="flex-1 h-6 relative bg-gray-800 rounded overflow-hidden">
            <div
              className="h-full bg-yellow-500/60 rounded"
              style={{ width: `${(stat.count / maxCount) * 100}%` }}
            />
            <span className="absolute inset-0 flex items-center justify-center text-xs text-white">
              {stat.count}건
            </span>
          </div>
          <span className={`w-16 text-xs text-right font-mono ${
            stat.avg_return && stat.avg_return > 0 ? 'text-green-400' : 'text-red-400'
          }`}>
            {stat.avg_return !== null ? `${stat.avg_return.toFixed(2)}%` : '-'}
          </span>
        </div>
      ))}
    </div>
  );
};

const DeltaStatsChart: React.FC<{ stats: DeltaRangeStats[] }> = ({ stats }) => {
  if (stats.length === 0) {
    return <div className="text-center text-gray-500 py-4">데이터가 없습니다</div>;
  }

  const maxCount = Math.max(...stats.map(s => s.count));

  return (
    <div className="space-y-2">
      {stats.map((stat) => (
        <div key={stat.range} className="flex items-center space-x-3">
          <span className="w-16 text-xs text-gray-400">{stat.range}</span>
          <div className="flex-1 h-6 relative bg-gray-800 rounded overflow-hidden">
            <div
              className="h-full bg-purple-500/60 rounded"
              style={{ width: `${(stat.count / maxCount) * 100}%` }}
            />
            <span className="absolute inset-0 flex items-center justify-center text-xs text-white">
              {stat.count}건
            </span>
          </div>
          <span className={`w-16 text-xs text-right font-mono ${
            stat.avg_return && stat.avg_return > 0 ? 'text-green-400' : 'text-red-400'
          }`}>
            {stat.avg_return !== null ? `${stat.avg_return.toFixed(2)}%` : '-'}
          </span>
        </div>
      ))}
    </div>
  );
};

const EventsTable: React.FC<{
  events: ResearchEvent[];
  onEventClick: (id: number) => void;
}> = ({ events, onEventClick }) => {
  if (events.length === 0) {
    return <div className="p-4 text-center text-gray-500">이벤트가 없습니다</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="bg-gray-800/50">
          <tr>
            <th className="px-4 py-2 text-left text-gray-400 font-medium">시간</th>
            <th className="px-4 py-2 text-left text-gray-400 font-medium">유형</th>
            <th className="px-4 py-2 text-right text-gray-400 font-medium">가격</th>
            <th className="px-4 py-2 text-right text-gray-400 font-medium">Delta</th>
            <th className="px-4 py-2 text-right text-gray-400 font-medium">1분</th>
            <th className="px-4 py-2 text-right text-gray-400 font-medium">5분</th>
            <th className="px-4 py-2 text-right text-gray-400 font-medium">10분</th>
            <th className="px-4 py-2 text-right text-gray-400 font-medium">30분</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => {
            const isBuySurge = event.event_type === 'buy_surge';

            return (
              <tr
                key={event.id}
                onClick={() => onEventClick(event.id)}
                className="border-t border-border-color hover:bg-gray-800/30 cursor-pointer transition-colors"
              >
                <td className="px-4 py-2 text-gray-300">
                  {event.event_time.split(' ')[1]}
                </td>
                <td className="px-4 py-2">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs ${
                    isBuySurge ? 'bg-kr-red/20 text-kr-red' : 'bg-kr-blue/20 text-kr-blue'
                  }`}>
                    {isBuySurge ? '매수' : '매도'}
                  </span>
                </td>
                <td className="px-4 py-2 text-right font-mono text-gray-300">
                  {event.price_at_event.toLocaleString()}
                </td>
                <td className="px-4 py-2 text-right font-mono text-gray-300">
                  {event.delta_vol.toLocaleString()}
                </td>
                <ReturnCell value={event.return_1m} />
                <ReturnCell value={event.return_5m} />
                <ReturnCell value={event.return_10m} />
                <ReturnCell value={event.return_30m} />
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

const ReturnCell: React.FC<{ value: number | null }> = ({ value }) => (
  <td className={`px-4 py-2 text-right font-mono ${
    value === null ? 'text-gray-500' :
    value > 0 ? 'text-green-400' : 'text-red-400'
  }`}>
    {value !== null ? `${value > 0 ? '+' : ''}${value.toFixed(2)}%` : '-'}
  </td>
);

export default StockDetailPage;
