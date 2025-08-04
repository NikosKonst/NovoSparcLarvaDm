library(Seurat)
library(readxl)
library(ggplot2)
library(reshape2)
library(forcats)

setwd("~/Desktop/NovoSparc_paper_Figures")

### Download dataset from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE167266 ###
larva<-readRDS("GSE167266_OL.L3_P15_merged.rds")
larva<-UpdateSeuratObject(larva)
### Download Table with the developmental origin of the clusters from https://www.biorxiv.org/content/biorxiv/early/2025/01/29/2024.02.05.578975/DC4/embed/media-4.xlsx?download=true ###
DevO = read_xlsx("media-4.xlsx")
### Download Mixture Modeling data from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE142787 ###
MM_table = read_xlsx("GSE142787_Mixture_modeling.xlsx", sheet = "P15_MM_final", range = "A1:GO11300")
### Download Cluster Annotation Table from  https://github.com/NikosKonst/NovoSparcLarvaDm/blob/main/data/Cluster_information_table.xlsx ###
Annotation_table <- read_excel("Cluster_information_table.xlsx")

setwd("Figures")

### identify central brain and P15 cells and remove ###
### based on Konstantinides et al 2022 (https://pubmed.ncbi.nlm.nih.gov/35388222/) ###
DimPlot(larva, reduction = "umap")+NoLegend()
CB_cells<- WhichCells(larva, idents = c("L3_15","L3_18","L3_39","L3_92","L3_93","L3_77","L3_4","L3_26","L3_50","L3_51","L3_64","L3_79","L3_89","L3_90","L3_29","L3_70", "L3_0"))
larva_cells <- colnames(larva@assays$RNA@counts)[larva@meta.data$L3_vs_P15=="2"]
optic_lobe_cells<-setdiff(larva_cells, CB_cells)
larva_optic_lobe<-subset(larva, cells = optic_lobe_cells)

# saveRDS(optic_lobe_only_dataset, file = "optic_lobe_only_dataset.rds")
# 
# larva_optic_lobe<-readRDS("optic_lobe_only_dataset.rds")

#########################################
### GENERATE THE FIGURES OF THE PAPER ###
#########################################

###### Figure 1D and S1B ######

larva<-SetIdent(larva, value = "Nikos_Neset_ID")

### Transform the developmental origin list to a dataframe and keep the useful columns ###
spatial_temporal_origin<- do.call(cbind, DevO)
rownames(spatial_temporal_origin)<-spatial_temporal_origin[,1]
spatial_temporal_origin<-  spatial_temporal_origin[,2:16]
#spatial_temporal_origin_old<-read.table("../spatial_temporal_origin.txt", quote = "\t", header = T, row.names = 1)


#spatial origin (columns 2:7)
colors_to_use<-c("#CBA4C8", "#B177AB", "#96498F", "#96498F", "#B177AB", "#CBA4C8", "#4B0082", "#6A5ACD", "#483D8B","#34495E", "#2F4F4F",  "#556B2F", "#8B0000","#8B4513")

for (i in 2:7) {
spatial_P15<- spatial_temporal_origin[spatial_temporal_origin[,i]==1,]
spatial_cell_types<-row.names(spatial_P15)
spatial_cell_types2<-intersect(spatial_cell_types, names(table(Idents(larva))))
spatial<- WhichCells(larva, idents = spatial_cell_types2)

plot_name <- colnames(spatial_temporal_origin)[i]

plot<-DimPlot(larva, label=F, cells.highlight= spatial, cols.highlight = colors_to_use[i-1], cols= "grey", reduction = "umap", raster = F)

pdf(file = paste0("Figure_S1B_",plot_name, ".pdf"), width = 10, height = 10)
print(plot)+NoLegend()
dev.off()
}

# colors:
# Rx : #CBA4C8
# Optix:  #B177AB
# Vsx: #96498F


