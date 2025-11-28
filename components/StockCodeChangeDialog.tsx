import React, { useState, useEffect } from 'react';
import { fetchStockInfo, subscribeToStock, fetchWatchlist } from '../services/websocketDataService';
import './StockCodeChangeDialog.css';

interface StockCodeChangeDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onApply: (code: string, name: string) => void;
  initialCode: string;
  dataSource?: 'mock' | 'raw' | 'websocket';
}

interface WatchlistItem {
  code: string;
  name: string;
  isLoading: boolean;
}

const StockCodeChangeDialog: React.FC<StockCodeChangeDialogProps> = ({
  isOpen,
  onClose,
  onApply,
  initialCode,
  dataSource = 'mock'
}) => {
  const [inputCode, setInputCode] = useState(initialCode);
  const [stockName, setStockName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [subscribeStatus, setSubscribeStatus] = useState<string | null>(null);

  // Watchlist 관련 상태
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [isLoadingWatchlist, setIsLoadingWatchlist] = useState(false);
  const [selectedWatchlistCode, setSelectedWatchlistCode] = useState<string | null>(null);

  // 다이얼로그 열릴 때 watchlist 로드
  useEffect(() => {
    if (isOpen && dataSource === 'websocket') {
      loadWatchlist();
      setInputCode(initialCode);
      setStockName('');
      setError(null);
      setSubscribeStatus(null);
      setSelectedWatchlistCode(null);
    }
  }, [isOpen, dataSource, initialCode]);

  const loadWatchlist = async () => {
    setIsLoadingWatchlist(true);
    try {
      const codes = await fetchWatchlist();

      // 각 종목의 이름을 조회
      const items: WatchlistItem[] = codes.map(code => ({
        code,
        name: '',
        isLoading: true
      }));
      setWatchlist(items);

      // 병렬로 종목명 조회
      const updatedItems = await Promise.all(
        codes.map(async (code) => {
          try {
            const info = await fetchStockInfo(code);
            return { code, name: info.name, isLoading: false };
          } catch {
            return { code, name: '조회 실패', isLoading: false };
          }
        })
      );
      setWatchlist(updatedItems);
    } catch (err) {
      console.error('Failed to load watchlist:', err);
    } finally {
      setIsLoadingWatchlist(false);
    }
  };

  const handleWatchlistSelect = (item: WatchlistItem) => {
    setSelectedWatchlistCode(item.code);
    setInputCode(item.code);
    setStockName(item.name);
    setError(null);
  };

  const handleFetchStockInfo = async () => {
    if (!inputCode.trim()) {
      setError('종목 코드를 입력하세요');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSelectedWatchlistCode(null);

    try {
      const info = await fetchStockInfo(inputCode);
      setStockName(info.name);
      setError(null);
    } catch (err) {
      setError('종목 정보를 가져올 수 없습니다');
      setStockName('');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApply = () => {
    if (inputCode && stockName) {
      onApply(inputCode, stockName);
    }
  };

  const handleSubscribe = async () => {
    if (!inputCode.trim()) {
      setError('종목 코드를 입력하세요');
      return;
    }

    setIsLoading(true);
    setSubscribeStatus(null);
    setError(null);

    try {
      const result = await subscribeToStock(inputCode);
      if (result.status === 'success') {
        setSubscribeStatus(`✅ ${result.message}`);
        // Watchlist 새로고침
        loadWatchlist();
      } else if (result.status === 'already_subscribed') {
        setSubscribeStatus(`ℹ️ 이미 구독 중인 종목입니다`);
      } else {
        setSubscribeStatus(`⚠️ ${result.message}`);
      }
    } catch (err) {
      setError('구독 요청 실패');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isLoading) {
      handleFetchStockInfo();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-content stock-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h3>종목 변경</h3>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="dialog-body">
          {/* WebSocket 모드일 때만 Watchlist 표시 */}
          {dataSource === 'websocket' && (
            <div className="watchlist-section">
              <label>
                구독 중인 종목
                {isLoadingWatchlist && <span className="loading-text"> (로딩중...)</span>}
              </label>
              <div className="watchlist-grid">
                {watchlist.map((item) => (
                  <button
                    key={item.code}
                    className={`watchlist-item ${selectedWatchlistCode === item.code ? 'selected' : ''} ${item.code === initialCode ? 'current' : ''}`}
                    onClick={() => handleWatchlistSelect(item)}
                    disabled={item.isLoading}
                  >
                    <span className="watchlist-code">{item.code}</span>
                    <span className="watchlist-name">
                      {item.isLoading ? '...' : item.name}
                    </span>
                    {item.code === initialCode && (
                      <span className="current-badge">현재</span>
                    )}
                  </button>
                ))}
                {watchlist.length === 0 && !isLoadingWatchlist && (
                  <div className="watchlist-empty">구독 중인 종목이 없습니다</div>
                )}
              </div>
            </div>
          )}

          <div className="divider-section">
            <div className="divider-line"></div>
            <span className="divider-text">또는 새 종목 입력</span>
            <div className="divider-line"></div>
          </div>

          <div className="input-group">
            <label>종목 코드</label>
            <div className="input-row">
              <input
                type="text"
                value={inputCode}
                onChange={(e) => {
                  setInputCode(e.target.value.toUpperCase());
                  setSelectedWatchlistCode(null);
                }}
                onKeyPress={handleKeyPress}
                placeholder="예: 005930"
                maxLength={6}
                disabled={isLoading}
              />
              <button
                onClick={handleFetchStockInfo}
                disabled={isLoading || !inputCode.trim()}
                className="fetch-button"
              >
                {isLoading ? '조회중...' : '조회'}
              </button>
            </div>
          </div>

          {stockName && (
            <div className="stock-info">
              <label>종목명</label>
              <div className="stock-name">{stockName}</div>
            </div>
          )}

          {error && (
            <div className="error-message">{error}</div>
          )}

          {subscribeStatus && (
            <div className="subscribe-status">{subscribeStatus}</div>
          )}
        </div>

        <div className="dialog-footer">
          <button
            className="cancel-button"
            onClick={onClose}
            disabled={isLoading}
          >
            취소
          </button>
          {dataSource === 'websocket' && (
            <button
              className="subscribe-button"
              onClick={handleSubscribe}
              disabled={!inputCode.trim() || isLoading}
              title="Watchlist에 종목 추가 (서버 재시작 불필요)"
            >
              Watchlist 추가
            </button>
          )}
          <button
            className="apply-button"
            onClick={handleApply}
            disabled={!stockName || isLoading}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
};

export default StockCodeChangeDialog;
