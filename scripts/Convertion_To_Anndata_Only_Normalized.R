install.packages(AnnData)

library(Seurat)
library(SeuratData)
library(SeuratDisk)
library(reticulate)
library(cowplot)

L3 <- readRDS("~/Desktop/optic_lobe_only_dataset.rds")

# Convert to AnnData, ensuring to use the normalized counts

library(Seurat)
library(SeuratDisk)

# Save the Seurat object
SaveH5Seurat(L3, filename = "new.h5Seurat", assays="RNA")

# Load your Seurat object
seurat_object <- LoadH5Seurat("new.h5Seurat")

# Create a new assay with normalized data
normalized_assay <- CreateAssayObject(counts = seurat_object[["RNA"]]@data)

# Add the normalized assay to the Seurat object
seurat_object[["normalized"]] <- normalized_assay

# Optionally, set this new assay as the active assay
DefaultAssay(seurat_object) <- "normalized"

# Save the modified Seurat object
SaveH5Seurat(seurat_object, filename = "normalized.h5Seurat")

# Convert to AnnData format, using the normalized assay and the "data" slot
Convert("normalized.h5Seurat", dest = "h5ad", assay = "normalized", slot = "data")

# Clean up: Optionally remove the temporary file
file.remove("normalized.h5Seurat")
rm(normalized_assay)
rm(seurat_object)
file.remove("new.h5Seurat")
