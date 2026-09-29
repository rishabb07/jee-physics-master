/**
 * Student Learning Analytics & Progress Dashboard View
 */

import { state } from "../state.js";

export function renderProgress(container) {
  const stats = state.getStats();
  const attempts = Object.entries(state.state.attempts || {});
  const bookmarks = state.state.bookmarks || [];
  const visitedChapters = state.state.visitedChapters || [];

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <h1 class="hero-title">Student Learning Analytics</h1>
        <p class="hero-subtitle">
          Continuous tracking of questions attempted, accuracy rate, visited chapters, and bookmarked questions.
          All state is safely stored in your browser's persistent storage.
        </p>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">${stats.totalAttempted}</div>
          <div class="stat-label">Total Questions Solved</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: ${stats.accuracy >= 70 ? "var(--success)" : "var(--primary)"};">${stats.accuracy}%</div>
          <div class="stat-label">Overall Accuracy</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: var(--success);">${stats.correctCount}</div>
          <div class="stat-label">Correct Answers</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: var(--danger);">${stats.incorrectCount}</div>
          <div class="stat-label">Errors Analyzed</div>
        </div>
      </div>

      <!-- Visited Chapters -->
      <div class="card">
        <h3 class="card-title">Visited Chapters (${visitedChapters.length})</h3>
        ${
          visitedChapters.length > 0
            ? `<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
                ${visitedChapters
                  .map((ch) => `<a href="#/chapter/${ch}" class="badge badge-primary" style="padding: 6px 12px; font-size: 0.85rem;">${ch}</a>`)
                  .join("")}
               </div>`
            : `<p style="color: var(--text-muted);">No chapters visited yet during this session.</p>`
        }
      </div>

      <!-- Bookmarked Questions -->
      <div class="card">
        <h3 class="card-title">Bookmarked Questions (${bookmarks.length})</h3>
        ${
          bookmarks.length > 0
            ? `<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
                ${bookmarks
                  .map((qid) => `<a href="#/practice?q=${qid}" class="badge badge-active" style="padding: 6px 12px; font-size: 0.85rem;">&#9733; ${qid}</a>`)
                  .join("")}
               </div>`
            : `<p style="color: var(--text-muted);">No questions bookmarked yet. Click the "Bookmark" button during practice to save challenging problems.</p>`
        }
      </div>

      <!-- Recent Practice History -->
      <div class="card">
        <h3 class="card-title">Recent Question Attempts</h3>
        ${
          attempts.length > 0
            ? `<div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
                  <thead>
                    <tr style="border-bottom: 2px solid var(--border-color); color: var(--text-subtle);">
                      <th style="padding: 8px;">Question ID</th>
                      <th style="padding: 8px;">Your Answer</th>
                      <th style="padding: 8px;">Verdict</th>
                      <th style="padding: 8px;">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${attempts
                      .map(
                        ([qid, a]) => `
                      <tr style="border-bottom: 1px solid var(--border-light);">
                        <td style="padding: 8px; font-family: var(--font-mono);">${qid}</td>
                        <td style="padding: 8px;"><strong>${a.answer}</strong></td>
                        <td style="padding: 8px;">
                          <span class="badge ${a.isCorrect ? "badge-active" : "badge"}" style="${!a.isCorrect ? "background: var(--danger-light); color: var(--danger);" : ""}">
                            ${a.isCorrect ? "CORRECT" : "INCORRECT"}
                          </span>
                        </td>
                        <td style="padding: 8px;">
                          <a href="#/practice?q=${qid}" class="btn btn-outline" style="font-size: 0.75rem; padding: 2px 8px;">Re-try</a>
                        </td>
                      </tr>
                    `
                      )
                      .join("")}
                  </tbody>
                </table>
               </div>`
            : `<p style="color: var(--text-muted);">No practice questions attempted yet.</p>`
        }
      </div>

      <!-- Reset Data -->
      <div style="margin-top: 2rem; display: flex; justify-content: flex-end;">
        <button class="btn btn-outline" style="color: var(--danger); border-color: var(--danger);" onclick="if(confirm('Are you sure you want to reset all local progress statistics?')) { window.resetProgress(); }">
          Reset Learning Analytics
        </button>
      </div>
    </div>
  `;

  window.resetProgress = () => {
    state.clearAll();
    renderProgress(container);
  };
}
