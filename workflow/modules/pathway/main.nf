// =====================================================
// Module: PATHWAY
// GO/KEGG enrichment on the DESeq2 output via the validated
// R entry point scripts/R/run_pathway_analysis.R.
// Input CSV is staged into results/differential_expression/,
// outputs go to results/pathway_analysis/.
// =====================================================

process PATHWAY {
    tag "PATHWAY"
    publishDir "${params.outdir}/pathway_analysis",
        mode: 'copy', overwrite: true,
        pattern: '**/real_*'

    input:
    path deseq2_csv
    path script

    output:
    path "results/pathway_analysis/real_gene_map.csv", emit: gene_map
    path "results/pathway_analysis/real_go_bp.csv", emit: go_bp
    path "results/pathway_analysis/real_go_mf.csv", emit: go_mf
    path "results/pathway_analysis/real_go_cc.csv", emit: go_cc
    path "results/pathway_analysis/real_kegg.csv", emit: kegg
    path "results/pathway_analysis/real_pathway_run.log", emit: log

    script:
    """
    mkdir -p results/differential_expression
    cp ${deseq2_csv} results/differential_expression/real_deseq2_results.csv
    Rscript ${script}
    """

    stub:
    """
    mkdir -p results/pathway_analysis
    touch results/pathway_analysis/real_gene_map.csv \\
          results/pathway_analysis/real_go_bp.csv \\
          results/pathway_analysis/real_go_mf.csv \\
          results/pathway_analysis/real_go_cc.csv \\
          results/pathway_analysis/real_kegg.csv \\
          results/pathway_analysis/real_pathway_run.log
    """
}