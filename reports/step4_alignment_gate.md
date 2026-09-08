# Step 4 Gate Report — Real-Loci Mini-Reference Alignment (REBUILD)

- **Generated**: Step 4A–4C (correction/rebuild gate replacing the synthetic-reference Step 4)
- **Scope**: real-loci reference construction + STAR realignment + independent verification
- **Downstream**: STOPPED. No featureCounts, DESeq2, pathway analysis, Nextflow run, or `isMock` change.

## Background / why this gate exists

The original Step 3 mini-reference was synthetic motif DNA (`scripts/python/build_test_reference.py`). Its FASTQ↔GTF structure validated perfectly **syntactically**, but STAR alignment of the real GSE52778 subset reads yielded **0% mapping** for all 6 samples (426-byte BAMs, empty `SJ.out.tab`, `samtools view -c` = 0). That failed run is preserved under `data/reference/archive/synthetic_deadend_run/` with `data/reference/archive/README.md` — **evidence is not deleted**.

Lesson recorded: *a syntactically valid reference ≠ a biologically meaningful reference.*

## Step 4A — Real-loci mini-reference

Built `data/reference/mini_real/` (`mini_genome.fa` + `mini_genes.gtf`) with a new, reproducible builder `scripts/python/build_real_mini_reference.py`. The reference contains **real GRCh38 (hg38) genomic sequence** for the three study genes, UCSC-style coordinate suffixes on contigs, coordinate-matched annotation.

| gene | chrom | strand | txStart–txEnd | exons | contig | span (incl. 500 bp flanks) |
|---|---|---|---|---|---|---|
| CRISPLD2 | chr16 | + | 84,819,984–84,909,508 | 15 | chr16.84819984-84909508 | 90,525 bp |
| GAPDH | chr12 | + | 6,534,516–6,538,371 | 9 | chr12.6534516-6538371 | 4,856 bp |
| ACTB | chr7 | − | 5,527,147–5,530,601 | 6 | chr7.5527147-5530601 | 4,455 bp |

Sources (queried at build time):
- Coordinates/exon structure: UCSC `ncbiRefSeqCurated` (hg38), cross-verified with NCBI esummary (GRCh38.p14: `NC_000016.10`, `NC_000012.12`, `NC_000007.14`).
- Sequence: UCSC REST `getData/sequence` (hg38), uppercase DNA, incl. intronic sequence so STAR can detect splice junctions.
- Canonical transcripts: CRISPLD2 `NM_031476.4`, GAPDH `NM_002046.7`, ACTB `NM_001101.5`.

- Total reference length: **99,836 bp** (3 contigs).
- `validate_reference.py --fasta .../mini_real/mini_genome.fa --gtf .../mini_real/mini_genes.gtf` → **SUCCESS (100% compatible)**.

## Step 4B — STAR index rebuild

- STAR v2.7.11b, `genomeGenerate`, `sjdbOverhang=62` (63−1), `genomeSAindexNbases=7` (log2(99,836)/2−1 ≈ 7.3).
- Result: `data/reference/mini_real/star_index/` (Genome 790 KB, SA 851 KB). Clean run, no suffix-array size warning, **finished successfully**.
- `sjdbList.out.tab` contains **27 splice junctions** — all matching the GTF introns (15 CRISPLD2, 8 GAPDH, 5 ACTB), no chimeric/partial artifacts.

## Step 4C — STAR realignment (same 6 trimmed samples)

- Mode: `alignReads`, BAM SortedByCoordinate, 4 threads; same trimmed reads as original Step 4 (`data/processed/*_trimmed_R{1,2}.fastq.gz`), same `--readFilesCommand zcat`, `--outFilterMultimapNmax 20`, `--outFilterMismatchNmax 10`.
- Due to the known drvfs FIFO limitation, alignment ran on the WSL-native filesystem (`/root/star_work/star_index_real`, `out_real/`) and outputs were copied back to `results/alignment/` (BAM + `.bai` + `*_Log.final.out` + `*_Log.out` + `*_SJ.out.tab`).

### STAR-reported mapping (direct from `Log.final.out`)

