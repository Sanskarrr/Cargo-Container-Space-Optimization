#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Tire {
    int length;
    char symbol; // Added a symbol to represent each tire

    // Constructor
    Tire(int l, char s) : length(l), symbol(s) {}
};

class Container {
private:
    vector<vector<char>> container; // Changed the container type to store characters
    int rows, cols;
    int filledSpace;

public:
    // Constructor
    Container(int r, int c) : rows(r), cols(c), filledSpace(0) {
        container.resize(rows, vector<char>(cols, '-')); // Initialize the container with all elements set to '-'
    }

    // Function to place a tire into the container
    bool placeTire(Tire tire) {
        // Find the first available position to place the tire
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                if (canPlaceTire(tire, i, j)) {
                    placeTireAtPosition(tire, i, j);
                    return true; // Tire placed successfully
                }
            }
        }
        return false; // Tire cannot be placed in the container
    }

    // Function to check if a tire can be placed at a given position
    bool canPlaceTire(Tire tire, int row, int col) {
        for (int i = 0; i < tire.length; ++i) {
            for (int j = 0; j < tire.length; ++j) {
                int r = row + i;
                int c = col + j;
                if (r >= rows || c >= cols || container[r][c] != '-') {
                    return false; // Cannot place the tire at this position
                }
            }
        }
        return true; // Tire can be placed at this position
    }

    // Function to place the tire at a given position
    void placeTireAtPosition(Tire tire, int row, int col) {
        for (int i = 0; i < tire.length; ++i) {
            for (int j = 0; j < tire.length; ++j) {
                container[row + i][col + j] = tire.symbol; // Place the tire symbol
            }
        }
        filledSpace += tire.length * tire.length; // Update the filled space
    }

    // Function to check if a position is occupied by a tire
    bool isOccupied(int row, int col) const {
        return container[row][col] != '-';
    }

    // Function to retrieve the container contents
    const vector<vector<char>>& getContainer() const {
        return container;
    }

    // Function to calculate the percentage of container filled
    double getPercentageFilled() const {
        return static_cast<double>(filledSpace) / (rows * cols) * 100.0;
    }
};

// Comparator function for sorting tires in descending order of length
bool compareTires(const Tire& a, const Tire& b) {
    return a.length > b.length;
}

int main() {
    int containerRows, containerCols;
    cout << "Enter the number of rows and columns of the container: ";
    cin >> containerRows >> containerCols;

    int numTires;
    cout << "Enter the number of tires: ";
    cin >> numTires;

    vector<Tire> tires;
    cout << "Enter the lengths and symbols of each tire (e.g., 4 A):\n";
    for (int i = 0; i < numTires; ++i) {
        int length;
        char symbol;
        cin >> length >> symbol;
        tires.push_back(Tire(length, symbol));
    }

    // Sort the tires in descending order of length
    sort(tires.begin(), tires.end(), compareTires);

    Container container(containerRows, containerCols);

    // Try to place each tire in the container
    for (const Tire& tire : tires) {
        if (!container.placeTire(tire)) {
            cout << "Cannot fit all tires into the container." << endl;
            return 1;
        }
    }

    // Output the arrangement of tires in the container
    cout << "Arrangement of tires in the container:\n";
    const vector<vector<char>>& containerContents = container.getContainer();
    for (int i = 0; i < containerRows; ++i) {
        for (int j = 0; j < containerCols; ++j) {
            cout << (container.isOccupied(i, j) ? containerContents[i][j] : '-') << " ";
        }
        cout << endl;
    }

    // Output the percentage of the container filled
    cout << "Percentage of the container filled: " << container.getPercentageFilled() << "%" << endl;

    return 0;
}
