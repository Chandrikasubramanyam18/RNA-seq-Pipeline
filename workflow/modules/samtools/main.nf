// =====================================================
// Module: SAMTOOLS
// Alignment QC via samtools 1.24: flagstat, idxstats, stats.
// =====================================================

process SAMTOOLS {
    tag "${meta.id}"
    publishDir "${params.outdir}/alignment_qc/samtools",
        mode: 'copy', overwrite: true,
        pattern: '*.{flagstat,idxstats,stats.txt}'

    input:
    tuple val(meta), path(bam)

    output:
    tuple val(meta), path("${meta.id}.flagstat"), emit: flagstat
    tuple val(meta), path("${meta.id}.idxstats"), emit: idxstats
    tuple val(meta), path("${meta.id}.stats.txt"), emit: stats

    script:
    """
    samtools flagstat ${bam} > ${meta.id}.flagstat
    samtools idxstats ${bam} > ${meta.id}.idxstats
    samtools stats ${bam} > ${meta.id}.stats.txt
    """

    stub:
    """
    touch ${meta.id}.flagstat ${meta.id}.idxstats ${meta.id}.stats.txt
    """
}