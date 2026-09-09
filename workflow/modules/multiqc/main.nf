// =====================================================
// Module: MULTIQC
// Final aggregation (MultiQC 1.35) of FastQC (raw+clean),
// fastp, STAR, SAMtools and RSeQC reports into one HTML.
// =====================================================

process MULTIQC {
    tag "MULTIQC"
    publishDir "${params.outdir}/multiqc",
        mode: 'copy', overwrite: true

    input:
    path fastqc_complete
    path fastp_complete
    path star_complete
    path samtools_complete
    path rseqc_complete

    output:
    path "multiqc_report.html", emit: report

    script:
    """
    multiqc \\
        -q \\
        --title '${params.multiqc_title}' \\
        --filename multiqc_report.html \\
        --outdir . \\
        ${fastqc_complete} ${fastp_complete} ${star_complete} ${samtools_complete} ${rseqc_complete}
    """

    stub:
    """
    touch multiqc_report.html
    """
}