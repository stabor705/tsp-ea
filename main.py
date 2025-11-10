# Main entry point for the TSP Evolutionary Algorithm

import numpy as np
from src.tsp_problem import (
    create_synthetic_dataset, 
    calculate_distance_matrix, 
    calculate_tour_distance
)

def run_problem_setup():
    """
    Tests the dataset and distance functions.
    """
    print("--- 1. Setting up TSP Problem ---")
    
    NUM_CITIES = 10
    cities = create_synthetic_dataset(num_cities=NUM_CITIES, seed=101)
    print(f"Generated {NUM_CITIES} cities:\n{cities}\n")
    
    dist_matrix = calculate_distance_matrix(cities)
    print(f"Distance Matrix (shape {dist_matrix.shape}):\n{np.round(dist_matrix, 2)}\n")

    example_tour = np.arange(NUM_CITIES)
    tour_len = calculate_tour_distance(example_tour, dist_matrix)
    print(f"Distance for 'in-order' tour {example_tour}:\n{tour_len:.2f}\n")
    
    shuffled_tour = np.random.permutation(NUM_CITIES)
    shuffled_tour_len = calculate_tour_distance(shuffled_tour, dist_matrix)
    print(f"Distance for 'shuffled' tour {shuffled_tour}:\n{shuffled_tour_len:.2f}\n")



if __name__ == "__main__":
    run_problem_setup()