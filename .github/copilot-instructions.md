## Quick copilot instructions for EA-TSP

This repository implements a small Evolutionary Algorithm (EA) for the Travelling Salesperson Problem (TSP). The goal of this document is to provide concise, actionable guidance to an AI coding agent so it can be productive immediately in this codebase.

Key facts (big picture)
- Entry point: `main.py` contains a small demo that uses `src.tsp_problem` to generate cities, compute a distance matrix and evaluate tours.
- Core library: `src/tsp_problem.py` provides the data-model and utilities currently used by the runner:
  - `create_synthetic_dataset(num_cities, grid_size, seed)` -> numpy array shape (N,2) of coordinates (float)
  - `calculate_distance_matrix(cities)` -> (N,N) numpy distance matrix computed with `scipy.spatial.distance`
  - `calculate_tour_distance(tour, distance_matrix)` -> scalar total tour length; `tour` is a permutation array of indices (0..N-1)
- Planned core EA logic should live in `src/ea_core.py` (currently a placeholder). That module should implement functions like `generate_initial_population`, `selection`, `crossover`, `mutation`, and a top-level `evolve` or `run_ea` loop.

Project-specific conventions and patterns
- Tours are represented as 1D numpy arrays of integer indices (permutations). Example: `np.arange(N)` or `np.random.permutation(N)` as used in `main.py`.
- Distance matrix is dense `(N,N)` numpy.ndarray and is indexed using numpy's advanced indexing: `distance_matrix[from_cities, to_cities]` (see `calculate_tour_distance`). Algorithms should avoid Python loops over cities where possible and use numpy vectorized ops.
- Random seeds are used in `create_synthetic_dataset` via `np.random.seed(seed)` for reproducibility. Preserve the seed parameter when writing tests or experiments.

How to run / developer workflows
- Install dependencies: `pip install -r requirements.txt` (project uses `numpy` and `scipy`).
- Quick smoke run: `python main.py` — this runs `run_problem_setup()` which demonstrates dataset creation and tour evaluation.
- Adding experiments: place experiment scripts at the repository root or under a new `experiments/` directory and use the functions from `src.tsp_problem` to avoid duplication.

Integration points & where to implement features
- EA implementation: implement the EA in `src/ea_core.py`. Follow these contracts:
  - Input: distance matrix or city coordinates and EA config (population size, mutation rate, generations)
  - Population: numpy array of shape (pop_size, N) where each row is a permutation
  - Output: best tour (1D numpy int array), best distance, and optional history (best/avg per generation)
- Use `src/tsp_problem.py` utilities for dataset and distance computations; avoid re-implementing them unless optimizing.

Examples (use these in tests or docstrings)
- Compute distance of an in-order tour:
  - `cities = create_synthetic_dataset(10, seed=101)`
  - `D = calculate_distance_matrix(cities)`
  - `tour = np.arange(10)`
  - `len = calculate_tour_distance(tour, D)`

Current gaps and safe assumptions
- `src/ea_core.py` is incomplete. When adding functions, prefer explicit typing (`int`, `np.ndarray`) and avoid undefined names like `Int`.
- There are no unit tests yet — when adding tests, use the above example calls as quick smoke tests.

Style notes for AI edits
- Keep changes minimal and localized. Preserve the `src/` package layout.
- Follow existing simple style: small helper functions, clear docstrings, prefer numpy/scipy for numeric work.
- If adding new dependencies, add them to `requirements.txt` and keep the dependency list minimal.

Files to reference when working on this project
- `main.py` — example runner and smoke tests
- `src/tsp_problem.py` — dataset + distance utilities (high value reference)
- `src/ea_core.py` — where EA logic should be implemented/extended
- `requirements.txt` — runtime deps (numpy, scipy)

If anything in this guidance is unclear or you want me to expand a specific area (e.g., testing layout, an example EA implementation, or a recommended config format), tell me which area and I'll iterate.
