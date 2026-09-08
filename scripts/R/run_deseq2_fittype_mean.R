options(warn = 1, width = 120)
suppressMessages(library(DESeq2))

out_dir <- "results/differential_expression"

counts <- read.delim("results/counts/gene_counts.txt", header = TRUE, skip = 1, row.names = 1, check.names = FALSE)
sample_cols <- grep("Aligned.sortedByCoord.out.bam", colnames(counts), value = TRUE)
order_ids <- c("C1", "C2", "C3", "T1", "T2", "T3")
counts <- as.matrix(counts[, sample_cols, drop = FALSE])
colnames(counts) <- order_ids
storage.mode(counts) <- "integer"

coldata <- data.frame(
  row.names = order_ids,
  donor = factor(c("N61311", "N052611", "N080611", "N61311", "N052611", "N080611")),
  condition = factor(c("control", "control", "control", "treatment", "treatment", "treatment"))
)

cat("== Retry: design = ~ donor + condition, fitType = 'mean' (DESeq2 documented remedy for very small gene sets) ==\n")
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ donor + condition)
dds <- DESeq(dds, fitType = "mean")

cat("\n== sizeFactors ==", "\n")
print(sizeFactors(dds))
cat("\n== dispersions (gene-wise / final) ==", "\n")
print(dispersions(dds))

cat("\n== results(treatment vs control, paired donor model) ==", "\n")
res <- results(dds, contrast = c("condition", "treatment", "control"))
print(res)

res_df <- as.data.frame(res)
res_df$gene_id <- rownames(res)
res_df$significant <- ifelse(!is.na(res_df$padj) & res_df$padj < 0.05 & abs(res_df$log2FoldChange) >= 1.0, "YES", "NO")
res_df <- res_df[, c("gene_id", "baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj", "significant")]
res_df[, c("baseMean", "log2FoldChange", "lfcSE", "stat")] <- round(res_df[, c("baseMean", "log2FoldChange", "lfcSE", "stat")], 4)
write.csv(res_df, file = file.path(out_dir, "real_deseq2_results.csv"), row.names = FALSE, na = "")

up <- res_df[res_df$padj < 0.05 & res_df$log2FoldChange >= 1.0, , drop = FALSE]
down <- res_df[res_df$padj < 0.05 & res_df$log2FoldChange <= -1.0, , drop = FALSE]
write.csv(up, file = file.path(out_dir, "real_sig_upregulated_genes.csv"), row.names = FALSE, na = "")
write.csv(down, file = file.path(out_dir, "real_sig_downregulated_genes.csv"), row.names = FALSE, na = "")
saveRDS(dds, file.path(out_dir, "real_dds_fitted.rds"))
saveRDS(res, file.path(out_dir, "real_deseq2_results.rds"))

cat("\n== files written ==\n")
print(list.files(out_dir))