/**
 * Client-Side Inverted Search Engine.
 * Loads pre-indexed tokens and ranks matches across chapters, concepts, formulas, and questions.
 */

class SearchEngine {
  constructor() {
    this.index = [];
    this.loaded = false;
  }

  async init() {
    if (this.loaded) return;
    try {
      const res = await fetch("data/search_index.json");
      if (res.ok) {
        this.index = await res.json();
        this.loaded = true;
      }
    } catch (e) {
      console.warn("Failed to load search index:", e);
    }
  }

  query(searchTerm, maxResults = 8) {
    if (!searchTerm || searchTerm.trim().length < 2) return [];

    const rawTokens = searchTerm
      .toLowerCase()
      .replace(/[^\w\s-]/g, " ")
      .split(/\s+/)
      .filter((w) => w.length > 1);

    if (rawTokens.length === 0) return [];

    const scored = [];

    for (const item of this.index) {
      let score = 0;
      const titleLower = item.title.toLowerCase();
      const snippetLower = item.snippet.toLowerCase();

      for (const token of rawTokens) {
        // Direct title match gives high score
        if (titleLower.includes(token)) {
          score += 15;
          if (titleLower.startsWith(token)) score += 10;
        }
        // Keywords match
        if (item.keywords && item.keywords.includes(token)) {
          score += 5;
        }
        // Snippet match
        if (snippetLower.includes(token)) {
          score += 2;
        }
      }

      // Prioritize chapters and concepts slightly
      if (item.entity_type === "chapter") score += 3;
      if (item.entity_type === "concept") score += 2;

      if (score > 0) {
        scored.push({ item, score });
      }
    }

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, maxResults).map((s) => s.item);
  }
}

export const searchEngine = new SearchEngine();
