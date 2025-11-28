/**
 * LS증권 실시간 데이터 WebSocket 서비스
 * 백엔드 서버를 통해 실시간 체결 데이터를 수신합니다.
 */

import { Tick } from '../types';

// 동적으로 WebSocket URL 생성 (브라우저 호스트에 맞춤)
const getWebSocketURL = () => {
  // 개발 환경: 항상 localhost 사용 (방화벽 문제 회피)
  // 배포 시: 실제 hostname 사용
  const isDevelopment = window.location.hostname === 'localhost' ||
                        window.location.hostname === '127.0.0.1' ||
                        window.location.hostname.startsWith('192.168.');

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = isDevelopment ? 'localhost' : window.location.hostname;
  const port = '8000'; // Backend 포트
  return `${protocol}//${host}:${port}/ws`;
};

const WS_URL = getWebSocketURL();

interface LSTickData {
  price?: string;
  cvolume?: string;
  cgubun?: string;
  chetime?: string;
  code?: string;  // 종목코드 필드 추가 (Backend에서 전송)
}

/**
 * LS증권 데이터를 앱의 Tick 형식으로 변환
 */
function convertLSDataToTick(data: LSTickData): (Tick & { code?: string }) | null {
  try {
    const price = parseInt(String(data.price || '0').trim());
    const volume = parseInt(String(data.cvolume || '0').trim());
    const gubun = String(data.cgubun || '').trim();
    const rawTime = String(data.chetime || '');

    if (price === 0 || volume === 0) return null;

    // 매수/매도 구분 ('+' 또는 '1' = 매수, '-' 또는 '2' = 매도)
    const isBuy = gubun === '+' || gubun === '1';

    // 시간 포맷 변환 (HHMMSS → HH:MM:SS)
    let timeStr = rawTime;
    let timestamp = Date.now(); // 기본값: 현재 시각

    if (rawTime.length === 6) {
      timeStr = `${rawTime.slice(0, 2)}:${rawTime.slice(2, 4)}:${rawTime.slice(4, 6)}`;

      // HHMMSS → timestamp 변환 (오늘 날짜 기준)
      const today = new Date();
      const hours = parseInt(rawTime.slice(0, 2));
      const minutes = parseInt(rawTime.slice(2, 4));
      const seconds = parseInt(rawTime.slice(4, 6));

      timestamp = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate(),
        hours,
        minutes,
        seconds
      ).getTime();
    }

    return {
      id: `ws_${Date.now()}_${Math.random()}`,
      time: timeStr,
      price,
      volume,
      side: isBuy ? 'Buy' : 'Sell',
      timestamp: timestamp,
      code: data.code,  // 종목코드 포함 (Backend에서 전송)
    };
  } catch (error) {
    console.error('LS 데이터 변환 실패:', error, data);
    return null;
  }
}

/**
 * 백엔드 WebSocket 서버에 연결
 * @param onTick 틱 데이터 수신 콜백
 * @param onError 에러 콜백
 * @param onStatus 상태 메시지 콜백
 * @param filterCode 필터링할 종목코드 (선택 사항, 지정 시 해당 종목만 콜백 호출)
 * @returns WebSocket 인스턴스
 */
export function connectWebSocket(
  onTick: (tick: Tick) => void,
  onError: (error: string) => void,
  onStatus?: (message: string) => void,
  filterCode?: string
): WebSocket {
  console.log(`🔌 Connecting to WebSocket: ${WS_URL}`);
  const ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    console.log('✅ 백엔드 WebSocket 연결 성공');
    console.log('WebSocket readyState:', ws.readyState);
    onStatus?.('LS증권 실시간 연결 중...');
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      // 상태 메시지 처리
      if (data.type === 'status') {
        console.log('📡 상태:', data.message);
        onStatus?.(data.message);
        return;
      }

      // Ping 처리
      if (data.type === 'ping') {
        ws.send(JSON.stringify({ type: 'pong' }));
        return;
      }

      // 종목 변경 알림 처리
      if (data.type === 'code_changed') {
        console.log('📊 종목 변경 완료:', data.code, '-', data.name);
        onStatus?.(data.message || `종목 변경: ${data.code}`);
        return;
      }

      // LS증권 체결 데이터 처리
      // 모든 데이터를 전달 (App.tsx에서 filterCodeRef로 필터링)
      const tick = convertLSDataToTick(data);
      if (tick) {
        onTick(tick);
      }
    } catch (error) {
      console.error('WebSocket 메시지 파싱 실패:', error);
    }
  };

  ws.onerror = (event) => {
    console.error('❌ WebSocket 에러:', event);
    onError('WebSocket 연결 오류');
  };

  ws.onclose = (event) => {
    console.log('🔌 WebSocket 연결 해제:', event.reason || '정상 종료');
    onStatus?.('연결 해제됨');
  };

  return ws;
}

