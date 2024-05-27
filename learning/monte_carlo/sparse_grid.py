import numpy as np
import itertools
import matplotlib.pyplot as plt

# Step 1: Define the univariate quadrature rules
def univariate_quadrature(level):
    if level == 0:
        return np.array([0]), np.array([2])
    else:
        x = np.linspace(-1, 1, 2**level + 1)
        w = 2 / (2**level * (2**level + 1)) * (1 - x**2)
        return x, w

# Step 2: Define the Smolyak coefficient
def smolyak_coefficient(q, d, l):
    return (-1)**(q - l) * (d - 1 + l) * np.math.factorial(d - 1) / (np.math.factorial(q - l) * np.math.factorial(l))

# Step 3: Define the Smolyak index set
def smolyak_index_set(q, d):
    return [i for i in itertools.product(range(q + 1), repeat=d) if q - d <= sum(i) <= q]

# Step 4: Compute the Smolyak grid
def smolyak_grid(q, d):
    index_set = smolyak_index_set(q, d)
    grid = []
    weights = []
    for i in index_set:
        x = [univariate_quadrature(level)[0] for level in i]
        w = [univariate_quadrature(level)[1] for level in i]
        grid.extend(list(itertools.product(*x)))
        weights.extend(list(itertools.product(*w)))
    return np.array(grid), np.array(weights)

# Example usage:
q = 6  # Level of approximation
d = 2  # Number of dimensions
grid, weights = smolyak_grid(q, d)
print("Grid points:", grid)
print("Weights:", weights)

# Plot the Smolyak grid
plt.scatter(grid[:, 0], grid[:, 1], s=1, alpha=0.5)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Smolyak grid")
plt.savefig("smolyak_grid.png")