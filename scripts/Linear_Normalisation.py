import pandas as pd

# Load the CSV file
input_file = "Website_FINAL_NONORM.csv"  # Replace with the path to your input CSV file
output_file = "Last_Novo_NormV2.csv"  # Replace with the desired output file path

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Keep the first three columns as is
first_three_columns = df.iloc[:, :3]

# Normalize the remaining columns (columns after the third one)
remaining_columns = df.iloc[:, 3:]
normalized_columns = (remaining_columns - remaining_columns.min()) / (remaining_columns.max() - remaining_columns.min())

# Combine the first three columns with the normalized columns
result_df = pd.concat([first_three_columns, normalized_columns], axis=1)

# Save the result to a new CSV file
result_df.to_csv(output_file, index=False)

print(f"Normalized CSV saved to {output_file}")
