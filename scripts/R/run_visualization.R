options(warn = 1, width = 120)
suppressMessages(library(DESeq2))
suppressMessages(library(MatrixGenerics))

out_dir <- "results/visualization"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

## Real inputs: the fitted DESeq2 object produced in Step 7 (fitType="mean"),
## plus the real count matrix and real results table.
dds <- readRDS("results/differential_expression/real_dds_fitted.rds")
res <- readRDS("results/differential_expression/real_deseq2_results.rds")
res_df <- as.data.frame(res)
res_df$gene_id <- rownames(res_df)
res_df$significant <- ifelse(!is.na(res_df$padj) & res_df$padj < 0.05 & abs(res_df$log2FoldChange) >= 1.0, "YES", "NO")

cat("== Real inputs: fitted DESeq2 dds (", nrow(dds), " genes x ", ncol(dds), " samples) ==\n", sep = "")
cat("Samples:", colnames(dds), "\n")

## ---------- 1. VST-stabilized counts ----------
cat("\n[1] VST stabilization\n")
vst_out <- vst(dds, blind = FALSE, nsub = 3, fitType = "mean")
vst_mat <- assay(vst_out)
write.csv(as.data.frame(vst_mat), file = file.path(out_dir, "real_vst_counts.csv"))
cat("VST matrix written: ", nrow(vst_mat), "x", ncol(vst_mat), "\n", sep = "")

## ---------- 2. PCA (samples in gene space) ----------
cat("\n[2] PCA\n")
pca <- prcomp(t(vst_mat), center = TRUE, scale. = TRUE)
props <- summary(pca)$importance[2, ]
pca_df <- data.frame(
  sample  = rownames(pca$x),
  pc1     = pca$x[, 1],
  pc2     = pca$x[, 2],
  pc1_var = props[1],
  pc2_var = props[2],
  donor    = colData(dds)$donor,
  condition = colData(dds)$condition
)
write.csv(pca_df, file = file.path(out_dir, "real_pca_data.csv"), row.names = FALSE)
cat("PCA (PC1 ", round(100*props[1], 1), "%, PC2 ", round(100*props[2], 1), "%)\n", sep = "")
print(pca_df[, c("sample", "pc1", "pc2", "condition", "donor")])

## ---------- 3. MA data ----------
cat("\n[3] MA data\n")
ma_df <- data.frame(
  gene_id       = res_df$gene_id,
  baseMean      = res_df$baseMean,
  log2FoldChange = res_df$log2FoldChange
)
write.csv(ma_df, file = file.path(out_dir, "real_ma_data.csv"), row.names = FALSE)

## ---------- 4. Volcano data (real 3 genes only) ----------
cat("\n[4] Volcano data\n")
volcano_df <- data.frame(
  gene           = res_df$gene_id,
  log2FoldChange = res_df$log2FoldChange,
  minusLog10Padj = round(-log10(pmax(res_df$padj, 1e-300)), 3),
  significant    = res_df$significant
)
write.csv(volcano_df, file = file.path(out_dir, "real_volcano_data.csv"), row.names = FALSE)
print(volcano_df)

## ---------- 5. Sample-distance + clustered heatmap data ----------
cat("\n[5] Sample-distance heatmap data\n")
dist_mat <- as.matrix(dist(t(vst_mat)))
write.csv(as.data.frame(dist_mat), file = file.path(out_dir, "real_sample_distances.csv"))
hclust_col <- hclust(dist(t(vst_mat)), method = "complete")
cat("Column clustering order (complete linkage):", hclust_col$order, "\n")

gene_dist <- dist(vst_mat)
hclust_row <- hclust(gene_dist, method = "complete")
row_order <- vst_mat[hclust_row$order, , drop = FALSE]
write.csv(as.data.frame(row_order), file = file.path(out_dir, "real_heatmap_clustered_matrix.csv"))
cat("Clustered heatmap matrix (rows ordered):\n")
print(round(row_order, 2))

saveRDS(list(dist_mat = dist_mat, hclust_col = hclust_col, hclust_row = hclust_row),
        file = file.path(out_dir, "real_heatmap_clustering.rds"))

## ---------- summary ----------
cat("\n== Written files ==", "\n")
print(list.files(out_dir, pattern = "^real_"))