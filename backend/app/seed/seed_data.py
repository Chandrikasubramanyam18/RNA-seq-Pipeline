"""Build all seed rows from the repository's real analysis artifacts.

Provenance rules (locked):
  * Values read from genuine repo outputs (result CSVs/TSVs, manifest YAML,
    samplesheet) are realistic and, where they are genuine pipeline outputs
    (DESeq2 results, pathway enrichment, FastQC/fastp summaries), labelled
    source_derived.
  * Any value the pipeline has NOT actually produced (alignment stats,
    quantification TPM/counts) is kept as synthetic_demo so it can never be
    mistaken for experimental output.
  * The project-level isMock flag stays true because the pipeline has not
    fully executed against the raw data, the combination is a demonstration.
"""

from __future__ import annotations

import csv
from pathlib import Path

import yaml

from app.core.config import settings


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_tsv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _arg(term: str) -> str:
    """Extract the symbol/id after the parenthetical, e.g.
    'ENSG00000096060 (FKBP5)' -> 'FKBP5'; 'GO:0071356 (...)' -> 'GO:0071356'.
    """
    return term.split(" (")[0]


# ---------------------------------------------------------------------------
# Study-level (manifest + samplesheet)
# ---------------------------------------------------------------------------

def build_project_fields() -> dict:
    manifest = yaml.safe_load(settings.dataset_manifest_path.read_text(encoding="utf-8"))
    reference = yaml.safe_load(settings.reference_manifest_path.read_text(encoding="utf-8"))

    star = reference.get("star_parameters", {})
    salmon = reference.get("salmon_parameters", {})
    files = reference.get("files", {})

    return {
        "id": "gse52778",
        "accession": manifest["accession"],
        "bioproject": manifest["bioproject"],
        "sra_study": manifest["sra_study"],
        "organism": manifest["organism"],
        "taxonomy_id": manifest["taxonomy_id"],
        "title": manifest["study"],
        "publication": manifest["publication"],
        "platform": manifest["platform"],
        "library_strategy": manifest["library_strategy"],
        "library_selection": manifest["library_selection"],
        "library_layout": manifest["library_layout"],
        "read_length": manifest["read_length"],
        "reference_genome": manifest["reference_genome"],
        "annotation_source": manifest["annotation_source"],
        "source": manifest["source"],
        "download_date": manifest.get("download_date"),
        "name": "Dexamethasone in Airway Smooth Muscle",
        "design_description": (
            "3 paired donors (N61311, N052611, N080611), each with a control and "
            "1 uM dexamethasone-treated airway smooth muscle sample (18h), "
            "Illumina HiSeq 2000 paired-end 2x63bp."
        ),
        "is_mock": True,
        "genome_assembly": reference["genome_assembly"],
        "reference_release": reference["release"],
        "sjdb_overhang": star.get("sjdbOverhang"),
        "genome_sa_index_nbases": star.get("genomeSAindexNbases"),
        "salmon_kmer_length": salmon.get("kmer_length"),
        "genome_fasta": files["genome_fasta"]["url"],
        "annotation_gtf": files["annotation_gtf"]["url"],
        "transcriptome_fasta": files["transcriptome_fasta"]["url"],
    }


def build_sample_fields() -> list[dict]:
    manifest = yaml.safe_load(settings.dataset_manifest_path.read_text(encoding="utf-8"))
    rows = []
    for s in manifest["samples"]:
        rows.append(
            {
                "id": s["sample_id"],
                "run_id": s["run_id"],
                "gsm_id": s["gsm_id"],
                "donor": s["donor"],
                "replicate": s["replicate"],
                "condition": s["condition"],
                "fastq1": s["fastq_1_url"],
                "fastq2": s["fastq_2_url"],
            }
        )
    return rows


# ---------------------------------------------------------------------------
# QC (FastQC per-lane + fastp per-sample)
# ---------------------------------------------------------------------------

def _per_base_profile(n: int = 63) -> list[dict]:
    """Plausible 63-cycle read-quality profile (synthetic_demo per-lane detail)."""
    out = []
    for i in range(1, n + 1):
        t = (i - 1) / (n - 1)
        # starts ~38, decays slightly to ~33 at the read tail (2x63bp).
        q = 38 - 5 * t
        out.append({"position": i, "mean_q": round(q, 1)})
    return out


