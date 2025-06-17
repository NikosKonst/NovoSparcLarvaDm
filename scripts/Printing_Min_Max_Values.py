import csv


def find_max_min(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = list(reader)

        # Initialize dictionary to store max and min values for each column
        max_min_values = {}
        for col_idx, header in enumerate(headers):
            # Initialize max and min values for each column
            max_val = float('-inf')
            min_val = float('inf')
            for row in data:
                cell_value = float(row[col_idx])  # Assuming all values are numeric
                if cell_value > max_val:
                    max_val = cell_value
                if cell_value < min_val:
                    min_val = cell_value
            # Store max and min values for each column
            max_min_values[header] = {'max': max_val, 'min': min_val}

        return max_min_values


def main():
    csv_file = 'Novo_Only_Few_Columns_V6.csv'  # Replace 'your_file.csv' with the path to your CSV file
    max_min_values = find_max_min(csv_file)

    for header, values in max_min_values.items():
        print(f"Column: {header}")
        print(f"Maximum value: {values['max']}")
        print(f"Minimum value: {values['min']}\n")


if __name__ == "__main__":
    main()
