#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

vector<vector<int>> bestFitDecreasing(const vector<int>& tires, int containerSize) {
    // Sort the tires in decreasing order of size
    vector<int> sortedTires = tires;
    sort(sortedTires.rbegin(), sortedTires.rend());

    // Initialize a vector to hold the bins and their current fill level
    vector<pair<int, vector<int>>> bins;
    bins.emplace_back(containerSize, vector<int>());

    // Iterate through each tire and try to place it in the bins
    for (int tire : sortedTires) {
        // Find the bin with the best fit (minimizes the remaining space)
        int bestFitBin = -1;
        int minRemainingSpace = containerSize + 1; // Initialize to a value greater than containerSize

        for (size_t i = 0; i < bins.size(); ++i) {
            int remainingSpace = bins[i].first;

            if (tire <= remainingSpace && remainingSpace < minRemainingSpace) {
                bestFitBin = i;
                minRemainingSpace = remainingSpace;
            }
        }

        if (bestFitBin != -1) {
            // Place the tire in the best fit binz
            bins[bestFitBin].second.push_back(tire);
            bins[bestFitBin].first -= tire;
        } else {
            // If the tire couldn't fit in any existing bins, create a new bin for it
            bins.emplace_back(containerSize - tire, vector<int>{tire});
        }
    }

    // Create the final packing arrangement
    vector<vector<int>> packingArrangement;
    for (const auto& bin : bins) {
        if (!bin.second.empty()) {
            packingArrangement.push_back(bin.second);
        }
    }

    return packingArrangement;
}

int main() {
    // Example usage:
    vector<int> tires = {8, 6, 5, 7, 10, 15};
    int containerSize = 20;

    vector<vector<int>> packingArrangement = bestFitDecreasing(tires, containerSize);

    // Display the packing arrangement
    cout << "Packing Arrangement:\n";
    for (int i = 0; i < packingArrangement.size(); ++i) {
        cout << "Bin " << i + 1 << ": ";
        for (int tire : packingArrangement[i]) {
            cout << tire << " ";
        }
        cout << endl;
    }

    return 0;
}
