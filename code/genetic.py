import numpy as np

def save_genotype(genotype, filename):
    file = open(filename, "w")
    file.write(f"genotype = np.{repr(genotype)}\n\n")
    file.close()

def mating(gens1, gens2, mutation_rate):
    crossover_point = np.random.randint(1, len(gens1))
    result = np.where(np.arange(len(gens1)) < crossover_point, gens1, gens2)
    result = np.where(np.random.random(result.shape) > mutation_rate, result, np.random.randn(*result.shape))
    return result


def reproduce2(parents: np.array, scores: np.array, children_n: int, mutation_rate: float, min_distance: float):
    '''
    parents: parents' genotype
    scores: parents' scores
    children_n: number of new children
    mutation_rate: rate of the random mutation in genotype
    min_distance: distance added to score, so everyone can have non-zero chance to reproduce
    '''
    parents = np.array(parents)
    output = [parents[0], parents[1]]  # elitism
    scores[scores < 1e-3] = 1e-3
    scores += min_distance
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