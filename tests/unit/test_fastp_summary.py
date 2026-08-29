"""
Unit tests for fastp summary parser (scripts/python/summarize_fastp.py).
Tests metric extraction, Q20/Q30 calculations, adapter counts, and TSV writing.
"""

import sys
import json
import tempfile
from pathlib import Path

# Add scripts/python to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "python"))
from summarize_fastp import (
    parse_fastp_json,
    write_fastp_summary_tsv,
)

SAMPLE_FASTP_JSON = {
    "summary": {
        "before_filtering": {
            "total_reads": 20000000,
            "total_bases": 1260000000,
            "q20_bases": 1200000000,
            "q30_bases": 1100000000,
            "q20_rate": 0.952,
            "q30_rate": 0.873,
            "read1_mean_length": 63,
            "read2_mean_length": 63,
            "gc_content": 0.495
        },
        "after_filtering": {
            "total_reads": 19600000,
            "total_bases": 1230000000,
            "q20_bases": 1210000000,
            "q30_bases": 1150000000,
            "q20_rate": 0.984,
            "q30_rate": 0.935,
            "read1_mean_length": 62,
            "read2_mean_length": 62,
            "gc_content": 0.496
        }
    },
    "filtering_result": {
        "passed_filter_reads": 19600000,
        "low_quality_reads": 300000,
        "too_many_N_reads": 20000,
        "too_short_reads": 80000,
        "too_long_reads": 0
    },
    "adapter_cutting": {
        "adapter_trimmed_reads": 450000,
        "adapter_trimmed_bases": 12500000
    },
    "duplication": {
        "rate": 0.32
    }
}

def test_parse_fastp_json_valid():
    with tempfile.NamedTemporaryFile(mode="w", suffix="_fastp.json", delete=False, encoding="utf-8") as f:
        json.dump(SAMPLE_FASTP_JSON, f)
        p = Path(f.name)

    try:
        rec = parse_fastp_json(p)
        assert rec is not None
        assert rec["raw_total_reads"] == 20000000
        assert rec["clean_total_reads"] == 19600000
        assert rec["q20_rate_before_pct"] == 95.2
        assert rec["q20_rate_after_pct"] == 98.4
        assert rec["q30_rate_before_pct"] == 87.3
        assert rec["q30_rate_after_pct"] == 93.5
        assert rec["adapter_trimmed_reads"] == 450000
        assert rec["duplication_rate_pct"] == 32.0
    finally:
        p.unlink(missing_ok=True)

def test_parse_fastp_json_corrupted():
    with tempfile.NamedTemporaryFile(mode="w", suffix="_fastp.json", delete=False, encoding="utf-8") as f:
        f.write("{ invalid json")
        p = Path(f.name)

    try:
        rec = parse_fastp_json(p)
        assert rec is None
    finally:
        p.unlink(missing_ok=True)

def test_write_fastp_summary_tsv():
    with tempfile.NamedTemporaryFile(mode="w", suffix="_fastp.json", delete=False, encoding="utf-8") as f:
        json.dump(SAMPLE_FASTP_JSON, f)
        json_path = Path(f.name)

    tsv_path = json_path.with_suffix(".tsv")
    try:
        rec = parse_fastp_json(json_path)
        write_fastp_summary_tsv([rec], tsv_path)
        content = tsv_path.read_text(encoding="utf-8")
        assert "sample\traw_total_reads\tclean_total_reads" in content
        assert "20000000\t19600000" in content
    finally:
        json_path.unlink(missing_ok=True)
        tsv_path.unlink(missing_ok=True)

if __name__ == "__main__":
    print("[RUNNING] Executing fastp summary unit tests...")
    test_parse_fastp_json_valid()
    test_parse_fastp_json_corrupted()
    test_write_fastp_summary_tsv()
    print("[ALL PASSED] 3/3 fastp summary unit tests passed successfully!")
