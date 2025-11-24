import numpy as np

from tsp_problem import *

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
        distances.append(dist)
    return 1 / np.array(distances)

def select_parents(population: np.ndarray, fitnesses: np.ndarray):
    total_fitness = np.sum(fitnesses)
    probabilities = fitnesses / total_fitness
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    return population[selected_indices]

def mutate(tour: np.ndarray):
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
        segment = tour[a:b+1]
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
    
    child1, child2 = np.full(size, -1), np.full(size, -1)
    
    mapping1 = { p1: p2 for p1, p2 in zip(parent1[a:b+1], parent2[a:b+1]) }
    mapping2 = { p2: p1 for p1, p2 in zip(parent1[a:b+1], parent2[a:b+1]) }

    for i in range(0, size):
        if a <= i <= b:
            child1[i], child2[i] = parent1[i], parent2[i]
        else:
            child1[i], child2[i] = parent2[i], parent1[i]
            if child1[i] in mapping1:
                child1[i] = mapping1[child1[i]]
            if child2[i] in mapping2:
                child2[i] = mapping2[child2[i]]
    
    return child1, child2


def run(cities: np.ndarray, population_size=100, generations=500, mutation_rate=0.1):
    num_of_cities = cities.shape[0]
    distance_matrix = calculate_distance_matrix(cities)

    population = generate_initial_population(population_size, num_of_cities)
    
    for _ in range(generations):
        fitnesses = fitness(population, distance_matrix)
        selected_parents = select_parents(population, fitnesses)
        
        next_generation = []
        
        for i in range(0, population_size, 2):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i+1]
            child1, child2 = crossover(parent1, parent2)
            
            if np.random.rand() < mutation_rate:
                child1 = mutate(child1)
            if np.random.rand() < mutation_rate:
                child2 = mutate(child2)
            
            next_generation.extend([child1, child2])
        
        population = np.array(next_generation)
    
    best_fitness_idx = np.argmax(fitness(population, distance_matrix))
    best_tour = population[best_fitness_idx]
    best_distance = calculate_tour_distance(best_tour, distance_matrix)
    
    return best_tour, best_distance


if __name__ == "__main__":
    dataset = create_synthetic_dataset(num_cities=20)
    print(run(dataset))