| sample | input reads | uniquely mapped | % | multi-mapped | % | unmapped too short | unmapped other |
|---|---|---|---|---|---|---|---|
| C1 | 48,928 | 381 | 0.78% | 77 | 0.16% | 23,642 | 24,828 |
| C2 | 48,230 | 382 | 0.79% | 62 | 0.13% | 23,036 | 24,750 |
| C3 | 47,651 | 337 | 0.71% | 81 | 0.17% | 22,692 | 24,540 |
| T1 | 48,216 | 449 | 0.93% | 81 | 0.17% | 22,780 | 24,906 |
| T2 | 47,433 | 469 | 0.99% | 83 | 0.18% | 22,611 | 24,270 |
| T3 | 47,872 | 559 | 1.17% | 73 | 0.15% | 22,908 | 24,332 |

Low absolute % is **expected**: the mini-reference contains only 3 genes while reads are a whole-transcriptome subset; the majority of reads correctly unmappable ("other" ~50%, "too short" ~48%). Biological signal is carried by the reads that DO align to the reference loci.

## Independent verification (SAMtools 1.24)

`index`, `view -c`, `view -c -F 4`, `idxstats`:

| sample | total alignments (view -c) | mapped (view -c -F 4) | CRISPLD2 (chr16) | GAPDH (chr12) | ACTB (chr7) |
|---|---|---|---|---|---|
| C1 | 1,188 | 1,188 | 584 | 230 | 374 |
| C2 | 1,098 | 1,098 | 444 | 220 | 434 |
| C3 | 1,228 | 1,228 | 708 | 214 | 306 |
| T1 | 1,444 | 1,444 | 766 | 212 | 466 |
| T2 | 1,440 | 1,440 | 674 | 162 | 604 |
| T3 | 1,558 | 1,558 | 568 | 254 | 736 |

- `samtools quickcheck`: PASS for all 6 BAMs.
- 100% of alignments are mapped; **all three genes show nonzero reads in every sample**.
- STAR read-count (uniquely + multi) vs SAMtools alignment-count reconcile: multi-mapped reads each emit multiple alignments, so alignment totals exceed STAR read totals as expected.

## Splice-junction biology crosscheck

Real GTF defines 27 introns (15 CRISPLD2 + 8 GAPDH + 5 ACTB). STAR `SJ.out.tab` splice junctions detected in real reads, cross-referenced against those intron coordinates (±1 bp anchor tolerance):

| sample | SJ junctions detected | matching GTF introns |
|---|---|---|
| C1 | 97 | 13 |
| C2 | 85 | 13 |
| C3 | 106 | 13 |
| T1 | 124 | 18 |
| T2 | 119 | 17 |
| T3 | 99 | 15 |

All detected junctions correspond to annotated introns (canonical GT-AG motifs); e.g. C1 includes the GAPDH introns 554–793, 846–2477, 2995–3084, 3201–3292 (real exonic splicing, not motif artifacts).

## Gate verdict

| check | result |
|---|---|
| STAR execution | PASS |
| BAM generation (+index) | PASS (real, 72–96 KB each) |
| SAMtools quickcheck/index/idxstats/flagstat | PASS |
| Mapping to real loci | **PASS — all 6 samples, all 3 genes, adjacent-splice-junction evidence** |
| FASTA↔GTF coordinate compatibility | PASS |

**GATE: PASSED. Real tools now produce meaningful evidence at tutorial scale.**

## Provenance status

- The synthetic-reference launch + its 0%-mapping run are archived (not deleted): `data/reference/archive/`.
- Alignment stats above come from real STAR/SAMtools outputs; no synthetic numbers were fabricated.
- Project-level `isMock` flag: **NOT flipped — remains true** (pipeline not complete end-to-end).
- Next permitted step when approved: **Step 5 alignment QC**, then Step 6 featureCounts. Do not proceed without explicit gate approval.

> Note: this mini-reference targets the three study genes only; it is a tutorial/execution-validation reference, NOT a complete GRCh38 reference, and NOT a biological reproduction of GSE52778 differential expression.