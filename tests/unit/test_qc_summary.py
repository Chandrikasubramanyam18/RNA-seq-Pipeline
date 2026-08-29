"""
Unit tests for FastQC summary parser (scripts/python/summarize_fastqc.py).
Tests valid parsing, empty data handling, zip extraction, and TSV output generation.
"""

import sys
import zipfile
import tempfile
from pathlib import Path

# Add scripts/python to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "python"))
from summarize_fastqc import (
    parse_fastqc_data_text,
    extract_from_zip,
    write_summary_tsv,
    MODULE_KEYS,
)

SAMPLE_FASTQC_DATA = """##FastQC	0.12.1
>>Basic Statistics	pass
#Measure	Value
Filename	SRR1039508_1.fastq.gz
File type	Conventional base calls
Encoding	Sanger / Illumina 1.9
Total Sequences	1000000
Sequences flagged as poor quality	0
Sequence length	63
%GC	49
>>END_MODULE
>>Per base sequence quality	pass
#Base	Mean	Median	Lower Quartile	Upper Quartile	10th Percentile	90th Percentile
1	35.2	36.0	34.0	38.0	30.0	38.0
>>END_MODULE
>>Per sequence GC content	warn
#GC Content	Count
0	0.0
>>END_MODULE
>>Sequence Duplication Levels	pass
#Duplication Level	Percentage of deduplicated	Percentage of total
1	65.0	40.0
>>END_MODULE
>>Adapter Content	pass
#Position	Illumina Universal Adapter
1	0.0
>>END_MODULE
"""

def test_parse_fastqc_data_valid():
    rec = parse_fastqc_data_text(SAMPLE_FASTQC_DATA)
    assert rec["filename"] == "SRR1039508_1.fastq.gz"
    assert rec["total_sequences"] == 1000000
    assert rec["sequence_length"] == "63"
    assert rec["gc_percent"] == 49.0
    assert rec["Per base sequence quality"] == "pass"
    assert rec["Per sequence GC content"] == "warn"
    assert rec["Adapter Content"] == "pass"

def test_parse_fastqc_data_empty():
    rec = parse_fastqc_data_text("")
    assert rec["total_sequences"] == 0
    assert rec["gc_percent"] == 0.0
    for mod in MODULE_KEYS:
        assert rec[mod] == "NOT_FOUND"

def test_parse_fastqc_data_malformed():
    malformed = ">>Basic Statistics\nSome bad line\n>>END_MODULE\n"
    rec = parse_fastqc_data_text(malformed)
    assert rec["filename"] == ""
    assert rec["total_sequences"] == 0

def test_extract_from_zip():
    with tempfile.NamedTemporaryFile(suffix="_fastqc.zip", delete=False) as tmp_zip:
        zip_path = Path(tmp_zip.name)

    try:
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("SRR1039508_1_fastqc/fastqc_data.txt", SAMPLE_FASTQC_DATA)

        rec = extract_from_zip(zip_path)
        assert rec is not None
        assert rec["filename"] == "SRR1039508_1.fastq.gz"
        assert rec["total_sequences"] == 1000000
    finally:
        zip_path.unlink(missing_ok=True)

def test_write_summary_tsv():
    rec = parse_fastqc_data_text(SAMPLE_FASTQC_DATA)
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as tmp_tsv:
        tsv_path = Path(tmp_tsv.name)

    try:
        write_summary_tsv([rec], tsv_path)
        content = tsv_path.read_text(encoding="utf-8")
        assert "filename\ttotal_sequences" in content
        assert "SRR1039508_1.fastq.gz\t1000000" in content
    finally:
        tsv_path.unlink(missing_ok=True)

if __name__ == "__main__":
    print("[RUNNING] Executing FastQC summary unit tests...")
    test_parse_fastqc_data_valid()
    test_parse_fastqc_data_empty()
    test_parse_fastqc_data_malformed()
    test_extract_from_zip()
    test_write_summary_tsv()
    print("[ALL PASSED] 5/5 FastQC summary unit tests passed successfully!")
