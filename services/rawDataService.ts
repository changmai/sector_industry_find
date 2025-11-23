import { Side, Tick } from '../types';

interface RawDataLine {
  header: {
    tr_cd?: string;
    tr_key?: string;
  };
  body: {
    chetime: string;
    price: string;
    cvolume: string;
    cgubun: string;
  } | null;
}

/**
 * Format time from HHMMSS to HH:MM:SS
 */
function formatTime(chetime: string): string {
  if (chetime.length !== 6) return chetime;
  return `${chetime.slice(0, 2)}:${chetime.slice(2, 4)}:${chetime.slice(4, 6)}`;
}

/**
 * Parse cgubun to determine Buy/Sell side
 */
function parseSide(cgubun: string): Side {
  return cgubun === '+' ? Side.Buy : Side.Sell;
}

/**
 * Load and parse raw data from NDJSON file
 */
export async function loadRawData(): Promise<Tick[]> {
  try {
    const response = await fetch('/raw_data_005930_20251120.txt');
    const text = await response.text();
    const lines = text.split('\n').filter(line => line.trim());

    const ticks: Tick[] = [];

    for (let i = 0; i < lines.length; i++) {
      try {
        const data: RawDataLine = JSON.parse(lines[i]);

        // Skip lines with null body (first line usually)
        if (!data.body) continue;

        const price = parseInt(data.body.price, 10);
        const volume = parseInt(data.body.cvolume, 10);

        // Skip invalid data (price = 0 or invalid)
        if (!price || price === 0 || !volume) continue;

        const tick: Tick = {
          id: `raw_${i}`,
          time: formatTime(data.body.chetime),
          price: price,
          volume: volume,
          side: parseSide(data.body.cgubun),
          timestamp: Date.now() + i // Use sequential timestamps for playback
        };

        ticks.push(tick);
      } catch (err) {
        console.warn(`Failed to parse line ${i}:`, err);
        continue;
      }
    }

    console.log(`✅ Loaded ${ticks.length} ticks from raw data`);
    return ticks;

  } catch (error) {
    console.error('Failed to load raw data:', error);
    return [];
  }
}
