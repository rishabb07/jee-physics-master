/**
 * Hash-based Single Page Application Client Router.
 * Maps URL hash paths to view renderers and updates active navigation state.
 */

class Router {
  constructor() {
    this.routes = {};
    this.currentRoute = null;
    this.container = null;

    window.addEventListener("hashchange", () => this._handleRoute());
  }

  register(path, handler) {
    this.routes[path] = handler;
  }

  init(containerElement) {
    this.container = containerElement;
    this._handleRoute();
  }

  navigate(hashPath) {
    window.location.hash = hashPath;
  }

  _parseHash() {
    const raw = window.location.hash.slice(1) || "/";
    const [pathPart, queryPart] = raw.split("?");
    const params = new URLSearchParams(queryPart || "");
    const segments = pathPart.split("/").filter(Boolean);
    return { pathPart, segments, params };
  }

  async _handleRoute() {
    const { pathPart, segments, params } = this._parseHash();
    this.currentRoute = pathPart;

    // Highlight top nav
    const activeRouteKey = segments[0] || "";
    document.querySelectorAll(".nav-link").forEach((link) => {
      const target = link.getAttribute("data-route") || "";
      if (target === activeRouteKey) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });

    // Match routes
    if (pathPart === "/" || pathPart === "") {
      if (this.routes["/"]) {
        await this.routes["/"](this.container, params);
      }
    } else if (segments[0] === "chapter" && segments[1]) {
      if (this.routes["/chapter/:id"]) {
        await this.routes["/chapter/:id"](this.container, segments[1], params);
      }
    } else if (segments[0] === "concept" && segments[1]) {
      if (this.routes["/concept/:id"]) {
        await this.routes["/concept/:id"](this.container, segments[1], params);
      }
    } else if (this.routes[`/${segments[0]}`]) {
      await this.routes[`/${segments[0]}`](this.container, params);
    } else {
      this._renderNotFound();
    }

    // Scroll to top
    const mainEl = document.getElementById("main-content");
    if (mainEl) mainEl.scrollTop = 0;
  }

  _renderNotFound() {
    if (!this.container) return;
    this.container.innerHTML = `
      <div class="content-container">
        <div class="card" style="text-align: center; padding: 3rem 1rem;">
          <h2 style="margin-bottom: 0.5rem; color: var(--danger);">404 — Page Not Found</h2>
          <p style="color: var(--text-muted); margin-bottom: 1.5rem;">The requested topic, concept, or chapter could not be located.</p>
          <a href="#/" class="btn btn-primary">Return to Curriculum Overview</a>
        </div>
      </div>
    `;
  }
}

export const router = new Router();