# temporal origin (columns 8:15)
for (i in 8:15) {
temporal_P15<- spatial_temporal_origin[spatial_temporal_origin[,i]==1,]
temporal_cell_types<-row.names(temporal_P15)
temporal_cell_types2<-intersect(temporal_cell_types, names(table(Idents(larva))))
temporal<- WhichCells(larva, idents = temporal_cell_types2)

plot_name <- colnames(spatial_temporal_origin)[i]

plot<-DimPlot(larva, label=F, cells.highlight= temporal, cols.highlight = colors_to_use[i-1], cols= "grey", reduction = "umap", raster = F)

pdf(file = paste0("Figure_1D_",i-7,plot_name, ".pdf"), width = 10, height = 10)
print(plot)+NoLegend()
dev.off()
}
#4B0082 (Indigo)
#34495E (Midnight Gray-Blue)
#8B4513 (Saddle Brown)
#6A5ACD (Slate Blue)
#2F4F4F (Dark Slate Gray)
#556B2F (Dark Olive Green)
#8B0000 (Dark Red)
#483D8B (Dark Slate Blue)
#800000 (Maroon)

# Tll origin
FeaturePlot(larva, features = "rna_tll")
Tll_cell_types_P15<-c("196", "197", "198", "203")
temporal<- WhichCells(larva, idents = Tll_cell_types_P15)
plot<-DimPlot(larva, label=F, cells.highlight= temporal, cols.highlight = c("#800000"), cols= "grey", reduction = "umap", raster = F)

plot_name<-"Tll"

pdf(file = paste0("Figure_1D_",9,plot_name, ".pdf"), width = 10, height = 10)
print(plot)+NoLegend()
dev.off()


###### Figure S1A ######

### annotate neuropils based on Konstantinides et al 2022 (https://pubmed.ncbi.nlm.nih.gov/35388222/) ###
medulla<- WhichCells(larva_optic_lobe, idents = c("L3_47","L3_32","L3_30","L3_62","L3_42","L3_52","L3_34","L3_24","L3_94","L3_33","L3_76","L3_86",
                                               "L3_75","L3_36","L3_73","L3_84","L3_31","L3_68","L3_14","L3_78","L3_40","L3_13","L3_82","L3_25",
                                               "L3_54","L3_83","L3_71","L3_12","L3_46","L3_60","L3_72","L3_21","L3_59","L3_41","L3_28","L3_12",
                                               "L3_71","L3_38","L3_23","L3_53"))
lamina<-WhichCells(larva_optic_lobe, idents = c("L3_49", "L3_65", "L3_5", "L3_57", "L3_66", "L3_65"))
lobula_plate<- WhichCells(larva_optic_lobe, idents = c("L3_35","L3_55","L3_48","L3_8"))
glia<-WhichCells(larva_optic_lobe, idents = c("L3_63","L3_87","L3_91","L3_44","L3_45","L3_67","L3_56","L3_2","L3_3","L3_85"))

annotation<-vector("character", length = length(Idents(larva_optic_lobe)))
annotation[]<-"progenitors"
annotation[medulla]<-"medulla"
annotation[lamina]<-"lamina"
annotation[lobula_plate]<-"lobula_plate"
annotation[glia]<-"glia"

larva_optic_lobe<-AddMetaData(larva_optic_lobe, metadata = annotation, col.name = "neuropil")

pdf(file = "Figure_S1A.pdf", width = 10, height = 10)
print(plot)+NoLegend()
dev.off()


###### Figure 3A-C ######

### plot the expression of different marker genes in the dataset ###

## Figure 3A ##

colors_to_use<-c("#4B0082", "#6A5ACD","#800000", "#FF7F00")
genes_to_plot<-c("rna_dpn", "rna_ase", "rna_elav", "rna_repo")

for (i in 1:length(genes_to_plot)) {
plot<-FeaturePlot(larva_optic_lobe, features = genes_to_plot[i], cols = c("grey", colors_to_use[i]))

pdf(file = paste0("Figure_3A_",genes_to_plot[i], ".pdf"), width = 10, height = 10)
print(plot)
dev.off()
}

## Figure 3B ##

genes_to_plot<-c("rna_hth", "rna_ey", "rna_slp1", "rna_D")

