import { useEffect, useRef } from "react";
import "mathlive";

function MathLiveEditor({ value = "", onChange, readOnly = false, id }) {
  const mathFieldRef = useRef(null);

  // ── Sync external `value` → math-field (without triggering onChange echo) ──
  useEffect(() => {
    const mf = mathFieldRef.current;
    if (!mf) return;
    // Only update the DOM if the content actually differs to avoid cursor jump
    if (mf.getValue() !== value) {
      mf.setValue(value, { suppressChangeNotifications: true });
    }
  }, [value]);

  // ── Wire up the math-field input event once on mount ──────────────
  useEffect(() => {
    const mf = mathFieldRef.current;
    if (!mf) return;

    const handleInput = () => {
      const newLatex = mf.getValue();
      console.log("[MathLiveEditor] onChange (mock):", newLatex);
      onChange?.(newLatex);
    };

    mf.addEventListener("input", handleInput);
    return () => mf.removeEventListener("input", handleInput);
  }, [onChange]);

  useEffect(() => {
    const mf = mathFieldRef.current;
    if (!mf) return;
    mf.readOnly = readOnly;
  }, [readOnly]);

  return (
    <div className="mathlive-wrapper rounded-lg border border-surface-500 bg-surface-900 p-1 transition-colors focus-within:border-primary-500 focus-within:ring-1 focus-within:ring-primary-500/50">
      <math-field
        ref={mathFieldRef}
        id={id}
        class="block w-full text-gray-900 bg-white"
        style={{ minHeight: "3rem" }}
      />
    </div>
  );
}

export default MathLiveEditor;
