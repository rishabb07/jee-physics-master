import json
import shutil
from pathlib import Path
from jee_physics.content.assembler import ChapterAssembler
from jee_physics.content.qa import ChapterQAAuditor

def main():
    root = Path.cwd()
    assembler = ChapterAssembler(root)
    auditor = ChapterQAAuditor(root)

    chapter_id = "work-energy-power"
    print(f"Assembling chapter: {chapter_id}...")
    blocks = assembler.assemble_chapter(chapter_id)
    print(f"Total blocks assembled: {len(blocks)}")
    
    # Save draft
    draft_dir = assembler.save_draft(chapter_id, blocks)
    print(f"Saved draft to {draft_dir}")

    # Run QA
    spec = assembler.load_spec(chapter_id)
    plan = assembler.load_plan(chapter_id)
    
    qa_report, rendering_report = auditor.audit_chapter(chapter_id, blocks, plan, spec)
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
    
    (reports_dir / f"chapter_qa_{chapter_id}.json").write_text(
        json.dumps(qa_report.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    (reports_dir / f"rendering_qa_{chapter_id}.json").write_text(
        json.dumps(rendering_report.model_dump(mode="json"), indent=2), encoding="utf-8"
    )

    assert qa_report.verdict == "PASSED", f"Chapter QA failed with verdict {qa_report.verdict}!"
    assert rendering_report.passed, f"Rendering QA failed! Errors: {rendering_report.latex_errors}"
    print("Chapter Assembly and QA Complete: 100% PASSED!")

if __name__ == "__main__":
    main()
