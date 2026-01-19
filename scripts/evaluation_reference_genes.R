  library(data.table)
  library(ggplot2)
  library(tidyr)
  
  setwd("~/Seafile/Konstantinides_lab/Konstantinides_lab_papers/drafts/Leonardo_paper/revised_DEVELOPMENTAL_BIOLOGY/")
  atlas<-read.csv("~/Seafile/Konstantinides_lab/Konstantinides_lab_papers/drafts/Leonardo_paper/GitHub_page/NovoSparcLarvaDm/data/Last_ATLAS.csv")
  atlas[,1:3]<-round(atlas[,1:3], digits = 3)
  head(atlas)
  lessDecimals<-read.csv("../Novosparc_WebApp/lessDecimals.csv")
  marker_genes <- read.table("marker_genes.txt", header = F)
  
  results<-matrix(nrow = dim(marker_genes)[1], ncol = 2)
  colnames(results)<-c("precision", "recall")
  rownames(results)<-marker_genes[,1]
  
  results2<-matrix(nrow = dim(marker_genes)[1], ncol = 5)
  colnames(results2)<-c("TP", "FP", "TN", "FN", "F1_score")
  rownames(results2)<-marker_genes[,1]
  
  for (j in 1:dim(marker_genes)[1]) {
  gene_of_interest<-marker_genes[j,1]
  
  reconstruction_pre<-lessDecimals[, c(1:3, which(names(lessDecimals) == gene_of_interest))]
  reconstruction <- reconstruction_pre[reconstruction_pre[[gene_of_interest]] > marker_genes[j,2], ]
  reconstruction[,1:3]<-round(reconstruction[,1:3], digits = 3)
  
  k=0
  for (i in 1:dim(reconstruction)[1]) {
    
    tryCatch({
      
      target <- as.numeric(reconstruction[i, 1:3])
      
      match_row <- atlas[
        atlas[,1] == target[1] &
          atlas[,2] == target[2] &
          atlas[,3] == target[3],
      ]
      
      if (sum(match_row[gene_of_interest]) > 0) {
        k <- k + 1
      }
      
    }, error = function(e) {
      message("Error at iteration ", i, ": ", e$message)
      # skip to next iteration
    })
    
  }
  
  
  precision=k/i # this is TP/TP+FP (precision)
  recall=k/sum(atlas[,gene_of_interest]) # this is TP/TP+FN (recall/sensitivity)
  TP=k
  FP=i-k
  FN=sum(atlas[,gene_of_interest])-k
  TN=dim(reconstruction_pre)[1]-(TP+FP+FN)
  F1_score <- ifelse((precision + recall) == 0, 0, 2 * (precision * recall) / (precision + recall))
  
  results[j,1]<-precision
  results[j,2]<-recall
  results2[j,1]<-TP
  results2[j,2]<-FP
  results2[j,3]<-TN
  results2[j,4]<-FN
  results2[j,5]<-F1_score
  print(j)
  }
  
  write.table(results, file = "precision_recall_markers.txt", quote=F, sep = "\t")
  write.table(results2, file = "../revised_DEVELOPMENTAL_BIOLOGY_round3/F1_score_markers.txt", quote=F, sep = "\t")
  
  
  # plot
  results <- as.data.frame(results)
  results_long <- pivot_longer(results,
                               cols = c("precision", "recall"),
                               names_to = "metric",
                               values_to = "value")
  

  ### PLOT OPTION 2
  p <- ggplot(results_long, aes(x = metric, y = value, fill = metric)) +
    geom_violin(width = 0.5, alpha = 0.4, color = "grey60") +
    geom_boxplot(width = 0.15, outlier.alpha = 0.2, color = "black", fill = "white", linewidth = 0.3) +
    scale_fill_manual(values = c(
      "precision" = "#08315c",
      "recall" = "grey40"
    )) +
    scale_y_continuous(limits = c(0, 1)) +   # Force y-axis to start at 0
    labs(title = "Precision and Recall Across Marker Genes",
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
  
  ggsave("precision_recall_marker_genes.pdf", p, width = 4, height = 8)
