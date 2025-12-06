# Visualization utilities for TSP EA

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List


def plot_evolution_metrics(history: Dict[str, List[float]], save_path=None):
    """
    Plot the evolution of fitness and distance metrics over generations.
    
    Args:
        history: dictionary with 'best_fitness', 'avg_fitness', 'best_distance' arrays
        save_path: optional path to save the figure (e.g., 'evolution.png')
    """
    generations = range(len(history['best_distance']))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot distances
    ax1.plot(generations, history['best_distance'], 'b-', linewidth=2, label='Best Distance')
    ax1.set_xlabel('Generation', fontsize=12)
    ax1.set_ylabel('Tour Distance', fontsize=12)
    ax1.set_title('Best Tour Distance over Generations', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot fitness values
    ax2.plot(generations, history['best_fitness'], 'g-', linewidth=2, label='Best Fitness')
    ax2.plot(generations, history['avg_fitness'], 'r--', linewidth=1.5, label='Average Fitness')
    ax2.set_xlabel('Generation', fontsize=12)
    ax2.set_ylabel('Fitness (1/Distance)', fontsize=12)
    ax2.set_title('Fitness Evolution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved evolution plot to {save_path}")
    
    plt.show()


def plot_tour(cities: np.ndarray, tour: np.ndarray, distance: float, 
              title="TSP Tour", save_path=None):
    """
    Visualize a TSP tour on a 2D plane.
    
    Args:
        cities: numpy array of city coordinates (N, 2)
        tour: permutation array representing the tour
        distance: total distance of the tour
        title: title for the plot
        save_path: optional path to save the figure
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot cities
    ax.scatter(cities[:, 0], cities[:, 1], c='red', s=200, zorder=3, 
               edgecolors='black', linewidth=2, label='Cities')
    
    # Annotate cities with numbers
    for i, (x, y) in enumerate(cities):
        ax.annotate(str(i), (x, y), fontsize=10, ha='center', va='center', 
                   color='white', weight='bold')
    
    # Plot tour edges
    tour_cities = cities[tour]
    for i in range(len(tour)):
        start = tour_cities[i]
        end = tour_cities[(i + 1) % len(tour)]
        ax.plot([start[0], end[0]], [start[1], end[1]], 
                'b-', linewidth=2, alpha=0.6, zorder=1)
        
        # Add arrow to show direction
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        ax.annotate('', xy=(mid_x + dx*0.1, mid_y + dy*0.1), 
                   xytext=(mid_x - dx*0.1, mid_y - dy*0.1),
                   arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
    
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_title(f'{title}\nTotal Distance: {distance:.2f}', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved tour plot to {save_path}")
    
    plt.show()


def plot_comparison(cities: np.ndarray, tours: List[np.ndarray], 
                   distances: List[float], labels: List[str], save_path=None):
    """
    Compare multiple tours side by side.
    
    Args:
        cities: numpy array of city coordinates (N, 2)
        tours: list of tour permutations to compare
        distances: list of distances for each tour
        labels: list of labels for each tour
        save_path: optional path to save the figure
    """
    n_tours = len(tours)
    fig, axes = plt.subplots(1, n_tours, figsize=(8*n_tours, 8))
    
    if n_tours == 1:
        axes = [axes]
    
    for ax, tour, distance, label in zip(axes, tours, distances, labels):
        # Plot cities
        ax.scatter(cities[:, 0], cities[:, 1], c='red', s=150, zorder=3,
                  edgecolors='black', linewidth=2)
        
        # Annotate cities
        for i, (x, y) in enumerate(cities):
            ax.annotate(str(i), (x, y), fontsize=9, ha='center', va='center',
                       color='white', weight='bold')
        
        # Plot tour
        tour_cities = cities[tour]
        for i in range(len(tour)):
            start = tour_cities[i]
            end = tour_cities[(i + 1) % len(tour)]
            ax.plot([start[0], end[0]], [start[1], end[1]],
                   'b-', linewidth=2, alpha=0.6, zorder=1)
        
        ax.set_xlabel('X Coordinate', fontsize=11)
        ax.set_ylabel('Y Coordinate', fontsize=11)
        ax.set_title(f'{label}\nDistance: {distance:.2f}', 
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved comparison plot to {save_path}")
    
    plt.show()


def print_summary(best_tour: np.ndarray, best_distance: float, 
                 history: Dict[str, List[float]], num_cities: int):
    """
    Print a summary of the EA run results.
    
    Args:
        best_tour: the best tour found
        best_distance: distance of the best tour
        history: evolution history dictionary
        num_cities: number of cities in the problem
    """
    initial_distance = history['best_distance'][0]
    final_distance = history['best_distance'][-1]
    improvement = ((initial_distance - final_distance) / initial_distance) * 100
    
    print("\n" + "="*60)
    print("TSP EVOLUTIONARY ALGORITHM - RESULTS SUMMARY")
    print("="*60)
    print(f"Number of cities: {num_cities}")
    print(f"Generations: {len(history['best_distance'])}")
    print(f"\nInitial best distance: {initial_distance:.2f}")
    print(f"Final best distance: {final_distance:.2f}")
    print(f"Improvement: {improvement:.2f}%")
    print(f"\nBest tour found: {best_tour}")
    print(f"Best tour distance: {best_distance:.2f}")
    print("="*60 + "\n")