for (i in 1:length(genes_to_plot)) {
  plot<-FeaturePlot(larva_optic_lobe, features = genes_to_plot[i], cols = c("grey", colors_to_use[i]))
  
  pdf(file = paste0("Figure_3B_",genes_to_plot[i], ".pdf"), width = 10, height = 10)
  print(plot)
  dev.off()
}

## Figure 3C ##

colors_to_use<-c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00", "#FFFF33",
                 "#A65628", "#F781BF")
genes_to_plot<-c("rna_acj6", "rna_eya", "rna_Lim1")

for (i in 1:length(genes_to_plot)) {
  plot<-FeaturePlot(larva_optic_lobe, features = genes_to_plot[i], cols = c("grey", colors_to_use[i]))
  
  pdf(file = paste0("Figure_3C_",genes_to_plot[i], ".pdf"), width = 10, height = 10)
  print(plot)
  dev.off()
}


###### Figure 3D ######

### plot heatmap of gene expression in optic lobe clusters in P15 based on the mixture modeling ###
### based on Ozel, Simon, et al (https://pubmed.ncbi.nlm.nih.gov/33149298/) ###

# removes the clusters for which no mOPC origin was found
to_keep = DevO[, c("vDpp", "vOptix", "vVsx", "dVsx", "dOptix", "dDpp")]
to_keep = apply(X = to_keep, MARGIN = 2, as.numeric)
# View(DevO[which(rowSums(to_keep, na.rm = T) <= 0), ])
to_keep = which(rowSums(to_keep, na.rm = T) > 0)
DevO = DevO[to_keep, ]

# Lists the clusters present in each SO
# Names including "vd": clusters could also come from only ventral
vDpp =              DevO$Annotation[DevO$vDpp == 1 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 0]
vdDpp =             DevO$Annotation[DevO$vDpp == 1 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 1]
dDpp =              DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 1]

vDpp.vOptix =       DevO$Annotation[DevO$vDpp == 1 & DevO$vOptix == 1 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 0]
vdDpp.vdOptix =     DevO$Annotation[DevO$vDpp == 1 & DevO$vOptix == 1 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 1 & DevO$dDpp == 1]
dDpp.dOptix =       DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 1 & DevO$dDpp == 1]

vOptix =            DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 1 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 0]
vdOptix =           DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 1 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 1 & DevO$dDpp == 0]
dOptix =            DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 0 & DevO$dOptix == 1 & DevO$dDpp == 0]

vOptix.vVsx =       DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 1 & DevO$vVsx == 1 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 0]
vdOptix.vdVsx =     DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 1 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 1 & DevO$dDpp == 0]
dOptix.dVsx =       DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 1 & DevO$dOptix == 1 & DevO$dDpp == 0]

vVsx.dVsx.dOptix =  DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 1 & DevO$dDpp == 0]
vOptix.vVsx.dVsx =  DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 1 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 0 & DevO$dDpp == 0]

vVsx =              DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 1 & DevO$dVsx == 0 & DevO$dOptix == 0 & DevO$dDpp == 0]
vdVsx =             DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 0 & DevO$dDpp == 0]
dVsx =              DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 0 & DevO$dVsx == 1 & DevO$dOptix == 0 & DevO$dDpp == 0]

vVsx.dVsx.dOptix =  DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 0 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 1 & DevO$dDpp == 0]
vOptix.vVsx.dVsx =  DevO$Annotation[DevO$vDpp == 0 & DevO$vOptix == 1 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 0 & DevO$dDpp == 0]

whole_OPC =         DevO$Annotation[DevO$vDpp == 1 & DevO$vOptix == 1 & DevO$vVsx == 1 & DevO$dVsx == 1 & DevO$dOptix == 1 & DevO$dDpp == 1]

