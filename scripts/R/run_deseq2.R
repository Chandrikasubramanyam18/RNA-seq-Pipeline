options(warn = 1, width = 120)
suppressMessages(library(DESeq2))
suppressMessages(library(GenomicRanges))

out_dir <- "results/differential_expression"
stopifnot(dir.exists(out_dir))

cts_file <- "results/counts/gene_counts.txt"
counts <- read.delim(cts_file, header = TRUE, skip = 1, row.names = 1, check.names = FALSE)
sample_cols <- grep("Aligned.sortedByCoord.out.bam", colnames(counts), value = TRUE)
order_ids <- c("C1", "C2", "C3", "T1", "T2", "T3")
stopifnot(length(sample_cols) == 6L)
counts <- as.matrix(counts[, sample_cols, drop = FALSE])
colnames(counts) <- order_ids
storage.mode(counts) <- "integer"

cat("== Count matrix ==", "\n")
print(counts)
cat("\nDimension: ", nrow(counts), " x ", ncol(counts), "\n", sep = "")

coldata <- data.frame(
  row.names = order_ids,
  donor = factor(c("N61311", "N052611", "N080611", "N61311", "N052611", "N080611")),
  condition = factor(c("control", "control", "control", "treatment", "treatment", "treatment"))
)
cat("\n== colData ==", "\n")
print(coldata)
cat("\nDesign: ~ donor + condition  (3 paired donors)\n")
with(coldata, table(donor, condition))

dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ donor + condition)
cat("\n== DESeqDataSet created ==", "\n")

cat("\n== Model matrix (design) ==", "\n")
print(model.matrix(~ donor + condition, coldata))

cat("\n== Running DESeq (real R/DESeq2) ==", "\n")
dds <- DESeq(dds)

cat("\n== Size factors ==", "\n")
sf <- sizeFactors(dds)
print(sf)

cat("\n== Per-gene dispersion estimates ==", "\n")
disp <- dispersions(dds)
print(disp)

cat("\n== Results: condition treatment vs control (Wald) ==", "\n")
res <- results(dds, contrast = c("condition", "treatment", "control"))
print(res)

res_df <- as.data.frame(res)
res_df$gene_id <- rownames(res)
res_df$significant <- ifelse(!is.na(res_df$padj) & res_df$padj < 0.05 & abs(res_df$log2FoldChange) >= 1.0, "YES", "NO")
res_df <- res_df[, c("gene_id", "baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj", "significant")]
res_df[, c("baseMean", "log2FoldChange", "lfcSE", "stat")] <- round(res_df[, c("baseMean", "log2FoldChange", "lfcSE", "stat")], 4)
write.csv(res_df, file = file.path(out_dir, "deseq2_results.csv"), row.names = FALSE, na = "")

up <- res_df[res_df$padj < 0.05 & res_df$log2FoldChange >= 1.0, , drop = FALSE]
down <- res_df[res_df$padj < 0.05 & res_df$log2FoldChange <= -1.0, , drop = FALSE]
write.csv(up, file = file.path(out_dir, "sig_upregulated_genes.csv"), row.names = FALSE, na = "")
write.csv(down, file = file.path(out_dir, "sig_downregulated_genes.csv"), row.names = FALSE, na = "")

mcols_df <- data.frame(mcols(res))
write.csv(mcols_df, file = file.path(out_dir, "deseq2_result_metadata.csv"), row.names = TRUE)

saveRDS(dds, file.path(out_dir, "dds_fitted.rds"))
saveRDS(res, file.path(out_dir, "deseq2_results.rds"))

cat("\n== Files written under ", out_dir, " ==", "\n")
print(list.files(out_dir))