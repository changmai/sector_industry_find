/**
 * Price Grouping Utility
 * Groups tick prices into specified intervals for cleaner footprint visualization
 */

/**
 * Groups a price to the nearest lower multiple of the step size
 * @param price - Original price (e.g., 72,523)
 * @param step - Grouping step size (e.g., 500)
 * @returns Grouped price (e.g., 72,500)
 *
 * @example
 * groupPriceLevel(72523, 500) // Returns 72500
 * groupPriceLevel(72123, 500) // Returns 72000
 * groupPriceLevel(72999, 500) // Returns 72500
 */
export function groupPriceLevel(price: number, step: number): number {
  if (step <= 0) {
    throw new Error('Price step must be greater than 0');
  }

  return Math.floor(price / step) * step;
}

/**
 * Available price grouping options (in Korean Won)
 */
export const PRICE_GROUPING_OPTIONS = [1, 5, 10, 25, 50, 100, 250, 500, 1000] as const;

export type PriceGroupingOption = typeof PRICE_GROUPING_OPTIONS[number];
