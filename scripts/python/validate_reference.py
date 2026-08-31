#!/usr/bin/env python3
"""
Reference Genome & GTF Compatibility Validator.
Verifies chromosome identifier matching, GTF syntax, and attribute integrity.
"""

import sys
import gzip
import argparse
from pathlib import Path
from typing import Set, Tuple, List, Dict

def get_fasta_chromosomes(fasta_path: Path) -> Set[str]:
    """Extracts chromosome sequence identifiers from FASTA file."""
    chroms = set()
    open_func = gzip.open if fasta_path.suffix == ".gz" or fasta_path.name.endswith(".fa.gz") else open
    with open_func(fasta_path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith(">"):
                # Header format: >chr1 AC:CM000663.2 ... -> extract "chr1"
                chrom_id = line[1:].split()[0].strip()
                if chrom_id:
                    chroms.add(chrom_id)
    return chroms

def inspect_gtf(gtf_path: Path, max_lines: int = 50000) -> Tuple[Set[str], Set[str], Dict[str, int]]:
    """
    Parses GTF file to extract chromosome names, feature types, and key attribute frequencies.
    """
    gtf_chroms = set()
    features = set()
    attr_counts = {"gene_id": 0, "transcript_id": 0, "gene_name": 0}
    
    open_func = gzip.open if gtf_path.suffix == ".gz" or gtf_path.name.endswith(".gtf.gz") else open
    line_count = 0
    with open_func(gtf_path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            line_count += 1
            parts = line.strip().split("\t")
            if len(parts) >= 9:
                gtf_chroms.add(parts[0])
                features.add(parts[2])
                attributes = parts[8]
                if 'gene_id "' in attributes or 'gene_id=' in attributes:
                    attr_counts["gene_id"] += 1
                if 'transcript_id "' in attributes or 'transcript_id=' in attributes:
                    attr_counts["transcript_id"] += 1
                if 'gene_name "' in attributes or 'gene_name=' in attributes:
                    attr_counts["gene_name"] += 1
            if line_count >= max_lines:
                break

    return gtf_chroms, features, attr_counts

def validate_compatibility(fasta_path: Path, gtf_path: Path) -> Tuple[bool, List[str]]:
    """
    Validates FASTA and GTF compatibility.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []
    
    if not fasta_path.exists():
        return False, [f"ERROR: Genome FASTA file not found: {fasta_path}"]
    if not gtf_path.exists():
        return False, [f"ERROR: Annotation GTF file not found: {gtf_path}"]

    try:
        fasta_chroms = get_fasta_chromosomes(fasta_path)
        if not fasta_chroms:
            errors.append(f"ERROR: No sequence headers found in FASTA file: {fasta_path}")
            return False, errors

        gtf_chroms, features, attr_counts = inspect_gtf(gtf_path)
        if not gtf_chroms:
            errors.append(f"ERROR: No genomic records parsed from GTF file: {gtf_path}")
            return False, errors

        # 1. Check chromosome naming compatibility
        overlap = fasta_chroms.intersection(gtf_chroms)
        if not overlap:
            fasta_sample = list(fasta_chroms)[:5]
            gtf_sample = list(gtf_chroms)[:5]
            has_chr_fasta = any(c.startswith("chr") for c in fasta_sample)
            has_chr_gtf = any(c.startswith("chr") for c in gtf_sample)
            
            if has_chr_fasta and not has_chr_gtf:
                errors.append(
                    f"CRITICAL MISMATCH: Chromosome naming incompatibility detected!\n"
                    f"  FASTA uses 'chr' prefix (e.g., {fasta_sample})\n"
                    f"  GTF lacks 'chr' prefix (e.g., {gtf_sample})\n"
                    f"Aligners will fail to match annotations to alignments."
                )
            elif not has_chr_fasta and has_chr_gtf:
                errors.append(
                    f"CRITICAL MISMATCH: Chromosome naming incompatibility detected!\n"
                    f"  FASTA lacks 'chr' prefix (e.g., {fasta_sample})\n"
                    f"  GTF uses 'chr' prefix (e.g., {gtf_sample})"
                )
            else:
                errors.append(
                    f"ERROR: Zero common chromosomes found between FASTA ({fasta_sample}) and GTF ({gtf_sample})."
                )

        # 2. Check essential features
        if "exon" not in features:
            errors.append("WARNING: No 'exon' features found in GTF sample. featureCounts requires exon records.")

        # 3. Check essential attributes
        if attr_counts["gene_id"] == 0:
            errors.append("ERROR: 'gene_id' attribute missing from GTF records.")

    except Exception as e:
        errors.append(f"ERROR: Validation encountered exception: {str(e)}")

    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(description="Validate compatibility between Genome FASTA and Annotation GTF.")
    parser.add_argument("--fasta", "-f", type=Path, required=True, help="Path to genome FASTA file")
    parser.add_argument("--gtf", "-g", type=Path, required=True, help="Path to annotation GTF file")
    args = parser.parse_args()

    print(f"[INFO] Validating Reference Assets:")
    print(f"       FASTA: {args.fasta}")
    print(f"       GTF  : {args.gtf}")

    is_valid, errors = validate_compatibility(args.fasta, args.gtf)

    if is_valid:
        print("[SUCCESS] Reference FASTA and GTF are 100% COMPATIBLE.")
        print("          Chromosome conventions and GTF attributes verified.")
        sys.exit(0)
    else:
        print(f"[FAILED] Compatibility check failed with {len(errors)} issue(s):")
        for err in errors:
            print(f"  * {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
