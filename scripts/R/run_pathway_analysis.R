options(warn = 1, width = 120)
suppressMessages(library(clusterProfiler))
suppressMessages(library(org.Hs.eg.db))
suppressMessages(library(AnnotationDbi))

out_dir <- "results/pathway_analysis"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
log_file <- file.path(out_dir, "real_pathway_run.log")
sink(log_file, split = TRUE)
on.exit(sink())

cat("== Real pathway analysis: clusterProfiler ORA on Step 7 real DESeq2 DEGs ==\n")
cat("clusterProfiler ", as.character(packageVersion("clusterProfiler")),
    " | org.Hs.eg.db ", as.character(packageVersion("org.Hs.eg.db")), "\n\n", sep = "")

## ---------- 1. Real DEG input ----------
res <- read.csv("results/differential_expression/real_deseq2_results.csv",
                stringsAsFactors = FALSE)
deg <- res[res$significant == "YES", "gene_id"]
cat("Real DESeq2 genes:", nrow(res), "| DEGs (significant=YES):",
    length(deg), paste(deg, collapse = ", "), "\n")

## Universe = the real mini-reference background genes (honest to experiment).
univ <- res$gene_id
stopifnot(length(univ) == 3)

strip_ver <- function(x) sub("\\..*$", "", x)

deg_univ_map <- unique(data.frame(
  original = c(deg, univ),
  versionless = strip_ver(c(deg, univ))
))

resmap <- bitr(strip_ver(c(deg, univ)),
               fromType = "ENSEMBL", toType = "ENTREZID",
               OrgDb = org.Hs.eg.db)
cat("\nEntrez mapping (real mini-reference universe):\n")
symbols <- AnnotationDbi::select(org.Hs.eg.db,
                                 keys = resmap$ENTREZID, columns = "SYMBOL", keytype = "ENTREZID")
print(merge(resmap, symbols, by = "ENTREZID"))
write.csv(merge(resmap, symbols, by = "ENTREZID"),
          file = file.path(out_dir, "real_gene_map.csv"), row.names = FALSE)

deg_entrez  <- unique(resmap$ENTREZID[resmap$ENSEMBL %in% strip_ver(deg)])
univ_entrez <- unique(resmap$ENTREZID)

## ---------- 2. GO ORA (BP / MF / CC) ----------
write_enrich <- function(x, file) {
  if (is.null(x) || nrow(as.data.frame(x)) == 0) {
    writeLines("ID\tDescription\tGeneRatio\tBgRatio\tpvalue\tp.adjust\tqvalue\tgeneID\tCount",
               file)
    cat("[empty] ", file, "\n", sep = "")
    return(invisible(NULL))
  }
  df <- as.data.frame(x)
  write.table(df, file, sep = "\t", row.names = FALSE, quote = FALSE)
  cat("[written] ", file, " (", nrow(df), " terms)\n", sep = "")
}

ontologies <- c("BP", "MF", "CC")
go_res <- list()
cat("\n## GO ORA (universe = real 3-gene mini-reference) ##\n")
for (ont in ontologies) {
  cat("-- ", ont, " --\n", sep = "")
  suppressMessages(
    go_res[[ont]] <- enrichGO(
      gene          = deg_entrez,
      universe      = univ_entrez,
      OrgDb         = org.Hs.eg.db,
      keyType       = "ENTREZID",
      ont           = ont,
      pAdjustMethod = "BH",
      pvalueCutoff  = 0.05,
      qvalueCutoff  = 0.2,
      readable      = TRUE
    )
  )
  write_enrich(go_res[[ont]], file.path(out_dir, sprintf("real_go_%s.csv", tolower(ont))))
}

## ---------- 3. KEGG ORA (online REST API; failure recorded as genuine) ----------
cat("\n## KEGG ORA (organism hsa, online KEGG REST) ##\n")
kegg_res <- NULL
kegg_err <- NULL
kegg_res <- tryCatch(
  enrichKEGG(gene = deg_entrez, universe = univ_entrez,
             organism = "hsa", keyType = "kegg",
             pvalueCutoff = 0.05, qvalueCutoff = 0.2),
  error = function(e) {
    kegg_err <<- conditionMessage(e)
    NULL
  }
)
if (is.null(kegg_res)) {
  msg <- if (is.null(kegg_err)) "no terms at thresholds (or downstream NA)" else kegg_err
  cat("KEGG enrichment not returned (genuine): ", msg, "\n", sep = "")
  writeLines(c("note", paste0("no KEGG enrichment returned: ", msg)),
             file.path(out_dir, "real_kegg.csv"))
} else {
  write_enrich(kegg_res, file.path(out_dir, "real_kegg.csv"))
}

## ---------- 4. Summary ----------
cat("\n== Summary ==")
cat("\nGO BP terms:", nrow(as.data.frame(go_res$BP)), "| MF:", nrow(as.data.frame(go_res$MF)),
    "| CC:", nrow(as.data.frame(go_res$CC)))
cat("\nKEGG terms:", ifelse(is.null(kegg_res), "NA (network/empty)", nrow(as.data.frame(kegg_res))))
cat("\nGSEA: SKIPPED (out of scope at 3 genes; a ranked list of 3 is not a meaningful GSEA).\n")
cat("\n-- sessionInfo --\n")
print(sessionInfo())