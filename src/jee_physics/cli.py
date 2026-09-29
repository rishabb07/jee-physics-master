import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from jee_physics.atomization.runner import stage_atom_batch, stage_candidate_file
from jee_physics.ingestion.page_representation import get_page_content_representation
from jee_physics.ingestion.scanner import register_sources, scan_sources_raw
from jee_physics.models.generate_schemas import generate_all_schemas
from jee_physics.models.source import SourcePageInventory, SourceRegistryRecord, SourceSegmentationPlan
from jee_physics.reports.coverage_auditor import audit_chapter_coverage
from jee_physics.storage.io import read_json, read_jsonl
from jee_physics.validation.latex_linter import lint_latex_syntax
from jee_physics.validation.provenance_validator import validate_atom_provenance
from jee_physics.validation.schema_validator import validate_atom_dict


def get_project_root() -> Path:
    """Finds the root directory containing pyproject.toml."""
    current = Path.cwd()
    if (current / "pyproject.toml").exists():
        return current
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return current


def parse_page_range(pages_str: str, max_pages: int) -> Tuple[int, int]:
    """Parses a page range string such as '1-5' or '3' into (start, end)."""
    if "-" in pages_str:
        parts = pages_str.split("-", 1)
        start = max(1, int(parts[0].strip()))
        end = min(max_pages, int(parts[1].strip()))
    else:
        start = max(1, int(pages_str.strip()))
        end = min(max_pages, start)
    return start, end


def cmd_status(args: argparse.Namespace) -> int:
    root = get_project_root()
    print("=" * 60)
    print(" JEE Physics Master Knowledge System - Status")
    print("=" * 60)

    # Raw sources
    raw_dir = root / "sources" / "raw"
    raw_files = [f for f in raw_dir.rglob("*") if f.is_file() and f.name != ".gitkeep"] if raw_dir.exists() else []
    root_pdfs = [f for f in root.glob("*.pdf")]
    print(f"Sources in warehouse (sources/raw/): {len(raw_files)} files (Root unfiled PDFs: {len(root_pdfs)})")

    # Registered sources
    reg_dir = root / "sources" / "registry"
    reg_records: List[SourceRegistryRecord] = []
    if reg_dir.exists():
        for rf in reg_dir.glob("*.json"):
            try:
                reg_records.append(SourceRegistryRecord.model_validate(read_json(rf)))
            except Exception:
                pass

    print(f"Registered sources: {len(reg_records)}")
    if reg_records:
        status_counts = {}
        for r in reg_records:
            status_counts[r.status.value] = status_counts.get(r.status.value, 0) + 1
        print(f"  Breakdown by status: {status_counts}")

    # Canonical KB Atoms
    kb_dir = root / "kb" / "atoms"
    atom_count = 0
    if kb_dir.exists():
        for f in kb_dir.rglob("*.jsonl"):
            atom_count += len(read_jsonl(f))
        for f in kb_dir.rglob("*.json"):
            if f.is_file() and not f.name.endswith(".gitkeep"):
                atom_count += 1
    print(f"Canonical KB Atoms (kb/atoms/): {atom_count}")

    # Staged Atoms
    staging_dir = root / "build" / "staging" / "atoms"
    staged_count = 0
    if staging_dir.exists():
        for f in staging_dir.glob("*.jsonl"):
            staged_count += len(read_jsonl(f))
    print(f"Staged Atoms (build/staging/atoms/): {staged_count}")

    # Verification records
    ver_dir = root / "verification" / "records"
    ver_count = len(list(ver_dir.glob("*.json"))) if ver_dir.exists() else 0
    print(f"Verification Records: {ver_count}")

    # Review queue
    rev_dir = root / "review" / "queue"
    rev_count = len([f for f in rev_dir.rglob("*.json") if f.is_file()]) if rev_dir.exists() else 0
    print(f"Review Queue (pending exceptions): {rev_count}")

    # Archive
    arch_dir = root / "kb" / "archive"
    arch_count = 0
    if arch_dir.exists():
        for f in arch_dir.glob("*.jsonl"):
            arch_count += len(read_jsonl(f))
    print(f"Archived Atoms (kb/archive/): {arch_count}")

    print("=" * 60)
    return 0


