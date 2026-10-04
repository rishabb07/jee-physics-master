/**
 * Chapter Detail & Reading View
 * Renders complete verified instructional content: concepts, formulas,
 * derivations, worked examples, misconceptions, and section practice questions.
 */

import { renderMath } from "../math.js";
import { state } from "../state.js";

export async function renderChapter(container, chapterId) {
  state.recordVisitedChapter(chapterId);

  let chapter = null;
  try {
    let res = await fetch(`data/chapter_${chapterId}.json`);
    if (!res.ok && chapterId === "dynamics") {
      res = await fetch("data/chapter_laws-of-motion.json");
    } else if (!res.ok && chapterId === "laws-of-motion") {
      res = await fetch("data/chapter_dynamics.json");
    } else if (!res.ok && (chapterId === "wep" || chapterId === "work-energy")) {
      res = await fetch("data/chapter_work-energy-power.json");
    } else if (!res.ok && chapterId === "work-energy-power") {
      res = await fetch("data/chapter_wep.json");
    }
    if (res.ok) {
      chapter = await res.json();
    }
  } catch (e) {
    console.warn(`Could not load chapter ${chapterId}:`, e);
  }

  if (!chapter) {
    container.innerHTML = `
      <div class="content-container">
        <div class="card" style="text-align: center; padding: 3rem 1rem;">
          <h2>Chapter Pending Production</h2>
          <p style="color: var(--text-muted); margin: 1rem 0;">
            Chapter <strong>${chapterId}</strong> is registered in the 30-chapter syllabus taxonomy,
            but is currently pending full atomic content generation and verification.
          </p>
          <a href="#/curriculum" class="btn btn-primary">Return to Syllabus</a>
        </div>
      </div>
    `;
    return;
  }

  // Learning objectives
  const objectivesHtml = chapter.learning_objectives && chapter.learning_objectives.length > 0
    ? `
      <div class="card" style="background: var(--bg-surface); border-left: 4px solid var(--primary);">
        <h4 style="font-size: 0.95rem; text-transform: uppercase; color: var(--text-subtle); margin-bottom: 0.5rem;">
          Learning Objectives
        </h4>
        <ul style="padding-left: 1.25rem; color: var(--text-main); line-height: 1.7;">
          ${chapter.learning_objectives.map((obj) => `<li>${obj}</li>`).join("")}
        </ul>
      </div>
    `
    : "";

  // Prerequisites
  const prereqsHtml = chapter.prerequisites && chapter.prerequisites.length > 0
    ? `
      <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
        <span style="font-weight: 600; font-size: 0.85rem; color: var(--text-subtle);">PREREQUISITES:</span>
        ${chapter.prerequisites.map((p) => `<span class="badge badge-subtle">${p}</span>`).join("")}
      </div>
    `
    : "";

  // Sections
  let sectionsHtml = "";
  if (chapter.sections && chapter.sections.length > 0) {
    sectionsHtml = chapter.sections
      .map((sec, sIdx) => {
        // Concepts
        const conceptsHtml = sec.concepts
          ? sec.concepts
              .map(
                (c) => `
            <div class="concept-card" id="${c.concept_id}">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span class="badge badge-primary">Concept</span>
                <span style="font-size: 0.75rem; color: var(--text-subtle); font-family: var(--font-mono);">${c.concept_id}</span>
              </div>
              <h4 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--text-main);">${c.title}</h4>
              <div style="font-size: 0.95rem; line-height: 1.7; margin-bottom: 0.75rem;">${c.statement}</div>
              ${
                c.physical_intuition
                  ? `<div class="concept-intuition">
                      <strong>Physical Intuition:</strong> ${c.physical_intuition}
                     </div>`
                  : ""
              }
              ${
                c.boundary_conditions && c.boundary_conditions.length > 0
                  ? `<div style="margin-top: 0.75rem; font-size: 0.88rem; color: var(--text-muted);">
                      <strong>Boundary Conditions:</strong>
                      <ul style="padding-left: 1.25rem; margin-top: 0.25rem;">
                        ${c.boundary_conditions.map((bc) => `<li>${bc}</li>`).join("")}
                      </ul>
                     </div>`
                  : ""
              }
            </div>
          `
              )
              .join("")
          : "";

        // Formulas
        const formulasHtml = sec.formulas
          ? sec.formulas
              .map(
                (f) => `
            <div class="formula-card" id="${f.formula_id}">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge badge-primary">Formula</span>
                <span style="font-size: 0.75rem; color: var(--text-subtle); font-family: var(--font-mono);">${f.formula_id}</span>
              </div>
              <h4 style="font-size: 1.1rem; font-weight: 700; margin-top: 0.3rem;">${f.title}</h4>
              
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
                  f.assumptions && f.assumptions.length > 0
                    ? `<div class="meta-box">
                        <h5>Assumptions</h5>
                        <ul style="padding-left: 1rem;">
                          ${f.assumptions.map((a) => `<li>${a}</li>`).join("")}
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
                      <strong>Common Pitfalls & Misuse:</strong>
                      <ul style="padding-left: 1.25rem; margin-top: 0.25rem;">
                        ${f.common_misuse.map((cm) => `<li>${cm}</li>`).join("")}
                      </ul>
                     </div>`
                  : ""
              }
            </div>
          `
              )
              .join("")
          : "";

        // Derivations (Expandable)
        const derivationsHtml = sec.derivations
          ? sec.derivations
              .map(
                (d) => `
            <div class="derivation-accordion" id="${d.derivation_id}">
              <div class="derivation-header" onclick="this.nextElementSibling.classList.toggle('hidden');">
                <div>
                  <span class="badge badge-subtle" style="margin-right: 6px;">Derivation</span>
                  <strong>${d.title}</strong>
                </div>
                <span style="font-size: 0.85rem; color: var(--primary);">Toggle Steps &darr;</span>
              </div>
              <div class="derivation-body hidden">
                <p style="margin-bottom: 0.75rem; font-weight: 600;">Target: $$${d.target_formula}$$</p>
                ${
                  d.assumptions && d.assumptions.length > 0
                    ? `<div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem;">
                        <strong>Starting Assumptions:</strong> ${d.assumptions.join("; ")}
                       </div>`
                    : ""
                }
                <div class="derivation-steps">
                  ${
                    d.steps && d.steps.length > 0
                      ? d.steps
                          .map(
                            (st, idx) => `
                        <div class="derivation-step">
                          <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 4px;">Step ${idx + 1}: ${st.step_title || st.title || ""}</div>
                          <div style="font-size: 0.9rem; margin-bottom: 4px;">${st.justification || st.description || ""}</div>
                          ${st.equation_latex ? `<div>$$${st.equation_latex}$$</div>` : ""}
                        </div>
                      `
                          )
                          .join("")
                      : `<p>Mathematical proof verified by independent solvers.</p>`
                  }
                </div>
              </div>
            </div>
          `
              )
              .join("")
          : "";

        // Worked Examples
        const examplesHtml = sec.worked_examples
          ? sec.worked_examples
              .map(
                (ex) => `
            <div class="example-card" id="${ex.example_id}">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="badge badge-active">Worked Example</span>
                <span style="font-size: 0.75rem; color: var(--text-subtle);">${ex.example_id}</span>
              </div>
              <div style="font-size: 1rem; font-weight: 500; margin-bottom: 1rem; line-height: 1.6;">
                ${ex.problem_statement}
              </div>
              ${
                ex.solution_strategy
                  ? `<div style="background: var(--bg-subtle); padding: 0.75rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-size: 0.9rem;">
                      <strong>Strategy:</strong> ${ex.solution_strategy}
                     </div>`
                  : ""
              }
              <div class="example-steps">
                ${
                  ex.solution_steps && ex.solution_steps.length > 0
                    ? ex.solution_steps
                        .map(
                          (st, idx) => `
                      <div class="example-step">
                        <div style="font-weight: 600; font-size: 0.9rem;">Step ${st.step_number || idx + 1}: ${st.concept_applied || ""}</div>
                        <div style="font-size: 0.9rem; margin: 4px 0;">${st.calculation_details || ""}</div>
                        ${st.equation_latex ? `<div>$$${st.equation_latex}$$</div>` : ""}
                      </div>
                    `
                        )
                        .join("")
                    : ""
                }
              </div>
              <div style="font-weight: 700; color: var(--primary); font-size: 1.05rem; margin-top: 0.75rem;">
                Final Answer: ${ex.final_answer}
              </div>
              ${
                ex.trap_alerts && ex.trap_alerts.length > 0
                  ? `<div class="trap-alert">
                      <strong>Cognitive Trap Alert:</strong> ${ex.trap_alerts.join("; ")}
                     </div>`
                  : ""
              }
            </div>
          `
              )
              .join("")
          : "";

        // Misconceptions
        const misconceptionsHtml = sec.misconceptions
          ? sec.misconceptions
              .map(
                (m) => `
            <div class="misconception-card" id="${m.misconception_id}">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="badge" style="background: var(--danger-light); color: var(--danger);">Common Misconception</span>
                <span style="font-size: 0.75rem; color: var(--text-subtle);">${m.category}</span>
              </div>
              <h4 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--danger);">
                "${m.statement}"
              </h4>
              <div class="misconception-comparison">
                <div class="erroneous-box">
                  <strong style="color: var(--danger);">Erroneous Thinking:</strong>
                  <p style="margin-top: 4px;">${m.erroneous_reasoning}</p>
                </div>
                <div class="correct-box">
                  <strong style="color: var(--success);">Correct Physics:</strong>
                  <p style="margin-top: 4px;">${m.correct_physics_explanation}</p>
                </div>
              </div>
              ${
                m.refutation_counterexample
                  ? `<div style="margin-top: 0.75rem; font-size: 0.88rem; color: var(--text-muted);">
                      <strong>Decisive Counterexample:</strong> ${m.refutation_counterexample}
                     </div>`
                  : ""
              }
            </div>
          `
              )
              .join("")
          : "";

        // Section Questions
        const questionsHtml = sec.questions && sec.questions.length > 0
          ? `
            <div style="margin-top: 2rem;">
              <h4 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 1rem; color: var(--text-main);">
                Section Practice Questions (${sec.questions.length})
              </h4>
              ${sec.questions
                .map(
                  (q) => `
                <div class="question-card" id="${q.question_id}">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                    <span class="badge badge-primary">${q.question_type}</span>
                    <span style="font-size: 0.75rem; color: var(--text-subtle);">${q.question_id}</span>
                  </div>
                  <div class="question-statement">${q.problem_statement}</div>
                  
                  ${
                    q.options
                      ? `<div class="options-grid">
                          ${Object.entries(q.options)
                            .map(
                              ([optKey, optVal]) => `
                            <button class="option-btn" data-qid="${q.question_id}" data-opt="${optKey}" onclick="window.selectOption('${q.question_id}', '${optKey}')">
                              <span class="option-label">${optKey}.</span>
                              <span>${optVal}</span>
                            </button>
                          `
                            )
                            .join("")}
                         </div>`
                      : `<div class="numerical-input-group">
                          <input type="text" id="input-${q.question_id}" class="numerical-input" placeholder="Enter numerical value">
                          <button class="btn btn-primary" onclick="window.submitNumerical('${q.question_id}', '${q.correct_answer}')">Check</button>
                         </div>`
                  }

                  ${
                    q.options
                      ? `<div class="question-actions">
                          <button class="btn btn-primary" onclick="window.submitMCQ('${q.question_id}', '${q.correct_answer}')">Submit Answer</button>
                          <button class="btn btn-outline" onclick="document.getElementById('sol-${q.question_id}').classList.toggle('hidden')">Show Solution</button>
                         </div>`
                      : `<button class="btn btn-outline" onclick="document.getElementById('sol-${q.question_id}').classList.toggle('hidden')">Show Solution</button>`
                  }

                  <div id="feedback-${q.question_id}" class="feedback-banner hidden"></div>

                  <div id="sol-${q.question_id}" class="solution-box hidden">
                    <h5 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.5rem;">Verified Physical Derivation:</h5>
                    <div style="font-size: 0.92rem; line-height: 1.6;">${q.solution_explanation}</div>
                  </div>
                </div>
              `
                )
                .join("")}
            </div>
          `
          : "";

        return `
          <div class="section-block">
            <h3 class="section-title">${sec.section_order}. ${sec.title}</h3>
            ${sec.pedagogical_purpose ? `<p class="section-purpose">${sec.pedagogical_purpose}</p>` : ""}
            
            ${conceptsHtml}
            ${formulasHtml}
            ${derivationsHtml}
            ${examplesHtml}
            ${misconceptionsHtml}
            ${questionsHtml}
          </div>
        `;
      })
      .join("");
  }

  // Revision checklist
  const revisionHtml = chapter.revision_checklist && chapter.revision_checklist.length > 0
    ? `
      <div class="card" style="margin-top: 2rem;">
        <h3 class="card-title">Chapter Revision Checklist</h3>
        <ul style="padding-left: 1.25rem; color: var(--text-muted); line-height: 1.8;">
          ${chapter.revision_checklist.map((item) => `<li>${item}</li>`).join("")}
        </ul>
      </div>
    `
    : "";

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 0.5rem;">
          <span class="badge badge-primary">${chapter.branch}</span>
          <span class="badge badge-active">Chapter ${chapter.order}</span>
          ${chapter.ladder_ids && chapter.ladder_ids.length > 0 ? `<a href="#/ladders?ch=${chapter.chapter_id}" class="badge badge-active" style="text-decoration:none;">View Question Ladder &rarr;</a>` : ""}
        </div>
        <h1 class="hero-title">${chapter.title}</h1>
      </div>

      ${prereqsHtml}
      ${objectivesHtml}
      ${sectionsHtml}
      ${revisionHtml}
    </div>
  `;

  // Attach global handlers for question interactions
  window.selectedMCQ = window.selectedMCQ || {};

  window.selectOption = (qid, optKey) => {
    window.selectedMCQ[qid] = optKey;
    document.querySelectorAll(`.option-btn[data-qid="${qid}"]`).forEach((b) => {
      if (b.getAttribute("data-opt") === optKey) {
        b.classList.add("selected");
      } else {
        b.classList.remove("selected");
      }
    });
  };

  window.submitMCQ = (qid, correctAns) => {
    const selected = window.selectedMCQ[qid];
    const fbEl = document.getElementById(`feedback-${qid}`);
    if (!fbEl) return;

    if (!selected) {
      fbEl.className = "feedback-banner incorrect";
      fbEl.textContent = "Please select an option first.";
      fbEl.classList.remove("hidden");
      return;
    }

    const isCorrect = String(selected).trim().toUpperCase() === String(correctAns).trim().toUpperCase();
    state.recordAttempt(qid, selected, isCorrect);

    fbEl.className = `feedback-banner ${isCorrect ? "correct" : "incorrect"}`;
    fbEl.textContent = isCorrect
      ? "Correct! Verified solution confirmed."
      : `Incorrect. You chose ${selected}. Correct answer is ${correctAns}.`;
    fbEl.classList.remove("hidden");

    // Reveal solution automatically on attempt
    const solEl = document.getElementById(`sol-${qid}`);
    if (solEl) solEl.classList.remove("hidden");

    // Highlight buttons
    document.querySelectorAll(`.option-btn[data-qid="${qid}"]`).forEach((b) => {
      const opt = b.getAttribute("data-opt");
      if (opt === correctAns) {
        b.classList.add("correct");
      } else if (opt === selected && !isCorrect) {
        b.classList.add("incorrect");
      }
    });
  };

  window.submitNumerical = (qid, correctAns) => {
    const inputEl = document.getElementById(`input-${qid}`);
    const fbEl = document.getElementById(`feedback-${qid}`);
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

    const solEl = document.getElementById(`sol-${qid}`);
    if (solEl) solEl.classList.remove("hidden");
  };

  renderMath(container);
}
