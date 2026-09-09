// =====================================================
// Module: FASTQC
// Runs FastQC on a single gzipped FASTQ file.
// The QC stage ('raw' | 'clean') is carried in meta.stage
// and selects the publish directory dynamically.
// Empty `stub:` reproduces the declared outputs.
// =====================================================

process FASTQC {
    tag "${meta.id}: ${reads}"

    publishDir path: { "${params.outdir}/fastqc/${meta.stage}" },
        mode: 'copy', overwrite: true,
        pattern: '*_fastqc.{zip,html}'
    publishDir path: { "${params.outdir}/fastqc/${meta.stage}" },
        mode: 'copy', overwrite: true,
        pattern: '*_fastqc/summary.txt'

    input:
    tuple val(meta), path(reads)

    output:
    tuple val(meta), path("*_fastqc.html"), emit: html
    tuple val(meta), path("*_fastqc.zip"),  emit: zip
    tuple val(meta), path("*_fastqc/summary.txt"), emit: summary

    script:
    """
    fastqc \\
        --threads ${task.cpus} \\
        --outdir . \\
        --extract \\
        ${reads}
    """

    stub:
    """
    base=\$(basename "${reads}" .fastq.gz)
    base=\${base%.fastq}
    mkdir -p "\${base}_fastqc"
    touch "\${base}_fastqc.html" "\${base}_fastqc.zip" "\${base}_fastqc/summary.txt"
    """
}