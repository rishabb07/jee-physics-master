from jee_physics.models.manifest import FileChecksumRecord, JobManifest


def test_job_manifest_artifact_tracking():
    inp = FileChecksumRecord(file_path="sources/raw/irodov.pdf", sha256="a" * 64, size_bytes=1024)
    out = FileChecksumRecord(file_path="build/staging/atoms/batch_01.jsonl", sha256="b" * 64, size_bytes=2048)

    manifest = JobManifest(
        manifest_id="man-atomize-001",
        job_type="ATOMIZE",
        stage="EXTRACTION",
        input_files=[inp],
        output_files=[out],
        generated_atom_ids=["kinematics-q-01", "kinematics-q-02"],
        status="COMPLETED",
        metadata={"model": "gemini-2.5-flash", "batch_size": 2},
    )

    assert manifest.job_type == "ATOMIZE"
    assert len(manifest.generated_atom_ids) == 2
    assert manifest.input_files[0].file_path == "sources/raw/irodov.pdf"
    assert manifest.output_files[0].file_path == "build/staging/atoms/batch_01.jsonl"
