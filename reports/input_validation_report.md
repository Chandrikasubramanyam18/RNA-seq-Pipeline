# Input Validation Report — GSE52778 (tutorial-scale subset)

- **Generated**: Step 1 (read-only input integrity check)
- **Scope**: data integrity & provenance only; NO downstream analysis performed
- **Files inventoried**: 12
- **Read pairs per file**: 50,000 (intentional tutorial subsample)
- **Read length**: 63 bp (matched-end 2x63, per manifest)

## Provenance summary

These files are the **first 50,000 read pairs** streamed from the genuine 
EMBL-EBI ENA source by `scripts/python/download_dataset.py` (`download_stream_subsample`, default `max_reads=50000`). They are 
**intentionally subsampled** for tutorial / CI-scale execution. The md5 of each 
subset file therefore differs from the manifest's original full-file checksum. 
**This is an expected consequence of subsampling, NOT file corruption.**

Classification rules:
  - `MD5 MATCH`   = file byte-identical to original full-run checksum (intact).
  - `MD5 SUBSET`  = structurally valid, md5 differs -> documented tutorial subset.

## Per-file validation

| sample | run | pair | file | gzip | reads | rlen | structure | md5 vs manifest | classification |
|---|---|---|---|---|---|---|---|---|---|
| C1 | SRR1039508 | 1 | SRR1039508_1.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| C1 | SRR1039508 | 2 | SRR1039508_2.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| T1 | SRR1039509 | 1 | SRR1039509_1.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| T1 | SRR1039509 | 2 | SRR1039509_2.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| C2 | SRR1039512 | 1 | SRR1039512_1.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| C2 | SRR1039512 | 2 | SRR1039512_2.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| T2 | SRR1039513 | 1 | SRR1039513_1.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| T2 | SRR1039513 | 2 | SRR1039513_2.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| C3 | SRR1039516 | 1 | SRR1039516_1.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| C3 | SRR1039516 | 2 | SRR1039516_2.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| T3 | SRR1039517 | 1 | SRR1039517_1.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |
| T3 | SRR1039517 | 2 | SRR1039517_2.fastq.gz | OK | 50,000 | 63 | OK | differs | MD5 SUBSET (tutorial, expected) |

## Samplesheet cross-check

- **PASS**: every `fastq_1`/`fastq_2` path in `metadata/samplesheet.csv` resolves to an existing raw file.
- **PASS**: all 12 raw files are referenced by exactly one sample in the samplesheet.

## Paired-end consistency

- **OK**: SRR1039508 R1 == R2 == 50,000 reads
- **OK**: SRR1039509 R1 == R2 == 50,000 reads
- **OK**: SRR1039512 R1 == R2 == 50,000 reads
- **OK**: SRR1039513 R1 == R2 == 50,000 reads
- **OK**: SRR1039516 R1 == R2 == 50,000 reads
- **OK**: SRR1039517 R1 == R2 == 50,000 reads
- **OK**: Mate-pair ID order verified (first 1,000 read IDs identical between R1 and R2 for all 6 samples)

## Summary

- Files: 12
- Structurally valid FASTQ (4-line, seq==qual, constant 63bp): 12/12
- md5 matches original full checksum: 0
- md5 subset (tutorial, expected): 12
- Samplesheet mapping: PASS
- Paired-end R1==R2 consistency: PASS
- Mate-pair ID order (R1 vs R2): PASS

**Verdict: INPUT VALIDATION PASSED (tutorial subset documented)**

> Note: Passing structural validation establishes input integrity/provenance only. 
> Nothing below is promoted to `source_derived`; these checks do not constitute biological analysis results.
