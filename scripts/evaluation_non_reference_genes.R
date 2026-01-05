library(data.table)
library(ggplot2)
library(tidyr)

lessDecimals<-read.csv("lessDecimals.csv")

### generate the non_reference_gene expression atlas
files <- list.files("~/Seafile/Konstantinides_lab/projects/Leonardo_Novosparc/atlas/_Updated_245_CSV_Files/", pattern = "\\.csv$", full.names = TRUE)

mat_list <- lapply(files, function(f) {
  as.matrix(fread(f))  # numeric only
})

non_reference_table <- do.call(rbind, mat_list)  # numeric matrix

source_files <- rep(tools::file_path_sans_ext(basename(files)), times = sapply(mat_list, nrow))


# df <- rbindlist(
#   lapply(files, function(f) {
#     dt <- fread(f)
#     # add filename without .csv
#     dt[, source_file := tools::file_path_sans_ext(basename(f))]
#     dt
#   }),
#   use.names = TRUE,
#   fill = TRUE
# )

non_reference_table<-non_reference_table[,1:3]
non_reference_gene_expression<-read.csv("non_reference_gene_expression.csv", sep = ";", row.names = 1)
non_reference_gene_expression<-as.matrix(non_reference_gene_expression)

non_reference_table <- cbind(non_reference_table, matrix(NA, nrow = nrow(non_reference_table), ncol = ncol(non_reference_gene_expression)))
colnames(non_reference_table)[4:19]<-colnames(non_reference_gene_expression)

for (i in 1:dim(non_reference_table)[1]) {
  non_reference_table[i,4:19]<-non_reference_gene_expression[source_files[i],]
print(i)
  }

head(non_reference_table)
non_reference_table[,1:3]<-round(non_reference_table[,1:3], digits = 3)


non_reference_genes <- read.table("non_reference_genes.txt", header = F)

results<-matrix(nrow = dim(non_reference_genes)[1], ncol = 2)
colnames(results)<-c("precision", "recall")

for (j in 1:dim(non_reference_genes)[1]) {
  gene_of_interest<-non_reference_genes[j,1]
  
  reconstruction_pre<-lessDecimals[, c(1:3, which(names(lessDecimals) == gene_of_interest))]
  reconstruction <- reconstruction_pre[reconstruction_pre[[gene_of_interest]] > non_reference_genes[j,2], ]
  reconstruction[,1:3]<-round(reconstruction[,1:3], digits = 3)
  
  k=0
  for (i in 1:dim(reconstruction)[1]) {
    
    tryCatch({
      
      target <- as.numeric(reconstruction[i, 1:3])
      
      match_row <- non_reference_table[
        non_reference_table[,1] == target[1] &
          non_reference_table[,2] == target[2] &
          non_reference_table[,3] == target[3],
      ]
      
      if (sum(match_row[gene_of_interest], na.rm = TRUE) > 0) {
        k <- k + 1
      }
      
    }, error = function(e) {
      message("Error at iteration ", i, ": ", e$message)
      # skip to next iteration
    })
    
  }
  
  
  precision=k/i # this is TP/TP+FP (precision)
  recall=k/sum(non_reference_table[,gene_of_interest], na.rm = TRUE) # this is TP/TP+FN (recall/sensitivity)
  
  results[j,1]<-precision
  results[j,2]<-recall
  print(j)
}

write.table(results, file = "precision_recall_non_reference_genes.txt", quote=F, sep = "\t")

results <- as.data.frame(results)
results_long <- pivot_longer(results,
                             cols = c("precision", "recall"),
                             names_to = "metric",
                             values_to = "value")


### PLOT OPTION 1
ggplot(results_long, aes(x = metric, y = value, fill = metric)) +
  geom_boxplot(width = 0.3, alpha = 0.8, outlier.alpha = 0.3, color = "black", linewidth = 0.3) +
  scale_fill_manual(values = c(
    "precision" = "#377eb8",   # stronger blue
    "recall"    = "grey70"     # subtle grey
  )) +
  labs(
    title = "Precision and Recall Across Non Reference Genes",
    x = "",
    y = "Value"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 16)
  )

### PLOT OPTION 2
p <- ggplot(results_long, aes(x = metric, y = value, fill = metric)) +
  geom_violin(width = 0.5, alpha = 0.4, color = "grey60") +
  geom_boxplot(width = 0.15, outlier.alpha = 0.2, color = "black", fill = "white", linewidth = 0.3) +
  scale_fill_manual(values = c(
    "precision" = "#08315c",
    "recall" = "grey40"
  )) +
  scale_y_continuous(limits = c(0, 1)) +   # Force y-axis to start at 0
  labs(title = "Precision and Recall Across Non Reference Genes",
       x = "", y = "Value") +
  coord_cartesian(ylim = c(0, NA)) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 16),
    #axis.line = element_line(colour = "grey60"),
    #axis.ticks = element_line(colour = "grey60"),
    panel.grid.major = element_line(colour = "grey80"),
    panel.grid.minor = element_line(colour = "grey80")
  )
p


ggsave("precision_recall_non_reference_genes.pdf", p, width = 4, height = 8)
