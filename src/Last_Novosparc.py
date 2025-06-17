import novosparc
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import altair as alt
import random
import anndata
from scipy.spatial.distance import cdist, squareform, pdist
from scipy.stats import ks_2samp
from scipy.stats import pearsonr
from scipy.sparse import csc_matrix, csr_matrix
import sys
import os
random.seed(0)

#Importing atlas file and dataset
atlas = sys.argv[1]
atlas_file = atlas  + ".csv"
alpha = float(sys.argv[2])
dataset2 = sc.read("Last_DATA.h5ad")

# Manipulating the X matrix from a sparse matrix to a dense format
dataset2.X = dataset2.X.toarray()

#Subsampling the dataset in function of the number of locations in the atlas
locations = pd.read_csv(atlas_file, sep=",")
num_cells = len(locations.index)
sc.pp.subsample(dataset2, n_obs=num_cells)

# Keeping the raw data subsampled in an object to be used at the end for final mapping
raw_data = dataset2.X
dge_full = pd.DataFrame(raw_data)

# Creating an object containing all gene names (for final file)
all_genes_names = dataset2.var.index.tolist()

# Selecting the more variable genes
var_genes = 5000
#float(sys.argv[3])
sc.pp.highly_variable_genes(dataset2, n_top_genes=var_genes)
dataset2 = dataset2[:, dataset2.var['highly_variable']]

#Creating an objects containing the names of the most variable genes
gene_names = dataset2.var.index.tolist()
num_cells, num_genes = dataset2.shape 
# Updating the locations file so that it only contains the position values (no marker gene info)
num_locations = len(locations.index)
locations = locations[:num_locations][["xcoord", "ycoord", "zcoord"]].values

# Creating an Anndata object from the Atlas file
atlas = sc.read(atlas_file)
atlas_genes = atlas.var.index.tolist()
atlas.obsm["spatial"] = locations

# Calculating Morans I for most spatially informative gene and exporting it to a csv
mI, pvals= novosparc.an.get_moran_pvals(atlas.X, locations)
dfmorans= pd.DataFrame({"moransI": mI, "pval": pvals}, index=atlas_genes)
dfmorans.to_csv("moransmatrix2")

# Setting parameters for smooth cost
num_neighbors_s = num_neighbors_t = 15
#float(sys.argv[4])

# Parameters for linear cost
markers = list(set(atlas_genes).intersection(gene_names))
num_markers = len(markers)
atlas_matrix = atlas.to_df()[markers].values
markers_idx = pd.DataFrame({"markers_idx": np.arange(len(gene_names))}, index=gene_names)
markers_to_use = np.concatenate(markers_idx.loc[markers].values)

# Construct Tissue Object
tissue = novosparc.cm.Tissue(dataset=dataset2, locations=locations, atlas_matrix=atlas_matrix, markers_to_use=markers_to_use)

# Set up reconstruction
tissue.setup_reconstruction(atlas_matrix=atlas_matrix,markers_to_use= markers_to_use, num_neighbors_s=num_neighbors_s, num_neighbors_t=num_neighbors_t)

# compute optimal transport of cells to locations
alpha_linear = alpha
epsilon = 1e-3
tissue.reconstruct(alpha_linear=alpha_linear, epsilon=epsilon, search_epsilon=True)

# Final sdge for Var_GENES
sdge = tissue.sdge
ending = pd.DataFrame(sdge.T, columns=gene_names)
ending.to_csv("newdatasetneigb15" + "_" + str(alpha) + "_" + str(var_genes) + "_" + str(num_neighbors_s) + "_" + str(epsilon) + "_Novosparc.csv")

# Getting the Entropy And Exporting as csv
ent_T = novosparc.an.get_cell_entropy(tissue.gw)

dataokok = {
    'ent_T': ent_T
}

dfokok = pd.DataFrame(dataokok)
dfokok.to_csv("entropy_distributions_" + str(alpha) + "_" + str(var_genes) + "_" + str(num_neighbors_s) + "_" + str(epsilon) + ".csv", index=False)

# Morans for the more variable genes
tissue.calculate_spatially_informative_genes(selected_genes=None, n_neighbors=8)
results = tissue.spatially_informative_genes
results.to_csv("MoranForAllgenes_"+ str(alpha) + "_" + str(var_genes) + "_" + str(num_neighbors_s) + "_" + str(epsilon) + ".csv", index=False)

# Final sdge for all genes
sdge_full = np.dot(dge_full.T, tissue.gw)
dataset_reconst= sc.AnnData(pd.DataFrame(sdge_full.T,columns=all_genes_names))
pl_genes = ("acj6","dpn","eya","toy","shg","elav","bsh","ap","hth","ey","slp1","tll","opa","tj","hbn","pxb","Optix","Vsx1","Rx","wg")
dataset_reconst.obsm["spatial"]= locations

# Exporting Final sdge 
endingv2 = pd.DataFrame(sdge_full.T, columns=all_genes_names)
endingv2.to_csv("newdatasetneigb15" + "_" + str(alpha) + "_" + str(var_genes) + "_" + str(num_neighbors_s) + "_" + str(epsilon) + "_Novosparc_allgenes.csv")

# Define the number of z-stacks and create a directory for saving images
num_stacks = 20
output_dir = "z_stack_images_FORNOVO_" + str(alpha) + "_" + str(var_genes) + "_" + str(num_neighbors_s) + "_" + str(epsilon) 

os.makedirs(output_dir, exist_ok=True)

# Get the z-coordinate range and divide into stacks
z_coords = locations[:, 2]
z_min, z_max = np.min(z_coords), np.max(z_coords)
stack_ranges = np.linspace(z_min, z_max, num_stacks + 1)

# Loop through each stack range and save each as a separate image
for i in range(num_stacks):
    z_start, z_end = stack_ranges[i], stack_ranges[i + 1]
    in_stack = (z_coords >= z_start) & (z_coords < z_end)
    stack_data = dataset_reconst[in_stack]
    
    # Create a new figure for each z-stack
    plt.figure(figsize=(6, 6))
    novosparc.pl.embedding(stack_data, pl_genes)
    plt.title(f"Z-stack {i + 1}")
    plt.axis('off')
    
    # Save each stack as a separate image
    stack_filename = os.path.join(output_dir, f"z_stack_{i + 1}.png")
    plt.savefig(stack_filename, format='png', dpi=300)
    plt.close()
    print(f"Figure saved as {stack_filename}")

# Save the plot as an image file
#plt.savefig(output_filename, format='png', dpi=300)  # Adjust dpi for resolution
#plt.close()
