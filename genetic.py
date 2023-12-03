import numpy as np

def save_genotype(genotype, filename):
    file = open(filename, "w")
    file.write(f"genotype = np.{repr(genotype)}\n\n")
    file.close()

def reproduce(gens1: np.array, gens2: np.array, children_n: int, mutation_rate: float):
    """
    Reproduce gens by performing crossover and random mutation
    """

    # Broadcasting to create n copies of each array
    copies_arr1 = np.tile(gens1, (children_n - 2, 1))
    copies_arr2 = np.tile(gens2, (children_n - 2, 1))
    
    # Generating random crossover indices
    crossover_points = np.random.randint(1, len(gens1), size=(children_n - 2, 1))
    
    # Perform crossover using boolean indexing
    result = np.where(np.arange(len(gens1)) < crossover_points, copies_arr1, copies_arr2)

    result = np.where(np.random.random(result.shape) > mutation_rate, result, np.random.randn(*result.shape))
    result = np.vstack((gens1, gens2, result))
    
    return result

def get_next_generation(gens1: np.array, gens2: np.array, score_func, children_n: int, mutation_rate=1e-2):
    children = reproduce(gens1, gens2, children_n, mutation_rate)
    top = [0, gens1, 0, gens2]

    for child in children:
        score = score_func(child)

        worst_top = 2
        if top[0] < top[2]:
            worst_top = 0

        if score > top[worst_top]:
            top[worst_top] = score
            top[worst_top + 1] = child

    return top