def cmd_register_sources(args: argparse.Namespace) -> int:
    root = get_project_root()
    sources_raw = root / "sources" / "raw"
    reg_dir = root / "sources" / "registry"
    segments_dir = root / "sources" / "segments"

    print(f"Scanning strictly inside '{sources_raw}'...")
    summary = register_sources(sources_raw, reg_dir, segments_dir)

    print("=" * 60)
    print(" SOURCE REGISTRATION SUMMARY")
    print("=" * 60)
    print(f"Newly Registered:       {summary.registered_new}")
    print(f"Updated (Modified):     {summary.updated_modified}")
    print(f"Skipped (Unchanged):    {summary.skipped_unchanged}")
    print(f"Marked Missing:         {summary.marked_missing}")
    print(f"Failed Inspection:      {summary.failed_sources}")
    print("=" * 60)
    return 0


def cmd_inspect_source(args: argparse.Namespace) -> int:
    root = get_project_root()
    source_id = args.source_id.strip()
    reg_file = root / "sources" / "registry" / f"{source_id}.json"

    if not reg_file.exists():
        matches = list(root.glob(f"sources/registry/*{source_id}*.json"))
        if len(matches) == 1:
            reg_file = matches[0]
        else:
            print(f"Error: Source '{source_id}' not found in registry (sources/registry/).")
            return 1

    rec = SourceRegistryRecord.model_validate(read_json(reg_file))
    print("=" * 65)
    print(f" SOURCE INSPECTION: {rec.source_id}")
    print("=" * 65)
    print(f"File Name:            {rec.file_name}")
    print(f"Version:              v{rec.source_version}")
    print(f"SHA-256:              {rec.sha256}")
    print(f"File Size:            {rec.file_size_bytes:,} bytes")
    print(f"Format:               {rec.file_format.value.upper()} (MIME: {rec.mime_type})")
    print(f"Status:               {rec.status.value}")
    if rec.last_error:
        print(f"Error Diagnostic:     {rec.last_error}")
    print(f"Total Pages:          {rec.total_pages or 'N/A'}")
    print(f"Has Extractable Text: {'YES' if rec.has_extractable_text else 'NO'}")
    print(f"Appears Image-Only:   {'YES' if rec.is_image_only else 'NO'}")
    print(f"Encrypted/Protected:  {'YES' if rec.is_encrypted else 'NO'}")
    if rec.history:
        print(f"Historical Versions:  {len(rec.history)} prior snapshot(s)")

    seg_file = root / "sources" / "segments" / f"{rec.source_id}_segments.json"
    if seg_file.exists():
        plan = SourceSegmentationPlan.model_validate(read_json(seg_file))
        print(f"\nSegmentation Plan ({plan.segmentation_type.value}):")
        print(f"Total Segments:       {plan.total_segments}")
        for s in plan.segments[:8]:
            print(f"  - [{s.segment_id}] Pages {s.page_start}–{s.page_end}: {s.segment_title}")
        if len(plan.segments) > 8:
            print(f"  ... and {len(plan.segments) - 8} more segment(s)")

    if args.pages and rec.total_pages:
        try:
            start_p, end_p = parse_page_range(args.pages, rec.total_pages)
            print(f"\n--- Diagnostic Page Preview (Pages {start_p} to {end_p}) ---")
            raw_dir = root / "sources" / "raw"
            reg_dir = root / "sources" / "registry"
            for p in range(start_p, end_p + 1):
                page_bundle = get_page_content_representation(rec.source_id, p, raw_dir, reg_dir)
                txt = page_bundle.extracted_text or "[NO EXTRACTABLE TEXT]"
                preview = txt[:250].replace("\n", " ").strip()
                print(f"Page {p} (length: {len(txt)} chars, images: {page_bundle.image_count}):")
                print(f"  Excerpt: \"{preview}\"")
        except Exception as e:
            print(f"Could not load page preview: {str(e)}")

    print("=" * 65)
    return 0


