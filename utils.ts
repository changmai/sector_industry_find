import { PriceLevelData } from './types';
import { CONFIG } from './constants';

/**
 * Raw Map data를 받아 분석 지표(Imbalance, POC, Stacked 등)가 포함된 배열로 변환
 */
export const calculateFootprintIndicators = (
  priceMap: Map<number, PriceLevelData>
): PriceLevelData[] => {
  const rawData: PriceLevelData[] = Array.from(priceMap.values());
  if (rawData.length === 0) return [];

  // 1. Find POC (Max Volume)
  const maxVol = Math.max(...rawData.map((d) => d.totalVolume));

  // 2. First Pass: Calculate Basic Diagonal Imbalances
  let processed = rawData.map((item) => {
    const priceStep = 100;

    const bidAtP = item.sellVolume;
    const askAtP = item.buyVolume;

    // Check for Sell Imbalance (Bid P vs Ask P+1)
    const levelAbove = priceMap.get(item.price + priceStep);
    const askAbove = levelAbove ? levelAbove.buyVolume : 0;
    const isSellImbalance =
      askAbove > 0 && bidAtP >= askAbove * CONFIG.IMBALANCE_RATIO;

    // Check for Buy Imbalance (Ask P vs Bid P-1)
    const levelBelow = priceMap.get(item.price - priceStep);
    const bidBelow = levelBelow ? levelBelow.sellVolume : 0;
    const isBuyImbalance =
      bidBelow > 0 && askAtP >= bidBelow * CONFIG.IMBALANCE_RATIO;

    return {
      ...item,
      isPOC: item.totalVolume === maxVol,
      imbalanceBuy: isBuyImbalance,
      imbalanceSell: isSellImbalance,
      // Reset advanced flags for second pass
      stackedImbalanceBuy: false,
      stackedImbalanceSell: false,
      isUnfinished: false,
    };
  });

  // Sort by price descending (High to Low)
  processed.sort((a, b) => b.price - a.price);

  // 3. Second Pass: Stacked Imbalances & Unfinished Business
  for (let i = 0; i < processed.length; i++) {
    // --- Stacked Imbalance Logic (3+ consecutive) ---
    if (i <= processed.length - 3) {
      // Check Buy Stack
      if (
        processed[i].imbalanceBuy &&
        processed[i + 1].imbalanceBuy &&
        processed[i + 2].imbalanceBuy
      ) {
        processed[i].stackedImbalanceBuy = true;
        processed[i + 1].stackedImbalanceBuy = true;
        processed[i + 2].stackedImbalanceBuy = true;
      }
      // Check Sell Stack
      if (
        processed[i].imbalanceSell &&
        processed[i + 1].imbalanceSell &&
        processed[i + 2].imbalanceSell
      ) {
        processed[i].stackedImbalanceSell = true;
        processed[i + 1].stackedImbalanceSell = true;
        processed[i + 2].stackedImbalanceSell = true;
      }
    }

    // --- Unfinished Business Logic (High/Low) ---
    // Check High (Index 0)
    if (i === 0) {
      if (processed[i].buyVolume > 0 && processed[i].sellVolume > 0) {
        processed[i].isUnfinished = true;
      }
    }
    // Check Low (Last Index)
    if (i === processed.length - 1) {
      if (processed[i].buyVolume > 0 && processed[i].sellVolume > 0) {
        processed[i].isUnfinished = true;
      }
    }
  }

  return processed;
};
