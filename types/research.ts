/**
 * 연구 대시보드 API 타입 정의
 */

// ============================================
// API 응답 타입
// ============================================

export interface ResearchSummary {
  total_events: number;
  buy_events: number;
  sell_events: number;
  avg_return_1m: number | null;
  avg_return_5m: number | null;
  avg_return_10m: number | null;
  avg_return_30m: number | null;
  win_rate_1m: number | null;
  win_rate_5m: number | null;
  win_rate_10m: number | null;
  win_rate_30m: number | null;
  last_updated: string;
}

export interface ResearchEvent {
  id: number;
  event_time: string;
  code: string;
  stock_name?: string;
  event_type: 'buy_surge' | 'sell_surge';
  trigger_value: number;
  price_at_event: number;
  delta_vol: number;
  bshrem?: number;
  bdhrem?: number;
  bshvolume?: number;
  bdhvolume?: number;
  tval?: number;
  return_1m: number | null;
  return_5m: number | null;
  return_10m: number | null;
  return_30m: number | null;
}

export interface StockSummary {
  code: string;
  stock_name?: string;
  event_count: number;
  avg_return_1m: number | null;
  win_rate_1m: number | null;
}

export interface LiveResearchResponse {
  status: string;
  summary: ResearchSummary;
  recent_events: ResearchEvent[];
  by_stock: StockSummary[];
}

// ============================================
// 이벤트 상세 응답 타입
// ============================================

export interface PriceTracking {
  minutes_after: number;
  price: number;
  price_change_pct: number;
  tracking_time: string;
}

export interface EventDetailResponse {
  status: string;
  event: {
    id: number;
    event_time: string;
    code: string;
    stock_name: string;
    event_type: string;
    trigger_value: number;
    price_at_event: number;
    delta_vol: number;
    bshrem: number;
    bdhrem: number;
    bshvolume: number;
    bdhvolume: number;
    tval: number;
  };
  price_tracking: PriceTracking[];
}

// ============================================
// 종목 상세 응답 타입
// ============================================

export interface HourlyStats {
  hour: string;
  count: number;
  avg_return: number | null;
  win_rate: number | null;
}

export interface DeltaRangeStats {
  range: string;
  count: number;
  avg_return: number | null;
  win_rate: number | null;
}

export interface StockDetailResponse {
  status: string;
  code: string;
  summary: {
    total_events: number;
    avg_return_1m: number | null;
    avg_return_5m: number | null;
    avg_return_10m: number | null;
    avg_return_30m: number | null;
    win_rate_1m: number | null;
  };
  events: ResearchEvent[];
  by_hour: HourlyStats[];
  by_delta: DeltaRangeStats[];
}

// ============================================
// 컴포넌트 Props 타입
// ============================================

export interface EventDetailModalProps {
  eventId: number | null;
  isOpen: boolean;
  onClose: () => void;
}

export interface SummaryCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
}

// ============================================
// 다이버전스 분석 타입
// ============================================

export interface DivergenceStats {
  count: number;
  avg_return_5m: number | null;
  win_rate: number | null;
}

export interface TrendStats {
  trend: 'up' | 'down' | 'sideways';
  event_type: 'buy_surge' | 'sell_surge';
  count: number;
  avg_return_1m: number | null;
  avg_return_5m: number | null;
  win_rate_5m: number | null;
}

export interface DivergenceAnalysisResponse {
  status: string;
  date: string | null;
  by_divergence: {
    bullish?: DivergenceStats;
    bearish?: DivergenceStats;
    none?: DivergenceStats;
  };
  by_trend: TrendStats[];
}
