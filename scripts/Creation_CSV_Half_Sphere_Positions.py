#Install required modules

import pandas as pd

# getCoord function gets the coordinates of all indices in the df
def getCoord(dataframe):
    all_points = []
    for i in range(dataframe.shape[0]):
        x = dataframe.loc[i, 'x']
        y = dataframe.loc[i, 'y']
        z = dataframe.loc[i, 'z']
        all_points.append([x, y, z])
    return all_points


# Split locations function : to create the half sphere structure
def splitLocations(dataframe):
    points = getCoord(dataframe)
    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        z = points[i][2]
        if x > 0 and y > 0 and z < 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y > 0 and z > 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y < 0 and z < 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y < 0 and z > 0:
            dataframe = dataframe.drop(i)

        if x > 0 and y < 0 and z == 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y > 0 and z == 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y == 0 and z < 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y == 0 and z > 0:
            dataframe = dataframe.drop(i)
        if x > 0 and y == 0 and z == 0:
            dataframe = dataframe.drop(i)
    return dataframe


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d  # Fonction pour la 3D
import numpy as np

# Plotting N^3 equidistant points inside a sphere of radius 1
N = 60  # This number is the one to increase or decrease depending on the number of locations
# desired inside and at the surface of the sphere

x = np.linspace(-1.0, 1.0, N)
y = np.linspace(-1.0, 1.0, N)
z = np.linspace(-1.0, 1.0, N)

# define center and radius of the sphere
x0, y0, z0, radius = 0.0, 0.0, 0.0, 1.0
center = [x0, y0, z0]

# Plot a grid of equidistant points
X, Y, Z = np.meshgrid(x, y, z)

# draw sphere of radius = 1.0
phi, theta = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
xx = np.cos(phi) * np.sin(theta)
yy = np.sin(phi) * np.sin(theta)
zz = np.cos(theta)

# Calc the distance of the grid points to the center of the sphere
r = np.sqrt((X - x0) ** 2 + (Y - y0) ** 2 + (Z - z0) ** 2)

# Define points that are inside the sphere
inside = r <= radius
num_locations = inside.size # is the number of locations
numpy_data = np.array([X[inside], Y[inside], Z[inside]])
numpy_data = numpy_data.T #Transpose the array
location_sphere_df = pd.DataFrame(numpy_data, columns=['x', 'y', 'z'])
#CalculateSphereRadius(location_sphere_df) #sphere of radius = 1 bien sûr !
half_sphere_df= splitLocations(location_sphere_df)


dataframe = pd.DataFrame(numpy_data, columns=['x', 'y', 'z'])

df_filtered = dataframe[dataframe['z'] >= 0]

# Export the DataFrame to a CSV file
csv_filename = 'Final_Atlas.csv'
df_filtered.to_csv(csv_filename, index=False)

print(f'DataFrame has been exported to {csv_filename}')
