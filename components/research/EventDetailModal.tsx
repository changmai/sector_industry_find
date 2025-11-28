import React, { useState, useEffect } from 'react';
import { X, TrendingUp, TrendingDown, Clock, DollarSign } from 'lucide-react';
import { EventDetailResponse, PriceTracking } from '../../types/research';
import LoadingSpinner from '../ui/LoadingSpinner';

interface EventDetailModalProps {
  eventId: number | null;
  isOpen: boolean;
  onClose: () => void;
}

const EventDetailModal: React.FC<EventDetailModalProps> = ({ eventId, isOpen, onClose }) => {
  const [data, setData] = useState<EventDetailResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && eventId) {
      fetchEventDetail();
    }
  }, [eventId, isOpen]);

  const fetchEventDetail = async () => {
    if (!eventId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/research/event/${eventId}/detail`);
      if (!response.ok) {
        throw new Error('이벤트 정보를 불러오지 못했습니다');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const isBuySurge = data?.event?.event_type === 'buy_surge';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-panel-bg border border-border-color rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border-color">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded ${isBuySurge ? 'bg-kr-red/20' : 'bg-kr-blue/20'}`}>
              {isBuySurge ? (
                <TrendingUp className="w-5 h-5 text-kr-red" />
              ) : (
                <TrendingDown className="w-5 h-5 text-kr-blue" />
              )}
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">
                이벤트 #{eventId}
              </h2>
              {data?.event && (
                <p className="text-sm text-gray-400">
                  {data.event.stock_name} ({data.event.code})
                </p>
              )}
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 overflow-y-auto max-h-[calc(90vh-120px)]">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <LoadingSpinner size="lg" />
            </div>
          )}

          {error && (
            <div className="text-center py-8 text-red-400">
              {error}
            </div>
          )}

          {data?.event && !loading && (
            <div className="space-y-6">
              {/* Event Info */}
              <div className="grid grid-cols-2 gap-4">
                <InfoCard
                  icon={<Clock className="w-4 h-4" />}
                  label="이벤트 시간"
                  value={data.event.event_time}
                />
                <InfoCard
                  icon={<DollarSign className="w-4 h-4" />}
                  label="이벤트 가격"
                  value={`${data.event.price_at_event.toLocaleString()}원`}
                />
                <InfoCard
                  label="이벤트 유형"
                  value={isBuySurge ? '비차익 매수 급증' : '비차익 매도 급증'}
                  valueClassName={isBuySurge ? 'text-kr-red' : 'text-kr-blue'}
                />
                <InfoCard
                  label="추정 금액"
                  value={`${(data.event.trigger_value / 100000000).toFixed(2)}억원`}
                />
                <InfoCard
                  label="Delta Volume"
                  value={`${data.event.delta_vol.toLocaleString()}주`}
                />
                <InfoCard
                  label="전체순매수금액"
                  value={`${(data.event.tval / 100000000).toFixed(2)}억원`}
                />
              </div>

              {/* Price Tracking Chart */}
              {data.event.price_tracking && data.event.price_tracking.length > 0 && (
                <div className="border border-border-color rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-gray-300 mb-4">가격 추적</h3>
                  <PriceTrackingChart
                    tracking={data.event.price_tracking}
                    isBuySurge={isBuySurge}
                  />
                </div>
              )}

              {/* Raw Data */}
              <div className="border border-border-color rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-300 mb-3">상세 데이터</h3>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <DataRow label="비차익매수호가잔량" value={data.event.bshrem?.toLocaleString()} />
                  <DataRow label="비차익매도호가잔량" value={data.event.bdhrem?.toLocaleString()} />
                  <DataRow label="비차익매수체결수량" value={data.event.bshvolume?.toLocaleString()} />
                  <DataRow label="비차익매도체결수량" value={data.event.bdhvolume?.toLocaleString()} />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Helper Components
const InfoCard: React.FC<{
  icon?: React.ReactNode;
  label: string;
  value: string;
  valueClassName?: string;
}> = ({ icon, label, value, valueClassName = 'text-white' }) => (
  <div className="bg-gray-800/50 rounded-lg p-3">
    <div className="flex items-center space-x-2 text-gray-400 text-xs mb-1">
      {icon}
      <span>{label}</span>
    </div>
    <div className={`font-semibold ${valueClassName}`}>{value}</div>
  </div>
);

const DataRow: React.FC<{ label: string; value?: string }> = ({ label, value }) => (
  <div className="flex justify-between">
    <span className="text-gray-500">{label}</span>
    <span className="text-gray-300 font-mono">{value || '-'}</span>
  </div>
);

const PriceTrackingChart: React.FC<{
  tracking: PriceTracking[];
  isBuySurge: boolean;
}> = ({ tracking, isBuySurge }) => {
  // Sort by minutes_after
  const sortedTracking = [...tracking].sort((a, b) => a.minutes_after - b.minutes_after);

  // Find min/max for scaling
  const values = sortedTracking.map(t => t.price_change_pct);
  const maxAbs = Math.max(Math.abs(Math.min(...values)), Math.abs(Math.max(...values)), 0.5);

  return (
    <div className="space-y-2">
      {sortedTracking.map((track) => {
        const pct = track.price_change_pct || 0;
        const width = Math.abs(pct) / maxAbs * 50;
        const isPositive = pct > 0;
        const isWin = isBuySurge ? isPositive : !isPositive;

        return (
          <div key={track.minutes_after} className="flex items-center space-x-3">
            <span className="w-12 text-xs text-gray-400 text-right">
              +{track.minutes_after}분
            </span>
            <div className="flex-1 h-6 relative bg-gray-800 rounded overflow-hidden">
              <div className="absolute inset-0 flex items-center">
                <div className="w-1/2 flex justify-end">
                  {!isPositive && (
                    <div
                      className={`h-4 rounded-l ${isWin ? 'bg-green-500' : 'bg-red-500'}`}
                      style={{ width: `${width}%` }}
                    />
                  )}
                </div>
                <div className="w-px h-full bg-gray-600" />
                <div className="w-1/2">
                  {isPositive && (
                    <div
                      className={`h-4 rounded-r ${isWin ? 'bg-green-500' : 'bg-red-500'}`}
                      style={{ width: `${width}%` }}
                    />
                  )}
                </div>
              </div>
            </div>
            <span className={`w-16 text-xs font-mono text-right ${isWin ? 'text-green-400' : 'text-red-400'}`}>
              {pct > 0 ? '+' : ''}{pct.toFixed(2)}%
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default EventDetailModal;
