// =====================================================
// Module: DESEQ2
// Differential expression with the validated R entry point
//   scripts/R/run_deseq2_fittype_mean.R
// Design ~ donor + condition, fitType="mean", contrast
// treatment vs control (documented remedy for very small gene sets).
// The script is invoked UNCHANGED, so inputs are staged into the
// workdir under the exact relative layout it expects
// (results/counts/gene_counts.txt -> results/differential_expression/).
// =====================================================

process DESEQ2 {
    tag "DESEQ2: design ~ donor + condition, fitType='mean'"
    publishDir "${params.outdir}/differential_expression",
        mode: 'copy', overwrite: true,
        pattern: '**/real_deseq2_results.csv'
    publishDir "${params.outdir}/differential_expression",
        mode: 'copy', overwrite: true,
        pattern: '**/real_{sig_upregulated,sig_downregulated}_genes.csv'
    publishDir "${params.outdir}/differential_expression",
        mode: 'copy', overwrite: true,
        pattern: '**/real_{dds_fitted,deseq2_results}.rds'

    input:
    path counts
    path script

    output:
    path "results/differential_expression/real_deseq2_results.csv", emit: csv
    path "results/differential_expression/real_dds_fitted.rds", emit: dds
    path "results/differential_expression/real_deseq2_results.rds", emit: rds
    path "results/differential_expression/real_sig_upregulated_genes.csv", emit: up
    path "results/differential_expression/real_sig_downregulated_genes.csv", emit: down

    script:
    """
    mkdir -p results/counts results/differential_expression
    cp ${counts} results/counts/gene_counts.txt
    Rscript ${script}
    """

    stub:
    """
    mkdir -p results/differential_expression
    touch results/differential_expression/real_deseq2_results.csv \\
          results/differential_expression/real_dds_fitted.rds \\
          results/differential_expression/real_deseq2_results.rds \\
          results/differential_expression/real_sig_upregulated_genes.csv \\
          results/differential_expression/real_sig_downregulated_genes.csv
    """
}