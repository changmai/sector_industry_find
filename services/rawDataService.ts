import { Side, Tick } from '../types';

// 중첩 구조 (header/body 포함)
interface RawDataLineNested {
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

// 플랫 구조 (직접 필드)
interface RawDataLineFlat {
  chetime: string;
  price: string;
  cvolume: string;
  cgubun: string;
}

type RawDataLine = RawDataLineNested | RawDataLineFlat;

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
 * Check if data is nested format (has header/body)
 */
function isNestedFormat(data: any): data is RawDataLineNested {
  return 'header' in data || 'body' in data;
}

/**
 * Parse raw data text content to Tick array
 * Supports both nested format (header/body) and flat format
 */
function parseRawDataText(text: string): Tick[] {
  const lines = text.split('\n').filter(line => line.trim());
  const ticks: Tick[] = [];

  for (let i = 0; i < lines.length; i++) {
    try {
      const data = JSON.parse(lines[i]);

      let chetime: string;
      let priceStr: string;
      let cvolumeStr: string;
      let cgubun: string;

      if (isNestedFormat(data)) {
        // 중첩 구조: {"header": {...}, "body": {...}}
        if (!data.body) continue;
        chetime = data.body.chetime;
        priceStr = data.body.price;
        cvolumeStr = data.body.cvolume;
        cgubun = data.body.cgubun;
      } else {
        // 플랫 구조: {"chetime": ..., "price": ..., ...}
        chetime = data.chetime;
        priceStr = data.price;
        cvolumeStr = data.cvolume;
        cgubun = data.cgubun;
      }

      const price = parseInt(priceStr, 10);
      const volume = parseInt(cvolumeStr, 10);

      // Skip invalid data (price = 0 or invalid)
      if (!price || price === 0 || !volume) continue;

      const tick: Tick = {
        id: `raw_${i}`,
        time: formatTime(chetime),
        price: price,
        volume: volume,
        side: parseSide(cgubun),
        timestamp: Date.now() + i // Use sequential timestamps for playback
      };

      ticks.push(tick);
    } catch (err) {
      console.warn(`Failed to parse line ${i}:`, err);
      continue;
    }
  }

  return ticks;
}

/**
 * Load and parse raw data from NDJSON file (legacy - uses hardcoded path)
 */
export async function loadRawData(): Promise<Tick[]> {
  try {
    const response = await fetch('/raw_data_005930_20251120.txt');
    const text = await response.text();
    const ticks = parseRawDataText(text);

    console.log(`✅ Loaded ${ticks.length} ticks from raw data`);
    return ticks;

  } catch (error) {
    console.error('Failed to load raw data:', error);
    return [];
  }
}

/**
 * Parse raw data from a File object (user-selected file)
 */
export async function parseRawDataFile(file: File): Promise<Tick[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (event) => {
      try {
        const text = event.target?.result as string;
        const ticks = parseRawDataText(text);
        console.log(`✅ Loaded ${ticks.length} ticks from file: ${file.name}`);
        resolve(ticks);
      } catch (error) {
        console.error('Failed to parse file:', error);
        reject(error);
      }
    };

    reader.onerror = () => {
      console.error('Failed to read file:', reader.error);
      reject(reader.error);
    };

    reader.readAsText(file, 'utf-8');
  });
}
