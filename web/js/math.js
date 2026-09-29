/**
 * KaTeX Mathematical Typesetting Helper.
 * Invokes auto-render engine on DOM elements with balanced delimiters.
 */

export function renderMath(element) {
  if (!element) return;

  if (typeof renderMathInElement === "function") {
    try {
      renderMathInElement(element, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false },
        ],
        throwOnError: false,
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
      });
    } catch (e) {
      console.warn("KaTeX rendering notice:", e);
    }
  }
}
