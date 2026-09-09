// =====================================================
// Subworkflow: QUANTIFICATION_FEATURECOUNTS
// Gene-level counts from all aligned BAMs.
// =====================================================

include { FEATURECOUNTS } from '../../../modules/featurecounts/main.nf'

workflow QUANTIFICATION_FEATURECOUNTS {
    take:
    gtf_ch    // channel: path(gtf)
    bam_ch    // channel: [ meta, bam ] (collected inside)

    main:
    ch_bams = bam_ch.collect { meta, bam -> bam }

    FEATURECOUNTS(gtf_ch, ch_bams)

    emit:
    counts       = FEATURECOUNTS.out.counts
    counts_summary = FEATURECOUNTS.out.summary
}