# TSP Definition and Utilities

import numpy as np

def create_synthetic_dataset(num_cities=15, grid_size=100, seed=42):
    """
    Generates a synthetic dataset of 2D coordinates for TSP.
    """
    np.random.seed(seed)
    cities = np.random.randint(0, grid_size + 1, size=(num_cities, 2))
    return cities.astype(float)