// =====================================================
// Module: VISUALIZATION
// Distances/PCA/MA/volcano/heatmap via the validated R entry point
//   scripts/R/run_visualization.R
// Input RDS files are staged into results/differential_expression/
// (the layout the script reads), outputs go to results/visualization/.
// =====================================================

process VISUALIZATION {
    tag "VISUALIZATION"
    publishDir "${params.outdir}/visualization",
        mode: 'copy', overwrite: true,
        pattern: '**/real_*'

    input:
    path dds
    path deseq2_rds
    path script

    output:
    path "results/visualization/real_vst_counts.csv", emit: vst
    path "results/visualization/real_pca_data.csv", emit: pca
    path "results/visualization/real_ma_data.csv", emit: ma
    path "results/visualization/real_volcano_data.csv", emit: volcano
    path "results/visualization/real_sample_distances.csv", emit: distances
    path "results/visualization/real_heatmap_clustered_matrix.csv", emit: heatmap
    path "results/visualization/real_heatmap_clustering.rds", emit: clustering

    script:
    """
    mkdir -p results/differential_expression
    cp ${dds} results/differential_expression/real_dds_fitted.rds
    cp ${deseq2_rds} results/differential_expression/real_deseq2_results.rds
    Rscript ${script}
    """

    stub:
    """
    mkdir -p results/visualization
    touch results/visualization/real_vst_counts.csv \\
          results/visualization/real_pca_data.csv \\
          results/visualization/real_ma_data.csv \\
          results/visualization/real_volcano_data.csv \\
          results/visualization/real_sample_distances.csv \\
          results/visualization/real_heatmap_clustered_matrix.csv \\
          results/visualization/real_heatmap_clustering.rds
    """
}