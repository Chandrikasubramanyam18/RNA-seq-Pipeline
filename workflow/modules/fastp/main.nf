// =====================================================
// Module: FASTP
// Paired-end adapter/quality trimming.
// Mirrors validated command: --qualified_quality_phred 20,
// --length_required 30, --detect_adapter_for_pe,
// --trim_poly_g, --trim_poly_x.
// =====================================================

process FASTP {
    tag "${meta.id}: ${reads1} + ${reads2}"
    publishDir "${params.outdir}/fastp",
        mode: 'copy', overwrite: true,
        pattern: '*.{json,html}'
    publishDir "${params.outdir}/processed",
        mode: 'copy', overwrite: true,
        pattern: '*_trimmed_R{1,2}.fastq.gz'

    input:
    tuple val(meta), path(reads1), path(reads2)

    output:
    tuple val(meta), path("${meta.id}_trimmed_R1.fastq.gz"), path("${meta.id}_trimmed_R2.fastq.gz"), emit: reads
    tuple val(meta), path("${meta.id}_fastp.json"), emit: json
    tuple val(meta), path("${meta.id}_fastp.html"), emit: html

    script:
    """
    fastp \\
        --in1 ${reads1} \\
        --in2 ${reads2} \\
        --out1 ${meta.id}_trimmed_R1.fastq.gz \\
        --out2 ${meta.id}_trimmed_R2.fastq.gz \\
        --thread ${task.cpus} \\
        --qualified_quality_phred ${params.fastp_qual} \\
        --length_required ${params.fastp_min_len} \\
        --detect_adapter_for_pe \\
        --trim_poly_g \\
        --trim_poly_x \\
        --html ${meta.id}_fastp.html \\
        --json ${meta.id}_fastp.json \\
        --report_title "fastp report: ${meta.id}"
    """

    stub:
    """
    touch ${meta.id}_trimmed_R1.fastq.gz ${meta.id}_trimmed_R2.fastq.gz ${meta.id}_fastp.json ${meta.id}_fastp.html
    """
}