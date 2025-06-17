import csv

def merge_csv(file1, file2, output_file):
    # Read the first CSV file
    with open(file1, 'r') as csv_file1:
        csv_reader1 = csv.reader(csv_file1)
        data1 = [row[:3] for row in csv_reader1]  # Extract first three columns

    # Read the second CSV file
    with open(file2, 'r') as csv_file2:
        csv_reader2 = csv.reader(csv_file2)
        data2 = [row for row in csv_reader2]  # Read all columns

    # Ensure both files have the same number of rows
    if len(data1) != len(data2):
        print("Error: Input CSV files have different number of rows.")
        return

    # Write the merged data to a new CSV file
    with open(output_file, 'w', newline='') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        for i in range(len(data1)):
            csv_writer.writerow(data1[i] + data2[i])

# Example usage
file1 = 'Last_ATLAS.csv'
file2 = 'Second_11GB.csv'
output_file = '../../Trying_To_Do_Website/Website_FINAL_NONORM.csv'
merge_csv(file1, file2, output_file)
