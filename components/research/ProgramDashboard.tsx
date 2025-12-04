import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, TrendingDown, RefreshCw, Activity, BarChart3, Target, GitBranch, Clock, AlertTriangle, Zap } from 'lucide-react';
import { LiveResearchResponse, ResearchEvent, ResearchSummary, StockSummary, DivergenceAnalysisResponse } from '../../types/research';
import LoadingSpinner from '../ui/LoadingSpinner';
import ErrorMessage from '../ui/ErrorMessage';
import EmptyState from '../ui/EmptyState';
import EventDetailModal from './EventDetailModal';

interface ProgramDashboardProps {
  autoRefresh?: boolean;
  refreshInterval?: number;
}

const ProgramDashboard: React.FC<ProgramDashboardProps> = ({
  autoRefresh = true,
  refreshInterval = 30000
}) => {
  const [data, setData] = useState<LiveResearchResponse | null>(null);
  const [divergenceData, setDivergenceData] = useState<DivergenceAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  // Modal state
  const [selectedEventId, setSelectedEventId] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      // 병렬로 데이터 조회
      const [liveResponse, divergenceResponse] = await Promise.all([
        fetch(`http://${window.location.hostname}:8000/api/research/live`),
        fetch(`http://${window.location.hostname}:8000/api/research/divergence`)
      ]);

      if (!liveResponse.ok) {
        throw new Error('데이터를 불러오지 못했습니다');
      }

      const liveResult = await liveResponse.json();
      setData(liveResult);

      if (divergenceResponse.ok) {
        const divergenceResult = await divergenceResponse.json();
        setDivergenceData(divergenceResult);
      }

      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();

    if (autoRefresh) {
      const interval = setInterval(fetchData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchData, autoRefresh, refreshInterval]);

  const handleEventClick = (eventId: number) => {
    setSelectedEventId(eventId);
    setIsModalOpen(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />;
  }

  if (!data) {
    return <EmptyState message="데이터가 없습니다" />;
  }

  return (
    <div className="space-y-6">
      {/* Header with refresh */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">프로그램 매매 연구</h2>
          <p className="text-sm text-gray-400">
            {lastUpdate && `마지막 업데이트: ${lastUpdate.toLocaleTimeString()}`}
          </p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center space-x-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          <span className="text-sm">새로고침</span>
        </button>
      </div>

      {/* Summary Cards */}
      <SummarySection summary={data.summary} />

      {/* Divergence Analysis Section */}
      {divergenceData && Object.keys(divergenceData.by_divergence).length > 0 && (
        <DivergenceSection data={divergenceData} />
      )}

      {/* Two Column Layout - Full Height */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" style={{ height: divergenceData && Object.keys(divergenceData.by_divergence).length > 0 ? 'calc(100vh - 400px)' : 'calc(100vh - 280px)' }}>
        {/* Recent Events */}
        <div className="bg-panel-bg border border-border-color rounded-lg overflow-hidden flex flex-col">
          <div className="px-3 py-2 border-b border-border-color flex items-center justify-between shrink-0">
            <h3 className="text-xs font-semibold text-white flex items-center">
              <Activity className="w-3 h-3 mr-1.5 text-yellow-400" />
              최근 이벤트
            </h3>
            <span className="text-[10px] text-gray-500">최근 20건</span>
          </div>
          <EventList
            events={data.recent_events}
            onEventClick={handleEventClick}
          />
        </div>

        {/* By Stock */}
        <div className="bg-panel-bg border border-border-color rounded-lg overflow-hidden flex flex-col">
          <div className="px-3 py-2 border-b border-border-color shrink-0">
            <h3 className="text-xs font-semibold text-white flex items-center">
              <BarChart3 className="w-3 h-3 mr-1.5 text-purple-400" />
              종목별 통계
            </h3>
          </div>
          <StockList stocks={data.by_stock} />
        </div>
      </div>

      {/* Event Detail Modal */}
      <EventDetailModal
        eventId={selectedEventId}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

// Summary Section
const SummarySection: React.FC<{ summary: ResearchSummary }> = ({ summary }) => (
  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
    <SummaryCard
      title="전체 이벤트"
      value={summary.total_events}
      icon={<Target className="w-4 h-4" />}
      iconColor="text-yellow-400"
    />
    <SummaryCard
      title="매수 급증"
      value={summary.buy_events}
      icon={<TrendingUp className="w-4 h-4" />}
      iconColor="text-kr-red"
    />
    <SummaryCard
      title="매도 급증"
      value={summary.sell_events}
      icon={<TrendingDown className="w-4 h-4" />}
      iconColor="text-kr-blue"
    />
    <SummaryCard
      title="1분 수익률"
      value={summary.avg_return_1m ? `${summary.avg_return_1m.toFixed(2)}%` : '-'}
      subtitle={summary.win_rate_1m ? `승률 ${summary.win_rate_1m.toFixed(1)}%` : undefined}
      valueColor={summary.avg_return_1m && summary.avg_return_1m > 0 ? 'text-green-400' : 'text-red-400'}
    />
    <SummaryCard
      title="5분 수익률"
      value={summary.avg_return_5m ? `${summary.avg_return_5m.toFixed(2)}%` : '-'}
      subtitle={summary.win_rate_5m ? `승률 ${summary.win_rate_5m.toFixed(1)}%` : undefined}
      valueColor={summary.avg_return_5m && summary.avg_return_5m > 0 ? 'text-green-400' : 'text-red-400'}
    />
    <SummaryCard
      title="30분 수익률"
      value={summary.avg_return_30m ? `${summary.avg_return_30m.toFixed(2)}%` : '-'}
      subtitle={summary.win_rate_30m ? `승률 ${summary.win_rate_30m.toFixed(1)}%` : undefined}
      valueColor={summary.avg_return_30m && summary.avg_return_30m > 0 ? 'text-green-400' : 'text-red-400'}
    />
  </div>
);

const SummaryCard: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  iconColor?: string;
  valueColor?: string;
}> = ({ title, value, subtitle, icon, iconColor = 'text-gray-400', valueColor = 'text-white' }) => (
  <div className="bg-panel-bg border border-border-color rounded-lg p-4">
    <div className="flex items-center justify-between mb-2">
      <span className="text-xs text-gray-400">{title}</span>
      {icon && <span className={iconColor}>{icon}</span>}
    </div>
    <div className={`text-2xl font-bold ${valueColor}`}>{value}</div>
    {subtitle && <div className="text-xs text-gray-500 mt-1">{subtitle}</div>}
  </div>
);

// Divergence Analysis Section
const DivergenceSection: React.FC<{ data: DivergenceAnalysisResponse }> = ({ data }) => {
  const { by_divergence } = data;
  const bullish = by_divergence.bullish;
  const bearish = by_divergence.bearish;
  const none = by_divergence.none;

  return (
    <div className="bg-panel-bg border border-border-color rounded-lg p-4">
      <div className="flex items-center mb-4">
        <GitBranch className="w-4 h-4 mr-2 text-cyan-400" />
        <h3 className="text-sm font-semibold text-white">다이버전스 패턴 분석</h3>
        <span className="text-[10px] text-gray-500 ml-2">(5분 수익률 기준)</span>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Bullish Divergence */}
        <div className="text-center p-3 bg-gray-800/30 rounded-lg">
          <div className="text-xs text-gray-400 mb-1">강세 다이버전스</div>
          <div className="text-[10px] text-gray-500 mb-2">가격↓ + 매수↑</div>
          {bullish ? (
            <>
              <div className={`text-xl font-bold ${
                bullish.avg_return_5m && bullish.avg_return_5m > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {bullish.avg_return_5m !== null ? `${bullish.avg_return_5m > 0 ? '+' : ''}${bullish.avg_return_5m.toFixed(2)}%` : '-'}
              </div>
              <div className="text-[10px] text-gray-500 mt-1">
                {bullish.count}건 | 승률 {bullish.win_rate?.toFixed(1) || '-'}%
              </div>
            </>
          ) : (
            <div className="text-gray-500 text-sm">데이터 없음</div>
          )}
        </div>

        {/* Bearish Divergence */}
        <div className="text-center p-3 bg-gray-800/30 rounded-lg">
          <div className="text-xs text-gray-400 mb-1">약세 다이버전스</div>
          <div className="text-[10px] text-gray-500 mb-2">가격↑ + 매도↑</div>
          {bearish ? (
            <>
              <div className={`text-xl font-bold ${
                bearish.avg_return_5m && bearish.avg_return_5m > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {bearish.avg_return_5m !== null ? `${bearish.avg_return_5m > 0 ? '+' : ''}${bearish.avg_return_5m.toFixed(2)}%` : '-'}
              </div>
              <div className="text-[10px] text-gray-500 mt-1">
                {bearish.count}건 | 승률 {bearish.win_rate?.toFixed(1) || '-'}%
              </div>
            </>
          ) : (
            <div className="text-gray-500 text-sm">데이터 없음</div>
          )}
        </div>

        {/* No Divergence (Direction Match) */}
        <div className="text-center p-3 bg-gray-800/30 rounded-lg">
          <div className="text-xs text-gray-400 mb-1">방향 일치</div>
          <div className="text-[10px] text-gray-500 mb-2">추세 추종</div>
          {none ? (
            <>
              <div className={`text-xl font-bold ${
                none.avg_return_5m && none.avg_return_5m > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {none.avg_return_5m !== null ? `${none.avg_return_5m > 0 ? '+' : ''}${none.avg_return_5m.toFixed(2)}%` : '-'}
              </div>
              <div className="text-[10px] text-gray-500 mt-1">
                {none.count}건 | 승률 {none.win_rate?.toFixed(1) || '-'}%
              </div>
            </>
          ) : (
            <div className="text-gray-500 text-sm">데이터 없음</div>
          )}
        </div>
      </div>
    </div>
  );
};

// Event List
const EventList: React.FC<{
  events: ResearchEvent[];
  onEventClick: (id: number) => void;
}> = ({ events, onEventClick }) => {
  if (events.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 text-xs">
        이벤트가 없습니다
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {events.map((event) => {
        const isBuySurge = event.event_type === 'buy_surge';
        const hasDivergence = event.divergence_type && event.divergence_type !== 'none';
        const hasOrderSignal = event.order_book_signal && event.order_book_signal !== '없음';

        return (
          <div
            key={event.id}
            onClick={() => onEventClick(event.id)}
            className="px-3 py-2 border-b border-border-color hover:bg-gray-800/50 cursor-pointer transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className={`w-1.5 h-1.5 rounded-full ${isBuySurge ? 'bg-kr-red' : 'bg-kr-blue'}`} />
                <div>
                  <span className="text-xs font-semibold text-white">{event.code}</span>
                  {event.stock_name && event.stock_name !== event.code && (
                    <span className="text-[10px] text-gray-400 ml-1">{event.stock_name}</span>
                  )}
                  <span className="text-[10px] text-gray-500 ml-2">
                    {event.event_time.split(' ')[1]}
                  </span>
                  {/* v2.0: 시간대 표시 */}
                  {event.time_session && event.time_session !== '정규' && (
                    <span className="text-[9px] text-yellow-500 ml-1 flex items-center inline-flex">
                      <Clock className="w-2.5 h-2.5 mr-0.5" />
                      {event.time_session}
                    </span>
                  )}
                </div>
              </div>
              <div className="text-right">
                <div className={`text-xs font-mono ${
                  event.return_1m && event.return_1m > 0 ? 'text-green-400' :
                  event.return_1m && event.return_1m < 0 ? 'text-red-400' : 'text-gray-400'
                }`}>
                  {event.return_1m !== null ? `${event.return_1m > 0 ? '+' : ''}${event.return_1m.toFixed(2)}%` : '-'}
                </div>
                <div className="text-[10px] text-gray-500">1분</div>
              </div>
            </div>
            {/* 상세 정보 행 */}
            <div className="mt-0.5 flex items-center justify-between text-[10px]">
              <div className="flex items-center space-x-3 text-gray-400">
                <span>Delta: {event.delta_vol.toLocaleString()}</span>
                <span>가격: {event.price_at_event.toLocaleString()}원</span>
                {/* v2.0: 동적 임계값 표시 */}
                {event.threshold_type === 'dynamic' && event.threshold_used && (
                  <span className="text-cyan-400">
                    임계: {(event.threshold_used / 1000000).toFixed(0)}M
                  </span>
                )}
              </div>
              {/* v2.0: 배지들 */}
              <div className="flex items-center space-x-1">
                {/* 다이버전스 배지 */}
                {hasDivergence && (
                  <span className={`px-1.5 py-0.5 rounded text-[9px] font-medium ${
                    event.divergence_type === 'bullish'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-red-500/20 text-red-400'
                  }`}>
                    {event.divergence_type === 'bullish' ? '📈강세' : '📉약세'}
                  </span>
                )}
                {/* 호가잔량 신호 배지 */}
                {hasOrderSignal && (
                  <span className="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 text-[9px] font-medium flex items-center">
                    <Zap className="w-2.5 h-2.5 mr-0.5" />
                    호가
                  </span>
                )}
                {/* 노이즈 시간대 경고 */}
                {event.is_noisy_time && (
                  <span className="text-yellow-500" title="노이즈 시간대">
                    <AlertTriangle className="w-3 h-3" />
                  </span>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Stock List
const StockList: React.FC<{ stocks: StockSummary[] }> = ({ stocks }) => {
  if (stocks.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 text-xs">
        종목 데이터가 없습니다
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {stocks.map((stock) => (
        <Link
          key={stock.code}
          to={`/research/stock/${stock.code}`}
          className="block px-3 py-2 border-b border-border-color hover:bg-gray-800/50 transition-colors"
        >
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-white">{stock.code}</span>
              {stock.stock_name && stock.stock_name !== stock.code && (
                <span className="text-[10px] text-gray-400 ml-1">{stock.stock_name}</span>
              )}
              <span className="text-[10px] text-gray-500 ml-2">{stock.event_count}건</span>
            </div>
            <div className="text-right">
              <div className={`text-xs font-mono ${
                stock.avg_return_1m && stock.avg_return_1m > 0 ? 'text-green-400' :
                stock.avg_return_1m && stock.avg_return_1m < 0 ? 'text-red-400' : 'text-gray-400'
              }`}>
                {stock.avg_return_1m !== null ? `${stock.avg_return_1m > 0 ? '+' : ''}${stock.avg_return_1m.toFixed(2)}%` : '-'}
              </div>
              {stock.win_rate_1m !== null && (
                <div className="text-[10px] text-gray-500">
                  승률 {stock.win_rate_1m.toFixed(1)}%
                </div>
              )}
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default ProgramDashboard;
