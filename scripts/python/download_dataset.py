#!/usr/bin/env python3
"""
Cross-Platform Dataset Downloader and Subsampler for GSE52778.
Downloads full FASTQ files from EMBL-EBI ENA or streams real subsampled reads
for ultra-fast, lightweight development and testing.
"""

import sys
import os
import gzip
import hashlib
import argparse
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

MANIFEST = {
    "C1": {
        "run": "SRR1039508",
        "r1_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/008/SRR1039508/SRR1039508_1.fastq.gz",
        "r2_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/008/SRR1039508/SRR1039508_2.fastq.gz",
        "md5_r1": "caec3ceea460dfde2b79e2c60de8f5d0",
        "md5_r2": "8c35272a8cbe22f28383f982424fa752",
    },
    "T1": {
        "run": "SRR1039509",
        "r1_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/009/SRR1039509/SRR1039509_1.fastq.gz",
        "r2_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/009/SRR1039509/SRR1039509_2.fastq.gz",
        "md5_r1": "740dfa3006dae2a77f985098ff3ea534",
        "md5_r2": "c463f8ec4e1fcf6c6f71b9c9f0a202d5",
    },
    "C2": {
        "run": "SRR1039512",
        "r1_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/002/SRR1039512/SRR1039512_1.fastq.gz",
        "r2_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/002/SRR1039512/SRR1039512_2.fastq.gz",
        "md5_r1": "c9c2ff14eb916f1d8c116c4fa2eb4ef6",
        "md5_r2": "3c36c2ef6a85859ca071804ba014c278",
    },
    "T2": {
        "run": "SRR1039513",
        "r1_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/003/SRR1039513/SRR1039513_1.fastq.gz",
        "r2_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/003/SRR1039513/SRR1039513_2.fastq.gz",
        "md5_r1": "c9a2d6771d9d94943fcf3a1e3895e69e",
        "md5_r2": "ef1356fcfd5843445e9942a73c1d9f82",
    },
    "C3": {
        "run": "SRR1039516",
        "r1_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/006/SRR1039516/SRR1039516_1.fastq.gz",
        "r2_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/006/SRR1039516/SRR1039516_2.fastq.gz",
        "md5_r1": "a99859f972b226e6a17b078fb8fa8d3c",
        "md5_r2": "38927aa8a666bf0ff48ff70c5ff9c3a3",
    },
    "T3": {
        "run": "SRR1039517",
        "r1_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/007/SRR1039517/SRR1039517_1.fastq.gz",
        "r2_url": "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/007/SRR1039517/SRR1039517_2.fastq.gz",
        "md5_r1": "b1fa8514101e4a113ecaa68a5c3fc6cf",
        "md5_r2": "aaec342371e721531e2adadceab8e8fe",
    },
}

def calculate_md5(filepath: Path) -> str:
    """Computes MD5 hash of a file in chunks."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def download_stream_subsample(url: str, output_path: Path, max_reads: int = 50000) -> int:
    """
    Streams a gzipped FASTQ file over HTTP, extracts the first max_reads records,
    and writes them as a clean, compressed .fastq.gz file.
    """
    print(f"  [STREAMING] {url.split('/')[-1]} (extracting {max_reads:,} real read pairs)...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    read_count = 0
    
    with urllib.request.urlopen(req, timeout=30) as response:
        with gzip.GzipFile(fileobj=response, mode="rb") as gz_in:
            with gzip.open(output_path, "wb") as gz_out:
                while read_count < max_reads:
                    # Each FASTQ record is 4 lines
                    line1 = gz_in.readline()
                    if not line1:
                        break
                    line2 = gz_in.readline()
                    line3 = gz_in.readline()
                    line4 = gz_in.readline()
                    
                    gz_out.write(line1)
                    gz_out.write(line2)
                    gz_out.write(line3)
                    gz_out.write(line4)
                    read_count += 1
                    
    print(f"  [SAVED] {output_path} ({read_count:,} reads, {output_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return read_count

def download_full_file(url: str, output_path: Path, expected_md5: str) -> bool:
    """Downloads a complete file with progress reporting and checksum verification."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        print(f"  [EXISTS] {output_path.name} already exists. Verifying checksum...")
        actual_md5 = calculate_md5(output_path)
        if actual_md5 == expected_md5:
            print(f"  [MD5 OK] {output_path.name} passed checksum verification.")
            return True
        else:
            print(f"  [MD5 MISMATCH] {output_path.name} is corrupted. Re-downloading...")
            output_path.unlink()

    print(f"  [DOWNLOADING FULL] {url} -> {output_path} ...")
    urllib.request.urlretrieve(url, output_path)
    actual_md5 = calculate_md5(output_path)
    if actual_md5 == expected_md5:
        print(f"  [MD5 OK] {output_path.name} successfully verified ({actual_md5}).")
        return True
    else:
        print(f"  [ERROR] MD5 mismatch for {output_path.name} (Expected: {expected_md5}, Got: {actual_md5})")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download or subsample GSE52778 RNA-seq dataset from ENA.")
    parser.add_argument("--out-dir", "-o", type=Path, default=Path("data/raw"), help="Output directory for FASTQ files")
    parser.add_argument("--subsample", "-n", type=int, default=50000, help="Number of read pairs to stream/subsample (0 for full 14GB download)")
    parser.add_argument("--samples", "-s", nargs="*", default=list(MANIFEST.keys()), help="Specific sample IDs to download")
    args = parser.parse_args()

    print("=" * 80)
    print("      GSE52778 Real RNA-seq Dataset Downloader / Streamer")
    print("=" * 80)
    print(f"Target Directory: {args.out_dir}")
    print(f"Mode            : {'Subsample ' + str(args.subsample) + ' read pairs (Fast testing)' if args.subsample > 0 else 'Full dataset download (14 GB)'}")
    print(f"Samples         : {', '.join(args.samples)}")
    print("=" * 80)

    for sample_id in args.samples:
        if sample_id not in MANIFEST:
            print(f"[ERROR] Unknown sample ID '{sample_id}'. Available: {list(MANIFEST.keys())}")
            continue

        info = MANIFEST[sample_id]
        run_id = info["run"]
        r1_path = args.out_dir / f"{run_id}_1.fastq.gz"
        r2_path = args.out_dir / f"{run_id}_2.fastq.gz"

        print(f"\n>>> Processing {sample_id} ({run_id}):")

        if args.subsample > 0:
            download_stream_subsample(info["r1_url"], r1_path, args.subsample)
            download_stream_subsample(info["r2_url"], r2_path, args.subsample)
        else:
            download_full_file(info["r1_url"], r1_path, info["md5_r1"])
            download_full_file(info["r2_url"], r2_path, info["md5_r2"])

    print("\n" + "=" * 80)
    print("[SUCCESS] All requested dataset files are staged in:", args.out_dir)
    print("=" * 80)

if __name__ == "__main__":
    main()
