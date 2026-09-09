// =====================================================
// Subworkflow: INTERPRETATION
// DESeq2 -> Visualization -> Pathway analysis.
// R scripts are the validated committed entry points under
// scripts/R/, staged at the exact relative layout they expect.
// =====================================================

include { DESEQ2         } from '../../modules/deseq2/main.nf'
include { VISUALIZATION  } from '../../modules/visualization/main.nf'
include { PATHWAY        } from '../../modules/pathway/main.nf'

workflow INTERPRETATION {
    take:
    counts_ch   // channel: path(gene_counts.txt)

    main:
    ch_script_deseq2 = Channel.fromPath("${projectDir}/../scripts/R/run_deseq2_fittype_mean.R")
    ch_script_viz    = Channel.fromPath("${projectDir}/../scripts/R/run_visualization.R")
    ch_script_pathw  = Channel.fromPath("${projectDir}/../scripts/R/run_pathway_analysis.R")

    DESEQ2(counts_ch, ch_script_deseq2)

    VISUALIZATION(DESEQ2.out.dds, DESEQ2.out.rds, ch_script_viz)
    PATHWAY(DESEQ2.out.csv, ch_script_pathw)

    emit:
    deseq2_results        = DESEQ2.out.csv
    visualization_vst     = VISUALIZATION.out.vst
    visualization_pca     = VISUALIZATION.out.pca
    pathway_gene_map      = PATHWAY.out.gene_map
    pathway_kegg          = PATHWAY.out.kegg
}