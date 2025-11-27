import React, { useEffect, useRef, useImperativeHandle, forwardRef, useState } from 'react';
import { createChart, IChartApi, ISeriesApi, CandlestickData, Time, CandlestickSeries } from 'lightweight-charts';
import { CVDCandle } from '../types';

interface CVDChartProps {
  data: CVDCandle[];
  height?: number;
}

export interface CVDChartHandle {
  scrollToBar: (index: number) => void;
  getVisibleRange: () => { from: number; to: number } | null;
}

const CVDChart = forwardRef<CVDChartHandle, CVDChartProps>(({ data, height = 150 }, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const [isReady, setIsReady] = useState(false);

  // Expose methods for parent component (scroll sync)
  useImperativeHandle(ref, () => ({
    scrollToBar: (index: number) => {
      if (chartRef.current && data.length > 0) {
        const timeScale = chartRef.current.timeScale();
        timeScale.scrollToPosition(-data.length + index + 10, false);
      }
    },
    getVisibleRange: () => {
      if (chartRef.current) {
        const range = chartRef.current.timeScale().getVisibleLogicalRange();
        if (range) {
          return { from: Math.floor(range.from), to: Math.ceil(range.to) };
        }
      }
      return null;
    }
  }));

  // Initialize chart - use ResizeObserver for proper sizing
  useEffect(() => {
    if (!containerRef.current) return;

    // Wait for container to have proper dimensions
    const initChart = () => {
      if (!containerRef.current) return;

      const containerWidth = containerRef.current.clientWidth;
      if (containerWidth === 0) {
        // Container not ready yet, retry
        requestAnimationFrame(initChart);
        return;
      }

      // Clean up existing chart if any
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
        seriesRef.current = null;
      }

      const chart = createChart(containerRef.current, {
        width: containerWidth,
        height: height,
        layout: {
          background: { color: '#1a1a2e' },
          textColor: '#d1d5db',
        },
        grid: {
          vertLines: { color: '#2d2d44' },
          horzLines: { color: '#2d2d44' },
        },
        crosshair: {
          mode: 1,
        },
        rightPriceScale: {
          borderColor: '#3d3d5c',
          scaleMargins: {
            top: 0.1,
            bottom: 0.1,
          },
        },
        timeScale: {
          borderColor: '#3d3d5c',
          timeVisible: false,
          tickMarkFormatter: (time: Time) => String(time),
        },
      });

      // v5 API: use addSeries with CandlestickSeries type
      const candleSeries = chart.addSeries(CandlestickSeries, {
        upColor: '#ef4444',
        downColor: '#3b82f6',
        borderUpColor: '#ef4444',
        borderDownColor: '#3b82f6',
        wickUpColor: '#ef4444',
        wickDownColor: '#3b82f6',
      });

      chartRef.current = chart;
      seriesRef.current = candleSeries;
      setIsReady(true);
    };

    // Use requestAnimationFrame to ensure DOM is ready
    requestAnimationFrame(initChart);

    // Handle resize with ResizeObserver
    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (chartRef.current && entry.contentRect.width > 0) {
          chartRef.current.applyOptions({ width: entry.contentRect.width });
        }
      }
    });

    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
        seriesRef.current = null;
      }
    };
  }, [height]);

  // Update data when it changes
  useEffect(() => {
    if (!isReady || !seriesRef.current) return;

    if (data.length > 0) {
      const chartData: CandlestickData<Time>[] = data.map((candle) => ({
        time: candle.time as Time,
        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close,
      }));

      seriesRef.current.setData(chartData);

      if (chartRef.current) {
        chartRef.current.timeScale().scrollToRealTime();
      }
    }
  }, [data, isReady]);

  return (
    <div className="bg-panel-bg border border-border-color rounded mt-1 shrink-0">
      <div className="flex items-center px-2 py-1 border-b border-border-color">
        <span className="w-2 h-2 rounded-full bg-purple-500 mr-2"></span>
        <h3 className="text-xs font-bold text-gray-300">CVD (Cumulative Volume Delta)</h3>
        <span className="ml-2 text-[10px] text-gray-500">
          {data.length > 0 ? `Latest: ${data[data.length - 1].close.toLocaleString()}` : 'No data'}
        </span>
      </div>
      <div
        ref={containerRef}
        style={{ height: `${height}px`, width: '100%' }}
      />
    </div>
  );
});

CVDChart.displayName = 'CVDChart';

export default CVDChart;
