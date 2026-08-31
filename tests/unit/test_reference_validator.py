"""
Unit tests for reference genome and GTF validator (scripts/python/validate_reference.py).
Tests chromosome compatibility, chr prefix mismatch detection, and GTF attributes.
"""

import sys
import tempfile
from pathlib import Path

# Add scripts/python to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "python"))
from validate_reference import validate_compatibility

def test_valid_reference():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".fa", delete=False, encoding="utf-8") as f_fa:
        f_fa.write(">chr1\nATGCATGC\n>chr2\nGGCCGGCC\n")
        p_fa = Path(f_fa.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".gtf", delete=False, encoding="utf-8") as f_gtf:
        f_gtf.write('chr1\tTEST\texon\t1\t100\t.\t+\t.\tgene_id "ENSG001"; transcript_id "ENST001"; gene_name "GENE1";\n')
        p_gtf = Path(f_gtf.name)

    try:
        is_valid, errors = validate_compatibility(p_fa, p_gtf)
        assert is_valid, f"Expected valid, got errors: {errors}"
        assert len(errors) == 0
    finally:
        p_fa.unlink(missing_ok=True)
        p_gtf.unlink(missing_ok=True)

def test_chr_prefix_mismatch():
    # FASTA has 'chr1', GTF has '1'
    with tempfile.NamedTemporaryFile(mode="w", suffix=".fa", delete=False, encoding="utf-8") as f_fa:
        f_fa.write(">chr1\nATGCATGC\n")
        p_fa = Path(f_fa.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".gtf", delete=False, encoding="utf-8") as f_gtf:
        f_gtf.write('1\tTEST\texon\t1\t100\t.\t+\t.\tgene_id "ENSG001"; transcript_id "ENST001";\n')
        p_gtf = Path(f_gtf.name)

    try:
        is_valid, errors = validate_compatibility(p_fa, p_gtf)
        assert not is_valid
        assert any("Chromosome naming incompatibility" in e for e in errors)
    finally:
        p_fa.unlink(missing_ok=True)
        p_gtf.unlink(missing_ok=True)

def test_missing_fasta_file():
    is_valid, errors = validate_compatibility(Path("nonexistent.fa"), Path("nonexistent.gtf"))
    assert not is_valid
    assert any("not found" in e for e in errors)

def test_missing_gene_id():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".fa", delete=False, encoding="utf-8") as f_fa:
        f_fa.write(">chr1\nATGCATGC\n")
        p_fa = Path(f_fa.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".gtf", delete=False, encoding="utf-8") as f_gtf:
        f_gtf.write('chr1\tTEST\texon\t1\t100\t.\t+\t.\ttranscript_id "ENST001";\n')
        p_gtf = Path(f_gtf.name)

    try:
        is_valid, errors = validate_compatibility(p_fa, p_gtf)
        assert not is_valid
        assert any("gene_id" in e for e in errors)
    finally:
        p_fa.unlink(missing_ok=True)
        p_gtf.unlink(missing_ok=True)

if __name__ == "__main__":
    print("[RUNNING] Executing reference validator unit tests...")
    test_valid_reference()
    test_chr_prefix_mismatch()
    test_missing_fasta_file()
    test_missing_gene_id()
    print("[ALL PASSED] 4/4 reference validator unit tests passed successfully!")
