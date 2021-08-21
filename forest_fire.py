from lattice_draw import LatticeDraw
import random
import matplotlib.patches as patch
import numpy as np
import scipy.ndimage.measurements as scnm


# ForestFire - main class for fire-spreading model
class ForestFire:

    def __init__(self, L, p, save_graphics=False):
        self.size = L
        self.probability = p
        self.hit_opposite_edge = False  # a flag for percolation threshold calculating
        self.save_graphics = save_graphics  # a flag responsible for saving graphics and gifs
        self.forest_state = {}  # trees and their states are stored in a dictionary
        # we consider four states: "Empty Cell", "Living Tree", "Burning Tree", "Burnt Tree"
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.forest_state[(x, y)] = "Empty Cell"
        if self.save_graphics:
            self.drawing_machine = LatticeDraw(self.size)

    # returning neighbors of considered tree (for spreading the fire)
    # two types of neighborhood (Neumann, Moore) and wind are available
    def get_neighbors(self, cell, type_of_neighborhood="Neumann", wind_direction="west", wind_strength=0):
        possible_neighbors = [(cell[0], cell[1] + 1),
                              (cell[0] + 1, cell[1]),
                              (cell[0], cell[1] - 1),
                              (cell[0] - 1, cell[1])]
        if type_of_neighborhood == "Moore":
            possible_neighbors.extend([(cell[0] + 1, cell[1] + 1),
                                       (cell[0] + 1, cell[1] - 1),
                                       (cell[0] - 1, cell[1] - 1),
                                       (cell[0] - 1, cell[1] + 1)])
        # if wind_strength = 0 -> no wind
        for i in range(wind_strength):  # wind - expanding the range of tree's neighbors in particular direction
            if wind_direction == "north":
                possible_neighbors.append((cell[0], cell[1] + (i + 2)))
            elif wind_direction == "south":
                possible_neighbors.append((cell[0], cell[1] - (i + 2)))
            elif wind_direction == "west":
                possible_neighbors.append((cell[0] - (i + 2), cell[1]))
            elif wind_direction == "east":
                possible_neighbors.append((cell[0] + (i + 2), cell[1]))
        neighbors = [neighbor for neighbor in possible_neighbors if neighbor in self.forest_state.keys()]
        return neighbors

    def get_opposite_edge_cells(self, edge="bottom"):
        opposite_edge_cells = []
        if edge == "bottom":
            for x in range(0, self.size):
                opposite_edge_cells.append((x, self.size - 1))
        elif edge == "top":
            for x in range(0, self.size):
                opposite_edge_cells.append((x, 0))
        elif edge == "right":
            for y in range(0, self.size):
                opposite_edge_cells.append((0, y))
        elif edge == "left":
            for y in range(0, self.size):
                opposite_edge_cells.append((self.size - 1, y))
        return opposite_edge_cells

    # returns three lists of living, burning and burnt trees, respectively
    def get_states(self):
        living_trees = []
        burning_trees = []
        burnt_trees = []
        for cell, state in self.forest_state.items():
            if state == "Burning Tree":
                burning_trees.append(cell)
            elif state == "Burnt Tree":
                burnt_trees.append(cell)
            elif state == "Living Tree":
                living_trees.append(cell)
        return living_trees, burning_trees, burnt_trees

    def setup_pictures(self, type_of_neighborhood="Neumann", wind_direction="west", wind_strength=0):
        if self.save_graphics:
            self.drawing_machine.create_directory()
            self.drawing_machine.draw_lines()
            if wind_strength > 0:
                self.drawing_machine.ax.set_title(
                    "Forest Fire Model with L={0}, p={1},\ntype of neighborhood={2}".format(
                        self.size,
                        self.probability,
                        type_of_neighborhood))
                self.drawing_machine.ax.set_xlabel("Additionally: wind direction={0}, wind strength={1}".format(
                    wind_direction,
                    wind_strength))
            else:
                self.drawing_machine.ax.set_title(
                    "Forest Fire Model with L={0}, p={1},\ntype of neighborhood={2}".format(self.size, self.probability,
                                                                                            type_of_neighborhood))
            self.drawing_machine.ax.get_xaxis().set_ticks([])
            self.drawing_machine.ax.get_yaxis().set_ticks([])
            custom_lines = [patch.Rectangle((0, 0), 1, 1, linewidth=0, edgecolor="none", facecolor="green"),
                            patch.Rectangle((0, 0), 1, 1, linewidth=0, edgecolor="none", facecolor="red"),
                            patch.Rectangle((0, 0), 1, 1, linewidth=0, edgecolor="none", facecolor="k")]
            self.drawing_machine.fig.legend(custom_lines, ["Living Tree", "Burning Tree", "Burnt Tree"], "center right")
            self.drawing_machine.fig.subplots_adjust(left=0.05, right=0.75, top=0.90, bottom=0.1)

    def update_pictures(self, living_trees, burning_trees, burnt_trees):
        if self.save_graphics:
            self.drawing_machine.remove_squares()
            self.drawing_machine.color_squares(living_trees, "green")
            self.drawing_machine.color_squares(burning_trees, "red")
            self.drawing_machine.color_squares(burnt_trees, "k")
            self.drawing_machine.save()

    # the next two methods allows to create a forest copy (stored in .txt) and then proceed with it
    def write_forest_copy(self):
        file = open("forest_copy.txt", "w")
        file.write("{0},{1}\n".format(self.size, self.probability))
        for cell, state in self.forest_state.items():
            file.write("{0},{1},{2}\n".format(cell[0], cell[1], state))
        file.close()

    @staticmethod  # reading the forest copy - creating the ForestFire object based on the .txt copy
    def read_forest_copy(file_name, save_graphics=False):
        file = open(file_name, "r")
        L, p = file.readline().split(",")
        my_read_forest = ForestFire(int(L), float(p), save_graphics)
        read_cells = []
        read_states = []
        for line in file:
            x, y, state = line.strip().split(",")
            read_cells.append((int(x), int(y)))
            read_states.append(state)
        read_forest_state = dict(zip(read_cells, read_states))
        my_read_forest.forest_state.update(read_forest_state)
        return my_read_forest

    # this method plants a tree on the lattice for given probability p
    def plant_forest(self):
        for x in range(0, self.size):
            for y in range(0, self.size):
                if random.random() <= self.probability:
                    self.forest_state[(x, y)] = "Living Tree"

    # here we can set on fire chosen edge
    def set_fire(self, edge="bottom"):
        if edge == "bottom":
            for x in range(0, self.size):
                if self.forest_state[(x, 0)] == "Living Tree":
                    self.forest_state[(x, 0)] = "Burning Tree"
        elif edge == "top":
            for x in range(0, self.size):
                if self.forest_state[(x, self.size - 1)] == "Living Tree":
                    self.forest_state[(x, self.size - 1)] = "Burning Tree"
        elif edge == "left":
            for y in range(0, self.size):
                if self.forest_state[(0, y)] == "Living Tree":
                    self.forest_state[(0, y)] = "Burning Tree"
        elif edge == "right":
            for y in range(0, self.size):
                if self.forest_state[(self.size - 1, y)] == "Living Tree":
                    self.forest_state[(self.size - 1, y)] = "Burning Tree"
        else:
            print("Setting fire failed.")

    # this method spreads fire to the neighbors
    # it also includes the influence of the wind if any
    def spread_fire(self, type_of_neighborhood="Neumann", wind_direction="west", wind_strength=0):
        burning_trees = self.get_states()[1]
        burning_trees_neighbors = set()
        for cell in burning_trees:
            burning_trees_neighbors.update(
                self.get_neighbors(cell, type_of_neighborhood, wind_direction, wind_strength))
        for cell in burning_trees_neighbors:
            if self.forest_state[cell] == "Living Tree":
                self.forest_state[cell] = "Burning Tree"
        for cell in burning_trees:
            self.forest_state[cell] = "Burnt Tree"

    # this method contains setting and spreading fire methods
    def simulate_forest_fire(self, edge="bottom", type_of_neighborhood="Neumann", wind_direction="west",
                             wind_strength=0):
        self.setup_pictures(type_of_neighborhood, wind_direction, wind_strength)
        self.set_fire(edge)
        opposite_edge_cells = self.get_opposite_edge_cells(edge)
        while True:
            living_trees, burning_trees, burnt_trees = self.get_states()
            self.update_pictures(living_trees, burning_trees, burnt_trees)
            for cell in burning_trees:
                if cell in opposite_edge_cells:
                    self.hit_opposite_edge = True
            if not burning_trees:
                break
            self.spread_fire(type_of_neighborhood, wind_direction, wind_strength)
        if self.save_graphics:
            self.drawing_machine.gif()

    # Hoshen-Kopelman algorithm - identifying the clusters (of burnt trees) basing on appropriately labeled matrix
    # again two available types of neighborhood (for cluster measuring, not fire-spreading!): Neumann and Moore
    def get_biggest_cluster_size(self, type_of_neighborhood="Neumann"):
        burnt_trees = self.get_states()[2]
        burnt_trees_matrix = np.zeros((self.size, self.size))
        for cell in burnt_trees:  # creating matrix of ones (burnt trees) and zeros (other states)
            burnt_trees_matrix[self.size - 1 - cell[1]][cell[0]] = 1
        Moore_neighborhood_matrix = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        if type_of_neighborhood == "Moore":
            labeled_matrix = scnm.label(burnt_trees_matrix, structure=Moore_neighborhood_matrix)[0]
        else:
            labeled_matrix = scnm.label(burnt_trees_matrix)[0]
        clusters_sizes = np.unique(labeled_matrix, return_counts=True)[1][1:]
        biggest_cluster_size = max(clusters_sizes, default=0)
        return biggest_cluster_size

    # this method restores burnt forest to a living one
    # (to make a comparisons between types of neighborhood and wind/no-wind situations on the same grid of trees):
    def restore_forest(self):
        self.hit_opposite_edge = False
        for cell, state in self.forest_state.items():
            if state == "Burnt Tree":
                self.forest_state[cell] = "Living Tree"