/**
 * 종목 코드 변경 요청
 * @param ws WebSocket 인스턴스
 * @param code 종목 코드 (예: '005930')
 */
export function changeTargetCode(ws: WebSocket, code: string): void {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'change_code',
      code,
    }));
  }
}

/**
 * REST API를 통해 종목 정보 조회
 * @param code 종목 코드
 * @returns 종목 코드와 이름
 */
export async function fetchStockInfo(code: string): Promise<{ code: string; name: string; status: string }> {
  try {
    // 개발 환경에서는 localhost 사용
    const isDev = window.location.hostname.startsWith('192.168.') ||
                  window.location.hostname === 'localhost' ||
                  window.location.hostname === '127.0.0.1';
    const host = isDev ? 'localhost' : window.location.hostname;
    const apiBase = `${window.location.protocol}//${host}:8000`;
    const response = await fetch(`${apiBase}/api/stock/${code}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch stock info: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching stock info:', error);
    throw error;
  }
}

/**
 * 과거 틱 데이터 조회
 * @param code 종목 코드
 * @param date 날짜 (YYYYMMDD, 선택 사항, default=오늘)
 * @returns Tick 배열
 */
export async function fetchHistoricalData(code: string, date?: string): Promise<Tick[]> {
  try {
    // 개발 환경에서는 localhost 사용
    const isDev = window.location.hostname.startsWith('192.168.') ||
                  window.location.hostname === 'localhost' ||
                  window.location.hostname === '127.0.0.1';
    const host = isDev ? 'localhost' : window.location.hostname;
    const apiBase = `${window.location.protocol}//${host}:8000`;
    const url = date
      ? `${apiBase}/api/history?code=${code}&date=${date}`
      : `${apiBase}/api/history?code=${code}`;

    console.log(`📥 Fetching historical data: ${url}`);

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch history: ${response.status}`);
    }

    const rawData: LSTickData[] = await response.json();
    console.log(`✅ Fetched ${rawData.length} historical ticks`);

    // 원본 데이터를 Tick 형식으로 변환
    const ticks: Tick[] = [];
    for (const data of rawData) {
      const tick = convertLSDataToTick(data);
      if (tick) {
        ticks.push(tick);
      }
    }

    console.log(`✅ Converted ${ticks.length} ticks`);
    return ticks;

  } catch (error) {
    console.error('Error fetching historical data:', error);
    return []; // 오류 시 빈 배열 반환 (신규 데이터만 표시)
  }
}

/**
 * 서버의 watchlist 조회 (구독 중인 종목 목록)
 * @returns watchlist 종목 코드 배열
 */
export async function fetchWatchlist(): Promise<string[]> {
  try {
    const isDev = window.location.hostname.startsWith('192.168.') ||
                  window.location.hostname === 'localhost' ||
                  window.location.hostname === '127.0.0.1';
    const host = isDev ? 'localhost' : window.location.hostname;
    const apiBase = `${window.location.protocol}//${host}:8000`;

    const response = await fetch(`${apiBase}/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch watchlist: ${response.status}`);
    }

    const data = await response.json();
    console.log(`📋 Watchlist loaded: ${data.watchlist?.length || 0} stocks`);
    return data.watchlist || [];

  } catch (error) {
    console.error('Error fetching watchlist:', error);
    return [];
  }
}

/**
 * 새로운 종목을 동적으로 구독 추가 (서버 재시작 불필요)
 * @param code 종목 코드 (예: '035720')
 * @returns 구독 결과
 */
export async function subscribeToStock(code: string): Promise<{ status: string; message: string }> {
  try {
    // 개발 환경에서는 localhost 사용
    const isDev = window.location.hostname.startsWith('192.168.') ||
                  window.location.hostname === 'localhost' ||
                  window.location.hostname === '127.0.0.1';
    const host = isDev ? 'localhost' : window.location.hostname;
    const apiBase = `${window.location.protocol}//${host}:8000`;

    console.log(`📡 Subscribing to new stock: ${code}`);

    const response = await fetch(`${apiBase}/api/subscribe/${code}`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to subscribe: ${response.status}`);
    }

    const data = await response.json();
    console.log(`✅ Subscription result:`, data);

    return {
      status: data.status,
      message: data.message || `${code} 구독 완료`
    };

  } catch (error) {
    console.error('Error subscribing to stock:', error);
    return {
      status: 'error',
      message: `구독 실패: ${error}`
    };
  }
}
