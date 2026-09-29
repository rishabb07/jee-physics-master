/**
 * Interactive Formula Sheet & Reference Handbook View
 */

import { renderMath } from "../math.js";

export async function renderFormulas(container, params) {
  let formulas = [];
  try {
    const res = await fetch("data/formulas.json");
    if (res.ok) formulas = await res.json();
  } catch (e) {
    console.warn("Could not load formulas:", e);
  }

  const highlightId = params ? params.get("id") : null;

  function renderFormulaCards(filterChapter = "all", searchQuery = "") {
    const filtered = formulas.filter((f) => {
      const matchCh = filterChapter === "all" || f.formula_id.includes(filterChapter);
      const q = searchQuery.toLowerCase();
      const matchSearch =
        !q ||
        f.title.toLowerCase().includes(q) ||
        f.equation_latex.toLowerCase().includes(q) ||
        f.formula_id.toLowerCase().includes(q);
      return matchCh && matchSearch;
    });

    if (filtered.length === 0) {
      return `
        <div class="card" style="text-align: center; padding: 2rem;">
          <p style="color: var(--text-muted);">No formulas matching your filters.</p>
        </div>
      `;
    }

    return filtered
      .map((f) => {
        const isHighlighted = f.formula_id === highlightId;
        return `
        <div class="formula-card" id="${f.formula_id}" style="${isHighlighted ? "border: 2px solid var(--primary); box-shadow: var(--shadow-md);" : ""}">
          <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
              <span class="badge badge-primary">Formula</span>
              <span style="font-size: 0.75rem; color: var(--text-subtle); font-family: var(--font-mono); margin-left: 6px;">${f.formula_id}</span>
            </div>
            <button class="btn btn-outline" style="font-size: 0.75rem; padding: 2px 8px;" onclick="navigator.clipboard.writeText('${f.equation_latex.replace(/\\/g, "\\\\")}'); this.textContent='Copied!'; setTimeout(()=>this.textContent='Copy LaTeX', 1500);">
              Copy LaTeX
            </button>
          </div>
          <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0.4rem 0;">${f.title}</h3>
          
          <div class="equation-box">
            $$${f.equation_latex}$$
          </div>

          <div class="formula-meta-grid">
            ${
              Object.keys(f.variables || {}).length > 0
                ? `<div class="meta-box">
                    <h5>Variables</h5>
                    <ul style="list-style: none; padding-left: 0;">
                      ${Object.entries(f.variables)
                        .map(([k, v]) => `<li><code>$${k}$</code>: ${v}</li>`)
                        .join("")}
                    </ul>
                   </div>`
                : ""
            }
            ${
              Object.keys(f.units || {}).length > 0
                ? `<div class="meta-box">
                    <h5>SI Units & Dimensions</h5>
                    <ul style="list-style: none; padding-left: 0;">
                      ${Object.entries(f.units)
                        .map(([k, u]) => `<li><code>$${k}$</code>: ${u} ${f.dimensions && f.dimensions[k] ? `(${f.dimensions[k]})` : ""}</li>`)
                        .join("")}
                    </ul>
                   </div>`
                : ""
            }
            ${
              f.validity_conditions && f.validity_conditions.length > 0
                ? `<div class="meta-box">
                    <h5>Validity Conditions</h5>
                    <ul style="padding-left: 1rem;">
                      ${f.validity_conditions.map((vc) => `<li>${vc}</li>`).join("")}
                    </ul>
                   </div>`
                : ""
            }
          </div>

          ${
            f.common_misuse && f.common_misuse.length > 0
              ? `<div class="trap-alert" style="margin-top: 0.75rem;">
                  <strong>Common Traps & Misuse:</strong>
                  <ul style="padding-left: 1.25rem; margin-top: 0.25rem;">
                    ${f.common_misuse.map((cm) => `<li>${cm}</li>`).join("")}
                  </ul>
                 </div>`
              : ""
          }
        </div>
      `;
      })
      .join("");
  }

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <h1 class="hero-title">Physics Formula Handbook & Cheat Sheet</h1>
        <p class="hero-subtitle">
          Comprehensive, verified mathematical relations, SI units, dimensional formulas,
          validity boundaries, and cognitive trap warnings.
        </p>
      </div>

      <!-- Controls Row -->
      <div class="card" style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center; justify-content: space-between;">
        <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
          <span style="font-weight: 600; font-size: 0.85rem; color: var(--text-subtle);">FILTER CHAPTER:</span>
          <button class="btn btn-primary formula-filter-btn" data-ch="all">All (${formulas.length})</button>
          <button class="btn btn-outline formula-filter-btn" data-ch="rot">Rotational Motion</button>
          <button class="btn btn-outline formula-filter-btn" data-ch="td">Thermodynamics</button>
          <button class="btn btn-outline formula-filter-btn" data-ch="curr">Current Electricity</button>
          <button class="btn btn-outline formula-filter-btn" data-ch="opt">Ray Optics</button>
        </div>
        <div>
          <input type="text" id="formula-search" placeholder="Filter by variable or formula name..." style="padding: 6px 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); background: var(--bg-subtle); color: var(--text-main); font-size: 0.88rem; width: 260px;">
        </div>
      </div>

      <!-- Cards Grid -->
      <div id="formula-grid">
        ${renderFormulaCards("all", "")}
      </div>
    </div>
  `;

  renderMath(container);

  // Setup filtering events
  let currentCh = "all";
  let currentQ = "";

  const gridEl = document.getElementById("formula-grid");
  const searchInput = document.getElementById("formula-search");

  function update() {
    gridEl.innerHTML = renderFormulaCards(currentCh, currentQ);
    renderMath(gridEl);
  }

  container.querySelectorAll(".formula-filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      container.querySelectorAll(".formula-filter-btn").forEach((b) => {
        b.className = "btn btn-outline formula-filter-btn";
      });
      btn.className = "btn btn-primary formula-filter-btn";
      currentCh = btn.getAttribute("data-ch");
      update();
    });
  });

  searchInput.addEventListener("input", (e) => {
    currentQ = e.target.value;
    update();
  });

  if (highlightId) {
    const el = document.getElementById(highlightId);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}