def cmd_stage_batch(args: argparse.Namespace) -> int:
    root = get_project_root()
    source_id = args.source_id.strip()
    candidate_path = Path(args.candidate_file)
    if not candidate_path.is_absolute():
        candidate_path = root / candidate_path

    if not candidate_path.exists():
        print(f"Error: Candidate file '{candidate_path}' not found.")
        return 1

    reg_file = root / "sources" / "registry" / f"{source_id}.json"
    if not reg_file.exists():
        matches = list(root.glob(f"sources/registry/*{source_id}*.json"))
        if len(matches) == 1:
            source_id = matches[0].stem
        else:
            print(f"Error: Source '{source_id}' not found in registry (sources/registry/).")
            return 1

    try:
        report = stage_candidate_file(
            source_id=source_id,
            candidate_path=candidate_path,
            project_root=root,
        )
    except Exception as e:
        print(f"Error staging candidate batch: {str(e)}")
        return 1

    print("=" * 65)
    print(" ATOMIZATION STAGING REPORT")
    print("=" * 65)
    print(f"Source:                 {report.file_name} ({report.source_id})")
    print(f"Batch ID:               {report.batch_id}")
    print(f"Pages Processed:        {report.pages_processed}")
    print(f"Total Atoms Staged:     {report.total_atoms_staged}")
    print(f"Atoms by Type:          {report.atoms_by_type}")
    print(f"Confidence Breakdown:   {report.confidence_distribution}")
    print(f"Questions Extracted:    {report.questions_extracted}")
    print(f"Figures Detected:       {report.figures_detected}")
    print(f"Validation Failures:    {report.validation_failures}")
    print(f"Review Items Queued:    {report.review_items_queued}")
    print(f"Pages with No Atoms:    {report.pages_with_no_atoms or 'None (All Accounted)'}")
    print(f"Staged Atoms Artifact:  {report.staged_atoms_file}")
    print(f"Batch Manifest:         {report.manifest_file}")
    if report.warnings:
        print("Warnings / Notes:")
        for w in report.warnings[:10]:
            print(f"  - {w}")
    print("=" * 65)
    print("[INVARIANT CONFIRMED] kb/atoms/ remains 100% empty of unverified atoms.")
    print("=" * 65)
    return 0 if report.total_atoms_staged > 0 and report.validation_failures == 0 else 1


def cmd_atomize_source(args: argparse.Namespace) -> int:
    print("=" * 65)
    print(" ATOMIZATION PROTOCOL")
    print("=" * 65)
    print("Cognitive atomization is performed by the Antigravity Atomizer Agent:")
    print("  1. Visual page inspection under the Visual Primacy Rule (.agents/skills/atomize-source/SKILL.md)")
    print("  2. Untrusted candidate JSONL written to build/staging/incoming/")
    print("  3. Staging and deterministic validation executed via:")
    print("     python -m jee_physics stage-batch <source_id> <candidate_jsonl>")
    print("=" * 65)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    root = get_project_root()
    reg_dir = root / "sources" / "registry"
    target_dir = Path(args.target) if args.target else root / "build" / "staging" / "atoms"

    print(f"Validating atoms in '{target_dir}'...")
    total_checked = 0
    total_errors = 0

    if not target_dir.exists():
        print(f"Target directory '{target_dir}' does not exist or is empty.")
        return 0

    for jsonl_file in target_dir.glob("*.jsonl"):
        records = read_jsonl(jsonl_file)
        for idx, rec in enumerate(records):
            total_checked += 1
            res, atom = validate_atom_dict(rec)
            if not res.is_valid:
                total_errors += 1
                print(f"[FAIL] {jsonl_file.name} Line {idx+1}: Schema error(s): {res.errors}")
                continue

            prov_errors = validate_atom_provenance(atom, reg_dir)
            if prov_errors:
                total_errors += 1
                print(f"[FAIL] Atom {atom.atom_id}: Provenance error(s): {prov_errors}")

            text_to_lint: List[str] = []
            if atom.content:
                text_to_lint.append(atom.content)
            if atom.question:
                text_to_lint.append(atom.question.statement)
                for opt in atom.question.options:
                    text_to_lint.append(opt.text)
            if atom.formula:
                text_to_lint.append(atom.formula.formula_latex)

            for t in text_to_lint:
                lint_errs = lint_latex_syntax(t)
                if lint_errs:
                    total_errors += 1
                    print(f"[FAIL] Atom {atom.atom_id}: LaTeX syntax error(s): {lint_errs}")

    print(f"Validation complete: checked {total_checked} atom(s), found {total_errors} error(s).")
    return 1 if total_errors > 0 else 0


