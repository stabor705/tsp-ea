import os
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import random

from src.tsp_problem import create_synthetic_dataset
from src.ea_core import run as run_ea

app = FastAPI(title="TSP Evolutionary Algorithm API")


class TSPRequest(BaseModel):
    num_cities: int = 20
    population_size: int = 100
    generations: int = 200
    mutation_rate: float = 0.15
    elitism_count: int = 2
    seed: Optional[int] = None

class TSPResponse(BaseModel):
    best_tour: List[int]
    best_distance: float
    cities: List[List[float]]
    history: Dict[str, List[float]]


# --- Utilities ---

def numpy_to_python(obj):
    """Helper to convert numpy types to native python types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


# --- Endpoints ---

@app.post("/api/solve", response_model=TSPResponse)
def solve_tsp(request: TSPRequest):
    cities = create_synthetic_dataset(
        num_cities=request.num_cities, 
        seed=request.seed if request.seed is not None else random.randint(0, 10000)
    )

    best_tour, best_distance, history = run_ea(
        cities=cities,
        population_size=request.population_size,
        generations=request.generations,
        mutation_rate=request.mutation_rate,
        elitism_count=request.elitism_count,
        verbose=False
    )

    return {
        "best_tour": best_tour.tolist(),
        "best_distance": float(best_distance),
        "cities": cities.tolist(),
        "history": {k: [float(v) for v in vals] for k, vals in history.items()}
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve the React Frontend
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            return f.read()
    return "<h1>Frontend not found. Make sure index.html is present.</h1>"
