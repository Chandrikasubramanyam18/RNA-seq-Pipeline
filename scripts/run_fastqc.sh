#!/usr/bin/env bash
# ==============================================================================
# Script: scripts/run_fastqc.sh
# Purpose: High-throughput Quality Control for raw/processed FASTQ files
# ==============================================================================
set -euo pipefail

# Defaults
INPUT_DIR="data/raw"
OUTPUT_DIR="results/fastqc/raw"
THREADS=4

usage() {
    echo "Usage: $0 [--input <dir>] [--output <dir>] [--threads <int>]"
    echo ""
    echo "Options:"
    echo "  -i, --input    Input directory containing FASTQ files (default: data/raw)"
    echo "  -o, --output   Output directory for FastQC reports (default: results/fastqc/raw)"
    echo "  -t, --threads  Number of parallel worker threads (default: 4)"
    echo "  -h, --help     Display this help message"
    exit 1
}

# Parse command-line flags
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
        -t|--threads)
            THREADS="$2"
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
echo "                   FastQC Quality Assessment Execution                          "
echo "================================================================================"
echo "Input Directory : $INPUT_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "Threads         : $THREADS"
echo "================================================================================"

# Verify input directory exists
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "ERROR: Input directory '$INPUT_DIR' does not exist." >&2
    exit 1
fi

# Find FASTQ files
shopt -s nullglob
FASTQ_FILES=("$INPUT_DIR"/*.fastq.gz "$INPUT_DIR"/*.fq.gz "$INPUT_DIR"/*.fastq "$INPUT_DIR"/*.fq)
shopt -u nullglob

if [[ ${#FASTQ_FILES[@]} -eq 0 ]]; then
    echo "ERROR: No FASTQ files (*.fastq.gz, *.fq.gz, *.fastq, *.fq) found in '$INPUT_DIR'." >&2
    exit 1
fi

echo "Found ${#FASTQ_FILES[@]} FASTQ file(s) for QC analysis."

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Verify FastQC is installed
if ! command -v fastqc &> /dev/null; then
    echo "ERROR: 'fastqc' command not found in PATH." >&2
    echo "Please activate the conda environment: conda activate rnaseq-pipeline" >&2
    exit 1
fi

# Execute FastQC
echo "[INFO] Running FastQC across ${#FASTQ_FILES[@]} files using $THREADS thread(s)..."
fastqc \
    --threads "$THREADS" \
    --outdir "$OUTPUT_DIR" \
    --extract \
    "${FASTQ_FILES[@]}"

echo "================================================================================"
echo "[SUCCESS] FastQC completed successfully."
echo "Reports generated in: $OUTPUT_DIR"
echo "================================================================================"
