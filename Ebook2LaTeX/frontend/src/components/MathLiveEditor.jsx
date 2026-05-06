/**
 * MathLiveEditor.jsx
 *
 * Wrapper around the MathLive <math-field> web component for interactive,
 * visual formula editing.
 *
 * SPEC §5.2: "MathLiveEditor (Interactive visual formula editor)"
 * SPEC §5.3: Synchronised via the `useFormulaSync` hook.
 *
 * MathLive registers <math-field> as a custom element; we import the module
 * side-effect to trigger registration.
 *
 * Phase 1: Emits console.log on every change instead of calling the API.
 */
import { useEffect, useRef } from 'react';
import 'mathlive';

/**
 * @param {{
 *   value:    string,   – controlled LaTeX string
 *   onChange: (latex: string) => void,
 *   readOnly?: boolean,
 *   id?:      string,
 * }} props
 */
function MathLiveEditor({ value = '', onChange, readOnly = false, id }) {
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
      console.log('[MathLiveEditor] onChange (mock):', newLatex);
      onChange?.(newLatex);
    };

    mf.addEventListener('input', handleInput);
    return () => mf.removeEventListener('input', handleInput);
  }, [onChange]);

  // ── Apply readOnly after mount ─────────────────────────────────────
  useEffect(() => {
    const mf = mathFieldRef.current;
    if (!mf) return;
    mf.readOnly = readOnly;
  }, [readOnly]);

  // ── Render ────────────────────────────────────────────────────────
  return (
    <div className="mathlive-wrapper rounded-lg border border-surface-500 bg-surface-900 p-1 transition-colors focus-within:border-primary-500 focus-within:ring-1 focus-within:ring-primary-500/50">
      {/* eslint-disable-next-line react/no-unknown-property */}
      <math-field
        ref={mathFieldRef}
        id={id}
        class="block w-full text-gray-900 bg-white"
        style={{ minHeight: '3rem' }}
      />
    </div>
  );
}

export default MathLiveEditor;
