import csv

def parse_obj_file(obj_file_path):
    data = []
    with open(obj_file_path, 'r') as obj_file:
        current_object = None
        for line in obj_file:
            if line.startswith('o '):
                current_object = line.strip().split(' ')[1]
            elif line.startswith('v '):
                coordinates = list(map(float, line.strip().split(' ')[1:]))
                data.append((current_object,) + tuple(coordinates))
    return data

def write_csv(data, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['xcoord', 'ycoord', 'zcoord', 'Blue', 'Purple1', 'Purple2', "Green1","Green2","Turquoise","Yellow1", "Yellow2", "Magenta"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for obj, xcoord, ycoord, zcoord in data:
            Blue = 1 if obj.startswith('Blue') else 0
            Purple1 = 1 if obj.startswith('Purple1') else 0
            Purple2 = 1 if obj.startswith('Purple2') else 0
            Green1 = 1 if obj.startswith('Green1') else 0
            Green2 = 1 if obj.startswith('Green2') else 0
            Turquoise = 1 if obj.startswith('Turquoise') else 0
            Yellow1 = 1 if obj.startswith('Yellow1') else 0
            Yellow2 = 1 if obj.startswith('Yellow2') else 0
            Magenta = 1 if obj.startswith('Magenta') else 0
            writer.writerow({'xcoord': xcoord, 'ycoord': ycoord, 'zcoord': zcoord, 'Blue': Blue, 'Purple1': Purple1, 'Purple2': Purple2, 'Green1': Green1, 'Green2': Green2, 'Turquoise': Turquoise, 'Yellow1': Yellow1, 'Yellow2': Yellow2, 'Magenta': Magenta})

def obj_to_csv(obj_file_path, csv_file_path):
    data = parse_obj_file(obj_file_path)
    write_csv(data, csv_file_path)

# Example usage:
obj_file_path = 'Atlas_FINobj.obj'
csv_file_path = 'Atlas_FIN.csv'
obj_to_csv(obj_file_path, csv_file_path)
