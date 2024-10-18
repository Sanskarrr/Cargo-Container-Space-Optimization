import numpy as np
import folium
from ipyleaflet import Map, Marker, basemaps, basemap_to_tiles, TileLayer

def generate_random_locations(num_locations):
    return {f'Location_{i}': np.random.rand(2) * 10 for i in range(num_locations)}

def calculate_distance(route, locations):
    total_distance = 0
    for i in range(len(route) - 1):
        current_location = locations[route[i]]
        next_location = locations[route[i + 1]]
        total_distance += np.linalg.norm(np.array(next_location) - np.array(current_location))
    return total_distance + 1e-6

def genetic_algorithm(locations, population_size=50, generations=1000):
    locations_list = list(locations.keys())

    population = [np.random.permutation(locations_list) for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = [1 / calculate_distance(route, locations) for route in population]

        selected_indices = np.argsort(fitness_scores)[-population_size:]
        selected_population = [population[i] for i in selected_indices]

        crossover_population = []
        for _ in range(population_size):
            parent1, parent2 = [selected_population[i] for i in np.random.choice(len(selected_population), size=2, replace=False)]
            crossover_point = np.random.randint(len(locations_list))
            child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            crossover_population.append(child)

        mutation_rate = 0.1
        for i in range(population_size):
            if np.random.rand() < mutation_rate:
                mutation_point1, mutation_point2 = np.random.choice(len(locations_list), size=2, replace=False)
                crossover_population[i][mutation_point1], crossover_population[i][mutation_point2] = \
                    crossover_population[i][mutation_point2], crossover_population[i][mutation_point1]

        population = crossover_population

    best_route_index = np.argmax([1 / calculate_distance(route, locations) for route in population])
    best_route = population[best_route_index]
    return best_route

def visualize_map(locations, route=None):
    m = Map(center=(np.mean([coord[0] for coord in locations.values()]),
                   np.mean([coord[1] for coord in locations.values()])),
            zoom=10,
            basemap=basemap_to_tiles(basemaps.Esri.WorldStreetMap))

    for location, coord in locations.items():
        marker = Marker(location=(coord[0], coord[1]), title=location)
        m.add_layer(marker)

    if route is not None and len(route) > 1:  # Check if route is not empty
        route_coordinates = [tuple(locations[loc]) for loc in route]
        route_line = TileLayer(tiles=[route_coordinates], opacity=0.8)
        m.add_layer(route_line)

    return m


# Generate random locations for demonstration
num_locations = 6
delivery_locations = generate_random_locations(num_locations)

# Visualize the map and allow user to select delivery locations
selected_locations = {}
for location, coord in delivery_locations.items():
    response = input(f"Do you want to include {location} in the delivery? (y/n): ").lower()
    if response == 'y':
        selected_locations[location] = coord

# Run the genetic algorithm and print the best route
best_route = genetic_algorithm(selected_locations)
print("Selected Delivery Locations:", selected_locations)
print("Best Route:", best_route)
print("Total Distance:", calculate_distance(best_route, selected_locations))

# Visualize the map with the best route
visualize_map(selected_locations, route=best_route)
