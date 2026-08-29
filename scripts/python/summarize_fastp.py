#!/usr/bin/env python3
"""
fastp JSON Summary Generator.
Parses fastp JSON logs across samples and produces a comprehensive tabular TSV summary
comparing read counts, filtering rates, Q20/Q30 quality improvement, and adapter trimming.
"""

import sys
import json
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

def parse_fastp_json(json_path: Path) -> Optional[Dict[str, Any]]:
    """Parses a single fastp JSON report and extracts key QC and trimming metrics."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        summary = data.get("summary", {})
        before = summary.get("before_filtering", {})
        after = summary.get("after_filtering", {})
        filt = data.get("filtering_result", {})
        adapters = data.get("adapter_cutting", {})
        dup = data.get("duplication", {})

        sample_name = json_path.stem.replace("_fastp", "")

        raw_reads = before.get("total_reads", 0)
        clean_reads = after.get("total_reads", 0)
        filter_rate = ((raw_reads - clean_reads) / raw_reads * 100.0) if raw_reads > 0 else 0.0

        return {
            "sample": sample_name,
            "raw_total_reads": raw_reads,
            "clean_total_reads": clean_reads,
            "passed_filter_reads": filt.get("passed_filter_reads", clean_reads),
            "low_quality_reads": filt.get("low_quality_reads", 0),
            "too_short_reads": filt.get("too_short_reads", 0),
            "too_many_N_reads": filt.get("too_many_N_reads", 0),
            "filter_drop_rate_pct": round(filter_rate, 2),
            "q20_rate_before_pct": round(before.get("q20_rate", 0.0) * 100.0, 2),
            "q20_rate_after_pct": round(after.get("q20_rate", 0.0) * 100.0, 2),
            "q30_rate_before_pct": round(before.get("q30_rate", 0.0) * 100.0, 2),
            "q30_rate_after_pct": round(after.get("q30_rate", 0.0) * 100.0, 2),
            "gc_content_before_pct": round(before.get("gc_content", 0.0) * 100.0, 2),
            "gc_content_after_pct": round(after.get("gc_content", 0.0) * 100.0, 2),
            "adapter_trimmed_reads": adapters.get("adapter_trimmed_reads", 0),
            "adapter_trimmed_bases": adapters.get("adapter_trimmed_bases", 0),
            "duplication_rate_pct": round(dup.get("rate", 0.0) * 100.0, 2),
        }
    except Exception as e:
        print(f"[WARNING] Failed to parse fastp JSON {json_path}: {e}", file=sys.stderr)
        return None

def summarize_fastp_dir(input_dir: Path) -> List[Dict[str, Any]]:
    """Scans directory for fastp JSON reports and returns a list of summary records."""
    records: List[Dict[str, Any]] = []
    if not input_dir.exists():
        return records

    for json_file in sorted(input_dir.glob("*fastp.json")):
        rec = parse_fastp_json(json_file)
        if rec:
            records.append(rec)
    return records

def write_fastp_summary_tsv(records: List[Dict[str, Any]], output_file: Path) -> None:
    """Writes extracted fastp metrics to a TSV file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return

    fieldnames = list(records[0].keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for r in records:
            writer.writerow(r)

def main():
    parser = argparse.ArgumentParser(description="Aggregate fastp JSON reports into a clean TSV summary.")
    parser.add_argument("--input-dir", "-i", type=Path, default=Path("results/fastp"), help="Directory containing fastp JSON files")
    parser.add_argument("--output", "-o", type=Path, default=Path("results/fastp/fastp_summary.tsv"), help="Output TSV path")
    args = parser.parse_args()

    print(f"[INFO] Scanning fastp JSON reports in: {args.input_dir}")
    records = summarize_fastp_dir(args.input_dir)

    if not records:
        print(f"[WARNING] No fastp JSON files found in '{args.input_dir}'.")
        sys.exit(0)

    write_fastp_summary_tsv(records, args.output)
    print(f"[SUCCESS] Summarized {len(records)} sample(s) into: {args.output}")

if __name__ == "__main__":
    main()
