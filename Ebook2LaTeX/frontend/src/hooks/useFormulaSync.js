/**
 * useFormulaSync.js
 *
 * Custom hook that manages the bidirectional synchronisation state between
 * the raw LaTeX text input (<LaTeXInput>) and the visual MathLive editor
 * (<MathLiveEditor>) for a single formula entry.
 *
 * SPEC §5.3: "Custom hook `useFormulaSync` to manage the bidirectional
 * synchronisation state between `MathLiveEditor` and `LaTeXInput`."
 *
 * Usage:
 *   const { latex, isDirty, setFromLatex, setFromMathLive, reset } =
 *     useFormulaSync(initialLatex);
 */
import { useState, useCallback, useRef } from 'react';

/**
 * @param {string} initialLatex - The starting LaTeX string for this formula.
 * @returns {{
 *   latex:         string,
 *   isDirty:       boolean,
 *   setFromLatex:  (value: string) => void,
 *   setFromMathLive: (value: string) => void,
 *   reset:         () => void,
 * }}
 */
function useFormulaSync(initialLatex = '') {
  const [latex, setLatex] = useState(initialLatex);
  const [isDirty, setIsDirty] = useState(false);

  // Guard against infinite update loops when one side sets the other
  const updatingFrom = useRef(null); // 'latex' | 'mathlive' | null

  /**
   * Called when the user types in the raw <LaTeXInput> textarea.
   * Updates internal state and allows MathLive to re-render.
   */
  const setFromLatex = useCallback((value) => {
    if (updatingFrom.current === 'mathlive') return; // ignore echo
    updatingFrom.current = 'latex';
    setLatex(value);
    setIsDirty(value !== initialLatex);
    // Micro-task reset so the next MathLive event isn't blocked
    setTimeout(() => { updatingFrom.current = null; }, 0);
  }, [initialLatex]);

  /**
   * Called when the MathLive <math-field> fires an `input` event.
   * Updates internal state and reflects changes in the LaTeX textarea.
   */
  const setFromMathLive = useCallback((value) => {
    if (updatingFrom.current === 'latex') return; // ignore echo
    updatingFrom.current = 'mathlive';
    setLatex(value);
    setIsDirty(value !== initialLatex);
    setTimeout(() => { updatingFrom.current = null; }, 0);
  }, [initialLatex]);

  /**
   * Resets the formula back to its initial (server-saved) value
   * and clears the dirty flag.
   */
  const reset = useCallback(() => {
    setLatex(initialLatex);
    setIsDirty(false);
  }, [initialLatex]);

  return { latex, isDirty, setFromLatex, setFromMathLive, reset };
}

export default useFormulaSync;
