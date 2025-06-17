import pandas as pd
import numpy as np
from scipy.stats import spearmanr

# Path to the CSV file
file_path = "../FinalFinalCODE/less_GENES.csv" # Change For your Directory choice

# Load the dataset (only the gene columns)
data = pd.read_csv(file_path, usecols=range(3, 16))  # Adjust range to match gene columns

# Convert data to a NumPy array
data_array = data.values  # Rows: samples, Columns: genes

# Compute Spearman correlation matrix using vectorized computation
# Spearman correlation automatically ranks the data
correlation, _ = spearmanr(data_array, axis=0)  # axis=0 computes correlations between columns (genes)

# Convert the correlation matrix to a DataFrame for easy export
correlation_matrix = pd.DataFrame(correlation, index=data.columns, columns=data.columns)

# Save the correlation matrix to a CSV file
correlation_matrix.to_csv("lesslessSpear.csv")  # Change For your Directory choice
