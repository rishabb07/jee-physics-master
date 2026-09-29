/**
 * Client-side persistent state manager for student learning progress.
 * Stores attempts, accuracy, bookmarks, and visited content in localStorage.
 */

const STORAGE_KEY = "jee_physics_user_state_v1";

class StateManager {
  constructor() {
    this.state = this._loadState();
  }

  _loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        return JSON.parse(raw);
      }
    } catch (e) {
      console.warn("Failed to load user state from localStorage:", e);
    }
    return {
      attempts: {},
      bookmarks: [],
      visitedChapters: [],
      theme: "light",
      lastActive: new Date().toISOString(),
    };
  }

  _saveState() {
    try {
      this.state.lastActive = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
    } catch (e) {
      console.warn("Failed to save user state to localStorage:", e);
    }
  }

  recordAttempt(questionId, selectedAnswer, isCorrect) {
    this.state.attempts[questionId] = {
      answer: selectedAnswer,
      isCorrect: Boolean(isCorrect),
      timestamp: new Date().toISOString(),
    };
    this._saveState();
  }

  getAttempt(questionId) {
    return this.state.attempts[questionId] || null;
  }

  toggleBookmark(id) {
    const idx = this.state.bookmarks.indexOf(id);
    if (idx >= 0) {
      this.state.bookmarks.splice(idx, 1);
    } else {
      this.state.bookmarks.push(id);
    }
    this._saveState();
    return this.isBookmarked(id);
  }

  isBookmarked(id) {
    return this.state.bookmarks.includes(id);
  }

  recordVisitedChapter(chapterId) {
    if (!this.state.visitedChapters.includes(chapterId)) {
      this.state.visitedChapters.push(chapterId);
      this._saveState();
    }
  }

  getStats() {
    const attemptsList = Object.values(this.state.attempts);
    const totalAttempted = attemptsList.length;
    const correctCount = attemptsList.filter((a) => a.isCorrect).length;
    const accuracy = totalAttempted > 0 ? Math.round((correctCount / totalAttempted) * 100) : 0;

    return {
      totalAttempted,
      correctCount,
      incorrectCount: totalAttempted - correctCount,
      accuracy,
      bookmarkedCount: this.state.bookmarks.length,
      visitedChaptersCount: this.state.visitedChapters.length,
    };
  }

  setTheme(themeName) {
    this.state.theme = themeName;
    this._saveState();
  }

  getTheme() {
    return this.state.theme || "light";
  }

  clearAll() {
    this.state = {
      attempts: {},
      bookmarks: [],
      visitedChapters: [],
      theme: "light",
      lastActive: new Date().toISOString(),
    };
    this._saveState();
  }
}

export const state = new StateManager();
