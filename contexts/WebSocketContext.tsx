/**
 * WebSocket 연결 상태 Context
 *
 * 역할: 연결 상태 + 오늘 이벤트 카운트만 관리 (FootprintPage 로직과 분리)
 * - FootprintPage의 기존 WebSocket 로직은 그대로 유지
 * - Context는 Header 네비게이션에서 연결 상태 표시용으로만 사용
 * - 서버 상태를 주기적으로 확인하여 연결 상태 표시 (연구 페이지에서도 동작)
 */

import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';

interface WebSocketContextType {
  isConnected: boolean;
  todayEventCount: number;
  setConnected: (status: boolean) => void;
  incrementEventCount: () => void;
  setEventCount: (count: number) => void;
}

const WebSocketContext = createContext<WebSocketContextType | null>(null);

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within WebSocketProvider');
  }
  return context;
};

interface WebSocketProviderProps {
  children: React.ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [todayEventCount, setTodayEventCount] = useState(0);

  // FootprintPage에서 직접 설정한 연결 상태
  const manualConnectionRef = useRef(false);

  const setConnected = useCallback((status: boolean) => {
    manualConnectionRef.current = status;
    setIsConnected(status);
  }, []);

  const incrementEventCount = useCallback(() => {
    setTodayEventCount(prev => prev + 1);
  }, []);

  const setEventCount = useCallback((count: number) => {
    setTodayEventCount(count);
  }, []);

  // 자정에 이벤트 카운트 리셋
  useEffect(() => {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);
    const msUntilMidnight = tomorrow.getTime() - now.getTime();

    const resetTimeout = setTimeout(() => {
      setTodayEventCount(0);
    }, msUntilMidnight);

    return () => clearTimeout(resetTimeout);
  }, []);

  // 서버 상태 확인 (연구 페이지에서도 연결 상태 표시용)
  useEffect(() => {
    const checkServerStatus = async () => {
      // FootprintPage에서 직접 연결 관리 중이면 스킵
      if (manualConnectionRef.current) {
        return;
      }

      try {
        const response = await fetch(`http://${window.location.hostname}:8000/`);
        if (response.ok) {
          const data = await response.json();
          // LS WebSocket 클라이언트가 실행 중인지 확인
          setIsConnected(data.ls_client_running === true);
        } else {
          setIsConnected(false);
        }
      } catch {
        setIsConnected(false);
      }
    };

    // 초기 확인
    checkServerStatus();

    // 10초마다 확인 (FootprintPage가 아닌 곳에서)
    const interval = setInterval(checkServerStatus, 10000);

    return () => clearInterval(interval);
  }, []);

  // 서버에서 오늘 이벤트 수 가져오기
  useEffect(() => {
    const fetchTodayEvents = async () => {
      try {
        const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
        const response = await fetch(`http://${window.location.hostname}:8000/api/research/events?date=${today}`);
        if (response.ok) {
          const data = await response.json();
          setTodayEventCount(data.count || 0);
        }
      } catch {
        // 서버 연결 실패 시 무시
      }
    };

    fetchTodayEvents();

    // 30초마다 이벤트 수 갱신
    const interval = setInterval(fetchTodayEvents, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <WebSocketContext.Provider value={{
      isConnected,
      todayEventCount,
      setConnected,
      incrementEventCount,
      setEventCount
    }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export default WebSocketContext;
