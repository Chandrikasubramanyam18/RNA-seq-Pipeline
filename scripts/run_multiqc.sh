#!/usr/bin/env bash
# ==============================================================================
# Script: scripts/run_multiqc.sh
# Purpose: Aggregate QC statistics from multiple bioinformatics tools into MultiQC
# ==============================================================================
set -euo pipefail

INPUT_DIR="results/fastqc/raw"
OUTPUT_DIR="results/multiqc/raw_fastqc"
REPORT_TITLE="Raw Reads QC Report (FastQC)"

usage() {
    echo "Usage: $0 [--input <dir>] [--output <dir>] [--title <string>]"
    echo ""
    echo "Options:"
    echo "  -i, --input    Input directory containing QC logs/reports (default: results/fastqc/raw)"
    echo "  -o, --output   Output directory for MultiQC report (default: results/multiqc/raw_fastqc)"
    echo "  -t, --title    Title for the MultiQC interactive report"
    echo "  -h, --help     Display this help message"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--input)
            INPUT_DIR="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -t|--title)
            REPORT_TITLE="$2"
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
echo "                   MultiQC Report Aggregation                                   "
echo "================================================================================"
echo "Input Directory : $INPUT_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "Report Title    : $REPORT_TITLE"
echo "================================================================================"

if [[ ! -d "$INPUT_DIR" ]]; then
    echo "ERROR: Input directory '$INPUT_DIR' does not exist." >&2
    exit 1
fi

if ! command -v multiqc &> /dev/null; then
    echo "ERROR: 'multiqc' command not found in PATH." >&2
    echo "Please activate the conda environment: conda activate rnaseq-pipeline" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "[INFO] Aggregating QC metrics from '$INPUT_DIR'..."
multiqc \
    "$INPUT_DIR" \
    --outdir "$OUTPUT_DIR" \
    --title "$REPORT_TITLE" \
    --filename "multiqc_report.html" \
    --force

echo "================================================================================"
echo "[SUCCESS] MultiQC aggregation complete."
echo "Report file: $OUTPUT_DIR/multiqc_report.html"
echo "================================================================================"
