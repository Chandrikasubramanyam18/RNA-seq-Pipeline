#!/usr/bin/env python3
"""
Real-Loci Mini-Reference Builder (Phase 4 correction to Step 3).
Builds a tutorial-scale reference from REAL GRCh38 (hg38) genomic sequence
for the three study genes (CRISPLD2, GAPDH, ACTB) plus coordinate-matched
exon annotation, so that real GSE52778 subset reads can align meaningfully.

Replaces the synthetic motif mini-reference (build_test_reference.py), which
was syntactically valid but biologically meaningless (0% mapping).

Data sources (queried at build time via HTTPS):
  - Annotation: UCSC REST API (api.genome.ucsc.edu) getData/track
                ncbiRefSeqCurated (RefSeq genePred)
  - Sequence:   UCSC REST API (api.genome.ucsc.edu) getData/sequence (hg38)

Coordinate model: each contig is a genomic slice of the hg38 primary
assembly spanning the gene transcript plus FLANK bp on each side. GTF feature
coordinates are shifted to contig-local 1-based coordinates so FASTA and GTF
remain coordinate-compatible (STAR requirement).

Seed intervals verified against NCBI esummary (GRCh38.p14):
  CRISPLD2: chr16 NC_000016.10 chrstart 84819984 chrstop 84909507
  GAPDH:    chr12 NC_000012.12 chrstart 6534516  chrstop 6538370
  ACTB:     chr7  NC_000007.14 chrstart 5530600  chrstop 5527147 (minus strand)
"""

import json
import sys
import argparse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UCSC_BASE = "https://api.genome.ucsc.edu"
GENOME = "hg38"
TRACK = "ncbiRefSeqCurated"
FLANK = 500  # bp of real flanking genomic sequence on each side of the locus
UA = {"User-Agent": "rna-seq-pipeline/phase4"}

# seed: symbol -> (chrom, verified_start, verified_stop) from NCBI GRCh38.p14
SEED_WINDOW = {
    "CRISPLD2": ("chr16", 84819984, 84909507),
    "GAPDH": ("chr12", 6534516, 6538370),
    "ACTB": ("chr7", 5530600, 5527147),
}

# canonical RefSeq transcript per gene
PREFERRED_TRANSCRIPT = {
    "CRISPLD2": "NM_031476.4",
    "GAPDH": "NM_002046.7",
    "ACTB": "NM_001101.5",
}

# GENCODE-style gene_id (Ensembl, from GRCh38 annotation)
GENE_ID = {
    "CRISPLD2": "ENSG00000103196.14",
    "GAPDH": "ENSG00000111640.16",
    "ACTB": "ENSG00000075624.17",
}


