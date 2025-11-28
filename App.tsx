import React from 'react';
import { Routes, Route } from 'react-router-dom';
import FootprintPage from './pages/FootprintPage';
import DashboardPage from './pages/DashboardPage';
import StockDetailPage from './pages/StockDetailPage';

const App: React.FC = () => {
  return (
    <Routes>
      {/* FootprintPage has its own Header, so no Navigation wrapper needed */}
      <Route path="/" element={<FootprintPage />} />
      <Route path="/research" element={<DashboardPage />} />
      <Route path="/research/stock/:code" element={<StockDetailPage />} />
    </Routes>
  );
};

export default App;
