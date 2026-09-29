/**
 * Interactive Question Practice Engine View
 * Real-time quiz runner with immediate feedback, step-by-step verified proofs,
 * distractor rationale analysis, and student performance tracking.
 */

import { renderMath } from "../math.js";
import { state } from "../state.js";

export async function renderPractice(container, params) {
  let questions = [];
  try {
    const res = await fetch("data/questions.json");
    if (res.ok) questions = await res.json();
  } catch (e) {
    console.warn("Could not load questions:", e);
  }

  const focusQid = params ? params.get("q") : null;
  let activeChapter = "all";
  let activeDifficulty = "all";
  let activeType = "all";

  function getFilteredQuestions() {
    return questions.filter((q) => {
      const matchCh = activeChapter === "all" || q.chapter_id.includes(activeChapter);
      const diff = (q.difficulty && (q.difficulty.difficulty_band || q.difficulty.derived_difficulty_band)) || "L2";
      const matchDiff = activeDifficulty === "all" || diff === activeDifficulty;
      const matchType = activeType === "all" || q.question_type.toLowerCase().includes(activeType.toLowerCase());
      return matchCh && matchDiff && matchType;
    });
  }

  function renderQuestionCard(q, idx, total) {
    const attempt = state.getAttempt(q.question_id);
    const isBookmarked = state.isBookmarked(q.question_id);
    const diff = (q.difficulty && (q.difficulty.difficulty_band || q.difficulty.derived_difficulty_band)) || "L2";
    const origin = q.provenance && q.provenance.origin === "CANONICAL_SOURCE" ? "CANONICAL SOURCE" : "GENERATED QB";

    let optionsHtml = "";
    if (q.options) {
      optionsHtml = `
        <div class="options-grid" id="opts-${q.question_id}">
          ${Object.entries(q.options)
            .map(([optKey, optVal]) => {
              let optClass = "option-btn";
              if (attempt) {
                if (optKey === q.correct_answer) {
                  optClass += " correct";
                } else if (optKey === attempt.answer && !attempt.isCorrect) {
                  optClass += " incorrect";
                }
              }
              return `
              <button class="${optClass}" data-qid="${q.question_id}" data-opt="${optKey}" onclick="window.selectPracticeOption('${q.question_id}', '${optKey}')">
                <span class="option-label">${optKey}.</span>
                <span>${optVal}</span>
              </button>
            `;
            })
            .join("")}
        </div>
      `;
    } else {
      optionsHtml = `
        <div class="numerical-input-group">
          <input type="text" id="practice-input-${q.question_id}" class="numerical-input" placeholder="Value (e.g. 160)" value="${attempt ? attempt.answer : ""}">
          <button class="btn btn-primary" onclick="window.submitPracticeNumerical('${q.question_id}', '${q.correct_answer}')">Check</button>
        </div>
      `;
    }

    // Distractor rationales
    let distractorHtml = "";
    if (q.distractor_rationales && Object.keys(q.distractor_rationales).length > 0) {
      distractorHtml = `
        <div class="distractor-grid">
          <strong style="font-size: 0.85rem; color: var(--danger);">Cognitive Trap & Distractor Audit:</strong>
          ${Object.entries(q.distractor_rationales)
            .map(
              ([k, rationale]) => `
            <div class="distractor-card">
              <strong>Option ${k}:</strong> ${rationale}
            </div>
          `
            )
            .join("")}
        </div>
      `;
    }

    const isFocused = q.question_id === focusQid;

    return `
      <div class="question-card" id="${q.question_id}" style="${isFocused ? "border: 2px solid var(--primary); box-shadow: var(--shadow-md);" : ""}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <span class="badge badge-primary">${q.question_type}</span>
            <span class="badge badge-active">${diff}</span>
            <span class="badge badge-subtle">${origin}</span>
            <span style="font-size: 0.8rem; color: var(--text-subtle);">${q.chapter_id}</span>
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <button class="btn btn-outline" style="padding: 2px 8px; font-size: 0.75rem;" onclick="window.toggleQuestionBookmark('${q.question_id}', this)">
              ${isBookmarked ? "&#9733; Bookmarked" : "&#9734; Bookmark"}
            </button>
            <span style="font-size: 0.75rem; color: var(--text-subtle); font-family: var(--font-mono);">${q.question_id}</span>
          </div>
        </div>

        <div class="question-statement">${q.problem_statement}</div>

        ${optionsHtml}

        <div class="question-actions">
          ${q.options ? `<button class="btn btn-primary" onclick="window.submitPracticeMCQ('${q.question_id}', '${q.correct_answer}')">Submit Answer</button>` : ""}
          <button class="btn btn-outline" onclick="document.getElementById('sol-box-${q.question_id}').classList.toggle('hidden')">
            Toggle Verified Proof
          </button>
        </div>

        <div id="practice-feedback-${q.question_id}" class="feedback-banner ${attempt ? (attempt.isCorrect ? "correct" : "incorrect") : "hidden"}">
          ${
            attempt
              ? attempt.isCorrect
                ? "Correct! Independently verified answer."
                : `Incorrect. Your answer: ${attempt.answer}. Correct answer: ${q.correct_answer}.`
              : ""
          }
        </div>

        <div id="sol-box-${q.question_id}" class="solution-box ${attempt ? "" : "hidden"}">
          <h5 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--text-main);">
            Verified Physical Derivation & First-Principles Solution:
          </h5>
          <div style="font-size: 0.92rem; line-height: 1.7; margin-bottom: 0.75rem;">
            ${q.solution_explanation}
          </div>
          ${distractorHtml}
        </div>
      </div>
    `;
  }

  function renderList() {
    const filtered = getFilteredQuestions();
    const listEl = document.getElementById("practice-questions-list");
    if (!listEl) return;

    if (filtered.length === 0) {
      listEl.innerHTML = `
        <div class="card" style="text-align: center; padding: 3rem 1rem;">
          <p style="color: var(--text-muted);">No practice questions matched your current filter.</p>
        </div>
      `;
      return;
    }

    listEl.innerHTML = filtered.map((q, idx) => renderQuestionCard(q, idx, filtered.length)).join("");
    renderMath(listEl);

    if (focusQid) {
      const el = document.getElementById(focusQid);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <h1 class="hero-title">Interactive Physics Question Practice</h1>
        <p class="hero-subtitle">
          Practice certified questions independently verified by dual blind solvers.
          Get instant feedback, analyze distractor rationales, and review rigorous mathematical derivations.
        </p>
      </div>

      <!-- Filter Bar -->
      <div class="card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center; justify-content: space-between;">
          <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
            <span style="font-weight: 600; font-size: 0.85rem; color: var(--text-subtle);">TOPIC:</span>
            <button class="btn btn-primary q-ch-btn" data-ch="all">All</button>
            <button class="btn btn-outline q-ch-btn" data-ch="rot">Rotational</button>
            <button class="btn btn-outline q-ch-btn" data-ch="td">Thermo</button>
            <button class="btn btn-outline q-ch-btn" data-ch="curr">Current</button>
            <button class="btn btn-outline q-ch-btn" data-ch="opt">Optics</button>
          </div>

          <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
            <span style="font-weight: 600; font-size: 0.85rem; color: var(--text-subtle);">DIFFICULTY:</span>
            <button class="btn btn-primary q-diff-btn" data-diff="all">All</button>
            <button class="btn btn-outline q-diff-btn" data-diff="L1">L1</button>
            <button class="btn btn-outline q-diff-btn" data-diff="L2">L2</button>
            <button class="btn btn-outline q-diff-btn" data-diff="L3">L3</button>
          </div>
        </div>
      </div>

      <!-- Questions Stream -->
      <div id="practice-questions-list"></div>
    </div>
  `;

  // Filter event bindings
  container.querySelectorAll(".q-ch-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      container.querySelectorAll(".q-ch-btn").forEach((b) => (b.className = "btn btn-outline q-ch-btn"));
      btn.className = "btn btn-primary q-ch-btn";
      activeChapter = btn.getAttribute("data-ch");
      renderList();
    });
  });

  container.querySelectorAll(".q-diff-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      container.querySelectorAll(".q-diff-btn").forEach((b) => (b.className = "btn btn-outline q-diff-btn"));
      btn.className = "btn btn-primary q-diff-btn";
      activeDifficulty = btn.getAttribute("data-diff");
      renderList();
    });
  });

  // Global window functions for practice actions
  window.practiceSelected = window.practiceSelected || {};

  window.selectPracticeOption = (qid, optKey) => {
    window.practiceSelected[qid] = optKey;
    document.querySelectorAll(`#opts-${qid} .option-btn`).forEach((b) => {
      if (b.getAttribute("data-opt") === optKey) {
        b.classList.add("selected");
      } else {
        b.classList.remove("selected");
      }
    });
  };

  window.submitPracticeMCQ = (qid, correctAns) => {
    const selected = window.practiceSelected[qid];
    const fbEl = document.getElementById(`practice-feedback-${qid}`);
    if (!fbEl) return;

    if (!selected) {
      fbEl.className = "feedback-banner incorrect";
      fbEl.textContent = "Please select an option before submitting.";
      fbEl.classList.remove("hidden");
      return;
    }

    const isCorrect = String(selected).trim().toUpperCase() === String(correctAns).trim().toUpperCase();
    state.recordAttempt(qid, selected, isCorrect);

    fbEl.className = `feedback-banner ${isCorrect ? "correct" : "incorrect"}`;
    fbEl.textContent = isCorrect
      ? "Correct! Physical derivation verified."
      : `Incorrect. You chose ${selected}. Correct answer is ${correctAns}.`;
    fbEl.classList.remove("hidden");

    const solEl = document.getElementById(`sol-box-${qid}`);
    if (solEl) solEl.classList.remove("hidden");

    document.querySelectorAll(`#opts-${qid} .option-btn`).forEach((b) => {
      const opt = b.getAttribute("data-opt");
      if (opt === correctAns) {
        b.classList.add("correct");
      } else if (opt === selected && !isCorrect) {
        b.classList.add("incorrect");
      }
    });
  };

  window.submitPracticeNumerical = (qid, correctAns) => {
    const inputEl = document.getElementById(`practice-input-${qid}`);
    const fbEl = document.getElementById(`practice-feedback-${qid}`);
    if (!inputEl || !fbEl) return;

    const val = parseFloat(inputEl.value);
    const target = parseFloat(correctAns);

    if (isNaN(val)) {
      fbEl.className = "feedback-banner incorrect";
      fbEl.textContent = "Please enter a valid numerical number.";
      fbEl.classList.remove("hidden");
      return;
    }

    const isCorrect = Math.abs(val - target) <= 0.05 * Math.abs(target || 1.0);
    state.recordAttempt(qid, val, isCorrect);

    fbEl.className = `feedback-banner ${isCorrect ? "correct" : "incorrect"}`;
    fbEl.textContent = isCorrect
      ? `Correct! Target value: ${correctAns}`
      : `Incorrect. Your answer: ${val}. Correct value: ${correctAns}`;
    fbEl.classList.remove("hidden");

    const solEl = document.getElementById(`sol-box-${qid}`);
    if (solEl) solEl.classList.remove("hidden");
  };

  window.toggleQuestionBookmark = (qid, btn) => {
    const isNow = state.toggleBookmark(qid);
    btn.innerHTML = isNow ? "&#9733; Bookmarked" : "&#9734; Bookmark";
  };

  renderList();
}
