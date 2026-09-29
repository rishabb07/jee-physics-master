/**
 * Complete 30-Chapter Syllabus & Curriculum Browser View
 */

import { renderMath } from "../math.js";

export async function renderCurriculum(container) {
  let taxonomy = null;
  try {
    const res = await fetch("data/taxonomy.json");
    if (res.ok) taxonomy = await res.json();
  } catch (e) {
    console.warn("Could not load taxonomy:", e);
  }

  if (!taxonomy || !taxonomy.chapters) {
    container.innerHTML = `<div class="content-container"><p>Unable to load curriculum hierarchy.</p></div>`;
    return;
  }

  // Group chapters by branch
  const branchMap = {};
  taxonomy.branches.forEach((b) => {
    branchMap[b] = [];
  });

  taxonomy.chapters.forEach((ch) => {
    if (!branchMap[ch.branch]) {
      branchMap[ch.branch] = [];
    }
    branchMap[ch.branch].push(ch);
  });

  let branchesHtml = "";

  for (const [branchName, chList] of Object.entries(branchMap)) {
    if (chList.length === 0) continue;

    const chaptersHtml = chList
      .map((ch) => {
        const isPilot = ch.status === "PILOT_ACTIVE";
        const badgeClass = isPilot ? "badge-active" : "badge-pending";
        const badgeText = isPilot ? "Pilot implementation: live" : "Pending assembly";
        const link = isPilot ? `#/chapter/${ch.chapter_id}` : `#/curriculum?pending=${ch.chapter_id}`;

        const topicsCount = ch.topics ? ch.topics.length : 0;
        const topicChips = ch.topics
          ? ch.topics
              .slice(0, 4)
              .map((t) => `<span class="badge badge-subtle" style="margin-right: 4px; margin-bottom: 4px;">${t.name}</span>`)
              .join("")
          : "";

        return `
          <div class="card" style="margin-bottom: 1rem; border-left: 4px solid ${isPilot ? "var(--primary)" : "var(--border-color)"};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
              <div>
                <span style="font-size: 0.75rem; color: var(--text-subtle); font-weight: 700;">CH ${ch.order}</span>
                <h3 style="font-size: 1.15rem; margin-top: 2px;">
                  <a href="${link}" style="color: var(--text-main);">${ch.title}</a>
                </h3>
              </div>
              <span class="badge ${badgeClass}">${badgeText}</span>
            </div>
            <div style="margin: 0.5rem 0;">
              ${topicChips}
              ${topicsCount > 4 ? `<span style="font-size: 0.75rem; color: var(--text-subtle);">+${topicsCount - 4} more topics</span>` : ""}
            </div>
            ${
              isPilot
                ? `<div style="margin-top: 0.75rem;">
                    <a href="#/chapter/${ch.chapter_id}" class="btn btn-primary" style="font-size: 0.8rem; padding: 4px 10px;">
                      Open Chapter Text &rarr;
                    </a>
                   </div>`
                : `<div style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 0.5rem;">
                    Canonical taxonomy nodes defined. Detailed chapter generation scheduled for subsequent phases.
                   </div>`
            }
          </div>
        `;
      })
      .join("");

    branchesHtml += `
      <div class="branch-section" style="margin-bottom: 2rem;">
        <h2 style="font-size: 1.35rem; font-weight: 700; color: var(--text-main); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: var(--primary);"></span>
          ${branchName}
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem;">
          ${chaptersHtml}
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="content-container">
      <div class="hero-header">
        <h1 class="hero-title">Authoritative JEE Physics Syllabus</h1>
        <p class="hero-subtitle">
          Complete 30-chapter JEE Physics syllabus hierarchy structured into 6 primary branches,
          aligned with JEE Advanced, JEE Main, and Physics Olympiad syllabi.
        </p>
      </div>

      <div style="margin-bottom: 1.5rem; display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
        <span class="badge badge-active" style="padding: 6px 12px; font-size: 0.85rem;">4 Chapters (Pilot implementation: live)</span>
        <span class="badge badge-pending" style="padding: 6px 12px; font-size: 0.85rem;">26 Chapters pending content generation</span>
        <a href="#/formulas" class="btn btn-outline" style="margin-left: auto;">Browse Formula Sheet</a>
      </div>

      ${branchesHtml}
    </div>
  `;

  renderMath(container);
}
