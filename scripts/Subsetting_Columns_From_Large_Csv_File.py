 import csv

# Function to extract specified columns from CSV file
def extract_columns(input_file, output_file):
    columns_to_extract = ['xcoord', 'ycoord', 'zcoord', 'acj6', 'ase', 'bsh', 'dll', 'dpn',
                          'Ets65A', 'eya', 'fd59A', 'fkh', 'kn', 'run', 'shg', 'Sox102F',
                          'svp', 'TfAP-2', 'toy', 'vvl', "elav", "hth", "ey","D","scro","erm","slp1","opa","B-H1","tll","L","hbn","dac","sim","gcm","repo","Vsx1","Optix","Rx","beat-Ic","dpr","dpr1","dpr8","beat-IIa","beat-Ib", "nAChRalpha6"]
    with open(input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames
        extracted_fieldnames = [field for field in fieldnames if field in columns_to_extract]

        with open(output_file, 'w', newline='') as new_csv_file:
            writer = csv.DictWriter(new_csv_file, fieldnames=extracted_fieldnames)
            writer.writeheader()
            for row in reader:
                extracted_row = {key: row[key] for key in extracted_fieldnames}
                writer.writerow(extracted_row)

# Example usage
if __name__ == "__main__":
    input_file = 'Final_NOVO_ALL.csv'  # Replace 'input.csv' with your CSV file path
    output_file = 'Novo_Only_Few_Columns_V6.csv'  # Replace 'output.csv' with the desired output file path
    extract_columns(input_file, output_file)
