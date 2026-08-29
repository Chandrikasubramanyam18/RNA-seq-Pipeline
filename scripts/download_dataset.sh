#!/usr/bin/env bash
# ==============================================================================
# Script: scripts/download_dataset.sh
# Purpose: Reproducible download and checksum verification for GSE52778 RNA-seq data
# Source: EMBL-EBI European Nucleotide Archive (ENA) / NCBI SRA
# ==============================================================================
set -euo pipefail

DATA_DIR="data/raw"
mkdir -p "$DATA_DIR"

echo "================================================================================"
echo "    Downloading GSE52778 Benchmark RNA-seq Dataset (Airway Smooth Muscle)      "
echo "================================================================================"

# Array of ENA FTP URLs (HTTP/FTP mirrors)
URLS=(
    # C1 (SRR1039508)
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/008/SRR1039508/SRR1039508_1.fastq.gz"
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/008/SRR1039508/SRR1039508_2.fastq.gz"
    # T1 (SRR1039509)
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/009/SRR1039509/SRR1039509_1.fastq.gz"
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/009/SRR1039509/SRR1039509_2.fastq.gz"
    # C2 (SRR1039512)
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/002/SRR1039512/SRR1039512_1.fastq.gz"
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/002/SRR1039512/SRR1039512_2.fastq.gz"
    # T2 (SRR1039513)
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/003/SRR1039513/SRR1039513_1.fastq.gz"
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/003/SRR1039513/SRR1039513_2.fastq.gz"
    # C3 (SRR1039516)
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/006/SRR1039516/SRR1039516_1.fastq.gz"
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/006/SRR1039516/SRR1039516_2.fastq.gz"
    # T3 (SRR1039517)
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/007/SRR1039517/SRR1039517_1.fastq.gz"
    "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/007/SRR1039517/SRR1039517_2.fastq.gz"
)

# Download each file with resume capability
for url in "${URLS[@]}"; do
    filename=$(basename "$url")
    target="$DATA_DIR/$filename"
    if [[ -f "$target" ]]; then
        echo "[EXISTS] $target already downloaded. Skipping."
    else
        echo "[DOWNLOADING] $filename from $url ..."
        curl -C - --retry 3 --retry-delay 5 -o "$target" "$url"
    fi
done

echo ""
echo "================================================================================"
echo "Verifying MD5 Checksums..."
echo "================================================================================"

cat << 'EOF' > "$DATA_DIR/checksums.md5"
caec3ceea460dfde2b79e2c60de8f5d0  data/raw/SRR1039508_1.fastq.gz
8c35272a8cbe22f28383f982424fa752  data/raw/SRR1039508_2.fastq.gz
740dfa3006dae2a77f985098ff3ea534  data/raw/SRR1039509_1.fastq.gz
c463f8ec4e1fcf6c6f71b9c9f0a202d5  data/raw/SRR1039509_2.fastq.gz
c9c2ff14eb916f1d8c116c4fa2eb4ef6  data/raw/SRR1039512_1.fastq.gz
3c36c2ef6a85859ca071804ba014c278  data/raw/SRR1039512_2.fastq.gz
c9a2d6771d9d94943fcf3a1e3895e69e  data/raw/SRR1039513_1.fastq.gz
ef1356fcfd5843445e9942a73c1d9f82  data/raw/SRR1039513_2.fastq.gz
a99859f972b226e6a17b078fb8fa8d3c  data/raw/SRR1039516_1.fastq.gz
38927aa8a666bf0ff48ff70c5ff9c3a3  data/raw/SRR1039516_2.fastq.gz
b1fa8514101e4a113ecaa68a5c3fc6cf  data/raw/SRR1039517_1.fastq.gz
aaec342371e721531e2adadceab8e8fe  data/raw/SRR1039517_2.fastq.gz
EOF

if command -v md5sum >/dev/null 2>&1; then
    md5sum -c "$DATA_DIR/checksums.md5"
    echo "[SUCCESS] All FASTQ checksums verified successfully."
else
    echo "[WARNING] md5sum not available; skipping checksum verification."
fi
