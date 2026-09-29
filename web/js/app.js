/**
 * Application Bootstrap & Main Entry Point
 */

import { state } from "./state.js";
import { router } from "./router.js";
import { searchEngine } from "./search.js";
import { renderHome } from "./views/home.js";
import { renderCurriculum } from "./views/curriculum.js";
import { renderChapter } from "./views/chapter.js";
import { renderConcept } from "./views/concept.js";
import { renderFormulas } from "./views/formulas.js";
import { renderPractice } from "./views/practice.js";
import { renderLadders } from "./views/ladders.js";
import { renderProgress } from "./views/progress.js";

async function init() {
  // Apply saved theme
  const savedTheme = state.getTheme();
  document.body.className = `theme-${savedTheme}`;

  // Theme toggle button
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const isDark = document.body.classList.contains("theme-dark");
      const newTheme = isDark ? "light" : "dark";
      document.body.className = `theme-${newTheme}`;
      state.setTheme(newTheme);
    });
  }

  // Sidebar toggle
  const sidebarToggle = document.getElementById("sidebar-toggle");
  const sidebar = document.getElementById("sidebar");
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
    });
  }

  // Initialize search engine
  searchEngine.init();
  setupGlobalSearch();

  // Populate sidebar navigation
  await populateSidebar();

  // Register SPA routes
  router.register("/", renderHome);
  router.register("/curriculum", renderCurriculum);
  router.register("/chapter/:id", renderChapter);
  router.register("/concept/:id", renderConcept);
  router.register("/formulas", renderFormulas);
  router.register("/practice", renderPractice);
  router.register("/ladders", renderLadders);
  router.register("/progress", renderProgress);

  // Mount router into #view-outlet
  const outlet = document.getElementById("view-outlet");
  router.init(outlet);
}

async function populateSidebar() {
  const sidebarNav = document.getElementById("sidebar-nav");
  if (!sidebarNav) return;

  try {
    const res = await fetch("data/taxonomy.json");
    if (!res.ok) throw new Error("Could not load taxonomy");
    const taxonomy = await res.json();

    const branchMap = {};
    taxonomy.branches.forEach((b) => (branchMap[b] = []));
    taxonomy.chapters.forEach((ch) => {
      if (!branchMap[ch.branch]) branchMap[ch.branch] = [];
      branchMap[ch.branch].push(ch);
    });

    let navHtml = "";
    for (const [branchName, chList] of Object.entries(branchMap)) {
      if (chList.length === 0) continue;

      const itemsHtml = chList
        .map((ch) => {
          const isPilot = ch.status === "PILOT_ACTIVE";
          const badgeClass = isPilot ? "badge-active" : "badge-pending";
          const badgeText = isPilot ? "Pilot" : "Pending";
          const link = isPilot ? `#/chapter/${ch.chapter_id}` : `#/curriculum?pending=${ch.chapter_id}`;

          return `
          <a href="${link}" class="chapter-nav-item" data-chapter="${ch.chapter_id}">
            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 190px;">${ch.title}</span>
            <span class="badge ${badgeClass}" style="font-size: 0.65rem;">${badgeText}</span>
          </a>
        `;
        })
        .join("");

      navHtml += `
        <div class="branch-group">
          <div class="branch-title">${branchName}</div>
          ${itemsHtml}
        </div>
      `;
    }

    sidebarNav.innerHTML = navHtml;

    // Filter input
    const filterInput = document.getElementById("sidebar-filter-input");
    if (filterInput) {
      filterInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase();
        document.querySelectorAll(".chapter-nav-item").forEach((item) => {
          const text = item.textContent.toLowerCase();
          item.style.display = text.includes(q) ? "flex" : "none";
        });
      });
    }
  } catch (e) {
    console.warn("Sidebar population failed:", e);
    sidebarNav.innerHTML = `<div style="padding: 1rem; color: var(--text-muted); font-size: 0.85rem;">Failed to load navigation menu.</div>`;
  }
}

function setupGlobalSearch() {
  const searchInput = document.getElementById("global-search-input");
  const dropdown = document.getElementById("search-dropdown");
  if (!searchInput || !dropdown) return;

  // Keyboard shortcut Ctrl+K / Cmd+K
  window.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });

  searchInput.addEventListener("input", (e) => {
    const val = e.target.value;
    if (val.trim().length < 2) {
      dropdown.classList.add("hidden");
      dropdown.innerHTML = "";
      return;
    }

    const results = searchEngine.query(val, 6);
    if (results.length === 0) {
      dropdown.innerHTML = `<div style="padding: 12px; color: var(--text-muted); font-size: 0.85rem;">No matching concepts or formulas found.</div>`;
      dropdown.classList.remove("hidden");
      return;
    }

    dropdown.innerHTML = results
      .map(
        (item) => `
      <div class="search-result-item" onclick="window.location.hash='${item.route}'; document.getElementById('search-dropdown').classList.add('hidden');">
        <div class="search-item-header">
          <span class="search-item-title">${item.title}</span>
          <span class="badge badge-subtle">${item.entity_type}</span>
        </div>
        <div class="search-item-snippet">${item.snippet}</div>
      </div>
    `
      )
      .join("");

    dropdown.classList.remove("hidden");
  });

  // Close dropdown on click outside
  document.addEventListener("click", (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.add("hidden");
    }
  });
}

// Start application
window.addEventListener("DOMContentLoaded", init);
