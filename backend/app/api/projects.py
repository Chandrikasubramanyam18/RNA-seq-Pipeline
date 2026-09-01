from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.project import ProjectModel
from app.schemas.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


def _to_schema(p: ProjectModel) -> Project:
    return Project(
        **{
            # Dataset fields
            "accession": p.accession,
            "bioproject": p.bioproject,
            "sraStudy": p.sra_study,
            "organism": p.organism,
            "taxonomyId": p.taxonomy_id,
            "title": p.title,
            "publication": p.publication,
            "platform": p.platform,
            "libraryStrategy": p.library_strategy,
            "librarySelection": p.library_selection,
            "libraryLayout": p.library_layout,
            "readLength": p.read_length,
            "referenceGenome": p.reference_genome,
            "annotationSource": p.annotation_source,
            "source": p.source,
            "downloadDate": p.download_date,
            # Provenance
            "id": p.id,
            "name": p.name,
            "designDescription": p.design_description,
            "isMock": p.is_mock,
            "reference": {
                "genomeAssembly": p.genome_assembly,
                "release": p.reference_release,
                "sjdbOverhang": p.sjdb_overhang,
                "genomeSAindexNbases": p.genome_sa_index_nbases,
                "salmonKmerLength": p.salmon_kmer_length,
                "files": {
                    "genomeFasta": p.genome_fasta,
                    "annotationGtf": p.annotation_gtf,
                    "transcriptomeFasta": p.transcriptome_fasta,
                },
            },
        }
    )


@router.get("", response_model=list[Project])
def list_projects(db: Session = Depends(get_db)) -> list[Project]:
    return [_to_schema(p) for p in db.scalars(select(ProjectModel)).all()]


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, db: Session = Depends(get_db)) -> Project:
    p = db.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
    if p is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return _to_schema(p)