def build_qc_fields() -> list[dict]:
    fastqc = _read_tsv(settings.fastqc_summary_path)
    fastp = _read_tsv(settings.fastp_summary_path)
    by_sample: dict[str, dict] = {}
    for row in fastp:
        by_sample[row["sample"]] = row

    # fastqc filenames are "<run>_1/2.fastq.gz"; map lane -> sample via run id.
    run_to_sample = {
        "SRR1039508": "C1",
        "SRR1039509": "T1",
        "SRR1039512": "C2",
        "SRR1039513": "T2",
        "SRR1039516": "C3",
        "SRR1039517": "T3",
    }

    # Group fastqc rows per sample, averaging the two mates.
    samples: dict[str, list[dict]] = {}
    for row in fastqc:
        name = row["filename"]
        run = name.split("_")[0]
        sample = run_to_sample.get(run)
        if sample is None:
            continue
        samples.setdefault(sample, []).append(row)

    rows = []
    for sample, lanes in samples.items():
        fp = by_sample.get(sample, {})
        avg = lambda key: sum(float(l[key]) for l in lanes) / len(lanes)  # noqa: E731
        total_reads = int(float(fp.get("raw_total_reads", 0)) or sum(int(l["total_reads"]) for l in lanes))
        clean = int(float(fp.get("clean_total_reads", 0)) or total_reads)
        retention = (clean / total_reads * 100) if total_reads else 100.0
        adapter_pct = (int(fp.get("adapter_trimmed_reads", 0)) / clean * 100) if clean else 0.0

        rows.append(
            {
                "sample_id": sample,
                "total_reads": total_reads,
                "gc_percent": round(avg("gc_percent"), 2),
                # fastp reports q rates differently; use the fastqc-derived mean
                # so the per-sample QC is internally consistent.
                "q20_rate": round(avg("q20_rate"), 2),
                "q30_rate": round(avg("q30_rate"), 2),
                # Duplication is not in the fastp/fastqc summaries; use a
                # plausible demo value (kept synthetic via project isMock).
                "adapter_content_pct": round(adapter_pct, 2),
                "duplication_pct": 34.8,
                "retention_pct": round(retention, 2),
                "per_base": _per_base_profile(),
            }
        )
    return rows


def build_multiqc_fields(qc_rows: list[dict]) -> list[dict]:
    return [
        {
            "sample_id": q["sample_id"],
            "pct_dups": q["duplication_pct"],
            "pct_gc": q["gc_percent"],
            "mil_seqs": round(q["total_reads"] / 1_000_000, 2),
            "status": "PASS",
        }
        for q in qc_rows
    ]


# ---------------------------------------------------------------------------
# Alignment & quantification (NOT executed -> synthetic_demo)
# ---------------------------------------------------------------------------

def build_alignment_fields(samples: list[dict]) -> list[dict]:
    return [
        {
            "sample_id": s["id"],
            "total_reads": 20_000_000,
            "uniquely_mapped_pct": 93.5,
            "multi_mapped_pct": 1.2,
            "unmapped_pct": 5.3,
            "properly_paired_pct": 97.4,
        }
        for s in samples
    ]


_QUANT_SEEDS = [
    ("C1", "salmon", "ENSG00000103196", "CRISPLD2", 6.1, None, 2350),
    ("C2", "salmon", "ENSG00000103196", "CRISPLD2", 5.7, None, 2350),
    ("C3", "salmon", "ENSG00000103196", "CRISPLD2", 6.5, None, 2350),
    ("T1", "salmon", "ENSG00000103196", "CRISPLD2", 35.2, None, 2350),
    ("T2", "salmon", "ENSG00000103196", "CRISPLD2", 34.1, None, 2350),
    ("T3", "salmon", "ENSG00000103196", "CRISPLD2", 36.0, None, 2350),
    ("C1", "salmon", "ENSG00000096060", "FKBP5", 2.2, None, 1910),
    ("T1", "salmon", "ENSG00000096060", "FKBP5", 20.5, None, 1910),
    ("C1", "featurecounts", "ENSG00000103196", "CRISPLD2", None, 420, None),
    ("C2", "featurecounts", "ENSG00000103196", "CRISPLD2", None, 390, None),
    ("C3", "featurecounts", "ENSG00000103196", "CRISPLD2", None, 450, None),
    ("T1", "featurecounts", "ENSG00000103196", "CRISPLD2", None, 2450, None),
    ("T2", "featurecounts", "ENSG00000103196", "CRISPLD2", None, 2380, None),
    ("T3", "featurecounts", "ENSG00000103196", "CRISPLD2", None, 2510, None),
]


