#!/usr/bin/env python3
"""
Lightweight Mini-Reference Builder for Rapid Testing.
Creates a compact, valid FASTA genome and GTF annotation containing
target test chromosomes/genes (e.g. CRISPLD2, GAPDH, ACTB) for fast CI/CD and local runs.
"""

import sys
import argparse
from pathlib import Path

# Mini test sequences representing human chromosomal loci with exons & introns
MINI_FASTA_CONTENT = """>chr16 Human Chromosome 16 locus (CRISPLD2 region)
ATGCGATCGATCGATCGATCGATCGATCGACTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAG
AATTCCGGTTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCG
>chr12 Human Chromosome 12 locus (GAPDH region)
GGCCAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCC
GGCCAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCC
GGCCAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCC
AATTCCGGTTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCG
>chr7 Human Chromosome 7 locus (ACTB region)
TTTTAAAACCCCGGGGTTTTAAAACCCCGGGGTTTTAAAACCCCGGGGTTTTAAAACCCCG
TTTTAAAACCCCGGGGTTTTAAAACCCCGGGGTTTTAAAACCCCGGGGTTTTAAAACCCCG
TTTTAAAACCCCGGGGTTTTAAAACCCCGGGGTTTTAAAACCCCGGGGTTTTAAAACCCCG
AATTCCGGTTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCGGAATTCCG
"""

MINI_GTF_CONTENT = """##gencode.v44.test.gtf
chr16	HAVANA	gene	1	200	.	+	.	gene_id "ENSG00000103196.14"; gene_type "protein_coding"; gene_name "CRISPLD2"; level 2;
chr16	HAVANA	transcript	1	200	.	+	.	gene_id "ENSG00000103196.14"; transcript_id "ENST00000219431.9"; gene_type "protein_coding"; gene_name "CRISPLD2"; transcript_type "protein_coding"; transcript_name "CRISPLD2-201"; level 2;
chr16	HAVANA	exon	1	90	.	+	.	gene_id "ENSG00000103196.14"; transcript_id "ENST00000219431.9"; exon_number 1; gene_name "CRISPLD2";
chr16	HAVANA	exon	110	200	.	+	.	gene_id "ENSG00000103196.14"; transcript_id "ENST00000219431.9"; exon_number 2; gene_name "CRISPLD2";
chr12	HAVANA	gene	1	200	.	+	.	gene_id "ENSG00000111640.16"; gene_type "protein_coding"; gene_name "GAPDH"; level 2;
chr12	HAVANA	transcript	1	200	.	+	.	gene_id "ENSG00000111640.16"; transcript_id "ENST00000229239.10"; gene_type "protein_coding"; gene_name "GAPDH"; transcript_type "protein_coding"; transcript_name "GAPDH-201"; level 2;
chr12	HAVANA	exon	1	80	.	+	.	gene_id "ENSG00000111640.16"; transcript_id "ENST00000229239.10"; exon_number 1; gene_name "GAPDH";
chr12	HAVANA	exon	100	200	.	+	.	gene_id "ENSG00000111640.16"; transcript_id "ENST00000229239.10"; exon_number 2; gene_name "GAPDH";
chr7	HAVANA	gene	1	200	.	+	.	gene_id "ENSG00000075624.17"; gene_type "protein_coding"; gene_name "ACTB"; level 2;
chr7	HAVANA	transcript	1	200	.	+	.	gene_id "ENSG00000075624.17"; transcript_id "ENST00000193433.8"; gene_type "protein_coding"; gene_name "ACTB"; transcript_type "protein_coding"; transcript_name "ACTB-201"; level 2;
chr7	HAVANA	exon	1	85	.	+	.	gene_id "ENSG00000075624.17"; transcript_id "ENST00000193433.8"; exon_number 1; gene_name "ACTB";
chr7	HAVANA	exon	105	200	.	+	.	gene_id "ENSG00000075624.17"; transcript_id "ENST00000193433.8"; exon_number 2; gene_name "ACTB";
"""

def create_mini_reference(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    fasta_file = output_dir / "mini_genome.fa"
    gtf_file = output_dir / "mini_genes.gtf"

    fasta_file.write_text(MINI_FASTA_CONTENT.strip() + "\n", encoding="utf-8")
    gtf_file.write_text(MINI_GTF_CONTENT.strip() + "\n", encoding="utf-8")

    print(f"[SUCCESS] Mini reference created in: {output_dir}")
    print(f"          FASTA: {fasta_file} ({fasta_file.stat().st_size} bytes)")
    print(f"          GTF  : {gtf_file} ({gtf_file.stat().st_size} bytes)")

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic mini-reference for testing.")
    parser.add_argument("--out-dir", "-o", type=Path, default=Path("data/reference/mini"), help="Output directory")
    args = parser.parse_args()
    create_mini_reference(args.out_dir)

if __name__ == "__main__":
    main()
