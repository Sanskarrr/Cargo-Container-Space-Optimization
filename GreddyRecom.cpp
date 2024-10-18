#include <iostream>
#include <vector>
#include <cstdlib>  // Include for rand()

using namespace std;

// Function to display the container
void displayContainer(const vector<vector<string>>& container) {
    for (const auto& row : container) {
        for (const auto& cell : row) {
            cout << cell << '\t';
        }
        cout << endl;
    }
}

// Function to check if a tire can be added at a specific position
bool canAddTire(const vector<vector<string>>& container, int row, int col, int sideLength) {
    for (int i = 0; i < sideLength; ++i) {
        for (int j = 0; j < sideLength; ++j) {
            if (container[row + i][col + j] != "") {
                return false; // Tire cannot be added here
            }
        }
    }
    return true;
}

// Function for greedy tire arrangement with recommendations
void greedyTireArrangementWithRecommendations(int containerRows, int containerCols,
                                              int numInitialTires,
                                              double targetFillPercentage) {
    // Initialize the container with empty cells
    vector<vector<string>> container(containerRows, vector<string>(containerCols, ""));

    // Generate initial tires
    for (int i = 0; i < numInitialTires; ++i) {
        int row = rand() % containerRows;
        int col = rand() % containerCols;
        string symbol = to_string(i + 1);  // Use numbers as symbols for simplicity

        // Assuming each tire has a side length of 1 (square)
        container[row][col] = symbol;
    }

    // Display the initial tire arrangement
    cout << "Initial Tire Arrangement:" << endl;
    displayContainer(container);

    // Calculate the percentage of container filled
    int filledCount = 0;
    for (const auto& row : container) {
        for (const auto& cell : row) {
            if (cell != "") {
                ++filledCount;
            }
        }
    }
    double utilizationPercentage = (static_cast<double>(filledCount) / (containerRows * containerCols)) * 100;

    // Display the percentage of container filled
    cout << "Container filled: " << utilizationPercentage << "%" << endl;

    // Recommend extra tires until the target fill percentage is reached
    while (utilizationPercentage < targetFillPercentage) {
        cout << "Recommendation: Add more tires to fill up the container." << endl;
        int row = rand() % containerRows;
        int col = rand() % containerCols;
        container[row][col] = to_string(numInitialTires + 1);  // Use numbers as symbols for simplicity
        ++numInitialTires;
        // Recalculate container fill percentage
        filledCount = 0;
        for (const auto& row : container) {
            for (const auto& cell : row) {
                if (cell != "") {
                    ++filledCount;
                }
            }
        }
        utilizationPercentage = (static_cast<double>(filledCount) / (containerRows * containerCols)) * 100;
    }

    // Display the final tire arrangement
    cout << "Final Tire Arrangement:" << endl;
    displayContainer(container);

    // Display the percentage of container filled
    cout << "Container filled: " << utilizationPercentage << "%" << endl;
}

int main() {
    int containerRows, containerCols;
    cout << "Enter the number of rows of the container: ";
    cin >> containerRows;

    cout << "Enter the number of columns of the container: ";
    cin >> containerCols;

    int numInitialTires;
    cout << "Enter the number of initial tires: ";
    cin >> numInitialTires;

    double targetFillPercentage;
    cout << "Enter the target fill percentage: ";
    cin >> targetFillPercentage;

    greedyTireArrangementWithRecommendations(containerRows, containerCols, numInitialTires, targetFillPercentage);

    return 0;
}
