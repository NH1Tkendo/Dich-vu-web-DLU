import { useState, useCallback, useRef } from "react";

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
function useFormulaSync(initialLatex = "") {
  const [latex, setLatex] = useState(initialLatex);
  const [isDirty, setIsDirty] = useState(false);

  // Guard against infinite update loops when one side sets the other
  const updatingFrom = useRef(null); // 'latex' | 'mathlive' | null

  const setFromLatex = useCallback(
    (value) => {
      if (updatingFrom.current === "mathlive") return; // ignore echo
      updatingFrom.current = "latex";
      setLatex(value);
      setIsDirty(value !== initialLatex);
      // Micro-task reset so the next MathLive event isn't blocked
      setTimeout(() => {
        updatingFrom.current = null;
      }, 0);
    },
    [initialLatex],
  );

  const setFromMathLive = useCallback(
    (value) => {
      if (updatingFrom.current === "latex") return; // ignore echo
      updatingFrom.current = "mathlive";
      setLatex(value);
      setIsDirty(value !== initialLatex);
      setTimeout(() => {
        updatingFrom.current = null;
      }, 0);
    },
    [initialLatex],
  );

  const reset = useCallback(() => {
    setLatex(initialLatex);
    setIsDirty(false);
  }, [initialLatex]);

  return { latex, isDirty, setFromLatex, setFromMathLive, reset };
}

export default useFormulaSync;
