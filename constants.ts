
// Korean Market Logic: Red is UP/BUY, Blue is DOWN/SELL
export const COLORS = {
  BUY_TEXT: 'text-kr-red',
  BUY_BG: 'bg-kr-red-bg',
  BUY_BORDER: 'border-kr-red',
  SELL_TEXT: 'text-kr-blue',
  SELL_BG: 'bg-kr-blue-bg',
  SELL_BORDER: 'border-kr-blue',
  POC_BORDER: 'border-highlight',
  POC_TEXT: 'text-highlight',
  NEUTRAL: 'text-gray-400',
  IMBALANCE_BORDER: 'border-orange-400',
  VA_LINE: 'bg-gray-400',
  VAH_VAL_LINE: 'bg-white',
  LVN_BG: 'bg-yellow-500/30',
};

export const ROW_HEIGHT = 16; // px height for a single price row (at 100% zoom)
export const BAR_WIDTH = 140; // px width for a single bar (at 100% zoom)

// Zoom settings
export const ZOOM_LEVELS = [50, 75, 100, 125, 150] as const;
export type ZoomLevel = typeof ZOOM_LEVELS[number];
export const DEFAULT_ZOOM = 100;

export const CONFIG = {
  // Target Stock: Samsung Electronics (Example)
  TARGET_NAME: "Samsung Electronics",
  TARGET_CODE: "005930",
  INITIAL_PRICE: 72500,
  
  // Price Step (Tick Size)
  PRICE_STEP: 100,

  // Imbalance Settings (from PDF: 300% - 400%)
  IMBALANCE_RATIO: 3.0, 
  
  // Simulation Speed
  TICK_RATE_MS: 200, 
};
