/**
 * LaTeXInput.jsx
 *
 * Controlled textarea for raw LaTeX editing.
 * SPEC §5.2: "LaTeXInput (Raw LaTeX text editor)"
 *
 * Changes here propagate through `useFormulaSync.setFromLatex` which in turn
 * updates the <MathLiveEditor> visual view (bidirectional sync).
 *
 * Phase 1: Logs every keystroke to the console.
 */
import { useId } from 'react';

/**
 * @param {{
 *   value:       string,
 *   onChange:    (value: string) => void,
 *   label?:      string,
 *   placeholder?: string,
 *   rows?:       number,
 *   id?:         string,
 * }} props
 */
function LaTeXInput({
  value = '',
  onChange,
  label = 'LaTeX Source',
  placeholder = String.raw`e.g. \frac{a}{b}`,
  rows = 3,
  id: externalId,
}) {
  const generatedId = useId();
  const inputId = externalId ?? generatedId;

  const handleChange = (e) => {
    const newValue = e.target.value;
    console.log('[LaTeXInput] onChange (mock):', newValue);
    onChange?.(newValue);
  };

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={inputId} className="text-xs font-medium uppercase tracking-widest text-gray-500">
          {label}
        </label>
      )}
      <textarea
        id={inputId}
        className="input-latex resize-none scrollbar-thin"
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        rows={rows}
        spellCheck={false}
        autoComplete="off"
        autoCorrect="off"
        aria-label={label}
      />
      {/* Character count hint */}
      <span className="self-end text-xs text-gray-600">
        {value.length} chars
      </span>
    </div>
  );
}

export default LaTeXInput;