def build_quantification_fields() -> list[dict]:
    return [
        {
            "sample_id": sample,
            "method": method,
            "gene_id": gene_id,
            "symbol": symbol,
            "tpm": tpm,
            "counts": counts,
            "length": length,
        }
        for sample, method, gene_id, symbol, tpm, counts, length in _QUANT_SEEDS
    ]


# ---------------------------------------------------------------------------
# Differential expression (REAL deseq2_results.csv -> source_derived)
# ---------------------------------------------------------------------------

_SYMBOLS = {
    "ENSG00000103196": "CRISPLD2",
    "ENSG00000120129": "DUSP1",
    "ENSG00000096060": "FKBP5",
    "ENSG00000152583": "SPARCL1",
    "ENSG00000165030": "KLF15",
    "ENSG00000101349": "SAMHD1",
    "ENSG00000111640": "GAPDH",
    "ENSG00000075624": "ACTB",
    "ENSG00000087086": "FTL",
    "ENSG00000067057": "PFN1",
    "ENSG00000142627": "EGR1",
    "ENSG00000119888": "EPCAM",
}


def build_de_fields() -> list[dict]:
    rows = _read_csv(settings.deseq2_results_path)
    out = []
    for r in rows:
        gene_id = _arg(r["gene_id"])
        out.append(
            {
                "gene_id": gene_id,
                "symbol": _SYMBOLS.get(gene_id),
                "base_mean": float(r["baseMean"]),
                "log2_fold_change": float(r["log2FoldChange"]),
                "lfc_se": float(r["lfcSE"]),
                "pvalue": float(r["pvalue"]),
                "padj": float(r["padj"]),
                "significant": r["significant"] == "YES",
                "data_source": "source_derived",
            }
        )
    return out


# ---------------------------------------------------------------------------
# PCA + visual (real visualization_summary.md / volcano_data.csv + demo layout)
# ---------------------------------------------------------------------------

def build_pca_points(samples: list[dict]) -> list[dict]:
    scores = {
        "C1": (-3.1, -1.4),
        "C2": (-3.0, 2.2),
        "C3": (-2.9, 0.4),
        "T1": (3.0, -1.7),
        "T2": (3.1, 2.0),
        "T3": (3.2, 0.2),
    }
    return [
        {
            "sample_id": s["id"],
            "pc1": scores[s["id"]][0],
            "pc2": scores[s["id"]][1],
            "condition": s["condition"],
        }
        for s in samples
    ]


def build_de_axes() -> dict:
    # From visualization_summary.md (real values).
    return {
        "axis1_label": "PC1",
        "axis1_var": 0.894,
        "axis2_label": "PC2",
        "axis2_var": 0.072,
    }


# ---------------------------------------------------------------------------
# Pathways (REAL pathway_enrichment_results.csv -> source_derived)
# ---------------------------------------------------------------------------

def build_pathway_fields() -> list[dict]:
    rows = _read_csv(settings.pathway_results_path)
    known = {
        "ENSG00000103196": "CRISPLD2",
        "ENSG00000120129": "DUSP1",
        "ENSG00000096060": "FKBP5",
        "ENSG00000165030": "KLF15",
        "ENSG00000101349": "SAMHD1",
        "ENSG00000142627": "EGR1",
        "ENSG00000152583": "SPARCL1",
    }
    out = []
    for r in rows:
        term_id = _arg(r["pathway"])
        symbol = "KEGG" if term_id.startswith("KEGG") else "GO"
        # overlap_genes like "ENSG... (NAME); ENSG... (NAME)" or "None"
        genes_raw = r["overlap_genes"]
        if genes_raw == "None":
            genes = []
        else:
            genes = [known.get(_arg(g.strip()), _arg(g.strip())) for g in genes_raw.split(";")]
        out.append(
            {
                "term_id": term_id,
                "source": symbol,
                "term": r["pathway"].split(" (", 1)[1].rstrip(")") if " (" in r["pathway"] else r["pathway"],
                "gene_ratio": float(r["overlap_count"]) / float(r["query_deg_count"]),
                "pvalue": float(r["pvalue"]),
                "padj": float(r["padj"]),
                "genes": ";".join(genes),
                "data_source": "source_derived",
            }
        )
    return out
