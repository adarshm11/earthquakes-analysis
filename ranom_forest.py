import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# load the earthquake data from the CSV file
read_file = 'cleaned_earthquakes_data.csv'
earthquake_data = pd.read_csv(read_file)

# drop rows with missing latitude, longitude, date
earthquake_data.dropna(subset=['latitude', 'longitude', 'date'], inplace=True)

# define features and target (use only latitude and longitude)
X = earthquake_data[['latitude', 'longitude']]
y = earthquake_data[['latitude', 'longitude']]

# split the data into training and testing sets
# test_size  = 0.2 means use 20% of data for testing and 80% of data for training
# random_state = usually use 42 as a parameter
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train a random forest regressor model for predicting earthquake location
# n_estimators = 100 is default value
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

model_y = model.predict(X_test)

# Convert predictions and actual values to DataFrame for better readability
model_y_df = pd.DataFrame(model_y, columns=['pred_latitude', 'pred_longitude'])
test_y_df = pd.DataFrame(y_test.values, columns=['latitude', 'longitude'])

# Concatenate the actual and predicted values for comparison
compare_df = pd.concat([test_y_df.reset_index(drop=True), model_y_df], axis=1)
print("show actual data and predicted")
print(compare_df.head(10))

# model evaluate
mse = mean_squared_error(y_test, model_y)
print(f"random forest mse: {mse:.2f}")

# Predict the next possible earthquake location
next_earthquake = model.predict([[X['latitude'].mean(), X['longitude'].mean()]])
next_latitude, next_longitude = next_earthquake[0]
print(f"predicted next earthquake location: latitude: {next_latitude:.2f}, longitude: {next_longitude:.2f}")

# Plot Actual vs Predicted locations
plt.figure(figsize=(10, 6))
plt.scatter(test_y_df['longitude'], test_y_df['latitude'], color='blue', label='Actual Locations', alpha=0.6)
plt.scatter(model_y_df['pred_longitude'], model_y_df['pred_latitude'], color='red', label='Predicted Locations', alpha=0.6)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Actual Earthquake occurred location vs Predicted Earthquake location')
plt.legend()
plt.tight_layout()
plt.show()

# Plot next earthquake location
plt.figure(figsize=(10, 6))
plt.scatter(X['longitude'], X['latitude'], color='blue', alpha=0.3, label='Earthquake happened')
plt.scatter(next_longitude, next_latitude, color='green', marker='X', s=200, label='Predicted Next Earthquake Location')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Predicted Next Earthquake Location')
plt.legend()
plt.tight_layout()
plt.show()
