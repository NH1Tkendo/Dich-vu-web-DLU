/**
 * PDFUploader.jsx
 *
 * File upload component with drag-and-drop support.
 * SPEC §5.2: "PDFUploader (File upload component with drag-drop support)"
 *
 * Phase 1: Validates file type/size client-side, then logs the File object
 * to the console instead of calling the real API.
 */
import { useState, useCallback, useId } from 'react';

const MAX_SIZE_MB = 50;
const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

/**
 * @param {{ onUpload: (file: File) => void }} props
 *   onUpload – callback invoked with the validated File when the user selects one.
 */
function PDFUploader({ onUpload }) {
  const inputId = useId();
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError]           = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  // ── Validation ────────────────────────────────────────────────────
  const validate = (file) => {
    if (!file) return 'No file selected.';
    if (file.type !== 'application/pdf') return 'Only PDF files are accepted.';
    if (file.size > MAX_SIZE_BYTES) return `File must be smaller than ${MAX_SIZE_MB} MB.`;
    return null;
  };

  const handleFile = useCallback((file) => {
    const err = validate(file);
    if (err) {
      setError(err);
      setSelectedFile(null);
      return;
    }
    setError(null);
    setSelectedFile(file);
    console.log('[PDFUploader] File selected:', file.name);
    onUpload?.(file);
  }, [onUpload]);

  // ── Event handlers ────────────────────────────────────────────────
  const onInputChange = (e) => handleFile(e.target.files?.[0]);

  const onDragOver  = (e) => { e.preventDefault(); setIsDragging(true); };
  const onDragLeave = ()  => setIsDragging(false);
  const onDrop      = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  // ── Render ────────────────────────────────────────────────────────
  return (
    <div className="w-full animate-fade-in" id="pdf-uploader">
      <label
        htmlFor={inputId}
        className={`drop-zone ${isDragging ? 'drop-zone-active' : ''}`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        aria-label="Upload PDF file"
      >
        {/* Icon */}
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary-500/10 ring-1 ring-primary-500/30">
          <svg className="h-8 w-8 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
            />
          </svg>
        </div>

        {/* Text */}
        <div>
          <p className="text-base font-semibold text-gray-200">
            {isDragging ? 'Drop your PDF here…' : 'Drag & drop a PDF file'}
          </p>
          <p className="mt-1 text-sm text-gray-500">or click to browse — max {MAX_SIZE_MB} MB</p>
        </div>

        {/* Selected file indicator */}
        {selectedFile && (
          <div className="flex items-center gap-2 rounded-lg bg-primary-500/10 px-4 py-2 text-sm text-primary-300 ring-1 ring-primary-500/30">
            <svg className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
            </svg>
            <span className="truncate font-medium">{selectedFile.name}</span>
            <span className="ml-auto shrink-0 text-gray-500">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </span>
          </div>
        )}

        {/* Hidden file input */}
        <input
          id={inputId}
          type="file"
          accept="application/pdf"
          className="sr-only"
          onChange={onInputChange}
          aria-label="PDF file input"
        />
      </label>

      {/* Error message */}
      {error && (
        <p role="alert" className="mt-3 flex items-center gap-1.5 text-sm text-danger">
          <svg className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
}

export default PDFUploader;