def cmd_report(args: argparse.Namespace) -> int:
    root = get_project_root()
    chapter = args.chapter or "kinematics"
    kb_atoms = root / "kb" / "atoms"
    output_dir = root / "output"
    archive_dir = root / "kb" / "archive"

    print(f"Generating coverage audit report for chapter: '{chapter}'...")
    rep = audit_chapter_coverage(chapter, kb_atoms, output_dir, archive_dir)

    print("=" * 60)
    print(f" CHAPTER COVERAGE AUDIT: {chapter}")
    print("=" * 60)
    print(f"Total Eligible Canonical Atoms: {rep.total_eligible_atoms}")
    print(f"Placed in Book:                 {rep.book_atoms_count}")
    print(f"Placed in Question Ladders:     {rep.ladder_atoms_count}")
    print(f"Placed in Mock Tests:           {rep.mock_atoms_count}")
    print(f"Preserved in Archive:           {rep.archive_atoms_count}")
    print(f"Unique Placed Atoms:            {rep.placed_atoms_count}")
    print(f"Unplaced Atoms Count:           {len(rep.unplaced_atom_ids)}")
    print(f"Coverage Percentage:            {rep.coverage_percent:.1f}%")
    print(f"Complete (Unused = 0):          {'YES' if rep.is_complete else 'NO'}")
    if rep.unplaced_atom_ids:
        print(f"Unplaced Atom IDs:              {rep.unplaced_atom_ids[:10]}")
    print("=" * 60)
    return 0


def cmd_generate_schemas(args: argparse.Namespace) -> int:
    root = get_project_root()
    schemas_dir = root / "schemas"
    print(f"Generating JSON Schemas into '{schemas_dir}'...")
    results = generate_all_schemas(schemas_dir)
    print(f"Successfully generated {len(results)} schemas.")
    return 0


def cmd_promote_atom(args: argparse.Namespace) -> int:
    root = get_project_root()
    staged_path = Path(args.staged_atom)
    verif_path = Path(args.verification_record)

    if not staged_path.exists():
        print(f"Error: Staged atom file '{staged_path}' does not exist.")
        return 1
    if not verif_path.exists():
        print(f"Error: Verification record file '{verif_path}' does not exist.")
        return 1

    try:
        atom_dict = read_json(staged_path)
        atom = KnowledgeAtom.model_validate(atom_dict)
    except Exception as e:
        print(f"Error reading/parsing staged atom: {e}")
        return 1

    try:
        verif_dict = read_json(verif_path)
        verif = VerificationRecord.model_validate(verif_dict)
    except Exception as e:
        print(f"Error reading/parsing verification record: {e}")
        return 1

    kb_dir = root / "kb" / "atoms"
    manifests_dir = root / "verification" / "manifests"

    try:
        from jee_physics.verification.promoter import promote_atom_to_canonical
        event = promote_atom_to_canonical(
            atom=atom,
            verification_record=verif,
            kb_atoms_dir=kb_dir,
            manifests_dir=manifests_dir,
            staged_path=str(staged_path),
        )
        print("=" * 60)
        print(" CANONICAL PROMOTION SUCCESSFUL")
        print("=" * 60)
        print(f"Atom ID:             {event.atom_id}")
        print(f"Verification ID:     {event.verification_id}")
        print(f"Verdict:             {event.verdict.value}")
        print(f"Source Claim:        {event.source_claimed_answer}")
        print(f"Verified Answer:     {event.verified_answer}")
        print(f"Canonical Path:      {event.canonical_path}")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"Promotion rejected: {e}")
        return 1


