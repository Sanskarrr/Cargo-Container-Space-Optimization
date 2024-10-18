import numpy as np
import random

def generate_population(population_size, tire_volumes, container_volume):
    population = []
    for _ in range(population_size):
        individual = np.random.choice(len(tire_volumes), size=len(tire_volumes))

        # Check if the sum of tire volumes exceeds the container volume
        if not np.any(np.sum(tire_volumes[individual]) > container_volume):
            population.append(individual)

    return population

def fitness_function(individual, tire_volumes, container_volume):
    if np.sum(tire_volumes[individual]) > container_volume:
        return 0  # Penalize for overfilling the container

    return container_volume - np.sum(tire_volumes[individual])

def selection(population, fitness_values):
    selected_individuals = []
    for _ in range(len(population)):
        selected_individual = population[np.argmax(fitness_values)]
        selected_individuals.append(selected_individual)

    return selected_individuals

def crossover(parents, crossover_rate):
    offspring = []
    for parent1, parent2 in zip(parents, parents[1:]):
        if random.random() < crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            offspring1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            offspring2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        else:
            offspring1 = parent1
            offspring2 = parent2

        offspring.append(offspring1)
        offspring.append(offspring2)

    return offspring

def mutation(offspring, mutation_rate):
    for individual in offspring:
        for i, _ in enumerate(individual):
            if random.random() < mutation_rate:
                individual[i] = random.randint(0, len(tire_volumes) - 1)

    return offspring

def genetic_algorithm(population_size, tire_volumes, container_volume, num_generations, crossover_rate, mutation_rate):
    population = generate_population(population_size, tire_volumes, container_volume)

    for _ in range(num_generations):
        fitness_values = [fitness_function(individual, tire_volumes, container_volume) for individual in population]

        selected_individuals = selection(population, fitness_values)
        offspring = crossover(selected_individuals, crossover_rate)
        offspring = mutation(offspring, mutation_rate)

        population = selected_individuals + offspring

    # Find the individual with the highest fitness
    best_individual = population[np.argmax([fitness_function(individual, tire_volumes, container_volume) for individual in population])]

    return best_individual

if __name__ == "__main__":
    # Define the tire volumes and container volume
    tire_volumes = [20, 30, 50]
    container_volume = 100

    # GA parameters
    population_size = 100
    num_generations = 100
    crossover_rate = 0.8
    mutation_rate = 0.05

    # Run the genetic algorithm
    best_individual = genetic_algorithm(population_size, tire_volumes, container_volume, num_generations, crossover_rate, mutation_rate)

    # Print the best individual and the fitness value
    print("Best individual:", best_individual)
    print("Fitness value:", fitness_function(best_individual, tire_volumes, container_volume))
