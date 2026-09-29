# Web Application Deployment & Auto-Update Guide

This guide details the operations, build commands, development server workflows, and CI/CD validation steps for the **JEE Physics Master Book Web Application**.

---

## 1. Quick Start

### 1.1 Compile Web Application
To generate the static data bundle (`build/web/data/`) and compile the complete client application to `output/web/`:

```powershell
python -m jee_physics build-web
```

Flags:
- `--clean`: Clean previous build artifacts prior to compiling.
- `--output <path>`: Specify custom destination directory (defaults to `output/web/`).

### 1.2 Start Local Development Server
To launch the built-in HTTP server with live filesystem watching and auto-recompilation:

```powershell
python -m jee_physics web-dev --port 8080 --watch
```

Flags:
- `--port <number>`: Port number to bind to (default: `8080`).
- `--host <address>`: Host interface (default: `127.0.0.1`).
- `--watch`: Enable automatic background file watcher that re-runs `build-web` whenever files in `kb/`, `content/`, `curriculum/`, `question_bank/`, or `web/` change.

Once started, open `http://127.0.0.1:8080` in any modern web browser.

---

## 2. Directory Layout & Artifact Flow

```text
Sources (Authoritative)              Intermediate (Staging)             Published (Disposable)
kb/                                  build/web/data/                    output/web/
content/                   ------->  ├── manifest.json       ------->   ├── index.html
curriculum/    (build-web)           ├── taxonomy.json                  ├── css/app.css
question_bank/                       ├── chapters.json                  ├── js/
                                     ├── chapter_{id}.json              ├── vendor/katex/
                                     └── ...                            └── data/
```

- **`output/web/`** is entirely disposable and can be re-generated at any time using `build-web`.
- No sensitive or unverified material is ever placed into `build/web/data/` or `output/web/data/`.

---

## 3. Automated Validation & Verification Pipeline

Before any deployment, the deterministic verification pipeline executes:
1. **Schema Check:** All emitted JSON files conform strictly to Pydantic web models in `src/jee_physics/web/models.py`.
2. **Verification Boundary Check:**
   - Asserts that zero unverified questions from `question_bank/` or items from `review/queue/` are present in `output/web/data/questions.json`.
   - Asserts that all included questions have certified verification records.
3. **Referential Integrity Check:**
   - Every formula referenced in a chapter exists in `formulas.json`.
   - Every question referenced in a chapter exists in `questions.json`.
   - Every prerequisite link resolves to a valid chapter or curriculum node.
4. **Offline Asset Check:**
   - Verifies all KaTeX scripts, styles, and woff2 fonts exist locally in `output/web/vendor/katex/`. Zero external CDN calls needed.
5. **Mutation Test:**
   - Verifies that modifying a canonical entity propagates deterministically to the web bundle upon re-compilation.

Run the test suite:
```powershell
pytest tests/test_web_application.py -v
```

---

## 4. CI/CD & Automated Deployment Pipeline

The production CI/CD workflow is defined in [`.github/workflows/web_deploy.yml`](file:///.github/workflows/web_deploy.yml).

### 4.1 Pipeline Architecture
The workflow consists of two sequential jobs:
1. **`validate_and_build`:**
   - Sets up Python 3.12 with caching.
   - Installs dependencies and package (`pip install -e .[dev]`).
   - Runs full test suite (`pytest -v`).
   - Runs clean web build (`python -m jee_physics build-web --clean`).
   - Runs web release audit (`python -m jee_physics web-release-audit`).
   - Runs offline asset validation (asserts KaTeX scripts, styles, and woff2 font files exist locally).
   - Uploads `output/web/` as a deployment artifact (`actions/upload-pages-artifact@v3`).
2. **`deploy_production`:**
   - Triggers only on pushes to `master` or `main` after `validate_and_build` succeeds.
   - Deploys static bundle to GitHub Pages (`actions/deploy-pages@v4`).
   - Requires permissions: `contents: read`, `pages: write`, `id-token: write`.

### 4.2 Current Deployment Status
> [!NOTE]
> **`AUTO_DEPLOYMENT_NOT_YET_PROVEN`**: The repository currently operates in a local Git environment without a configured remote origin (`git remote -v` is empty). All CI/CD workflow definitions and deployment scripts are fully written, validated, and ready to trigger automatically once linked to a remote GitHub repository.

---

## 5. Versioning & System Information

Every web compilation automatically generates a cryptographic build manifest stored at `output/web/data/manifest.json`.

### 5.1 Manifest Schema
```json
{
  "build_id": "build-web-20260929-195937",
  "built_at": "2026-09-29T14:29:37.382025Z",
  "app_version": "1.0.0",
  "git_commit": "master-local",
  "scope": "PILOT",
  "chapter_count": 30,
  "question_count": 8,
  "formula_count": 13,
  "concept_count": 12,
  "asset_hashes": { ... }
}
```

### 5.2 UI Exposure
The client application fetches `/data/manifest.json` on initialization and renders this metadata in the **System & Build Information** card on the Home dashboard:
- **App Version & Scope:** `v1.0.0 (Pilot implementation: live)`
- **Git Commit:** Current commit SHA or branch identifier
- **Build ID:** Unique timestamped build identifier
- **Math Engine:** KaTeX (offline math assets loaded locally from `/vendor/katex/`)

---

## 6. Rollback Procedures

A fundamental architectural invariant of the JEE Physics Master Knowledge System is:
> **The canonical knowledge base (`kb/`) is the source of truth; the web application is an ephemeral, generated projection.**

Rollbacks must operate strictly on the deployed projection or repository commit history, never modifying or corrupting canonical knowledge atoms.

### 6.1 Rollback Scenarios & Commands

#### Scenario A: Rolling back a failed web build locally
If an unverified or corrupted draft is compiled locally:
```powershell
# Clean the disposable web output directory
python -m jee_physics build-web --clean
```

#### Scenario B: Rolling back to a previous Git commit
If a bad commit was made to source or curriculum specifications:
```powershell
# 1. Identify previous known-good commit SHA
git log --oneline -n 5

# 2. Revert the commit cleanly
git revert <faulty-commit-sha> --no-edit

# 3. Re-run validation and compilation
pytest tests/test_release_gates.py
python -m jee_physics build-web --clean
```

#### Scenario C: Production Rollback in GitHub Actions
If a live GitHub Pages deployment must be rolled back to a previous release tag:
1. Re-run the successful GitHub Actions workflow run of the prior release from the GitHub Actions UI ("Re-run jobs").
2. Or check out the desired release tag and push to `master`:
   ```bash
   git checkout tags/v1.0.0-known-good -b rollback-branch
   git push origin rollback-branch:master --force-with-lease
   ```
3. GitHub Actions triggers `web_deploy.yml`, executes pre-flight release gates, and deploys the known-good artifact.

---

## 7. Terminology & Standards

To ensure precise communication and avoid misleading status claims:
1. **Pilot Status (`Pilot implementation: live`):**
   - The 4 pilot chapters (`rotational-motion`, `thermodynamics`, `current-electricity`, `ray-optics`) are fully populated with verified concepts, derivations, formulas, worked examples, misconceptions, and questions.
   - The remaining 26 chapters are structurally supported in taxonomy and curriculum graphs, but are pending chapter content generation. They must NOT be marked "Complete".
2. **Math Assets (`offline KaTeX/math assets`):**
   - Refers specifically to KaTeX fonts (`.woff2`), scripts (`katex.min.js`), and styles (`katex.min.css`) bundled locally in `output/web/vendor/katex/` to prevent external CDN reliance.
   - Must be distinguished from offline application caching / service worker offline modes.