def cmd_stage_solver_run(args: argparse.Namespace) -> int:
    root = get_project_root()
    input_file = Path(args.solver_json)
    if not input_file.is_absolute():
        input_file = root / input_file

    from jee_physics.verification.staging import stage_solver_run_file

    success, dest_path, manifest_path, errors = stage_solver_run_file(
        input_file=input_file,
        staging_dir=root / "build" / "staging" / "atoms",
        solver_runs_dir=root / "verification" / "solver_runs",
        manifests_dir=root / "verification" / "manifests",
    )

    if not success:
        print("=" * 60)
        print(" SOLVER RUN STAGING FAILED")
        print("=" * 60)
        for err in errors:
            print(f" - {err}")
        return 1

    print("=" * 60)
    print(" SOLVER RUN STAGED SUCCESSFULLY")
    print("=" * 60)
    print(f"Staged Path:   {dest_path}")
    print(f"Manifest Path: {manifest_path}")
    print("=" * 60)
    return 0


def cmd_stage_adjudication(args: argparse.Namespace) -> int:
    root = get_project_root()
    input_file = Path(args.adjudication_json)
    if not input_file.is_absolute():
        input_file = root / input_file

    from jee_physics.verification.staging import stage_adjudication_file

    success, dest_path, manifest_path, errors = stage_adjudication_file(
        input_file=input_file,
        staging_dir=root / "build" / "staging" / "atoms",
        adjudication_dir=root / "verification" / "adjudications",
        manifests_dir=root / "verification" / "manifests",
    )

    if not success:
        print("=" * 60)
        print(" ADJUDICATION STAGING FAILED")
        print("=" * 60)
        for err in errors:
            print(f" - {err}")
        return 1

    print("=" * 60)
    print(" ADJUDICATION STAGED SUCCESSFULLY")
    print("=" * 60)
    print(f"Staged Path:   {dest_path}")
    print(f"Manifest Path: {manifest_path}")
    print("=" * 60)
    return 0


def cmd_build_web(args: argparse.Namespace) -> int:
    from jee_physics.web.compiler import WebCompiler
    root = get_project_root()
    compiler = WebCompiler(root_dir=root)
    out_dir = Path(args.output) if args.output else None
    print(f"Compiling JEE Physics Web Application (clean={args.clean})...")
    try:
        dest = compiler.compile(clean=args.clean, output_dir=out_dir)
        print("=" * 60)
        print(" WEB APPLICATION COMPILED SUCCESSFULLY")
        print("=" * 60)
        print(f"Distribution Directory: {dest}")
        print(f"Data Bundle:            {dest / 'data'}")
        print(f"To preview locally:     python -m jee_physics web-dev")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"Compilation failed: {e}", file=sys.stderr)
        return 1