def _get(url: str, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_track(chrom: str, start: int, end: int) -> dict:
    url = (f"{UCSC_BASE}/getData/track?genome={GENOME};track={TRACK};"
           f"chrom={chrom};start={start};end={end}")
    return _get(url)


def fetch_sequence(chrom: str, start: int, end: int) -> str:
    """Fetch hg38 genomic sequence for [start, end): 1-based inclusive start,
    exclusive end (UCSC slice convention)."""
    url = (f"{UCSC_BASE}/getData/sequence?genome={GENOME};chrom={chrom};"
           f"start={start};end={end}")
    data = _get(url)
    assert data["chrom"] == chrom and data["start"] == start and data["end"] == end
    return data["dna"]


def bl2seq(pos: int, start: int) -> int:
    """Convert 1-based genomic pos to 1-based contig-local pos."""
    return pos - start + 1


def build_gene(symbol: str, out_dir: Path):
    chrom, seed_start, seed_stop = SEED_WINDOW[symbol]
    lo, hi = sorted((seed_start, seed_stop))

    track = fetch_track(chrom, lo - FLANK, hi + FLANK)
    items = track.get(TRACK, []) or track.get("ncbiRefSeqCurated", [])

    # locate the preferred transcript on the matching strand
    preferred = PREFERRED_TRANSCRIPT[symbol]
    item = next((it for it in items if it["name"] == preferred), None)
    if item is None:
        cands = [it for it in items if it.get("name2") == symbol]
        if not cands:
            raise RuntimeError(f"{symbol}: no {TRACK} record in window")
        item = next((it for it in cands
                     if it["name"].startswith("NM_")), cands[0])

    strand = item["strand"]
    tx_start, tx_end = item["txStart"], item["txEnd"]
    assert tx_start <= tx_end
    contig_start = tx_start - FLANK
    contig_end = tx_end + FLANK + 1  # exclusive end (UCSC slice convention)
    contig = f"{chrom}.{tx_start}-{tx_end}"

    seq = fetch_sequence(chrom, contig_start, contig_end)
    if len(seq) != (contig_end - contig_start):
        raise RuntimeError(
            f"{symbol}: UCSC returned {len(seq)} bp, expected {contig_end - contig_start}")

    exon_starts = item["exonStarts"].split(",")[:-1]
    exon_ends = item["exonEnds"].split(",")[:-1]
    exons = [(int(s), int(e)) for s, e in zip(exon_starts, exon_ends)]

    cds_start, cds_end = item["cdsStart"], item["cdsEnd"]
    gene_id = GENE_ID[symbol]

    # ---- GTF records (contig-local 1-based coords) ----
    lines = []
    g_start = bl2seq(tx_start, contig_start)
    g_end = bl2seq(tx_end, contig_start)
    lines.append(
        f'{contig}\tUCSC-ncbiRefSeqCurated\tgene\t{g_start}\t{g_end}\t.\t{strand}\t.\t'
        f'gene_id "{gene_id}"; gene_type "protein_coding"; gene_name "{symbol}";')
    lines.append(
        f'{contig}\tUCSC-ncbiRefSeqCurated\ttranscript\t{g_start}\t{g_end}\t.\t{strand}\t.\t'
        f'gene_id "{gene_id}"; transcript_id "{item["name"]}"; gene_type "protein_coding"; '
        f'gene_name "{symbol}"; transcript_name "{symbol}-{preferred.split(".")[0]}";')
    for i, (es, ee) in enumerate(exons, start=1):
        lines.append(
            f'{contig}\tUCSC-ncbiRefSeqCurated\texon\t{bl2seq(es, contig_start)}\t'
            f'{bl2seq(ee, contig_start)}\t.\t{strand}\t.\t'
            f'gene_id "{gene_id}"; transcript_id "{item["name"]}"; exon_number {i}; '
            f'gene_name "{symbol}";')
    if cds_start < cds_end:
        lines.append(
            f'{contig}\tUCSC-ncbiRefSeqCurated\tCDS\t{bl2seq(cds_start, contig_start)}\t'
            f'{bl2seq(cds_end, contig_start)}\t.\t{strand}\t0\t'
            f'gene_id "{gene_id}"; transcript_id "{item["name"]}"; gene_name "{symbol}";')

    return {
        "symbol": symbol,
        "chrom": chrom,
        "strand": strand,
        "tx_start": tx_start,
        "tx_end": tx_end,
        "contig": contig,
        "contig_start": contig_start,
        "contig_end": contig_end,
        "seq": seq,
        "gtf_lines": lines,
        "transcript": item["name"],
        "n_exons": len(exons),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Build real-loci mini-reference (FASTA + GTF) from UCSC hg38.")
    parser.add_argument("--out-dir", "-o", type=Path,
                        default=Path("data/reference/mini_real"))
    args = parser.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    fasta_lines = []
    gtf_lines = [f"##real-loci.mini-reference.gtf  genome={GENOME}  built={stamp}"]

    records = {}
    for symbol in ("CRISPLD2", "GAPDH", "ACTB"):
        rec = build_gene(symbol, out_dir)
        records[symbol] = rec
        header = (f">{rec['contig']} GRCh38(hg38) {rec['chrom']}:"
                  f"{rec['contig_start']}-{rec['contig_end']} "
                  f"{rec['symbol']} Tx:{rec['transcript']} "
                  f"{rec['tx_start']}-{rec['tx_end']} strand={rec['strand']}")
        fasta_lines.append(header)
        for i in range(0, len(rec["seq"]), 80):
            fasta_lines.append(rec["seq"][i:i + 80].upper())
        gtf_lines.extend(rec["gtf_lines"])

        print(f"[OK] {symbol:9s} {rec['chrom']}:{rec['tx_start']}-{rec['tx_end']} "
              f"strand={rec['strand']} exons={rec['n_exons']} "
              f"contig={rec['contig']} seq_len={len(rec['seq'])}")

    fasta_file = out_dir / "mini_genome.fa"
    gtf_file = out_dir / "mini_genes.gtf"
    fasta_file.write_text("\n".join(fasta_lines) + "\n", encoding="utf-8")
    gtf_file.write_text("\n".join(gtf_lines) + "\n", encoding="utf-8")

    print(f"[SUCCESS] Real-loci mini-reference created in: {out_dir}")
    print(f"          FASTA: {fasta_file} ({fasta_file.stat().st_size} bytes)")
    print(f"          GTF  : {gtf_file} ({gtf_file.stat().st_size} bytes)")


if __name__ == "__main__":
    main()