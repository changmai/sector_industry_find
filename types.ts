
export enum Side {
  Buy = 'Buy',
  Sell = 'Sell',
}

export interface Tick {
  id: string;
  time: string; // HH:MM:SS
  price: number;
  volume: number;
  side: Side;
  timestamp: number;
}

export interface PriceLevelData {
  price: number;
  buyVolume: number;   // Aggressive Buys (Ask side)
  sellVolume: number;  // Aggressive Sells (Bid side)
  totalVolume: number;
  delta: number;       // buyVolume - sellVolume
  imbalanceBuy: boolean; // If true, significant buying imbalance vs diagonal
  imbalanceSell: boolean; // If true, significant selling imbalance vs diagonal
  stackedImbalanceBuy: boolean; // 3+ consecutive buy imbalances (Support Zone)
  stackedImbalanceSell: boolean; // 3+ consecutive sell imbalances (Resistance Zone)
  isPOC: boolean;      // Point of Control (Max Volume)
  isUnfinished: boolean; // Unfinished Business at High/Low
}

export interface FootprintStats {
  totalVolume: number;
  cvd: number; // Cumulative Volume Delta
  high: number;
  low: number;
  open: number;
  close: number;
}

// New Interface for Sequential Bars
export interface FootprintCandle {
  id: number;
  startTime: string;
  endTime?: string;
  open: number;
  high: number;
  low: number;
  close: number;
  totalVolume: number;
  delta: number;
  maxDelta: number;
  minDelta: number;
  priceLevels: PriceLevelData[]; // Processed array, sorted descending
}

// CVD (Cumulative Volume Delta) Candle for visualization
export interface CVDCandle {
  time: number;    // Bar index (0, 1, 2, ...) for lightweight-charts
  open: number;    // Previous CVD Close (0 for first bar)
  high: number;    // CVD_Open + maxDelta
  low: number;     // CVD_Open + minDelta
  close: number;   // CVD_Open + delta
}
