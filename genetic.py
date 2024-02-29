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

def mating(gens1, gens2, mutation_rate):
    crossover_point = np.random.randint(1, len(gens1))
    result = np.where(np.arange(len(gens1)) < crossover_point, gens1, gens2)
    result = np.where(np.random.random(result.shape) > mutation_rate, result, np.random.randn(*result.shape))
    return result


def reproduce2(parents, scores, children_n, mutation_rate):
    parents = np.array(parents)
    output = [parents[0], parents[1]]
    scores[scores == -np.Inf] = 1e-3
    scores /= scores.sum()
    for _ in range(children_n-2):
        p1, p2 = np.random.choice(np.arange(len(parents)), size=(2, ), p=scores)
        output.append(mating(parents[p1], parents[p2], mutation_rate))

    return np.array(output)


if __name__ == "__main__":
    parents = np.array([[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]])
    scores = np.array([10.0, 2.0, 10.0])
    print(parents.shape)
    print(scores.shape)
    print(parents, scores)
    print(reproduce2(parents, scores, 10, 0.0))