import numpy as np
from typing import Tuple, Dict, List

from src.tsp_problem import *

def generate_initial_population(n: int, num_of_cities: int):
    samples = []
    for _ in range(n):
        sample = np.random.permutation(num_of_cities)
        samples.append(sample)
    return np.array(samples)

def fitness(tours: np.ndarray, distance_matrix: np.ndarray):
    distances = []
    for tour in tours:
        dist = calculate_tour_distance(tour, distance_matrix)
        # Add small epsilon to avoid division by zero
        distances.append(max(dist, 1e-10))
    return 1 / np.array(distances)

def select_parents(population: np.ndarray, fitnesses: np.ndarray):
    total_fitness = np.sum(fitnesses)
    probabilities = fitnesses / total_fitness
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    return population[selected_indices]

def mutate(tour: np.ndarray):
    tour = tour.copy()  # Always work on a copy
    
    def swap_mutation(tour):
        a, b = np.random.choice(len(tour), size=2, replace=False)
        tour[a], tour[b] = tour[b], tour[a]
        return tour

    def inversion_mutation(tour):
        a, b = sorted(np.random.choice(len(tour), size=2, replace=False))
        tour[a:b+1] = tour[a:b+1][::-1]
        return tour

    def scramble_mutation(tour):
        a, b = sorted(np.random.choice(len(tour), size=2, replace=False))
        segment = tour[a:b+1].copy()
        np.random.shuffle(segment)
        tour[a:b+1] = segment
        return tour

    mutations = [swap_mutation, inversion_mutation, scramble_mutation]
    mutation = np.random.choice(mutations)
    return mutation(tour)

# Partially Mapped Crossover (PMX)
def crossover(parent1: np.ndarray, parent2: np.ndarray):
    size = len(parent1)
    a, b = sorted(np.random.choice(size, size=2, replace=False))
    
    child1, child2 = np.full(size, -1, dtype=int), np.full(size, -1, dtype=int)
    
    # Copy crossover segment
    child1[a:b+1] = parent1[a:b+1]
    child2[a:b+1] = parent2[a:b+1]
    
    # Fill remaining positions for child1
    for i in range(size):
        if a <= i <= b:
            continue
        candidate = parent2[i]
        while candidate in child1[a:b+1]:
            # Find where candidate is in parent1's segment and get corresponding value from parent2
            idx = np.where(parent1[a:b+1] == candidate)[0][0] + a
            candidate = parent2[idx]
        child1[i] = candidate
    
    # Fill remaining positions for child2
    for i in range(size):
        if a <= i <= b:
            continue
        candidate = parent1[i]
        while candidate in child2[a:b+1]:
            # Find where candidate is in parent2's segment and get corresponding value from parent1
            idx = np.where(parent2[a:b+1] == candidate)[0][0] + a
            candidate = parent1[idx]
        child2[i] = candidate
    
    return child1, child2


def run(cities: np.ndarray, population_size=100, generations=500, mutation_rate=0.1, 
        elitism_count=2, verbose=True) -> Tuple[np.ndarray, float, Dict[str, List[float]]]:
    """
    Run the evolutionary algorithm with elitism and metrics tracking.
    
    Args:
        cities: numpy array of city coordinates (N, 2)
        population_size: number of individuals in the population
        generations: number of generations to evolve
        mutation_rate: probability of mutation for each child
        elitism_count: number of best individuals to carry forward unchanged
        verbose: whether to print progress during evolution
    
    Returns:
        best_tour: the best tour found (permutation array)
        best_distance: the distance of the best tour
        history: dictionary with 'best_fitness', 'avg_fitness', 'best_distance' per generation
    """
    num_of_cities = cities.shape[0]
    distance_matrix = calculate_distance_matrix(cities)

    population = generate_initial_population(population_size, num_of_cities)
    
    # History tracking
    history = {
        'best_fitness': [],
        'avg_fitness': [],
        'best_distance': []
    }
    
    for generation in range(generations):
        # Evaluate fitness
        fitnesses = fitness(population, distance_matrix)
        
        # Track metrics
        best_fitness = np.max(fitnesses)
        avg_fitness = np.mean(fitnesses)
        best_idx = np.argmax(fitnesses)
        best_distance = calculate_tour_distance(population[best_idx], distance_matrix)
        
        history['best_fitness'].append(float(best_fitness))
        history['avg_fitness'].append(float(avg_fitness))
        history['best_distance'].append(float(best_distance))
        
        if verbose and (generation % 50 == 0 or generation == generations - 1):
            print(f"Generation {generation:3d}: Best Distance = {best_distance:.2f}, "
                  f"Avg Fitness = {avg_fitness:.6f}")
        
        # Elitism: preserve top individuals
        elite_indices = np.argsort(fitnesses)[-elitism_count:]
        elites = population[elite_indices].copy()
        
        # Selection and reproduction
        selected_parents = select_parents(population, fitnesses)
        
        next_generation = []
        
        # Generate offspring (leaving room for elites)
        num_offspring = population_size - elitism_count
        for i in range(0, num_offspring, 2):
            parent1 = selected_parents[i % len(selected_parents)]
            parent2 = selected_parents[(i + 1) % len(selected_parents)]
            child1, child2 = crossover(parent1, parent2)
            
            if np.random.rand() < mutation_rate:
                child1 = mutate(child1)
            if np.random.rand() < mutation_rate:
                child2 = mutate(child2)
            
            next_generation.append(child1)
            if len(next_generation) < num_offspring:
                next_generation.append(child2)
        
        # Combine elites and offspring
        population = np.vstack([np.array(next_generation), elites])
    
    # Final evaluation
    final_fitnesses = fitness(population, distance_matrix)
    best_fitness_idx = np.argmax(final_fitnesses)
    best_tour = population[best_fitness_idx]
    best_distance = calculate_tour_distance(best_tour, distance_matrix)
    
    return best_tour, best_distance, history


if __name__ == "__main__":
    dataset = create_synthetic_dataset(num_cities=20)
    print(run(dataset))