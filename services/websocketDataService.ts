/**
 * LS증권 실시간 데이터 WebSocket 서비스
 * 백엔드 서버를 통해 실시간 체결 데이터를 수신합니다.
 */

import { Tick } from '../types';

const WS_URL = 'ws://localhost:8000/ws';

interface LSTickData {
  price?: string;
  cvolume?: string;
  cgubun?: string;
  chetime?: string;
}

/**
 * LS증권 데이터를 앱의 Tick 형식으로 변환
 */
function convertLSDataToTick(data: LSTickData): Tick | null {
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
    if (rawTime.length === 6) {
      timeStr = `${rawTime.slice(0, 2)}:${rawTime.slice(2, 4)}:${rawTime.slice(4, 6)}`;
    }

    return {
      id: `ws_${Date.now()}_${Math.random()}`,
      time: timeStr,
      price,
      volume,
      side: isBuy ? 'Buy' : 'Sell',
      timestamp: Date.now(),
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
 * @returns WebSocket 인스턴스
 */
export function connectWebSocket(
  onTick: (tick: Tick) => void,
  onError: (error: string) => void,
  onStatus?: (message: string) => void
): WebSocket {
  const ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    console.log('✅ 백엔드 WebSocket 연결 성공');
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

      // LS증권 체결 데이터 처리
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