# List of all these categories
SO =            c("vDpp", "vdDpp", "dDpp", "vDpp.vOptix", "vdDpp.vdOptix", "dDpp.dOptix", "vOptix", "vdOptix", "dOptix", "vOptix.vVsx", "vdOptix.vdVsx", "dOptix.dVsx", "vVsx.dVsx.dOptix", "vOptix.vVsx.dVsx", "vVsx", "vdVsx", "dVsx", "whole_OPC")
SO_clusters = list( vDpp,   vdDpp,   dDpp,   vDpp.vOptix,   vdDpp.vdOptix,   dDpp.dOptix,   vOptix,   vdOptix,   dOptix,   vOptix.vVsx,   vdOptix.vdVsx,   dOptix.dVsx,  vVsx.dVsx.dOptix,   vOptix.vVsx.dVsx,    vVsx,   vdVsx,   dVsx, whole_OPC)

# Lists the clusters present in each TO
Hth =       DevO$Annotation[DevO$Hth == 1]
HthOpa =    DevO$Annotation[DevO$Hth_Opa == 1]
OpaErm =    DevO$Annotation[DevO$Opa_Erm == 1]
ErmEy =     DevO$Annotation[DevO$Erm_Ey == 1]
EyHbn =     DevO$Annotation[DevO$Ey_Hbn == 1]
HbnOpaSlp = DevO$Annotation[DevO$Hbn_Opa_Slp == 1]
SlpD =      DevO$Annotation[DevO$Slp_D == 1]
DBarHI =    DevO$Annotation[DevO$D_BarHI == 1]
# List of all these categories    
TO =            c("Hth", "HthOpa", "OpaErm", "ErmEy", "EyHbn", "HbnOpaSlp", "SlpD", "DBarHI")
TO_clusters = list(Hth,   HthOpa,   OpaErm,   ErmEy,   EyHbn,   HbnOpaSlp,   SlpD,   DBarHI)

# Lists the clusters present in each NO
N_ON =  DevO$Annotation[DevO$N_ON == 1]
N_OFF = DevO$Annotation[DevO$N_ON == 0]
# List of all these categories    
NO = c("N_ON", "N_OFF")
NO_clusters = list(N_ON, N_OFF)

# loads and annotates the MM
MM_table <- as.data.frame(MM_table)  # required because tibbles discourage rownames
rownames(MM_table) <- MM_table[[1]]  # set the first column as row names
MM_table[[1]] <- NULL       
MM_table = MM_table > 0.5
names_to_keep = rownames(MM_table)
MM_table = apply(X = MM_table, MARGIN = 2, FUN = as.numeric)
rownames(MM_table) = names_to_keep



Annotation = match(as.character(colnames(MM_table)), Annotation_table$Cluster_number)
Annotation = Annotation_table$Annotation[Annotation]
colnames(MM_table) = Annotation

#000000000000000000000000000000000000000000000000000000000#        
#### Parameters of the plots. To change before running ####
#000000000000000000000000000000000000000000000000000000000#        

# Chose the plot name (between the quotation marks)
plot_name = "Figure_3D.pdf"

# Chose the features to plot (each separated by a coma, and between quotation marks)
features <- c("shg",	"dpn",	"ase", "elav",	"repo","wrapper",	"hth", "Dll", 
              "erm",	"opa", "ey",	"hbn", "scro", "slp1",	"D",	"B-H1",	"tll",	
              "Vsx1",	"Optix","Rx",	"acj6", "eya", "Lim1", "aop", "ap", "bsh", 
              "dac", "CG34340", "Ets65A",	"fd59A",	"fkh", "Hmx", "kn",	"Lim3",	
              "oc",	"run", "sim", "Sox102F",	"svp", "tj", "toy",	"tup", "vvl")
# Colors to plot
color_present = "#009E73"
color_absent = "#000000"

# Size of the plot
Plot_width = 14
Plot_height = length(features)*0.15+4

# Chose the number of origins to plot, and change the origins accordingly
Number_of_origins = 3 # 1, 2 or 3

Orig_1 = NO
Orig_1_clusters = NO_clusters

Orig_2 = TO
Orig_2_clusters = TO_clusters

Orig_3 = SO
Orig_3_clusters = SO_clusters

