from forest_fire import ForestFire

size = 30  # size of a lattice
probability = 0.5  # probability
edge = "bottom"  # possible edges: "bottom", "top", "right", "left"
type_of_neighborhood = "Neumann"  # possible types of neighborhoods: "Neumann", "Moore"
wind_strength = 0  # natural number
wind_direction = "north"  # possible wind directions: "north", "south", "east", "west"
save_graphics = True  # possible values: True, False

my_forest = ForestFire(size, probability, save_graphics)
my_forest.plant_forest()
# my_forest.write_forest_copy() # there is a possibility to save previously planted forest for further simulations
my_forest.simulate_forest_fire(edge, type_of_neighborhood, wind_direction, wind_strength)
# my_read_forest = ForestFire.read_forest_copy("forest_copy.txt", save_graphics)
# here we can load this saved forest and repeat simulation with different arguments
# my_read_forest.simulate_forest_fire(edge, type_of_neighborhood, wind_direction, wind_strength)

# simulation is saved in the directory Results
