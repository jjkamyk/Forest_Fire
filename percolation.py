from forest_fire import ForestFire
import numpy as np
import matplotlib.pyplot as plt

# percolation threshold analysis - for different sizes of grid (L) and neighbourhood's types

N = 10  # no. of iterations
sizes = np.array([20, 30])  # sizes of a lattices

probabilities = np.linspace(0.05, 0.95, 50)

edge = "top"  # possible edges: "bottom", "top", "right", "left"
results = np.zeros((len(sizes), len(probabilities), 2))
for i in range(len(sizes)):
    for j in range(len(probabilities)):
        hit_opposite_edge_times_Moore = 0
        hit_opposite_edge_times_Neumann = 0
        for k in range(N):
            my_forest = ForestFire(sizes[i], probabilities[j])
            my_forest.plant_forest()
            my_forest.simulate_forest_fire(edge, "Moore")
            hit_opposite_edge_times_Moore += my_forest.hit_opposite_edge
            my_forest.restore_forest()
            my_forest.simulate_forest_fire(edge, "Neumann")
            hit_opposite_edge_times_Neumann += my_forest.hit_opposite_edge
        results[i, j, 0] = hit_opposite_edge_times_Moore / N
        results[i, j, 1] = hit_opposite_edge_times_Neumann / N
    plt.figure()
    plt.plot(probabilities, results[i, :, 0], label="Moore's")
    plt.plot(probabilities, results[i, :, 1], label="Neumann's")
    plt.xlabel('probability of planting a tree on a single cell: p')
    plt.ylabel('percolation threshold: p*')
    plt.legend()
    plt.title("L = {0}, no. of iterations = {1}".format(sizes[i], N))

plt.figure()
for i in range(len(sizes)):
    plt.plot(probabilities, results[i, :, 0], label="L={0}".format(sizes[i]))

plt.xlabel('probability of planting a tree on a single cell: p')
plt.ylabel('percolation threshold: p*')
plt.legend()
plt.title("Moore's neighborhood, no. of iterations = {0}".format(N))
plt.show()
