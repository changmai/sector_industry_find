import React, { useState, useEffect } from 'react';
import { fetchStockInfo } from '../services/websocketDataService';
import './StockCodeChangeDialog.css';

interface StockCodeChangeDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onApply: (code: string, name: string) => void;
  initialCode: string;
}

const StockCodeChangeDialog: React.FC<StockCodeChangeDialogProps> = ({
  isOpen,
  onClose,
  onApply,
  initialCode
}) => {
  const [inputCode, setInputCode] = useState(initialCode);
  const [stockName, setStockName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setInputCode(initialCode);
      setStockName('');
      setError(null);
    }
  }, [isOpen, initialCode]);

  const handleFetchStockInfo = async () => {
    if (!inputCode.trim()) {
      setError('종목 코드를 입력하세요');
      return;
    }

    setIsLoading(true);
    setError(null);

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

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isLoading) {
      handleFetchStockInfo();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h3>종목 코드 변경</h3>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="dialog-body">
          <div className="input-group">
            <label>종목 코드</label>
            <div className="input-row">
              <input
                type="text"
                value={inputCode}
                onChange={(e) => setInputCode(e.target.value.toUpperCase())}
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
        </div>

        <div className="dialog-footer">
          <button
            className="cancel-button"
            onClick={onClose}
            disabled={isLoading}
          >
            취소
          </button>
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