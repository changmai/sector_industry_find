import React, { useState, useRef } from 'react';
import { Upload, FileText, X } from 'lucide-react';
import './RawDataFileDialog.css';

interface RawDataFileDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onApply: (file: File) => void;
}

const RawDataFileDialog: React.FC<RawDataFileDialogProps> = ({
  isOpen,
  onClose,
  onApply
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.endsWith('.txt')) {
        setError('.txt 파일만 선택할 수 있습니다');
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleApply = () => {
    if (selectedFile) {
      onApply(selectedFile);
      setSelectedFile(null);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setError(null);
    onClose();
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={handleClose}>
      <div className="dialog-content raw-data-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h3>Raw Data 파일 선택</h3>
          <button className="close-button" onClick={handleClose}>
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="dialog-body">
          <div className="file-upload-area" onClick={handleBrowseClick}>
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            <Upload className="upload-icon" />
            <p className="upload-text">클릭하여 파일을 선택하세요</p>
            <p className="upload-hint">raw_data_*.txt 형식의 NDJSON 파일</p>
          </div>

          {selectedFile && (
            <div className="file-info">
              <FileText className="file-icon" />
              <div className="file-details">
                <span className="file-name">{selectedFile.name}</span>
                <span className="file-size">{formatFileSize(selectedFile.size)}</span>
              </div>
              <button
                className="remove-file"
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedFile(null);
                }}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {error && (
            <div className="error-message">{error}</div>
          )}
        </div>

        <div className="dialog-footer">
          <button className="cancel-button" onClick={handleClose}>
            취소
          </button>
          <button
            className="apply-button"
            onClick={handleApply}
            disabled={!selectedFile}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
};

export default RawDataFileDialog;
