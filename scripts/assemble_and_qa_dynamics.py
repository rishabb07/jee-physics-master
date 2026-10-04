import json
import shutil
from pathlib import Path
from jee_physics.content.assembler import ChapterAssembler
from jee_physics.content.qa import ChapterQAAuditor

def main():
    root = Path.cwd()
    assembler = ChapterAssembler(root)
    auditor = ChapterQAAuditor(root)

    print("Assembling chapter: laws-of-motion...")
    blocks = assembler.assemble_chapter("laws-of-motion")
    print(f"Total blocks assembled: {len(blocks)}")
    
    # Save draft
    draft_dir = assembler.save_draft("laws-of-motion", blocks)
    print(f"Saved draft to {draft_dir}")

    # Copy to build/drafts/dynamics for dual compatibility
    dyn_draft_dir = root / "build" / "drafts" / "dynamics"
    dyn_draft_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(draft_dir / "laws-of-motion_blocks.json", dyn_draft_dir / "dynamics_blocks.json")
    shutil.copy2(draft_dir / "laws-of-motion_draft.md", dyn_draft_dir / "dynamics_draft.md")

    # Run QA
    spec = assembler.load_spec("laws-of-motion")
    plan = assembler.load_plan("laws-of-motion")
    
    qa_report, rendering_report = auditor.audit_chapter("laws-of-motion", blocks, plan, spec)
    print(f"QA Verdict: {qa_report.verdict}")
    print(f"Physics Passed: {qa_report.physics_passed}")
    print(f"Provenance Passed: {qa_report.provenance_passed}")
    print(f"Curriculum Passed: {qa_report.curriculum_passed}")
    print(f"Editorial Passed: {qa_report.editorial_passed}")
    print(f"Pedagogy Passed: {qa_report.pedagogy_passed}")
    print(f"LaTeX Rendering Passed: {rendering_report.passed}")
    print(f"LaTeX Errors: {len(rendering_report.latex_errors)}")
    print(f"Broken References: {len(rendering_report.broken_references)}")
    print(f"Empty Sections: {len(rendering_report.empty_sections)}")
    print(f"Findings: {len(qa_report.findings)}")
    for f in qa_report.findings:
        print(f"  [{f.severity}] {f.category} at {f.location}: {f.description}")

    reports_dir = root / "build" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    (reports_dir / "chapter_qa_laws-of-motion.json").write_text(
        json.dumps(qa_report.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    (reports_dir / "chapter_qa_dynamics.json").write_text(
        json.dumps(qa_report.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    (reports_dir / "rendering_qa_laws-of-motion.json").write_text(
        json.dumps(rendering_report.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    (reports_dir / "rendering_qa_dynamics.json").write_text(
        json.dumps(rendering_report.model_dump(mode="json"), indent=2), encoding="utf-8"
    )

    assert qa_report.verdict == "PASSED", f"Chapter QA failed with verdict {qa_report.verdict}!"
    assert rendering_report.passed, f"Rendering QA failed! Errors: {rendering_report.latex_errors}"
    print("Chapter Assembly and QA Complete: 100% PASSED!")

if __name__ == "__main__":
    main()
