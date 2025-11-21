import { Side, Tick } from '../types';
import { CONFIG } from '../constants';

let currentPrice = CONFIG.INITIAL_PRICE;
let lastTime = Date.now();

// Random walk parameters
const VOLATILITY = 100; // Price step size
const VOLUME_MIN = 1;
const VOLUME_MAX = 500;

export const generateTick = (): Tick => {
  const now = Date.now();
  
  // Determine side bias based on simple sine wave to simulate momentum
  const timeBias = Math.sin(now / 10000); 
  const isBuyBias = Math.random() > (0.5 - (timeBias * 0.1));
  
  const side = isBuyBias ? Side.Buy : Side.Sell;
  
  // Price Movement
  // 20% chance to move price, 80% chance to stay at level (build volume)
  const move = Math.random() > 0.8;
  
  if (move) {
    if (side === Side.Buy) {
      currentPrice += VOLATILITY;
    } else {
      currentPrice -= VOLATILITY;
    }
  }

  // Volume generation (weighted towards smaller lots, occasional whales)
  let volume = Math.floor(Math.random() * (VOLUME_MAX - VOLUME_MIN + 1)) + VOLUME_MIN;
  if (Math.random() > 0.95) volume *= 5; // Whale trade

  const date = new Date(now);
  const timeStr = date.toTimeString().split(' ')[0]; // HH:MM:SS

  return {
    id: Math.random().toString(36).substring(7),
    time: timeStr,
    price: currentPrice,
    volume: volume,
    side: side,
    timestamp: now,
  };
};