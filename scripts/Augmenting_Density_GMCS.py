import numpy as np
import pandas as pd
from scipy.spatial import Delaunay
import random


def alpha_shape(coords, alpha):
    """
    Compute the alpha shape (concave hull) of a set of points.
    This function identifies simplices with circumsphere radii smaller than the given alpha.
    """
    tetra = Delaunay(coords)
    # Calculate radii of the circumsphere for each simplex
    radii = np.array(
        [np.linalg.norm(np.mean(coords[simplex], axis=0) - coords[simplex[0]]) for simplex in tetra.simplices])
    mask = radii < alpha
    return tetra.simplices[mask]


def augment_points(input_file, output_file, alpha=0.1, target_point_count=5350):
    """
    Augment points in a dataset while preserving the original shape.

    Parameters:
        input_file: str - Path to the input CSV file containing xcoord, ycoord, zcoord.
        output_file: str - Path to save the augmented dataset.
        alpha: float - Alpha value for the alpha shape computation.
        target_point_count: int - Desired total number of points after augmentation.
    """
    # Load the dataset
    coords_df = pd.read_csv(input_file)
    coords = coords_df[['xcoord', 'ycoord', 'zcoord']].values

    # Compute the alpha shape
    alpha_simplices = alpha_shape(coords, alpha)

    # Calculate centroids of the alpha shape triangles
    alpha_centroids = np.mean(coords[alpha_simplices], axis=1)

    # Combine original points with alpha shape centroids
    augmented_coords = np.vstack([coords, alpha_centroids])

    # Adjust the number of points to meet the target
    if len(augmented_coords) > target_point_count:
        # Randomly sample from the augmented set
        indices = np.random.choice(len(augmented_coords), target_point_count, replace=False)
        final_coords = augmented_coords[indices]
    else:
        # Add more points by repeating centroids if needed
        additional_points = target_point_count - len(augmented_coords)
        additional_centroids = alpha_centroids[:additional_points]
        final_coords = np.vstack([augmented_coords, additional_centroids])

    # Save the final augmented dataset
    final_df = pd.DataFrame(final_coords, columns=['xcoord', 'ycoord', 'zcoord'])
    final_df.to_csv(output_file, index=False)
    print(f"Augmented dataset saved to {output_file}")


# Example usage
input_file = "fused_coordinates_corrected.csv"
output_file = "augmented_coordinates.csv"
augment_points(input_file, output_file, alpha=0.1, target_point_count=5350)
