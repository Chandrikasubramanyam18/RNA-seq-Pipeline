#!/usr/bin/env python3
"""
Production-Grade Samplesheet Validator for RNA-seq Pipeline.
Performs comprehensive validation on sample metadata before workflow execution.
"""

import sys
import csv
import re
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple

REQUIRED_COLUMNS = ["sample", "fastq_1", "fastq_2", "condition", "replicate"]
VALID_FASTQ_EXTENSIONS = (".fastq.gz", ".fq.gz", ".fastq", ".fq")
SAMPLE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

class ValidationError(Exception):
    """Custom exception for structured validation errors."""
    pass

def validate_samplesheet(
    filepath: Path,
    check_files_exist: bool = False,
    single_end: bool = False
) -> Tuple[bool, List[str]]:
    """
    Validates a samplesheet against pipeline integrity rules.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []
    
    if not filepath.exists():
        return False, [f"ERROR: Samplesheet file not found: {filepath}"]

    try:
        with open(filepath, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            if not headers:
                return False, [f"ERROR: Samplesheet {filepath} is empty or has no header line."]
            
            # 1. Check required columns
            expected_cols = ["sample", "fastq_1", "condition", "replicate"]
            if not single_end:
                expected_cols.append("fastq_2")
                
            missing_cols = [col for col in expected_cols if col not in headers]
            if missing_cols:
                errors.append(f"ERROR: Missing required column(s): {', '.join(missing_cols)}")
                return False, errors

            rows: List[Dict[str, str]] = list(reader)
            if not rows:
                errors.append(f"ERROR: Samplesheet {filepath} contains headers but no sample rows.")
                return False, errors

            seen_samples: Set[str] = set()
            seen_fastqs: Set[str] = set()
            conditions: Set[str] = set()
            
            for row_idx, row in enumerate(rows, start=2):  # row 1 is header
                # Check for empty / whitespace values
                for col in expected_cols:
                    val = row.get(col, "")
                    if val is None or not val.strip():
                        errors.append(f"ERROR: Row {row_idx}: Column '{col}' is empty or whitespace.")

                sample_id = row.get("sample", "").strip()
                f1 = row.get("fastq_1", "").strip()
                f2 = row.get("fastq_2", "").strip() if not single_end else ""
                condition = row.get("condition", "").strip()
                replicate = row.get("replicate", "").strip()

                # 2. Sample ID uniqueness & format
                if sample_id:
                    if not SAMPLE_ID_PATTERN.match(sample_id):
                        errors.append(
                            f"ERROR: Row {row_idx}: Sample ID '{sample_id}' contains invalid characters. "
                            "Only alphanumeric characters, underscores, and hyphens are allowed."
                        )
                    if sample_id in seen_samples:
                        errors.append(f"ERROR: Row {row_idx}: Duplicate sample ID '{sample_id}' detected.")
                    seen_samples.add(sample_id)

                # 3. Condition validation
                if condition:
                    conditions.add(condition)
                    if not SAMPLE_ID_PATTERN.match(condition):
                        errors.append(
                            f"ERROR: Row {row_idx}: Condition '{condition}' contains invalid characters."
                        )

                # 4. Replicate validation
                if replicate:
                    if not (replicate.isdigit() and int(replicate) > 0):
                        errors.append(
                            f"ERROR: Row {row_idx}: Replicate '{replicate}' must be a positive integer."
                        )

                # 5. FASTQ path & extension validation
                if f1:
                    if not any(f1.lower().endswith(ext) for ext in VALID_FASTQ_EXTENSIONS):
                        errors.append(
                            f"ERROR: Row {row_idx}: fastq_1 '{f1}' does not have a recognized FASTQ extension "
                            f"({', '.join(VALID_FASTQ_EXTENSIONS)})."
                        )
                    if f1 in seen_fastqs:
                        errors.append(f"ERROR: Row {row_idx}: FASTQ file '{f1}' is assigned to multiple samples.")
                    seen_fastqs.add(f1)

                if not single_end and f2:
                    if not any(f2.lower().endswith(ext) for ext in VALID_FASTQ_EXTENSIONS):
                        errors.append(
                            f"ERROR: Row {row_idx}: fastq_2 '{f2}' does not have a recognized FASTQ extension."
                        )
                    if f1 == f2:
                        errors.append(
                            f"ERROR: Row {row_idx}: fastq_1 and fastq_2 point to the exact same file: '{f1}'."
                        )
                    if f2 in seen_fastqs:
                        errors.append(f"ERROR: Row {row_idx}: FASTQ file '{f2}' is assigned to multiple samples.")
                    seen_fastqs.add(f2)

                # 6. Physical file existence check (optional / on-demand)
                if check_files_exist:
                    base_dir = filepath.parent.parent  # relative to workspace root
                    p1 = Path(f1) if Path(f1).is_absolute() else base_dir / f1
                    if not p1.exists():
                        errors.append(f"ERROR: Row {row_idx}: fastq_1 file does not exist: '{p1}'")
                    if not single_end and f2:
                        p2 = Path(f2) if Path(f2).is_absolute() else base_dir / f2
                        if not p2.exists():
                            errors.append(f"ERROR: Row {row_idx}: fastq_2 file does not exist: '{p2}'")

            # 7. Check experimental conditions count
            if len(conditions) < 2:
                errors.append(
                    f"ERROR: Differential expression requires at least 2 distinct conditions. "
                    f"Found: {list(conditions)}"
                )

    except Exception as e:
        errors.append(f"ERROR: Failed to read samplesheet: {str(e)}")

    is_valid = len(errors) == 0
    return is_valid, errors

def main():
    parser = argparse.ArgumentParser(
        description="Validate samplesheet CSV format and integrity for RNA-seq analysis."
    )
    parser.add_argument(
        "samplesheet",
        type=Path,
        help="Path to samplesheet CSV file (e.g., metadata/samplesheet.csv)"
    )
    parser.add_argument(
        "--check-files-exist",
        action="store_true",
        help="Verify that FASTQ files physically exist on the filesystem"
    )
    parser.add_argument(
        "--single-end",
        action="store_true",
        help="Allow single-end data (omit fastq_2 requirement)"
    )

    args = parser.parse_args()

    print(f"[INFO] Validating samplesheet: {args.samplesheet}")
    is_valid, errors = validate_samplesheet(
        args.samplesheet,
        check_files_exist=args.check_files_exist,
        single_end=args.single_end
    )

    if is_valid:
        print("[SUCCESS] Samplesheet validation PASSED.")
        print(f"         All format and consistency criteria are satisfied.")
        sys.exit(0)
    else:
        print(f"[FAILED] Samplesheet validation FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  * {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
