# Main entry point for the TSP Evolutionary Algorithm

import numpy as np
from src.tsp_problem import (
    create_synthetic_dataset, 
    calculate_distance_matrix, 
    calculate_tour_distance
)
from src.ea_core import run as run_ea
from src.visualization import (
    plot_evolution_metrics,
    plot_tour,
    plot_comparison,
    print_summary
)


def main(num_cities=20, population_size=100, generations=200, mutation_rate=0.15, 
         elitism_count=2, seed=42, show_plots=True, compare_with_random=True):
    """
    Main function to run the TSP Evolutionary Algorithm.
    
    Args:
        num_cities: number of cities in the TSP problem
        population_size: size of the population
        generations: number of generations to evolve
        mutation_rate: probability of mutation (0.0 to 1.0)
        elitism_count: number of best individuals to preserve
        seed: random seed for reproducibility
        show_plots: whether to display visualization plots
        compare_with_random: whether to compare EA result with a random tour
    """
    print("\n" + "="*60)
    print(f"TSP EVOLUTIONARY ALGORITHM")
    print(f"Cities: {num_cities} | Population: {population_size} | Generations: {generations}")
    print(f"Mutation Rate: {mutation_rate} | Elitism: {elitism_count}")
    print("="*60)
    
    # Generate dataset
    cities = create_synthetic_dataset(num_cities=num_cities, seed=seed)
    
    # Run EA
    best_tour, best_distance, history = run_ea(
        cities=cities,
        population_size=population_size,
        generations=generations,
        mutation_rate=mutation_rate,
        elitism_count=elitism_count,
        verbose=True
    )
    
    # Print summary
    print_summary(best_tour, best_distance, history, num_cities)
    
    # Visualize results
    if show_plots:
        plot_evolution_metrics(history)
        plot_tour(cities, best_tour, best_distance, "Best Tour Found by EA")
        
        # Compare with random tour if requested
        if compare_with_random:
            dist_matrix = calculate_distance_matrix(cities)
            random_tour = np.random.permutation(num_cities)
            random_distance = calculate_tour_distance(random_tour, dist_matrix)
            
            plot_comparison(
                cities,
                [random_tour, best_tour],
                [random_distance, best_distance],
                ["Random Tour", "EA Best Tour"]
            )
    
    return best_tour, best_distance, history


if __name__ == "__main__":
    # Run with default parameters
    # main()
    
    # Example: Run with custom parameters
    main(num_cities=30, population_size=150, generations=700, mutation_rate=0.2, elitism_count=3, seed=42)