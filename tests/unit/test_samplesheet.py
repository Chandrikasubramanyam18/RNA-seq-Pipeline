"""
Unit tests for samplesheet validation engine (scripts/python/validate_samplesheet.py).
Tests all edge cases: missing columns, duplicate samples, single conditions,
malformed extensions, paired-end file duplicates, and physical file checks.
"""

import tempfile
from pathlib import Path
import sys

# Add scripts directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "python"))
from validate_samplesheet import validate_samplesheet


def write_test_csv(content: str) -> Path:
    """Helper to create a temporary CSV file with given content."""
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", encoding="utf-8")
    tmp.write(content.strip())
    tmp.close()
    return Path(tmp.name)


def test_valid_samplesheet():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/C1_1.fastq.gz,data/raw/C1_2.fastq.gz,control,1
C2,data/raw/C2_1.fastq.gz,data/raw/C2_2.fastq.gz,control,2
T1,data/raw/T1_1.fastq.gz,data/raw/T1_2.fastq.gz,treatment,1
T2,data/raw/T2_1.fastq.gz,data/raw/T2_2.fastq.gz,treatment,2
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert is_valid, f"Expected valid samplesheet, got errors: {errors}"
        assert len(errors) == 0
    finally:
        p.unlink()


def test_missing_column():
    csv_text = """sample,fastq_1,fastq_2,replicate
C1,data/raw/C1_1.fastq.gz,data/raw/C1_2.fastq.gz,1
T1,data/raw/T1_1.fastq.gz,data/raw/T1_2.fastq.gz,1
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert not is_valid
        assert any("Missing required column" in e for e in errors)
    finally:
        p.unlink()


def test_duplicate_sample_id():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/C1_1.fastq.gz,data/raw/C1_2.fastq.gz,control,1
C1,data/raw/C2_1.fastq.gz,data/raw/C2_2.fastq.gz,control,2
T1,data/raw/T1_1.fastq.gz,data/raw/T1_2.fastq.gz,treatment,1
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert not is_valid
        assert any("Duplicate sample ID 'C1'" in e for e in errors)
    finally:
        p.unlink()


def test_single_condition_only():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/C1_1.fastq.gz,data/raw/C1_2.fastq.gz,control,1
C2,data/raw/C2_1.fastq.gz,data/raw/C2_2.fastq.gz,control,2
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert not is_valid
        assert any("requires at least 2 distinct conditions" in e for e in errors)
    finally:
        p.unlink()


def test_duplicate_fastq_assignment():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/shared_1.fastq.gz,data/raw/shared_2.fastq.gz,control,1
T1,data/raw/shared_1.fastq.gz,data/raw/T1_2.fastq.gz,treatment,1
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert not is_valid
        assert any("assigned to multiple samples" in e for e in errors)
    finally:
        p.unlink()


def test_identical_paired_end_files():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/C1_1.fastq.gz,data/raw/C1_1.fastq.gz,control,1
T1,data/raw/T1_1.fastq.gz,data/raw/T1_2.fastq.gz,treatment,1
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert not is_valid
        assert any("exact same file" in e for e in errors)
    finally:
        p.unlink()


def test_invalid_fastq_extension():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/C1_1.txt,data/raw/C1_2.fastq.gz,control,1
T1,data/raw/T1_1.fastq.gz,data/raw/T1_2.fastq.gz,treatment,1
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p)
        assert not is_valid
        assert any("recognized FASTQ extension" in e for e in errors)
    finally:
        p.unlink()


def test_file_existence_check():
    csv_text = """sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/nonexistent_1.fastq.gz,data/raw/nonexistent_2.fastq.gz,control,1
T1,data/raw/nonexistent_3.fastq.gz,data/raw/nonexistent_4.fastq.gz,treatment,1
"""
    p = write_test_csv(csv_text)
    try:
        is_valid, errors = validate_samplesheet(p, check_files_exist=True)
        assert not is_valid
        assert any("file does not exist" in e for e in errors)
    finally:
        p.unlink()


if __name__ == "__main__":
    print("[RUNNING] Executing samplesheet validation unit tests...")
    test_valid_samplesheet()
    test_missing_column()
    test_duplicate_sample_id()
    test_single_condition_only()
    test_duplicate_fastq_assignment()
    test_identical_paired_end_files()
    test_invalid_fastq_extension()
    test_file_existence_check()
    print("[ALL PASSED] 8/8 unit tests passed successfully!")
