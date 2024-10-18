#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

// Define a tire struct with length and width
struct Tire {
    int length;
    int width;
};

// Define a packing arrangement as a vector of bins, where each bin contains tires
using Bin = vector<Tire>;
using PackingArrangement = vector<Bin>;

// Function to generate a random tire
Tire generateRandomTire(int maxLength, int maxWidth) {
    Tire tire;
    tire.length = rand() % maxLength + 1;
    tire.width = rand() % maxWidth + 1;
    return tire;
}

// Function to initialize a random packing arrangement
PackingArrangement initializeRandomArrangement(int numTires, int containerLength, int containerWidth) {
    PackingArrangement arrangement;
    Bin currentBin;
    int remainingLength = containerLength;
    int remainingWidth = containerWidth;

    for (int i = 0; i < numTires; ++i) {
        Tire tire = generateRandomTire(remainingLength, remainingWidth);

        if (tire.length <= remainingLength && tire.width <= remainingWidth) {
            currentBin.push_back(tire);
            remainingLength -= tire.length;
            remainingWidth -= tire.width;
        } else {
            arrangement.push_back(currentBin);
            currentBin.clear();
            remainingLength = containerLength;
            remainingWidth = containerWidth;
        }
    }

    if (!currentBin.empty()) {
        arrangement.push_back(currentBin);
    }

    return arrangement;
}

// Function to calculate the fitness of a packing arrangement (e.g., percentage of container filled)
double calculateFitness(const PackingArrangement& arrangement, int containerLength, int containerWidth) {
    double usedArea = 0.0;

    for (const Bin& bin : arrangement) {
        for (const Tire& tire : bin) {
            usedArea += static_cast<double>(tire.length * tire.width);
        }
    }

    double totalArea = static_cast<double>(containerLength * containerWidth);
    double percentageFilled = (usedArea / totalArea) * 100.0;
    return percentageFilled;
}

int main() {
    srand(static_cast<unsigned>(time(nullptr)));

    int numTires;
    int containerLength;
    int containerWidth;

    // Get user inputs for container dimensions and the number of tires
    cout << "Enter the container length: ";
    cin >> containerLength;
    cout << "Enter the container width: ";
    cin >> containerWidth;
    cout << "Enter the number of tires: ";
    cin >> numTires;

    // Initialize the population
    vector<PackingArrangement> population;
    const int populationSize = 100;
    for (int i = 0; i < populationSize; ++i) {
        population.push_back(initializeRandomArrangement(numTires, containerLength, containerWidth));
    }

    // Genetic algorithm loop
    const int numGenerations = 1000;
    for (int generation = 0; generation < numGenerations; ++generation) {
        // Evaluate fitness of each arrangement
        vector<pair<PackingArrangement, double>> evaluatedPopulation;
        for (const PackingArrangement& arrangement : population) {
            double fitness = calculateFitness(arrangement, containerLength, containerWidth);
            evaluatedPopulation.push_back({arrangement, fitness});
        }

        // Sort the population by fitness in descending order
        sort(population.begin(), population.end(), [&](const PackingArrangement& a, const PackingArrangement& b) {
            return calculateFitness(a, containerLength, containerWidth) > calculateFitness(b, containerLength, containerWidth);
        });

        // Select the top-performing arrangements
        const int eliteSize = populationSize / 2;
        vector<PackingArrangement> newPopulation(population.begin(), population.begin() + eliteSize);

        // Randomly select the rest
        while (newPopulation.size() < populationSize) {
            int randIndex = rand() % eliteSize;
            newPopulation.push_back(population[randIndex]);
        }

        population = newPopulation;

        // Print the best fitness in this generation
        double bestFitness = calculateFitness(population[0], containerLength, containerWidth);
        cout << "Generation " << generation << ": Best Fitness = " << bestFitness << "%" << endl;
    }

    // Print the best packing arrangement found
    cout << "Best Packing Arrangement:" << endl;
    for (int i = 0; i < population[0].size(); ++i) {
        cout << "Bin " << i + 1 << ": ";
        for (const Tire& tire : population[0][i]) {
            cout << "(" << tire.length << "x" << tire.width << ") ";
        }
        cout << endl;
    }

    return 0;
}
