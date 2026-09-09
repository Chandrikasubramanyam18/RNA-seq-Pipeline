// =====================================================
// Module: FEATURECOUNTS
// Gene-level count summarisation with featureCounts (subread 2.1.1).
// Mirrors validated command:
//   featureCounts -a <gtf> -o gene_counts.txt -T <cpus> -p -s 0 <bams>
// BAM basenames (<sample>_Aligned.sortedByCoord.out.bam) become the
// count-table sample columns expected by the downstream DESeq2 R script.
// =====================================================

process FEATURECOUNTS {
    tag "featureCounts: ${bams.collect{it.toString().tokenize('/').last()}.join(', ')}"
    publishDir "${params.outdir}/counts",
        mode: 'copy', overwrite: true,
        pattern: 'gene_counts.txt*'

    input:
    path gtf
    path bams

    output:
    path "gene_counts.txt", emit: counts
    path "gene_counts.txt.summary", emit: summary

    script:
    """
    featureCounts \\
        -a ${gtf} \\
        -o gene_counts.txt \\
        -T ${task.cpus} \\
        -p \\
        -s 0 \\
        ${bams}
    """

    stub:
    """
    touch gene_counts.txt gene_counts.txt.summary
    """
}