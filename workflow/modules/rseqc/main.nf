// =====================================================
// Module: RSEQC
// Strandness inference with RSeQC 5.0.5 (infer_experiment.py)
// against the reference gene BED. Tutorial-scale bed = the
// mini_real refgene.bed12 file.
// =====================================================

process RSEQC {
    tag "${meta.id}"
    publishDir "${params.outdir}/alignment_qc/rseqc",
        mode: 'copy', overwrite: true,
        pattern: '*.txt'

    input:
    tuple val(meta), path(bam)
    path bed

    output:
    tuple val(meta), path("${meta.id}_rseqc_infer_experiment.txt"), emit: result

    script:
    """
    infer_experiment.py -i ${bam} -r ${bed} > ${meta.id}_rseqc_infer_experiment.txt
    """

    stub:
    """
    touch ${meta.id}_rseqc_infer_experiment.txt
    """
}