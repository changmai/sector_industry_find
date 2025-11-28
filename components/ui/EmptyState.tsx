import React from 'react';

interface EmptyStateProps {
  message: string;
  icon?: React.ReactNode;
}

const EmptyState: React.FC<EmptyStateProps> = ({ message, icon }) => (
  <div className="flex flex-col items-center justify-center py-12 text-gray-500">
    {icon && <div className="mb-4 text-4xl">{icon}</div>}
    <p className="text-lg">{message}</p>
  </div>
);

export default EmptyState;
