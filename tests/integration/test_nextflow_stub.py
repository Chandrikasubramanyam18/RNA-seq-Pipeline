#!/usr/bin/env python3
"""
Nextflow stub integration test (Step 14).

Runs the full workflow with `-stub -profile standard` on syntactically valid
synthetic fixtures (mini FASTA/GTF/BED12 + paired-end gzipped FASTQ), then
asserts the key published artifacts appear under `--outdir`.

Fixture inputs are generated at runtime under tests/integration/fixtures/ (a
git-ignored directory), so nothing biological is committed to the repo.
"""

import gzip
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "tests" / "integration" / "fixtures"

sys.path.insert(0, str(REPO_ROOT / "scripts" / "python"))
from build_test_reference import MINI_FASTA_CONTENT, MINI_GTF_CONTENT  # noqa: E402

NEXTFLOW = shutil.which("nextflow")

pytestmark = [
    pytest.mark.nextflow,
    pytest.mark.skipif(
        NEXTFLOW is None,
        reason="nextflow not found on PATH; install per docs/workflow.md",
    ),
]

SAMPLES = [
    ("C1", "control", 1),
    ("C2", "control", 2),
    ("C3", "control", 3),
    ("T1", "treatment", 1),
    ("T2", "treatment", 2),
    ("T3", "treatment", 3),
]

FASTQ_RECORD = textwrap.dedent("""\
    @sample_1
    ATGCGATCGATCGATCGATCGATCGATCGACTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
    +
    IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    """).rstrip()

MINI_BED12 = textwrap.dedent("""\
    chr16\t0\t200\tCRISPLD2\t0\t+\t0\t200\t0\t2\t90,90,\t0,110,
    chr12\t0\t200\tGAPDH\t0\t+\t0\t200\t0\t2\t80,100,\t0,100,
    chr7\t0\t200\tACTB\t0\t+\t0\t200\t0\t2\t85,95,\t0,105,
    """).rstrip()


def _write_gzip_fastq(path: Path, sample: str, read_no: int) -> None:
    record = FASTQ_RECORD.replace("sample_1", f"{sample}_R{read_no}")
    with gzip.open(path, "wt", encoding="ascii") as fh:
        for i in range(4):
            fh.write(record.replace("@sample", f"@{sample}_R{read_no}_{i}") + "\n")


def _build_fixtures() -> dict:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    fasta = FIXTURES_DIR / "mini_genome.fa"
    gtf = FIXTURES_DIR / "mini_genes.gtf"
    bed = FIXTURES_DIR / "refgene.bed12"
    fasta.write_text(MINI_FASTA_CONTENT.strip() + "\n", encoding="ascii")
    gtf.write_text(MINI_GTF_CONTENT.strip() + "\n", encoding="ascii")
    bed.write_text(MINI_BED12 + "\n", encoding="ascii")

    reads = {}
    for sample, _, _ in SAMPLES:
        for read_no in (1, 2):
            p = FIXTURES_DIR / f"{sample}_R{read_no}.fastq.gz"
            _write_gzip_fastq(p, sample, read_no)
            reads[(sample, read_no)] = p

    return {"fasta": fasta, "gtf": gtf, "bed": bed, "reads": reads}


def _write_samplesheet(reads: dict) -> Path:
    path = FIXTURES_DIR / "samplesheet.csv"
    with open(path, "w", encoding="ascii") as fh:
        fh.write("sample,fastq_1,fastq_2,condition,replicate\n")
        for sample, condition, replicate in SAMPLES:
            fq1 = reads[(sample, 1)]
            fq2 = reads[(sample, 2)]
            fh.write(
                f"{sample},{fq1.relative_to(REPO_ROOT).as_posix()},"
                f"{fq2.relative_to(REPO_ROOT).as_posix()},"
                f"{condition},{replicate}\n"
            )
    return path


def test_nextflow_stub_run_publishes_expected_artifacts(tmp_path):
    fixtures = _build_fixtures()
    samplesheet = _write_samplesheet(fixtures["reads"])
    outdir = tmp_path / "results"

    cmd = [
        NEXTFLOW,
        "run",
        "workflow",
        "-stub",
        "-profile",
        "standard",
        "--samplesheet",
        str(samplesheet),
        "--fasta",
        str(fixtures["fasta"]),
        "--gtf",
        str(fixtures["gtf"]),
        "--rseqc_bed",
        str(fixtures["bed"]),
        "--outdir",
        str(outdir),
    ]

    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=1800,
    )
    assert proc.returncode == 0, (
        f"nextflow -stub failed (rc={proc.returncode})\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )

    expected = [
        outdir / "counts" / "gene_counts.txt",
        outdir
        / "differential_expression"
        / "results"
        / "differential_expression"
        / "real_deseq2_results.csv",
        outdir / "multiqc" / "multiqc_report.html",
    ]
    for artifact in expected:
        assert artifact.is_file(), f"expected published artifact missing: {artifact}"
