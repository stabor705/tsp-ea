# **EA-TSP: Evolutionary Algorithm for the Travelling Salesperson Problem**

This project implements an Evolutionary Algorithm (EA) to find high-quality solutions for the **Travelling Salesperson Problem (TSP)**.

---

### **The Problem: Travelling Salesperson Problem (TSP)**

The TSP is a classic **NP-hard** optimization problem. Given a list of cities and the distances between each pair, the goal is to find the **shortest possible route** that visits each city exactly once and returns to the origin city.

Because it is NP-hard, finding the *perfect* solution (exhaustive search) becomes computationally impossible for even a moderate number of cities. We use heuristics, like Evolutionary Algorithms, to find *near-optimal* solutions efficiently.

---

### **The Method: Evolutionary Algorithm (EA)**

An Evolutionary Algorithm is a metaheuristic inspired by biological natural selection. It works by managing a **population** of candidate solutions (called **individuals**) and iteratively improving them using genetic operators.

---

### **Project Components**

This repository will be built in logical modules:

1. **Problem Definition:**

   * Functions to create or load city datasets (coordinates or distance matrices).
   * A highly-optimized distance calculator.
2. **Core EA Implementation:**

   * Implementation of the core genetic operators (Selection, Crossover, Mutation) specialized for permutation-based chromosomes.
   * A population initialization function.
   * The main evolution loop that runs the algorithm for a set number of generations.
3. **Experimentation & Evaluation:**

   * A central configuration system to manage algorithm parameters (e.g., population size, mutation rate).
   * Logging to track metrics like the **best and average fitness** per generation.
   * Baseline heuristics (like the Nearest Neighbor algorithm) for performance comparison.
4. **Visualization & Analysis:**

   * Tools to plot the final, optimized tour on a 2D plane.
   * Generation of **convergence graphs** (plotting fitness vs. generation) to analyze the algorithm's performance.
   * An example notebook demonstrating a full run from start to finish.

---

## Running with Docker

To run the application locally using Docker, follow these steps:

1. **Build the Docker image**
   Run the following command in the root directory of the project to build the image with the tag `tsp-ea`:

   ```bash
   docker build -t tsp-ea .
    ```

2. **Run the container**
Start the container and map port 8000 of the container to port 8000 on your host machine:
    ```bash
    docker run -p 8000:8000 tsp-ea
    ```

3. **Access the application**
Once the container is running, open your web browser and navigate to: ```http://localhost:8000```
