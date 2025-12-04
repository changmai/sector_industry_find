import React, { useMemo } from 'react';
import { Play, Pause, SkipBack, SkipForward, FastForward, Rewind } from 'lucide-react';
import './SimulationControls.css';

export type PlaybackSpeed = 1 | 2 | 4 | 8;

interface SimulationControlsProps {
  isPlaying: boolean;
  currentTime: number;  // Current timestamp in ms
  startTime: number;    // First tick timestamp
  endTime: number;      // Last tick timestamp
  speed: PlaybackSpeed;
  onPlay: () => void;
  onPause: () => void;
  onSeek: (time: number) => void;
  onSpeedChange: (speed: PlaybackSpeed) => void;
  onSkipBack: () => void;
  onSkipForward: () => void;
  tickCount: number;
  currentTickIndex: number;
}

const SimulationControls: React.FC<SimulationControlsProps> = ({
  isPlaying,
  currentTime,
  startTime,
  endTime,
  speed,
  onPlay,
  onPause,
  onSeek,
  onSpeedChange,
  onSkipBack,
  onSkipForward,
  tickCount,
  currentTickIndex
}) => {
  // Calculate progress percentage
  const progress = useMemo(() => {
    if (endTime <= startTime) return 0;
    return ((currentTime - startTime) / (endTime - startTime)) * 100;
  }, [currentTime, startTime, endTime]);

  // Format time for display
  const formatTime = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toTimeString().split(' ')[0]; // HH:MM:SS
  };

  // Handle slider change
  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const percent = parseFloat(e.target.value);
    const newTime = startTime + (percent / 100) * (endTime - startTime);
    onSeek(newTime);
  };

  // Speed button styles
  const getSpeedButtonClass = (s: PlaybackSpeed) => {
    return `speed-btn ${speed === s ? 'active' : ''}`;
  };

  return (
    <div className="simulation-controls">
      {/* Time Bar */}
      <div className="time-bar-container">
        <span className="time-label">{formatTime(startTime)}</span>
        <div className="slider-container">
          <input
            type="range"
            min="0"
            max="100"
            step="0.1"
            value={progress}
            onChange={handleSliderChange}
            className="time-slider"
          />
          <div
            className="slider-progress"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="time-label">{formatTime(endTime)}</span>
      </div>

      {/* Control Buttons */}
      <div className="controls-row">
        {/* Left: Tick Info */}
        <div className="tick-info">
          <span className="tick-count">
            {currentTickIndex.toLocaleString()} / {tickCount.toLocaleString()} ticks
          </span>
          <span className="current-time">{formatTime(currentTime)}</span>
        </div>

        {/* Center: Playback Controls */}
        <div className="playback-controls">
          <button
            className="control-btn"
            onClick={onSkipBack}
            title="처음으로"
          >
            <SkipBack className="w-4 h-4" />
          </button>

          <button
            className="control-btn rewind"
            onClick={() => onSeek(Math.max(startTime, currentTime - 60000))}
            title="1분 뒤로"
          >
            <Rewind className="w-4 h-4" />
          </button>

          <button
            className="control-btn play-pause"
            onClick={isPlaying ? onPause : onPlay}
            title={isPlaying ? '일시정지' : '재생'}
          >
            {isPlaying ? (
              <Pause className="w-5 h-5" />
            ) : (
              <Play className="w-5 h-5" />
            )}
          </button>

          <button
            className="control-btn forward"
            onClick={() => onSeek(Math.min(endTime, currentTime + 60000))}
            title="1분 앞으로"
          >
            <FastForward className="w-4 h-4" />
          </button>

          <button
            className="control-btn"
            onClick={onSkipForward}
            title="끝으로"
          >
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        {/* Right: Speed Controls */}
        <div className="speed-controls">
          <span className="speed-label">Speed:</span>
          <button
            className={getSpeedButtonClass(1)}
            onClick={() => onSpeedChange(1)}
          >
            1x
          </button>
          <button
            className={getSpeedButtonClass(2)}
            onClick={() => onSpeedChange(2)}
          >
            2x
          </button>
          <button
            className={getSpeedButtonClass(4)}
            onClick={() => onSpeedChange(4)}
          >
            4x
          </button>
          <button
            className={getSpeedButtonClass(8)}
            onClick={() => onSpeedChange(8)}
          >
            8x
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimulationControls;
