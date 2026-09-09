// =====================================================
// Module: STAR_ALIGN
// Spliced alignment of paired-end reads to the STAR index.
// Mirrors validated C1 command exactly:
//   --runMode alignReads --outSAMtype BAM SortedByCoordinate
//   --readFilesCommand zcat --outSAMattributes NH HI AS nM
//   --outFilterMultimapNmax 20 --outFilterMismatchNmax 10
// =====================================================

process STAR_ALIGN {
    tag "${meta.id}: ${reads1} + ${reads2}"
    publishDir "${params.outdir}/alignment",
        mode: 'copy', overwrite: true,
        pattern: '*.bam'
    publishDir "${params.outdir}/alignment",
        mode: 'copy', overwrite: true,
        pattern: '*_Log.{out,final.out}'
    publishDir "${params.outdir}/alignment",
        mode: 'copy', overwrite: true,
        pattern: '*_SJ.out.tab'

    input:
    path index
    tuple val(meta), path(reads1), path(reads2)

    output:
    tuple val(meta), path("*_Aligned.sortedByCoord.out.bam"), emit: bam
    tuple val(meta), path("*_Log.final.out"), emit: log_final
    tuple val(meta), path("*_Log.out"), emit: log
    tuple val(meta), path("*_SJ.out.tab"), emit: junctions

    script:
    """
    STAR \\
        --runMode alignReads \\
        --runThreadN ${task.cpus} \\
        --genomeDir ${index} \\
        --readFilesIn ${reads1} ${reads2} \\
        --readFilesCommand zcat \\
        --outSAMtype BAM SortedByCoordinate \\
        --outFileNamePrefix ${meta.id}_ \\
        --outSAMattributes NH HI AS nM \\
        --outFilterMultimapNmax ${params.star_multimap_nmax} \\
        --outFilterMismatchNmax ${params.star_mismatch_nmax} \\
        --outTmpDir star_tmp
    """

    stub:
    """
    touch ${meta.id}_Aligned.sortedByCoord.out.bam ${meta.id}_Aligned.sortedByCoord.out.bam.bai ${meta.id}_Log.final.out ${meta.id}_Log.out ${meta.id}_SJ.out.tab
    """
}