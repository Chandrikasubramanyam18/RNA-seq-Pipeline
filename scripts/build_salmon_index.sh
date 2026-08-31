#!/usr/bin/env bash
# ==============================================================================
# Script: scripts/build_salmon_index.sh
# Purpose: Salmon quasi-mapping transcriptome index generation with decoy support
# ==============================================================================
set -euo pipefail

TRANSCRIPTS_FASTA="data/reference/transcripts.fa"
GENOME_FASTA=""
INDEX_DIR="data/reference/salmon_index"
THREADS=4
KMER_SIZE=31

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -t, --transcripts   Path to transcriptome FASTA (default: data/reference/transcripts.fa)"
    echo "  -g, --genome        Optional genome FASTA to generate decoy-aware index"
    echo "  -o, --outdir        Target directory for Salmon index (default: data/reference/salmon_index)"
    echo "  -p, --threads       Number of parallel threads (default: 4)"
    echo "  -k, --kmer          K-mer size for indexing (default: 31)"
    echo "  -h, --help          Display this help message"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--transcripts)
            TRANSCRIPTS_FASTA="$2"
            shift 2
            ;;
        -g|--genome)
            GENOME_FASTA="$2"
            shift 2
            ;;
        -o|--outdir)
            INDEX_DIR="$2"
            shift 2
            ;;
        -p|--threads)
            THREADS="$2"
            shift 2
            ;;
        -k|--kmer)
            KMER_SIZE="$2"
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
echo "                   Salmon Transcriptome Index Generation                        "
echo "================================================================================"
echo "Transcripts FASTA  : $TRANSCRIPTS_FASTA"
echo "Genome Decoy FASTA : ${GENOME_FASTA:-None (direct transcriptome indexing)}"
echo "Target Index Dir   : $INDEX_DIR"
echo "Worker Threads     : $THREADS"
echo "K-mer Size         : $KMER_SIZE"
echo "================================================================================"

if [[ ! -f "$TRANSCRIPTS_FASTA" ]]; then
    echo "ERROR: Transcriptome FASTA '$TRANSCRIPTS_FASTA' not found." >&2
    exit 1
fi

if ! command -v salmon &> /dev/null; then
    echo "ERROR: 'salmon' command not found in PATH." >&2
    echo "Please activate the conda environment: conda activate rnaseq-pipeline" >&2
    exit 1
fi

mkdir -p "$INDEX_DIR"

if [[ -n "$GENOME_FASTA" && -f "$GENOME_FASTA" ]]; then
    echo "[INFO] Creating decoy-aware transcriptome index..."
    DECOY_DIR=$(mktemp -d)
    DECOYS_FILE="$DECOY_DIR/decoys.txt"
    GENTROME_FASTA="$DECOY_DIR/gentrome.fa"

    # Extract genome chromosome names as decoys
    grep "^>" "$GENOME_FASTA" | cut -d " " -f 1 | sed -e 's/>//g' > "$DECOYS_FILE"
    
    # Concatenate transcripts and genome
    cat "$TRANSCRIPTS_FASTA" "$GENOME_FASTA" > "$GENTROME_FASTA"

    salmon index \
        -t "$GENTROME_FASTA" \
        -d "$DECOYS_FILE" \
        -i "$INDEX_DIR" \
        -p "$THREADS" \
        -k "$KMER_SIZE"

    rm -rf "$DECOY_DIR"
else
    echo "[INFO] Indexing transcriptome directly..."
    salmon index \
        -t "$TRANSCRIPTS_FASTA" \
        -i "$INDEX_DIR" \
        -p "$THREADS" \
        -k "$KMER_SIZE"
fi

echo "================================================================================"
echo "[SUCCESS] Salmon index generated in: $INDEX_DIR"
echo "================================================================================"
