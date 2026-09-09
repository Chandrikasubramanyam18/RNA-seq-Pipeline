// =====================================================
// Subworkflow: ALIGNMENT_STAR
// STAR index build -> STAR alignment -> SAMtools QC -> RSeQC
// =====================================================

include { STAR_INDEX   } from '../../../modules/star/index/main.nf'
include { STAR_ALIGN   } from '../../../modules/star/align/main.nf'
include { SAMTOOLS     } from '../../../modules/samtools/main.nf'
include { RSEQC        } from '../../../modules/rseqc/main.nf'

workflow ALIGNMENT_STAR {
    take:
    fasta_ch    // channel: path(fasta)
    gtf_ch      // channel: path(gtf)
    reads_ch    // channel: [ meta, trimmed_reads1, trimmed_reads2 ]
    bed_ch      // channel: path(bed) for RSeQC

    main:
    STAR_INDEX(fasta_ch, gtf_ch)
    STAR_ALIGN(STAR_INDEX.out.index, reads_ch)

    SAMTOOLS(STAR_ALIGN.out.bam)
    RSEQC(STAR_ALIGN.out.bam, bed_ch)

    emit:
    bam         = STAR_ALIGN.out.bam
    bai         = STAR_ALIGN.out.bai
    log_final   = STAR_ALIGN.out.log_final
    junctions   = STAR_ALIGN.out.junctions
    index       = STAR_INDEX.out.index
    samtools    = SAMTOOLS.out.stats
    rseqc       = RSEQC.out.result
}