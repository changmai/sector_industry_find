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

  // Pre-allocate result array and find maxVol + totalVolume in single pass
  const processed: PriceLevelData[] = new Array(size);
  let maxVol = 0;
  let totalVolumeSum = 0;  // Calculate total volume in single pass
  let idx = 0;

  // Single iteration: copy to array + find max volume + calculate imbalances + sum total
  for (const item of priceMap.values()) {
    if (item.totalVolume > maxVol) maxVol = item.totalVolume;
    totalVolumeSum += item.totalVolume;  // Accumulate total volume

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
      isVA: false,
      isVAH: false,
      isVAL: false,
      isLVN: false,
    };
  }

  // Set POC flag and record index (second mini-pass, but O(n) with simple comparison)
  let pocIndex = 0;
  for (let i = 0; i < size; i++) {
    if (processed[i].totalVolume === maxVol) {
      processed[i].isPOC = true;
      pocIndex = i;  // Record POC index before sort
      break; // Only one POC needed
    }
  }

  // Sort by price descending (High to Low) - O(n log n), unavoidable
  processed.sort((a, b) => b.price - a.price);

  // Stacked Imbalances & Unfinished Business & Find POC index (single pass after sort)
  const lastIdx = size - 1;
  pocIndex = 0;  // Will be set when POC is found

  for (let i = 0; i < size; i++) {
    const current = processed[i];

    // Find POC index (sorted array)
    if (current.isPOC) {
      pocIndex = i;
    }

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

  // --- Value Area (VA) Calculation ---
  // TPO-style: Start from POC, expand to cover 70% of total volume
  // totalVolumeSum already calculated in first pass (no extra iteration needed)
  const vaTarget = totalVolumeSum * 0.7;

  // Initialize VA with POC
  let vaVolume = processed[pocIndex].totalVolume;
  let vaHigh = pocIndex;
  let vaLow = pocIndex;
  processed[pocIndex].isVA = true;

  // Expand VA until 70% is reached
  while (vaVolume < vaTarget && (vaHigh > 0 || vaLow < lastIdx)) {
    const aboveVol = vaHigh > 0 ? processed[vaHigh - 1].totalVolume : 0;
    const belowVol = vaLow < lastIdx ? processed[vaLow + 1].totalVolume : 0;

    if (aboveVol >= belowVol && vaHigh > 0) {
      vaHigh--;
      vaVolume += processed[vaHigh].totalVolume;
      processed[vaHigh].isVA = true;
    } else if (vaLow < lastIdx) {
      vaLow++;
      vaVolume += processed[vaLow].totalVolume;
      processed[vaLow].isVA = true;
    } else {
      break;
    }
  }

  // Mark VAH and VAL
  processed[vaHigh].isVAH = true;
  processed[vaLow].isVAL = true;

  // --- LVN Detection (Low Volume Nodes) ---
  // Find levels within VA with significantly lower volume than neighbors
  for (let i = vaHigh; i <= vaLow; i++) {
    if (i <= vaHigh || i >= vaLow) continue; // Skip boundaries

    const current = processed[i];
    const above = processed[i - 1];
    const below = processed[i + 1];
    const avgNeighbors = (above.totalVolume + below.totalVolume) / 2;

    // LVN: current volume is less than 40% of neighbor average
    if (current.totalVolume < avgNeighbors * 0.4 && avgNeighbors > 0) {
      current.isLVN = true;
    }
  }

  return processed;
};
