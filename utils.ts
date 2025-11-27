import { PriceLevelData } from './types';
import { CONFIG } from './constants';

/**
 * Raw Map data를 받아 분석 지표(Imbalance, POC, Stacked 등)가 포함된 배열로 변환
 * Optimized: Single pass for most operations, in-place mutation where possible
 */
export const calculateFootprintIndicators = (
  priceMap: Map<number, PriceLevelData>
): PriceLevelData[] => {
  const size = priceMap.size;
  if (size === 0) return [];

  const priceStep = 100;
  const imbalanceRatio = CONFIG.IMBALANCE_RATIO;

  // Pre-allocate result array and find maxVol in single pass
  const processed: PriceLevelData[] = new Array(size);
  let maxVol = 0;
  let idx = 0;

  // Single iteration: copy to array + find max volume + calculate imbalances
  for (const item of priceMap.values()) {
    if (item.totalVolume > maxVol) maxVol = item.totalVolume;

    const bidAtP = item.sellVolume;
    const askAtP = item.buyVolume;

    // Check for Sell Imbalance (Bid P vs Ask P+1)
    const levelAbove = priceMap.get(item.price + priceStep);
    const askAbove = levelAbove ? levelAbove.buyVolume : 0;
    const isSellImbalance = askAbove > 0 && bidAtP >= askAbove * imbalanceRatio;

    // Check for Buy Imbalance (Ask P vs Bid P-1)
    const levelBelow = priceMap.get(item.price - priceStep);
    const bidBelow = levelBelow ? levelBelow.sellVolume : 0;
    const isBuyImbalance = bidBelow > 0 && askAtP >= bidBelow * imbalanceRatio;

    // Create new object with calculated flags
    processed[idx++] = {
      price: item.price,
      buyVolume: item.buyVolume,
      sellVolume: item.sellVolume,
      totalVolume: item.totalVolume,
      delta: item.delta,
      isPOC: false, // Will set after loop
      imbalanceBuy: isBuyImbalance,
      imbalanceSell: isSellImbalance,
      stackedImbalanceBuy: false,
      stackedImbalanceSell: false,
      isUnfinished: false,
    };
  }

  // Set POC flag (second mini-pass, but O(n) with simple comparison)
  for (let i = 0; i < size; i++) {
    if (processed[i].totalVolume === maxVol) {
      processed[i].isPOC = true;
      break; // Only one POC needed
    }
  }

  // Sort by price descending (High to Low) - O(n log n), unavoidable
  processed.sort((a, b) => b.price - a.price);

  // Stacked Imbalances & Unfinished Business (single pass)
  const lastIdx = size - 1;

  for (let i = 0; i < size; i++) {
    const current = processed[i];

    // --- Stacked Imbalance Logic (3+ consecutive) ---
    if (i <= lastIdx - 2) {
      const next1 = processed[i + 1];
      const next2 = processed[i + 2];

      // Check Buy Stack
      if (current.imbalanceBuy && next1.imbalanceBuy && next2.imbalanceBuy) {
        current.stackedImbalanceBuy = true;
        next1.stackedImbalanceBuy = true;
        next2.stackedImbalanceBuy = true;
      }
      // Check Sell Stack
      if (current.imbalanceSell && next1.imbalanceSell && next2.imbalanceSell) {
        current.stackedImbalanceSell = true;
        next1.stackedImbalanceSell = true;
        next2.stackedImbalanceSell = true;
      }
    }

    // --- Unfinished Business Logic (High/Low) ---
    if ((i === 0 || i === lastIdx) && current.buyVolume > 0 && current.sellVolume > 0) {
      current.isUnfinished = true;
    }
  }

  return processed;
};
