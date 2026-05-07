import { useId } from "react";

function LaTeXInput({
  value = "",
  onChange,
  label = "LaTeX Source",
  placeholder = String.raw`e.g. \frac{a}{b}`,
  rows = 3,
  id: externalId,
}) {
  const generatedId = useId();
  const inputId = externalId ?? generatedId;

  const handleChange = (e) => {
    const newValue = e.target.value;
    console.log("[LaTeXInput] onChange (mock):", newValue);
    onChange?.(newValue);
  };

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label
          htmlFor={inputId}
          className="text-xs font-medium uppercase tracking-widest text-gray-500"
        >
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
