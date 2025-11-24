The problem is solved using Evolutionary Algorithm (EA), where:
- Individuals are represented as sequence of visited cities, essentially
permutations of cities e.g. [[1, 3, 2], [1, 2, 3], [3, 1, 2]]
- Fitness function is inverse of total distance travelled
- Individuals are selected using roulette selection
- For crossover genetic operation Partially Mapped Crossover (PMX) is used
- Mutation involves randomly selected one of three possible variants and applying it
    - Swap - two random cities swap places e.g. [1, **2**, 3, **4**] -> [1, **4**, 3, **2**]
    - Inversion - random fragment of individuals is inverted e.g. [1, **2**, **3**, 4] -> [1, **3**, **2**, 4]
    - Scramble -> random fragment of individuals is shuffled e.g. [1, **2**, **3**, **4**] -> [1, **3**, **2**, **4**]
- Algorithm is terminated after reaching some number of generations