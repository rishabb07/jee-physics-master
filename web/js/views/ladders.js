/**
 * Question Ladder & Scaffolding View
 * Explores pedagogical question progressions with explicit physical deltas.
 */

import { renderMath } from "../math.js";

export async function renderLadders(container, params) {
  let ladders = [];
  try {
    const res = await fetch("data/ladders.json");
    if (res.ok) ladders = await res.json();
  } catch (e) {
    console.warn("Could not load ladders:", e);
  }

  const chFilter = params ? params.get("ch") : null;

  const filteredLadders = chFilter
    ? ladders.filter((l) => l.chapter_id === chFilter)
    : ladders;

  let ladderCardsHtml = "";

  if (filteredLadders.length === 0) {
    ladderCardsHtml = `
      <div class="card" style="text-align: center; padding: 2rem;">
        <p style="color: var(--text-muted);">No question ladders registered for this topic.</p>
      </div>
    `;
  } else {
    ladderCardsHtml = filteredLadders
      .map(
        (lad) => `
      <div class="card" style="margin-bottom: 2rem; border-top: 4px solid var(--primary);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
          <div>
            <span class="badge badge-primary">${lad.chapter_id}</span>
            <span class="badge badge-subtle">${lad.topic_id}</span>
            <h2 style="font-size: 1.4rem; font-weight: 700; margin-top: 0.3rem; color: var(--text-main);">${lad.title}</h2>
          </div>
          <span style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-subtle);">${lad.ladder_id}</span>
        </div>

        <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
          <strong>Target Physical System:</strong> ${lad.physical_system}
        </p>

        <h4 style="font-size: 1rem; font-weight: 700; margin-bottom: 1rem; color: var(--text-main);">
          Progressive Problem Rungs (${lad.rungs.length})
        </h4>

        <div class="ladder-stream">
          ${lad.rungs
            .map(
              (r) => `
            <div class="ladder-rung">
              <div class="rung-badge">${r.rung_number}</div>
              <div class="rung-content">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <h4 style="font-size: 1.1rem; font-weight: 700;">${r.rung_name}</h4>
                  <span class="badge badge-subtle">Reasoning Depth: ${r.reasoning_depth}</span>
                </div>
                
                <p style="margin-bottom: 0.5rem; font-size: 0.95rem;">
                  <strong>Physical Delta:</strong> ${r.physical_delta}
                </p>

                <div style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.75rem;">
                  <strong>Concepts Involved:</strong> ${r.concepts_involved ? r.concepts_involved.join(", ") : "N/A"} | 
                  <strong>Complexity:</strong> ${r.mathematical_complexity}
                </div>

                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <a href="#/practice?q=${r.question_id}" class="btn btn-primary" style="font-size: 0.82rem; padding: 4px 10px;">
                    Solve Rung Problem (${r.question_id}) &rarr;
                  </a>
                </div>
              </div>
            </div>
          `
            )
            .join("")}
        </div>
      </div>
    `
      )
      .join("");
  }

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <h1 class="hero-title">Cognitive Question Ladders</h1>
        <p class="hero-subtitle">
          Pedagogically scaffolded problem sequences designed to train physical intuition
          from direct single-step application to multi-step coupled systems.
        </p>
      </div>

      ${ladderCardsHtml}
    </div>
  `;

  renderMath(container);
}
