#!/usr/bin/env bash
# ==============================================================================
# Script: scripts/build_star_index.sh
# Purpose: Splice-aware STAR genome index generation with junction databases
# ==============================================================================
set -euo pipefail

GENOME_FASTA="data/reference/genome.fa"
ANNOTATION_GTF="data/reference/genes.gtf"
INDEX_DIR="data/reference/star_index"
THREADS=4
READ_LENGTH=63
SA_INDEX_NBASES=14

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -f, --fasta       Path to reference genome FASTA (default: data/reference/genome.fa)"
    echo "  -g, --gtf         Path to gene annotation GTF (default: data/reference/genes.gtf)"
    echo "  -o, --outdir      Target directory for STAR index (default: data/reference/star_index)"
    echo "  -t, --threads     Number of parallel worker threads (default: 4)"
    echo "  -r, --read-len    Sequencing read length in bp (default: 63)"
    echo "  -s, --sa-bases    genomeSAindexNbases (default: 14 for human; reduce for mini-genomes)"
    echo "  -h, --help        Display this help message"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--fasta)
            GENOME_FASTA="$2"
            shift 2
            ;;
        -g|--gtf)
            ANNOTATION_GTF="$2"
            shift 2
            ;;
        -o|--outdir)
            INDEX_DIR="$2"
            shift 2
            ;;
        -t|--threads)
            THREADS="$2"
            shift 2
            ;;
        -r|--read-len)
            READ_LENGTH="$2"
            shift 2
            ;;
        -s|--sa-bases)
            SA_INDEX_NBASES="$2"
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

SJDB_OVERHANG=$((READ_LENGTH - 1))

echo "================================================================================"
echo "                   STAR Genome Index Generation                                 "
echo "================================================================================"
echo "Genome FASTA       : $GENOME_FASTA"
echo "Annotation GTF     : $ANNOTATION_GTF"
echo "Target Index Dir   : $INDEX_DIR"
echo "Worker Threads     : $THREADS"
echo "Read Length        : $READ_LENGTH bp (sjdbOverhang = $SJDB_OVERHANG)"
echo "genomeSAindexNbases: $SA_INDEX_NBASES"
echo "================================================================================"

if [[ ! -f "$GENOME_FASTA" ]]; then
    echo "ERROR: Genome FASTA '$GENOME_FASTA' does not exist." >&2
    exit 1
fi
if [[ ! -f "$ANNOTATION_GTF" ]]; then
    echo "ERROR: Annotation GTF '$ANNOTATION_GTF' does not exist." >&2
    exit 1
fi

if ! command -v STAR &> /dev/null; then
    echo "ERROR: 'STAR' command not found in PATH." >&2
    echo "Please activate the conda environment: conda activate rnaseq-pipeline" >&2
    exit 1
fi

# Pre-flight compatibility validation
if command -v python3 &> /dev/null; then
    echo "[INFO] Verifying FASTA and GTF chromosome compatibility..."
    python3 scripts/python/validate_reference.py --fasta "$GENOME_FASTA" --gtf "$ANNOTATION_GTF"
fi

mkdir -p "$INDEX_DIR"

echo "[INFO] Executing STAR genomeGenerate..."
STAR \
    --runMode genomeGenerate \
    --runThreadN "$THREADS" \
    --genomeDir "$INDEX_DIR" \
    --genomeFastaFiles "$GENOME_FASTA" \
    --sjdbGTFfile "$ANNOTATION_GTF" \
    --sjdbOverhang "$SJDB_OVERHANG" \
    --genomeSAindexNbases "$SA_INDEX_NBASES"

echo "================================================================================"
echo "[SUCCESS] STAR Genome Index created in: $INDEX_DIR"
echo "================================================================================"
