/**
 * App.jsx – Main application shell for Ebook2LaTeX.
 */
import { useState, useEffect } from "react";
import PDFUploader from "./components/PDFUploader";
import MathLiveEditor from "./components/MathLiveEditor";
import LaTeXInput from "./components/LaTeXInput";
import useFormulaSync from "./hooks/useFormulaSync";
import {
  uploadDocument,
  processDocument,
  batchUpdateFormulas,
} from "./services/api";

// ── Inline: FormulaEditorItem ──────────────────────────────────────
function FormulaEditorItem({ formula, index, onChange }) {
  const { latex, isDirty, setFromLatex, setFromMathLive } = useFormulaSync(
    formula.raw_latex,
  );

  // Gửi state mới nhất lên App để chuẩn bị cho quá trình Submit All
  useEffect(() => {
    onChange(formula.id, latex, isDirty);
  }, [latex, isDirty, formula.id, onChange]);

  const statusClass =
    {
      pending: "badge-pending",
      reviewed: "badge-reviewed",
      submitted: "badge-submitted",
    }[formula.status] ?? "badge-pending";

  return (
    <article
      className="card animate-slide-up space-y-4"
      id={`formula-item-${formula.id}`}
      aria-label={`Formula ${index + 1}`}
    >
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-sm font-semibold text-gray-300">
          Formula #{index + 1}
        </h3>
        <div className="flex items-center gap-2">
          {isDirty && (
            <span className="text-xs text-warning animate-pulse-slow">
              ● unsaved
            </span>
          )}
          <span className={statusClass}>{formula.status}</span>
        </div>
      </div>

      <MathLiveEditor
        value={latex}
        onChange={setFromMathLive}
        id={`math-field-${formula.id}`}
      />

      <LaTeXInput
        value={latex}
        onChange={setFromLatex}
        id={`latex-input-${formula.id}`}
      />
    </article>
  );
}

// ── App ────────────────────────────────────────────────────────────
function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [formulas, setFormulas] = useState([]);
  const [drafts, setDrafts] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleUpload = async (file) => {
    setUploadedFile(file);
    setIsProcessing(true);
    setFormulas([]);
    setDrafts({});

    try {
      // 1. Upload file
      const uploadRes = await uploadDocument(file);
      const docId = uploadRes.data.id;

      // 2. Chạy OCR Process
      const processRes = await processDocument(docId);

      setFormulas(processRes.data);
    } catch (err) {
      console.error("Error in flow:", err);
      alert(
        "Đã xảy ra lỗi trong quá trình xử lý file PDF. Vui lòng xem console.",
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFormulaChange = (id, latex, isDirty) => {
    setDrafts((prev) => ({ ...prev, [id]: { latex, isDirty } }));
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      // Tạo payload gom toàn bộ dữ liệu mới nhất
      const payload = formulas.map((f) => ({
        id: f.id,
        raw_latex: drafts[f.id]?.latex ?? f.raw_latex,
        status: "submitted",
      }));

      const res = await batchUpdateFormulas(payload);
      if (res.data.success) {
        // Cập nhật lại UI hiển thị status "submitted"
        setFormulas((prev) =>
          prev.map((f) => ({
            ...f,
            raw_latex: drafts[f.id]?.latex ?? f.raw_latex,
            status: "submitted",
          })),
        );
        setDrafts({}); // reset drafts
        alert(`Đã lưu thành công ${res.data.updated_count} công thức!`);
      }
    } catch (err) {
      console.error("Submit error:", err);
      alert("Lưu thất bại. Xem console.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-dvh bg-surface-900 bg-grid-pattern bg-grid font-sans text-white">
      <header className="sticky top-0 z-30 border-b border-surface-700 bg-surface-900/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-500 shadow-glow-sm">
              <svg
                className="h-4 w-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776"
                />
              </svg>
            </div>
            <h1 className="text-lg font-bold tracking-tight">
              <span className="text-gradient">Ebook2LaTeX</span>
            </h1>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-10" id="main-content">
        <section aria-labelledby="upload-heading" className="mb-10">
          <PDFUploader onUpload={handleUpload} />
          {isProcessing && (
            <div className="mt-4 flex items-center gap-3 text-primary-300 animate-pulse">
              <svg
                className="h-5 w-5 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              <span>Đang phân tích, Vui lòng chờ.</span>
            </div>
          )}

          {!isProcessing && uploadedFile && (
            <p className="mt-3 text-sm text-gray-500">
              Đã phân tích:{" "}
              <span className="text-primary-300 font-medium">
                {uploadedFile.name}
              </span>
            </p>
          )}
        </section>

        {formulas.length > 0 && (
          <section
            aria-labelledby="formulas-heading"
            className="animate-fade-in"
          >
            <div className="mb-6 flex items-center justify-between gap-4">
              <div>
                <h2
                  id="formulas-heading"
                  className="text-2xl font-bold tracking-tight"
                >
                  Extracted Formulas
                </h2>
                <p className="mt-1 text-sm text-gray-500">
                  {formulas.length} công thức đã được tìm thấy
                </p>
              </div>
              <button
                id="submit-btn"
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="btn-primary"
                type="button"
              >
                {isSubmitting ? "Đang lưu..." : "Submit All"}
              </button>
            </div>

            <div className="space-y-5">
              {formulas.map((formula, idx) => (
                <FormulaEditorItem
                  key={formula.id}
                  formula={formula}
                  index={idx}
                  onChange={handleFormulaChange}
                />
              ))}
            </div>
          </section>
        )}
      </main>

      <footer className="mt-20 border-t border-surface-700 py-6 text-center text-xs text-gray-600">
        Dự án môn dịch vụ web
      </footer>
    </div>
  );
}

export default App;
