#!/usr/bin/env bash
# ==============================================================================
# Script: scripts/run_fastp.sh
# Purpose: Ultra-fast read preprocessing, adapter clipping, and quality filtering
# ==============================================================================
set -euo pipefail

SAMPLESHEET="metadata/samplesheet.csv"
OUTPUT_FASTQ_DIR="data/processed"
OUTPUT_REPORT_DIR="results/fastp"
THREADS=4
QUAL_PHRED=20
MIN_LENGTH=30

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -s, --samplesheet   Path to sample design CSV (default: metadata/samplesheet.csv)"
    echo "  -o, --out-fastq     Directory for cleaned FASTQ files (default: data/processed)"
    echo "  -r, --out-report    Directory for fastp HTML/JSON logs (default: results/fastp)"
    echo "  -t, --threads       Number of parallel threads per sample (default: 4)"
    echo "  -q, --quality       Qualified quality Phred score cutoff (default: 20 -> 99% accuracy)"
    echo "  -l, --min-length    Minimum read length filter after trimming (default: 30)"
    echo "  -h, --help          Display this help message"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--samplesheet)
            SAMPLESHEET="$2"
            shift 2
            ;;
        -o|--out-fastq)
            OUTPUT_FASTQ_DIR="$2"
            shift 2
            ;;
        -r|--out-report)
            OUTPUT_REPORT_DIR="$2"
            shift 2
            ;;
        -t|--threads)
            THREADS="$2"
            shift 2
            ;;
        -q|--quality)
            QUAL_PHRED="$2"
            shift 2
            ;;
        -l|--min-length)
            MIN_LENGTH="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "ERROR: Unknown option '$1'"
            usage
            ;;
    esac
done

echo "================================================================================"
echo "                   fastp Read Preprocessing Execution                           "
echo "================================================================================"
echo "Samplesheet        : $SAMPLESHEET"
echo "Processed Data Dir : $OUTPUT_FASTQ_DIR"
echo "Report Output Dir  : $OUTPUT_REPORT_DIR"
echo "Threads per Sample : $THREADS"
echo "Quality Threshold  : Q >= $QUAL_PHRED"
echo "Minimum Length     : $MIN_LENGTH bp"
echo "================================================================================"

if [[ ! -f "$SAMPLESHEET" ]]; then
    echo "ERROR: Samplesheet '$SAMPLESHEET' not found." >&2
    exit 1
fi

if ! command -v fastp &> /dev/null; then
    echo "ERROR: 'fastp' command not found in PATH." >&2
    echo "Please activate the conda environment: conda activate rnaseq-pipeline" >&2
    exit 1
fi

mkdir -p "$OUTPUT_FASTQ_DIR" "$OUTPUT_REPORT_DIR"

# Parse CSV skipping header
# Format: sample,fastq_1,fastq_2,condition,replicate
tail -n +2 "$SAMPLESHEET" | while IFS=',' read -r sample f1 f2 condition replicate; do
    # Trim potential carriage return / whitespace
    sample=$(echo "$sample" | tr -d '\r\n ')
    f1=$(echo "$f1" | tr -d '\r\n ')
    f2=$(echo "$f2" | tr -d '\r\n ')

    if [[ -z "$sample" || -z "$f1" ]]; then
        continue
    fi

    out_r1="$OUTPUT_FASTQ_DIR/${sample}_trimmed_R1.fastq.gz"
    out_r2="$OUTPUT_FASTQ_DIR/${sample}_trimmed_R2.fastq.gz"
    html_report="$OUTPUT_REPORT_DIR/${sample}_fastp.html"
    json_report="$OUTPUT_REPORT_DIR/${sample}_fastp.json"

    echo ""
    echo ">>> Processing Sample: $sample"
    echo "    Input R1: $f1"

    if [[ -n "$f2" && "$f2" != "null" ]]; then
        echo "    Input R2: $f2"
        fastp \
            --in1 "$f1" \
            --in2 "$f2" \
            --out1 "$out_r1" \
            --out2 "$out_r2" \
            --html "$html_report" \
            --json "$json_report" \
            --thread "$THREADS" \
            --qualified_quality_phred "$QUAL_PHRED" \
            --length_required "$MIN_LENGTH" \
            --detect_adapter_for_pe \
            --trim_poly_g \
            --trim_poly_x \
            --report_title "fastp report: $sample"
    else
        echo "    Layout  : Single-End"
        fastp \
            --in1 "$f1" \
            --out1 "$out_r1" \
            --html "$html_report" \
            --json "$json_report" \
            --thread "$THREADS" \
            --qualified_quality_phred "$QUAL_PHRED" \
            --length_required "$MIN_LENGTH" \
            --trim_poly_g \
            --trim_poly_x \
            --report_title "fastp report: $sample"
    fi

    echo "    [DONE] Cleaned reads -> $out_r1"
    echo "           Report HTML   -> $html_report"
    echo "           Report JSON   -> $json_report"
done

echo ""
echo "================================================================================"
echo "[SUCCESS] fastp preprocessing completed for all samples."
echo "Cleaned FASTQ files in : $OUTPUT_FASTQ_DIR"
echo "Quality logs in        : $OUTPUT_REPORT_DIR"
echo "================================================================================"
