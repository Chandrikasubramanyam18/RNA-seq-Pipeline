"""Pydantic v2 request/response schemas.

These mirror the TypeScript contracts in ``ui/src/types/index.ts`` one-for-one
so that the UI can consume API responses without remapping.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Study-level
# ---------------------------------------------------------------------------

class LibraryLayout(str, Enum):
    PAIRED = "PAIRED"
    SINGLE = "SINGLE"


class LibrarySelection(str, Enum):
    polyA = "polyA"
    RANDOM = "RANDOM"
    CDNA = "CDNA"
    other = "other"


class LibraryStrategy(str, Enum):
    RNA_SEQ = "RNA-Seq"
    MIRNA_SEQ = "miRNA-Seq"
    OTHER = "other"


class Dataset(BaseModel):
    accession: str
    bioproject: str
    sraStudy: str
    organism: str
    taxonomyId: int
    title: str
    publication: str
    platform: str
    libraryStrategy: LibraryStrategy
    librarySelection: LibrarySelection
    libraryLayout: LibraryLayout
    readLength: int
    referenceGenome: str
    annotationSource: str
    source: str
    downloadDate: str | None = None


class ReferenceInfo(BaseModel):
    genomeAssembly: str
    release: str
    sjdbOverhang: int
    genomeSAindexNbases: int
    salmonKmerLength: int
    files: dict[str, str]


class DataProvenance(BaseModel):
    isMock: bool


class Project(Dataset, DataProvenance):
    id: str
    name: str
    designDescription: str
    reference: ReferenceInfo


# ---------------------------------------------------------------------------
# Samples & cohorts
# ---------------------------------------------------------------------------

Condition = Literal["control", "treatment"]


class Sample(BaseModel):
    id: str
    runId: str
    gsmId: str | None = None
    donor: str
    replicate: int
    condition: Condition
    fastq1: str
    fastq2: str


class Cohort(BaseModel):
    condition: Condition
    label: str
    sampleIds: list[str]


# ---------------------------------------------------------------------------
# Pipeline run-state
# ---------------------------------------------------------------------------

StageStatus = Literal["done", "running", "pending", "blocked"]
StageKey = Literal[
    "metadata",
    "raw_qc",
    "preprocessing",
    "alignment",
    "quantification",
    "deseq2",
]


class RunStage(BaseModel):
    key: StageKey
    label: str
    status: StageStatus
    detail: str | None = None


# ---------------------------------------------------------------------------
# QC
# ---------------------------------------------------------------------------

class PerBaseQuality(BaseModel):
    position: int
    meanQ: float


class QcMetric(BaseModel):
    sampleId: str
    totalReads: int
    gcPercent: float
    q20Rate: float
    q30Rate: float
    adapterContentPct: float
    duplicationPct: float
    retentionPct: float
    perBaseQuality: list[PerBaseQuality]


class MultiQcSummary(BaseModel):
    sampleId: str
    pctDups: float
    pctGC: float
    milSeqs: float
    status: Literal["PASS", "WARN", "FAIL"]


class AlignmentStats(BaseModel):
    sampleId: str
    totalReads: int
    uniquelyMappedPct: float
    multiMappedPct: float
    unmappedPct: float
    properlyPairedPct: float


# ---------------------------------------------------------------------------
# Quantification
# ---------------------------------------------------------------------------

QuantMethod = Literal["salmon", "featurecounts"]


class Quantification(BaseModel):
    sampleId: str
    method: QuantMethod
    geneId: str
    symbol: str | None = None
    tpm: float | None = None
    counts: int | None = None
    length: int | None = None


# ---------------------------------------------------------------------------
# Differential expression
# ---------------------------------------------------------------------------

DeDataSource = Literal["source_derived", "synthetic_demo"]


class DeResult(BaseModel):
    geneId: str
    symbol: str | None = None
    baseMean: float
    log2FoldChange: float
    lfcSE: float | None = None
    pvalue: float
    padj: float
    significant: bool
    dataSource: DeDataSource


class PcaPoint(BaseModel):
    sampleId: str
    pc1: float
    pc2: float
    condition: Condition


class PcaAxisInfo(BaseModel):
    label: str
    varianceExplained: float


class DeVisualData(BaseModel):
    pca: list[PcaPoint]
    pcaAxis1: PcaAxisInfo
    pcaAxis2: PcaAxisInfo
    volcano: list[DeResult]
    ma: list[DeResult]
    sourceDerived: list[DeResult]


# ---------------------------------------------------------------------------
# Pathways
# ---------------------------------------------------------------------------

PathwaySource = Literal["GO", "KEGG", "Reactome", "Hallmark"]


class PathwayEnrichment(BaseModel):
    id: str
    source: PathwaySource
    term: str
    geneRatio: float | None = None
    pvalue: float
    padj: float
    genes: list[str]
    dataSource: DeDataSource


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------

class Health(BaseModel):
    status: Literal["ok"]
    app: str
    version: str


class ProvenanceSummary(BaseModel):
    """Per-stage provenance so consumers know what is real vs demo."""
    isMock: bool
    field: str = Field(
        description="Note explaining why the data is marked as demonstration."
    )
