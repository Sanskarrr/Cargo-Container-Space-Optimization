#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Tire {
    int width;
    int length;
    char symbol;

    Tire(int w, int l, char s) : width(w), length(l), symbol(s) {}
};

class Container3D {
    
private:
    vector<vector<vector<char>> > container; // 3D container
    int depth, rows, cols;
    int filledSpace;

public:
    Container3D(int d, int r, int c) : depth(d), rows(r), cols(c), filledSpace(0) {
        container.resize(depth, vector<vector<char>>(rows, vector<char>(cols, '-')));
    }

    bool placeTire(Tire tire) {
        for (int k = 0; k < depth; ++k) {
            for (int i = 0; i < rows; ++i) {
                for (int j = 0; j < cols; ++j) {
                    if (canPlaceTire(tire, k, i, j)) {
                        placeTireAtPosition(tire, k, i, j);
                        return true;
                    }
                }
            }
        }
        return false;
    }

    bool canPlaceTire(Tire tire, int depthIndex, int rowIndex, int colIndex) {
        for (int k = 0; k < tire.width; ++k) {
            for (int i = 0; i < tire.length; ++i) {
                for (int j = 0; j < tire.length; ++j) {
                    int d = depthIndex + k;
                    int r = rowIndex + i;
                    int c = colIndex + j;
                    if (d >= depth || r >= rows || c >= cols || container[d][r][c] != '-') {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    void placeTireAtPosition(Tire tire, int depthIndex, int rowIndex, int colIndex) {
        for (int k = 0; k < tire.width; ++k) {
            for (int i = 0; i < tire.length; ++i) {
                for (int j = 0; j < tire.length; ++j) {
                    container[depthIndex + k][rowIndex + i][colIndex + j] = tire.symbol;
                }
            }
        }
        filledSpace += tire.width * tire.length * tire.length;
    }

    bool isOccupied(int depthIndex, int rowIndex, int colIndex) const {
        return container[depthIndex][rowIndex][colIndex] != '-';
    }

    const vector<vector<vector<char>>>& getContainer() const {
        return container;
    }

    double getPercentageFilled() const {
        return static_cast<double>(filledSpace) / (depth * rows * cols) * 100.0;
    }
};

bool compareTires(const Tire& a, const Tire& b) {
    return a.length > b.length;
}

int main() {
    int containerDepth, containerRows, containerCols;
    cout << "Enter the depth, number of rows, and columns of the 3D container: ";
    cin >> containerDepth >> containerRows >> containerCols;

    int numTires;
    cout << "Enter the number of tires: ";
    cin >> numTires;

    vector<Tire> tires;
    cout << "Enter the width, lengths, and symbols of each tire (e.g., 2 4 A):\n";
    for (int i = 0; i < numTires; ++i) {
        int width, length;
        char symbol;
        cin >> width >> length >> symbol;
        tires.push_back(Tire(width, length, symbol));
    }

    sort(tires.begin(), tires.end(), compareTires);

    Container3D container(containerDepth, containerRows, containerCols);

    for (const Tire& tire : tires) {
        if (!container.placeTire(tire)) {
            cout << "Cannot fit all tires into the 3D container." << endl;
            break;
        }
    }

    double fillPercentage = container.getPercentageFilled();
    cout << "Percentage of the container filled: " << fillPercentage << "%" << endl;

    if (fillPercentage < 90.0) {
        cout << "To maximize space utilization, you can add more tires:" << endl;

        vector<Tire> additionalTires;
        while (fillPercentage < 90.0) {
            bool added = false;
            for (const Tire& tire : tires) {
                if (container.placeTire(tire)) {
                    additionalTires.push_back(tire);
                    fillPercentage = container.getPercentageFilled();
                    added = true;
                }
            }
            if (!added) {
                break;
            }
        }

        for (const Tire& tire : additionalTires) {
            cout << "Added tire with width " << tire.width << ", length " << tire.length << ", and symbol " << tire.symbol << endl;
        }

        cout << "New percentage of the container filled: " << fillPercentage << "%" << endl;
    }

    return 0;
}
