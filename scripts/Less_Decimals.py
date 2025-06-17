import pandas as pd

# File paths
input_file = 'Last_Novo_Normalized.csv'  # Replace with your input CSV file path
output_file = 'lessDecimals.csv'  # Replace with your desired output CSV file path

# Chunk size (number of rows per chunk)
chunk_size = 100000  # Adjust based on your system's memory capacity

# Open the output file to write processed chunks
with open(output_file, 'w') as f_out:
    # Process the file in chunks
    for chunk in pd.read_csv(input_file, header=None, chunksize=chunk_size):
        # Round numeric values in the chunk
        rounded_chunk = chunk.applymap(lambda x: round(x, 3) if isinstance(x, (int, float)) else x)

        # Write the chunk to the output file
        rounded_chunk.to_csv(f_out, index=False, header=False)

print(f"Rounded data saved to {output_file}")
