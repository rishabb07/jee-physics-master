"""
Web Application Compiler.
Assembles client assets (HTML/CSS/JS/Vendor) and deterministic JSON data bundles
into the production-ready distribution directory (output/web/).
"""

import shutil
import hashlib
import json
from pathlib import Path
from typing import Optional

from jee_physics.web.builder import WebDataBuilder
from jee_physics.web.models import WebBuildManifest


class WebCompiler:
    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path.cwd()
        self.web_src_dir = self.root_dir / "web"
        self.build_data_dir = self.root_dir / "build" / "web" / "data"
        self.default_output_dir = self.root_dir / "output" / "web"
        self.builder = WebDataBuilder(root_dir=self.root_dir)

    def compile(self, clean: bool = False, output_dir: Optional[Path] = None) -> Path:
        target_dir = output_dir or self.default_output_dir

        if clean and target_dir.exists():
            shutil.rmtree(target_dir)

        target_dir.mkdir(parents=True, exist_ok=True)

        # 1. Deterministically build web data
        manifest = self.builder.build_all(target_dir=self.build_data_dir)

        # 2. Copy static web shell & scripts
        # index.html
        shutil.copy2(self.web_src_dir / "index.html", target_dir / "index.html")

        # css/
        dest_css = target_dir / "css"
        if dest_css.exists():
            shutil.rmtree(dest_css)
        shutil.copytree(self.web_src_dir / "css", dest_css)

        # js/
        dest_js = target_dir / "js"
        if dest_js.exists():
            shutil.rmtree(dest_js)
        shutil.copytree(self.web_src_dir / "js", dest_js)

        # vendor/
        dest_vendor = target_dir / "vendor"
        if dest_vendor.exists():
            shutil.rmtree(dest_vendor)
        shutil.copytree(self.web_src_dir / "vendor", dest_vendor)

        # 3. Copy compiled data bundle
        dest_data = target_dir / "data"
        if dest_data.exists():
            shutil.rmtree(dest_data)
        shutil.copytree(self.build_data_dir, dest_data)

        # 4. Strict validation of compiled production bundle
        self._validate_distribution(target_dir)

        return target_dir

    def _validate_distribution(self, dist_dir: Path):
        # 1. Critical files exist
        assert (dist_dir / "index.html").exists(), "index.html missing in distribution"
        assert (dist_dir / "css" / "app.css").exists(), "app.css missing in distribution"
        assert (dist_dir / "js" / "app.js").exists(), "app.js missing in distribution"
        assert (dist_dir / "vendor" / "katex" / "katex.min.js").exists(), "KaTeX JS missing"
        assert (dist_dir / "vendor" / "katex" / "katex.min.css").exists(), "KaTeX CSS missing"
        assert (dist_dir / "vendor" / "katex" / "fonts").exists(), "KaTeX fonts missing"

        # 2. Data contracts exist
        data_dir = dist_dir / "data"
        required_data = [
            "manifest.json",
            "taxonomy.json",
            "chapters.json",
            "concepts.json",
            "formulas.json",
            "questions.json",
            "ladders.json",
            "prerequisites.json",
            "search_index.json",
        ]
        for rd in required_data:
            assert (data_dir / rd).exists(), f"Required dataset {rd} missing in distribution data"

        # 3. Manifest integrity and hash matching (Pre-flight integrity)
        with open(data_dir / "manifest.json", "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        assert manifest_data.get("scope") == "PILOT", "Manifest scope must be PILOT"
        assert len(manifest_data.get("chapters", [])) == 30, "Manifest must reflect 30 chapters"

        for fname, expected_hash in manifest_data.get("content_hashes", {}).items():
            fpath = data_dir / fname
            assert fpath.exists(), f"File {fname} in manifest content_hashes missing on disk"
            actual_hash = hashlib.sha256(fpath.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            assert actual_hash == expected_hash, f"Hash mismatch for {fname}: expected {expected_hash}, got {actual_hash}"

        # 4. Verification boundary audit on distribution questions
        with open(data_dir / "questions.json", "r", encoding="utf-8") as f:
            qs = json.load(f)

        forbidden_leak_ids = {
            "gen-q-ambig-test-01",
            "gen-q-dist-conflict-01",
            "gen-q-wrong-ans-01",
        }
        seen_qids = set()
        for q in qs:
            qid = q.get("question_id", "")
            assert qid not in forbidden_leak_ids, f"CRITICAL: Unverified review item {qid} leaked to output/web!"
            assert q.get("verification_status") == "VERIFIED", f"CRITICAL: Unverified question {qid} in output/web!"
            assert qid not in seen_qids, f"CRITICAL: Duplicate question ID {qid} detected in distribution!"
            seen_qids.add(qid)

        # 5. Referential integrity across chapters
        with open(data_dir / "formulas.json", "r", encoding="utf-8") as f:
            formulas = {item["formula_id"] for item in json.load(f)}
        with open(data_dir / "concepts.json", "r", encoding="utf-8") as f:
            concepts = {item["concept_id"] for item in json.load(f)}

        for ch_file in data_dir.glob("chapter_*.json"):
            with open(ch_file, "r", encoding="utf-8") as f:
                ch_data = json.load(f)
            for sec in ch_data.get("sections", []):
                for form in sec.get("formulas", []):
                    fid = form.get("formula_id")
                    assert fid in formulas, f"Dangling formula reference {fid} in {ch_file.name}"
                for qst in sec.get("questions", []):
                    qid = qst.get("question_id")
                    assert qid in seen_qids, f"Dangling question reference {qid} in {ch_file.name}"
                for conc in sec.get("concepts", []):
                    cid = conc.get("concept_id")
                    assert cid in concepts, f"Dangling concept reference {cid} in {ch_file.name}"
