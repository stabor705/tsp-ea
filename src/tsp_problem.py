# TSP Definition and Utilities

import numpy as np
from scipy.spatial.distance import pdist, squareform

def create_synthetic_dataset(num_cities=15, grid_size=100, seed=42):
    """
    Generates a synthetic dataset of 2D coordinates for TSP.
    """
    np.random.seed(seed)
    cities = np.random.randint(0, grid_size + 1, size=(num_cities, 2))
    return cities.astype(float)


def calculate_distance_matrix(cities):
    """
    Calculates a square distance matrix for all city pairs.
    """
    return squareform(pdist(cities, 'euclidean'))


def calculate_tour_distance(tour, distance_matrix):
    """
    Calculates the total distance of a given tour.
    """
    from_cities = tour
    to_cities = np.roll(tour, -1)
    return np.sum(distance_matrix[from_cities, to_cities])