#00000000000000000000000#
#### Makes the plots ####
#00000000000000000000000#


  # Makes a matrix in which the information to plot will be stored.
  # Each row will contains, for a given feature in a given cluster, 
  # the value of the feature (expressed, not expressed, unsure, which will be the info on the heatmap)
  # and the developmental origin of the cluster (which allows to groups clusters from the same origin when plotting).
  Table_to_plot = matrix(data = 0, nrow = 0, ncol = 4)
  colnames(Table_to_plot) = c("feature", "Clusters", "Value", "Dev_Origin")
  
  # Loop that goes through each possible combination of developmental origins
  a = 0
  for (i in 1:length(Orig_1)) {
    for (j in 1:length(Orig_2)) {
      for (k in 1:length(Orig_3)) {
        # Clusters that are from the combination of developmental origins
        clusters = Reduce(intersect, list(Orig_1_clusters[[i]], Orig_2_clusters[[j]], Orig_3_clusters[[k]]))
        # Acts ony if at least one cluster comes from the combination of origins
        if (sum(clusters %in% colnames(MM_table)) > 0) {
          # Makes a table that contains the expression of the selected features in the clusters from the combination of origins
          temp = MM_table[features, clusters[clusters %in% colnames(MM_table)], drop=FALSE]
          # Modifies the table to be able to add it to the data to plot
          # Makes it a matrix, because data frames cause problems later
          # however temp = as.matrix(temp) cannot be used because it sometimes add spaces that cause problems later: https://stackoverflow.com/questions/15618527/why-does-as-matrix-add-extra-spaces-when-converting-numeric-to-character
          # sapply(temp, format, trim = TRUE) adds sometimes spaces after the value
          temp = melt(as.matrix(temp))
          colnames(temp) = c("feature", "Clusters", "Value")
          temp$Dev_Origin = paste(Orig_1[[i]], Orig_2[[j]], Orig_3[[k]], sep = "_")
          temp = sapply(temp, as.character)
          # Adds the temporary table to the table to plot
          Table_to_plot = rbind(Table_to_plot, temp)
        }
      }
    }
  }
  
  # Makes sure Table_to_plot is a matrix to avoid problems later
  if (!is.matrix(Table_to_plot)) {
    print("Table_to_plot is not a matrix")
  }
  
  # Prepares the table for plotting
  Table_to_plot = as.data.frame(Table_to_plot)
  Table_to_plot[, "feature"] = factor(Table_to_plot[, "feature"])
  # Chooses the order in which to plot the developmental origins
  ord = c()
  for (orig1 in Orig_1) {
    for (orig2 in Orig_2) {
      for (orig3 in Orig_3) {
        ord = c(ord, paste(orig1, orig2, orig3, sep = "_"))
      }
    }
    
  }
  Table_to_plot[ , "Dev_Origin"] = factor(Table_to_plot[ , "Dev_Origin"], levels = ord[ord %in% Table_to_plot[ , "Dev_Origin"]])
  Table_to_plot[ , "Value"][Table_to_plot[ , "Value"] == 0.5] = "NA"
  Table_to_plot[ , "Value"][Table_to_plot[ , "Value"] == 1] = "Present"
  Table_to_plot[ , "Value"][Table_to_plot[ , "Value"] == 0] = "Absent"
  Table_to_plot$feature <- fct_rev(factor(Table_to_plot$feature))
  # Makes the heatmap
  pdf(file = plot_name, width = Plot_width, height = Plot_height)
  c = ggplot(data = Table_to_plot, mapping = aes(x = Clusters, y = feature, fill = Value)) +
    geom_tile() +
    scale_fill_manual(values = c(color_absent, color_present)) +
    facet_grid(~ Dev_Origin, scales = "free_x", space = "free_x") +
    theme(axis.text.x = element_text(angle = 90, face = "bold", vjust = 0.5, hjust = 1),
          axis.text.y = element_text(face = "bold", vjust = 0.5, hjust = 1),
          strip.text.x = element_text(angle = 90, face = "bold"),
          panel.spacing = unit(1, "pt"),
          axis.ticks.x = element_blank(),
          axis.ticks.y = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          panel.grid = element_blank(),
          panel.background = element_blank())
  print(c)
  dev.off()