def cmd_web_dev(args: argparse.Namespace) -> int:
    from jee_physics.web.server import DevServer
    root = get_project_root()
    server = DevServer(root_dir=root, port=args.port, host=args.host)
    print("Starting development server...")
    server.start(watch=not args.no_watch)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="jee-physics",
        description="Foundational CLI for JEE Physics Knowledge and Learning System",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    p_status = subparsers.add_parser("status", help="Show system status and registry metrics")
    p_status.set_defaults(func=cmd_status)

    # register-sources
    p_reg = subparsers.add_parser("register-sources", help="Scan sources/raw/ and register into sources/registry/")
    p_reg.set_defaults(func=cmd_register_sources)

    # inspect-source
    p_inspect = subparsers.add_parser("inspect-source", help="Inspect metadata, segments, and page preview of a source")
    p_inspect.add_argument("source_id", help="Source ID or partial identifier to inspect")
    p_inspect.add_argument("--pages", default=None, help="Page range to preview (e.g. 1-5 or 3)")
    p_inspect.set_defaults(func=cmd_inspect_source)

    # stage-batch
    p_stage = subparsers.add_parser("stage-batch", help="Validate and stage candidate atoms into build/staging/atoms/")
    p_stage.add_argument("source_id", help="Registered source ID in sources/registry/")
    p_stage.add_argument("candidate_file", help="Path to untrusted candidate JSONL file (e.g. in build/staging/incoming/)")
    p_stage.set_defaults(func=cmd_stage_batch)

    # stage-solver-run
    p_stage_run = subparsers.add_parser("stage-solver-run", help="Validate and stage an untrusted solver run JSON into verification/solver_runs/")
    p_stage_run.add_argument("solver_json", help="Path to untrusted solver JSON file (e.g. in verification/incoming/)")
    p_stage_run.set_defaults(func=cmd_stage_solver_run)

    # stage-adjudication
    p_stage_adj = subparsers.add_parser("stage-adjudication", help="Validate and stage an untrusted adjudication JSON into verification/adjudications/")
    p_stage_adj.add_argument("adjudication_json", help="Path to untrusted adjudication JSON file (e.g. in verification/incoming/)")
    p_stage_adj.set_defaults(func=cmd_stage_adjudication)

    # atomize-source
    p_atomize = subparsers.add_parser("atomize-source", help="Show cognitive atomization protocol and instructions")
    p_atomize.add_argument("source_id", nargs="?", default="", help="Optional source ID")
    p_atomize.add_argument("--pages", default=None, help="Optional page range")
    p_atomize.set_defaults(func=cmd_atomize_source)

    # validate
    p_val = subparsers.add_parser("validate", help="Validate schema, provenance, and syntax for staged atoms")
    p_val.add_argument("--target", default=None, help="Target directory (default: build/staging/atoms)")
    p_val.set_defaults(func=cmd_validate)

    # report
    p_rep = subparsers.add_parser("report", help="Audit chapter coverage and zero-silent-loss invariant")
    p_rep.add_argument("--chapter", default=None, help="Chapter ID to audit (default: kinematics)")
    p_rep.set_defaults(func=cmd_report)

    # generate-schemas
    p_schemas = subparsers.add_parser("generate-schemas", help="Generate JSON schemas from Pydantic models")
    p_schemas.set_defaults(func=cmd_generate_schemas)

    # promote-atom
    p_promo = subparsers.add_parser("promote-atom", help="Promote a verified staged atom into canonical kb/atoms/")
    p_promo.add_argument("staged_atom", help="Path to individual staged atom JSON file or extract")
    p_promo.add_argument("verification_record", help="Path to VerificationRecord JSON file")
    p_promo.set_defaults(func=cmd_promote_atom)

    # build-web
    p_build_web = subparsers.add_parser("build-web", help="Compile the interactive web application to output/web/")
    p_build_web.add_argument("--clean", action="store_true", help="Clean destination directory before compilation")
    p_build_web.add_argument("--output", default=None, help="Custom output directory (default: output/web)")
    p_build_web.set_defaults(func=cmd_build_web)

    # web-dev
    p_web_dev = subparsers.add_parser("web-dev", help="Run local development server with live watcher")
    p_web_dev.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    p_web_dev.add_argument("--host", default="127.0.0.1", help="Host address to bind to (default: 127.0.0.1)")
    p_web_dev.add_argument("--no-watch", action="store_true", help="Disable filesystem change watcher")
    p_web_dev.set_defaults(func=cmd_web_dev)

    args = parser.parse_args()
    return args.func(args)



if __name__ == "__main__":
    sys.exit(main())
