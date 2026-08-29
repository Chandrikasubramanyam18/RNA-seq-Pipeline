#!/usr/bin/env python3
"""
FastQC Summary Table Generator.
Parses FastQC data from extracted directories or .zip archives and generates
a unified tabular TSV summary of sequence quality metrics and module statuses.
"""

import sys
import os
import zipfile
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

MODULE_KEYS = [
    "Per base sequence quality",
    "Per tile sequence quality",
    "Per sequence quality scores",
    "Per base sequence content",
    "Per sequence GC content",
    "Per base N content",
    "Sequence Length Distribution",
    "Sequence Duplication Levels",
    "Overrepresented sequences",
    "Adapter Content",
]

def parse_fastqc_data_text(text: str) -> Dict[str, Any]:
    """
    Parses the contents of a fastqc_data.txt file.
    Returns a dictionary of extracted basic statistics and module statuses.
    """
    record: Dict[str, Any] = {
        "filename": "",
        "file_type": "",
        "encoding": "",
        "total_sequences": 0,
        "sequences_poor_quality": 0,
        "sequence_length": "",
        "gc_percent": 0.0,
    }
    for mod in MODULE_KEYS:
        record[mod] = "NOT_FOUND"

    lines = text.splitlines()
    in_basic_stats = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith(">>Basic Statistics"):
            in_basic_stats = True
            continue
        elif line.startswith(">>END_MODULE"):
            in_basic_stats = False
            continue
        elif line.startswith(">>"):
            parts = line[2:].split("\t")
            mod_name = parts[0]
            status = parts[1] if len(parts) > 1 else "UNKNOWN"
            if mod_name in record:
                record[mod_name] = status
            continue

        if in_basic_stats and "\t" in line and not line.startswith("#"):
            key, val = line.split("\t", 1)
            key = key.strip()
            val = val.strip()
            if key == "Filename":
                record["filename"] = val
            elif key == "File type":
                record["file_type"] = val
            elif key == "Encoding":
                record["encoding"] = val
            elif key == "Total Sequences":
                try:
                    record["total_sequences"] = int(val)
                except ValueError:
                    record["total_sequences"] = val
            elif key == "Sequences flagged as poor quality":
                try:
                    record["sequences_poor_quality"] = int(val)
                except ValueError:
                    record["sequences_poor_quality"] = val
            elif key == "Sequence length":
                record["sequence_length"] = val
            elif key == "%GC":
                try:
                    record["gc_percent"] = float(val)
                except ValueError:
                    record["gc_percent"] = val

    return record

def extract_from_zip(zip_path: Path) -> Optional[Dict[str, Any]]:
    """Extracts and parses fastqc_data.txt from a FastQC zip archive."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                if member.endswith("fastqc_data.txt"):
                    with zf.open(member) as f:
                        content = f.read().decode("utf-8", errors="replace")
                        rec = parse_fastqc_data_text(content)
                        if not rec["filename"]:
                            rec["filename"] = zip_path.stem.replace("_fastqc", "")
                        return rec
    except Exception as e:
        print(f"[WARNING] Could not parse zip {zip_path}: {e}", file=sys.stderr)
    return None

def extract_from_dir(dir_path: Path) -> Optional[Dict[str, Any]]:
    """Extracts and parses fastqc_data.txt from an extracted FastQC directory."""
    data_file = dir_path / "fastqc_data.txt"
    if data_file.exists():
        try:
            content = data_file.read_text(encoding="utf-8", errors="replace")
            rec = parse_fastqc_data_text(content)
            if not rec["filename"]:
                rec["filename"] = dir_path.stem.replace("_fastqc", "")
            return rec
        except Exception as e:
            print(f"[WARNING] Could not parse {data_file}: {e}", file=sys.stderr)
    return None

def summarize_fastqc_dir(input_dir: Path) -> List[Dict[str, Any]]:
    """Scans input_dir for FastQC zip files or extracted folders and aggregates results."""
    records: List[Dict[str, Any]] = []
    if not input_dir.exists():
        return records

    # 1. Check extracted directories
    for child in input_dir.iterdir():
        if child.is_dir() and (child / "fastqc_data.txt").exists():
            rec = extract_from_dir(child)
            if rec:
                records.append(rec)

    # 2. If no extracted dirs or check zip archives directly
    if not records:
        for zip_file in input_dir.glob("*_fastqc.zip"):
            rec = extract_from_zip(zip_file)
            if rec:
                records.append(rec)

    return sorted(records, key=lambda x: str(x.get("filename", "")))

def write_summary_tsv(records: List[Dict[str, Any]], output_file: Path) -> None:
    """Writes parsed records to a clean TSV file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "filename",
        "total_sequences",
        "sequences_poor_quality",
        "sequence_length",
        "gc_percent",
        "encoding",
    ] + MODULE_KEYS

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r)

def main():
    parser = argparse.ArgumentParser(description="Summarize FastQC metrics into a clean TSV report.")
    parser.add_argument("--input-dir", "-i", type=Path, default=Path("results/fastqc/raw"), help="Directory containing FastQC outputs")
    parser.add_argument("--output", "-o", type=Path, default=Path("results/fastqc/raw/fastqc_summary.tsv"), help="Output TSV path")
    args = parser.parse_args()

    print(f"[INFO] Scanning FastQC results in: {args.input_dir}")
    records = summarize_fastqc_dir(args.input_dir)

    if not records:
        print(f"[WARNING] No FastQC reports found in '{args.input_dir}'.")
        print(f"          Summary file will not be generated until FastQC runs.")
        sys.exit(0)

    write_summary_tsv(records, args.output)
    print(f"[SUCCESS] Summarized {len(records)} sample(s) into: {args.output}")

if __name__ == "__main__":
    main()