###### Figure S2 ######

## Figure S2A ##
CB_cells<- WhichCells(larva, idents = c("L3_15","L3_18","L3_39","L3_92","L3_93","L3_77","L3_4","L3_26","L3_50","L3_51","L3_64","L3_79","L3_89","L3_90","L3_29","L3_70", "L3_0"))
larva_cells <- colnames(larva@assays$RNA@counts)[larva@meta.data$L3_vs_P15=="2"]

plot<-DimPlot(larva, cells = larva_cells, cells.highlight = CB_cells, cols.highlight = "darkred", cols = "grey", shuffle = T)+NoLegend()

pdf(file = paste0("Figure_S2A", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

## Figure S2B ##
colors_to_use<-c("#FF7F00","#8B4513")
genes_to_plot<-c("rna_shg", "rna_wrapper")

for (i in 1:length(genes_to_plot)) {
  plot<-FeaturePlot(larva_optic_lobe, features = genes_to_plot[i], cols = c("grey", colors_to_use[i]))
  
  pdf(file = paste0("Figure_S2B_",genes_to_plot[i], ".pdf"), width = 10, height = 10)
  print(plot)
  dev.off()
}

## Figure S2C ##
colors_to_use<-c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00", 
                 "#FFFF33", "#A65628", "#F781BF", "#800000", "#66C2A5")
genes_to_plot<-c("rna_Dll", "rna_erm", "rna_opa", "rna_hbn", "rna_scro", "rna_B-H1", "rna_tll", "rna_Vsx1", "rna_Optix", "rna_Rx")

for (i in 1:length(genes_to_plot)) {
  plot<-FeaturePlot(larva_optic_lobe, features = genes_to_plot[i], cols = c("grey", colors_to_use[i]))
  
  pdf(file = paste0("Figure_S2C_",genes_to_plot[i], ".pdf"), width = 10, height = 10)
  print(plot)
  dev.off()
}

## Figure S2D ##
colors_to_use<-c("#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", 
"#E5C494", "#FF7F00", "#1B9E77", "#D95F02", "#7570B3", 
"#E7298A", "#66A61E", "#E6AB02", "#A6761D", "#800000", 
"#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#56B4E9")
genes_to_plot<-c("rna_aop", "rna_ap", "rna_bsh", "rna_dac", "rna_CG34340", "rna_Ets65A", "rna_fd59A", "rna_fkh", 
"rna_Hmx", "rna_kn", "rna_Lim3", "rna_oc","rna_run", "rna_sim", "rna_Sox102F", "rna_svp", 
"rna_tj", "rna_toy", "rna_tup", "rna_vvl")

for (i in 1:length(genes_to_plot)) {
  plot<-FeaturePlot(larva_optic_lobe, features = genes_to_plot[i], cols = c("grey", colors_to_use[i]))
  
  pdf(file = paste0("Figure_S2D_",genes_to_plot[i], ".pdf"), width = 10, height = 10)
  print(plot)
  dev.off()
}





###### Figure 5 ######

plot<-FeaturePlot(larva_optic_lobe, features = "rna_CG42368", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_DIPepsilon", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

plot<-FeaturePlot(larva_optic_lobe, features = "rna_CG42343", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_DIPbeta", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

plot<-FeaturePlot(larva_optic_lobe, features = "rna_CG14010", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_DIPeta", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

plot<-FeaturePlot(larva_optic_lobe, features = "rna_CG31646", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_DIPtheta", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

plot<-FeaturePlot(larva_optic_lobe, features = "rna_run", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_run", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

plot<-FeaturePlot(larva_optic_lobe, features = "rna_toy", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_toy", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

plot<-FeaturePlot(larva_optic_lobe, features = "rna_Wnt2", cols = c("grey", "#800000"), pt.size = 1)+NoLegend()
pdf(file = paste0("Figure_5A_Wnt2", ".pdf"), width = 10, height = 10)
print(plot)
dev.off()

