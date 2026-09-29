/**
 * Home / Dashboard View
 */

import { renderMath } from "../math.js";
import { state } from "../state.js";

export async function renderHome(container) {
  let manifest = null;
  try {
    const res = await fetch("data/manifest.json");
    if (res.ok) manifest = await res.json();
  } catch (e) {
    console.warn("Could not load manifest:", e);
  }

  const counts = manifest ? manifest.counts : {
    total_chapters: 30,
    pilot_active_chapters: 4,
    concepts: 12,
    formulas: 13,
    derivations: 13,
    worked_examples: 4,
    misconceptions: 8,
    verified_questions: 17,
    question_ladders: 1,
  };

  const stats = state.getStats();

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <h1 class="hero-title">JEE Physics Master Knowledge System</h1>
        <p class="hero-subtitle">
          An interactive, auto-updating digital learning platform for JEE Advanced and Main Physics,
          directly projected from the canonical verified physics knowledge base.
        </p>
      </div>

      <!-- Quick Stats Row -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">${counts.total_chapters}</div>
          <div class="stat-label">Syllabus Chapters</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${counts.pilot_active_chapters}</div>
          <div class="stat-label">Active Pilot Chapters</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${counts.concepts} / ${counts.formulas}</div>
          <div class="stat-label">Verified Concepts / Formulas</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${counts.verified_questions}</div>
          <div class="stat-label">Verified Practice Questions</div>
        </div>
      </div>

      <!-- Student Progress Widget -->
      <div class="card" style="background: linear-gradient(135deg, var(--bg-surface) 0%, var(--bg-subtle) 100%);">
        <div class="card-title">
          <span>Your Learning Session</span>
        </div>
        <p style="margin-bottom: 1rem; color: var(--text-muted);">
          Track your practice performance, bookmarked concepts, and chapter completion in real-time.
        </p>
        <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center;">
          <div><strong>Questions Attempted:</strong> ${stats.totalAttempted}</div>
          <div><strong>Accuracy:</strong> ${stats.accuracy}%</div>
          <div><strong>Correct:</strong> <span style="color: var(--success);">${stats.correctCount}</span></div>
          <div><strong>Bookmarked:</strong> ${stats.bookmarkedCount}</div>
          <a href="#/practice" class="btn btn-primary" style="margin-left: auto;">Jump to Practice Quiz</a>
        </div>
      </div>

      <!-- Active Pilot Chapters Showcase -->
      <div style="margin-top: 2rem;">
        <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem;">
          Production Pilot Chapters
        </h2>
        <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
          The Phase 10 pilot encompasses four complete, rigorously verified chapters across four primary subject branches.
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem;">
          <a href="#/chapter/rotational-motion" class="card" style="display: block; transition: transform 0.15s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
              <span class="badge badge-primary">Mechanics</span>
              <span class="badge badge-active">Pilot implementation: live</span>
            </div>
            <h3 style="font-size: 1.15rem; margin-bottom: 0.4rem; color: var(--text-main);">Rotational Motion</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Moments of inertia, torque dynamics, angular momentum conservation, and rolling constraints.
            </p>
          </a>

          <a href="#/chapter/thermodynamics" class="card" style="display: block; transition: transform 0.15s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
              <span class="badge badge-primary">Thermal Physics</span>
              <span class="badge badge-active">Pilot implementation: live</span>
            </div>
            <h3 style="font-size: 1.15rem; margin-bottom: 0.4rem; color: var(--text-main);">Thermodynamics</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              First law, adiabatic & polytropic processes, photon radiation gas, and state cycles.
            </p>
          </a>

          <a href="#/chapter/current-electricity" class="card" style="display: block; transition: transform 0.15s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
              <span class="badge badge-primary">Electrodynamics</span>
              <span class="badge badge-active">Pilot implementation: live</span>
            </div>
            <h3 style="font-size: 1.15rem; margin-bottom: 0.4rem; color: var(--text-main);">Current Electricity</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Microscopic conduction, drift velocity, wire drawing resistance scaling, and galvanometer shunts.
            </p>
          </a>

          <a href="#/chapter/ray-optics" class="card" style="display: block; transition: transform 0.15s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
              <span class="badge badge-primary">Optics</span>
              <span class="badge badge-active">Pilot implementation: live</span>
            </div>
            <h3 style="font-size: 1.15rem; margin-bottom: 0.4rem; color: var(--text-main);">Ray Optics</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Snell's law from Fermat's principle, total internal reflection, and prism ray geometry.
            </p>
          </a>
        </div>
      </div>

      <!-- System Architecture & Principles -->
      <div class="card" style="margin-top: 2rem;">
        <h3 class="card-title">Core System Invariants</h3>
        <ul style="padding-left: 1.5rem; color: var(--text-muted); line-height: 1.8;">
          <li><strong>Canonical Knowledge Base as Source of Truth:</strong> Canonical physics atoms (<code style="color: var(--primary);">kb/atoms/</code>) remain strictly immutable.</li>
          <li><strong>Zero Unverified Content:</strong> Every formula, derivation, example, and question has passed rigorous dual-solver independent verification.</li>
          <li><strong>Deterministic Pipeline:</strong> The entire web application is compiled deterministically from underlying JSON datasets.</li>
        </ul>
      </div>

      <!-- System & Build Information -->
      <div class="card" style="margin-top: 1.5rem; background: var(--bg-subtle);">
        <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-subtle); margin-bottom: 0.5rem; text-transform: uppercase;">
          System & Build Information
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; font-size: 0.85rem; color: var(--text-muted);">
          <div><strong>App Version:</strong> <code>${manifest ? manifest.version : "v1.0.0-pilot"}</code></div>
          <div><strong>Scope:</strong> <code>Pilot implementation: live (4/30 ch)</code></div>
          <div><strong>Git Commit:</strong> <code>${manifest ? manifest.git_commit : "local-uncommitted"}</code></div>
          <div><strong>Math Assets:</strong> <code>Offline KaTeX 0.16.9 (20 woff2 fonts)</code></div>
          <div style="grid-column: 1 / -1;"><strong>Build ID:</strong> <code>${manifest ? manifest.build_id : "N/A"}</code> | <strong>Timestamp:</strong> <code>${manifest ? manifest.build_timestamp : "N/A"}</code></div>
        </div>
      </div>
    </div>
  `;

  renderMath(container);
}
