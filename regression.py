import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Function to generate random data
def generate_data(num_samples=1000):
    np.random.seed(42)
    tire_volume_type1 = np.random.uniform(10, 20, num_samples)
    tire_volume_type2 = np.random.uniform(15, 25, num_samples)
    tire_volume_type3 = np.random.uniform(5, 15, num_samples)
    container_volume = np.random.uniform(500, 1000, num_samples)

    # Assuming a simple relationship between tire volumes and the number of tires
    num_tires = 0.5 * tire_volume_type1 + 0.3 * tire_volume_type2 + 0.2 * tire_volume_type3 + 100

    data = pd.DataFrame({
        'Tire_Volume_Type1': tire_volume_type1,
        'Tire_Volume_Type2': tire_volume_type2,
        'Tire_Volume_Type3': tire_volume_type3,
        'Container_Volume': container_volume,
        'Num_Tires': num_tires
    })

    return data

# Generate random data
data = generate_data()

# Split the data into training and testing sets
X = data[['Tire_Volume_Type1', 'Tire_Volume_Type2', 'Tire_Volume_Type3', 'Container_Volume']]
y = data['Num_Tires']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Predict the number of tires for a new configuration
new_configuration = [18, 22, 10, 800]  # Adjust these values based on your tire and container specifications
predicted_tires = model.predict([new_configuration])
print(f'Predicted number of tires for the new configuration: {predicted_tires[0]}')
