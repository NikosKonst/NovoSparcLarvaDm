import bpy
import csv
import os

# Get the path to the CSV file in the same directory as the Blender file
blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
csv_file_path = os.path.join(directory, "path/to/your/csv/file")

# Create a new mesh object
mesh = bpy.data.meshes.new("CSV_Mesh")
obj = bpy.data.objects.new("CSV_Object", mesh)

# Link the object to the current collection
bpy.context.collection.objects.link(obj)

# Set the object as the active object
bpy.context.view_layer.objects.active = obj
obj.select_set(True)


#Load CSV data
with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    columns = {name: [] for name in header}# Get the header row
    for row in reader: 
        for i, value in enumerate(row):
            columns[header[i]].append(float(value) if value.strip() else 0.0)

#vérification : 
print(columns)

# Calculate the number of points needed for the mesh
num_points = len(next(iter(columns.values())))
print(num_points) #544

# Set the total number of vertices in the mesh
mesh.vertices.add(num_points)

# Set the vertices location to ensure they are displayed
for i in range(num_points):
    mesh.vertices[i].co = (0, 0, 0)
    
mesh.update()
# Add the data to the object data properties as custom attributes
for name, values in columns.items():
    prop = obj.data.attributes.new(name, "FLOAT", domain="POINT")
    prop_data = prop.data[:]  # Explicitly initialize prop_data
    print(len(prop_data))
    max_length = min(len(values), len(prop_data))  # Use min instead of max
    padded_values = values[:] + [0.0] * (len(prop_data) - len(values))
    print(len(values))
    print(len(padded_values))
    for i in range(max_length):  # Iterate over the minimum length
        prop_data[i].value = padded_values[i]  # Use padded_values for assignment


print("CSV data imported successfully")
