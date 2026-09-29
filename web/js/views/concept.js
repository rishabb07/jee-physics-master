/**
 * Concept Detail View
 */

import { renderMath } from "../math.js";

export async function renderConcept(container, conceptId) {
  let concepts = [];
  try {
    const res = await fetch("data/concepts.json");
    if (res.ok) concepts = await res.json();
  } catch (e) {
    console.warn("Could not load concepts:", e);
  }

  const concept = concepts.find((c) => c.concept_id === conceptId);

  if (!concept) {
    container.innerHTML = `
      <div class="content-container">
        <div class="card" style="text-align: center; padding: 3rem 1rem;">
          <h2>Concept Not Found</h2>
          <p style="color: var(--text-muted); margin: 1rem 0;">
            The requested concept identifier <code>${conceptId}</code> could not be found.
          </p>
          <a href="#/curriculum" class="btn btn-primary">Return to Syllabus</a>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <span class="badge badge-primary" style="margin-bottom: 0.5rem;">Concept Detail</span>
        <h1 class="hero-title">${concept.title}</h1>
        <p style="font-family: var(--font-mono); color: var(--text-subtle);">${concept.concept_id}</p>
      </div>

      <div class="card" style="border-left: 4px solid var(--primary);">
        <h3 class="card-title">Formal Physics Explanation</h3>
        <div style="font-size: 1.05rem; line-height: 1.7; margin: 1rem 0;">
          ${concept.statement}
        </div>

        ${
          concept.physical_intuition
            ? `<div class="concept-intuition" style="margin-top: 1rem;">
                <strong>Physical Intuition:</strong>
                <p style="margin-top: 4px;">${concept.physical_intuition}</p>
               </div>`
            : ""
        }

        ${
          concept.boundary_conditions && concept.boundary_conditions.length > 0
            ? `<div style="margin-top: 1.25rem;">
                <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-subtle);">Boundary Conditions & Validity Range:</h4>
                <ul style="padding-left: 1.25rem; margin-top: 0.5rem; color: var(--text-muted);">
                  ${concept.boundary_conditions.map((bc) => `<li>${bc}</li>`).join("")}
                </ul>
               </div>`
            : ""
        }

        ${
          concept.related_formula_ids && concept.related_formula_ids.length > 0
            ? `<div style="margin-top: 1.25rem;">
                <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-subtle);">Associated Formulas:</h4>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap;">
                  ${concept.related_formula_ids
                    .map((fid) => `<a href="#/formulas?id=${fid}" class="badge badge-subtle" style="font-family: var(--font-mono);">${fid}</a>`)
                    .join("")}
                </div>
               </div>`
            : ""
        }
      </div>

      <div style="margin-top: 1.5rem;">
        <a href="#/curriculum" class="btn btn-outline">&larr; Back to Syllabus</a>
      </div>
    </div>
  `;

  renderMath(container);
}
