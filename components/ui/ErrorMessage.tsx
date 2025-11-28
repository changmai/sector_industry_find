import React from 'react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => (
  <div className="bg-red-900/50 border border-red-500 rounded-lg p-4 text-center">
    <p className="text-red-300 mb-2">{message}</p>
    {onRetry && (
      <button
        onClick={onRetry}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-500 transition-colors"
      >
        다시 시도
      </button>
    )}
  </div>
);

export default ErrorMessage;
