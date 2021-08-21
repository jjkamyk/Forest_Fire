from forest_fire import ForestFire
import numpy as np
import matplotlib.pyplot as plt

N = 10  # no. of simulations
size = 30  # size of a lattice

probabilities = np.linspace(0.05, 0.95, 50)

edge = "top"  # possible edges: "bottom", "top", "right", "left"
type_of_measuring_neighborhood = "Neumann"  # for cluster measuring - Neumann neighborhood assumed
# there is an option to put "Moore" here

biggest_cluster_sizes = np.zeros((N, len(probabilities), 2))
for i in range(len(probabilities)):
    for j in range(N):
        my_forest = ForestFire(size, probabilities[i])
        my_forest.plant_forest()
        my_forest.simulate_forest_fire(edge, "Moore")
        biggest_cluster_sizes[j, i, 0] = my_forest.get_biggest_cluster_size(type_of_measuring_neighborhood)
        my_forest.restore_forest()
        my_forest.simulate_forest_fire(edge, "Neumann")
        biggest_cluster_sizes[j, i, 1] = my_forest.get_biggest_cluster_size(type_of_measuring_neighborhood)

average_biggest_cluster_sizes = np.mean(biggest_cluster_sizes, 0)
plt.figure()
plt.plot(probabilities, average_biggest_cluster_sizes[:, 0], label="Moore")
plt.plot(probabilities, average_biggest_cluster_sizes[:, 1], label="Neumann")
plt.legend()
plt.xlabel('probability of planting a tree on a single cell: p')
plt.ylabel('average biggest cluster size')
plt.title("L = {0}, no. of iterations = {1}".format(size, N))
plt.show()
