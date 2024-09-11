import pandas as pd
import seaborn as sns
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('airdata.csv')

# Preview the dataset
print("Dataset Preview:")
print(df.head())

# Select independent variables (weather conditions and air quality)
x_df = df[['AQI', 'PM10', 'PM2_5', 'NO2', 'SO2', 'O3', 'Temperature', 'Humidity', 'WindSpeed']]

# Target variable: Predicting RespiratoryCases
y_df = df['RespiratoryCases']  # Modify this to predict other health issues if needed

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.3, random_state=42)

# Create Linear Regression model
model = linear_model.LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Print R^2 score for training data (to check model accuracy)
print("Training R^2 score:", model.score(X_train, y_train))

# Make predictions on the test set
prediction_test = model.predict(X_test)

# Compare actual vs predicted values
print("\nActual vs Predicted (Respiratory Cases):")
print(pd.DataFrame({'Actual': y_test, 'Predicted': prediction_test}).head())

# Calculate and print Mean Squared Error (MSE)
mse = np.mean((prediction_test - y_test) ** 2)
print("\nMean Squared Error (MSE) for Respiratory Cases:", mse)

# Save the trained model using pickle
pickle.dump(model, open('respiratory_cases_model.pkl', 'wb'))
print("\nModel saved as 'respiratory_cases_model.pkl'")

# Load the model back (for demonstration)
model = pickle.load(open('respiratory_cases_model.pkl', 'rb'))

# Test the loaded model with a sample prediction (replace with sample values)
sample_prediction = model.predict([[187.27, 295.85, 13.03, 6.63, 66.16, 54.62, 5.15, 84.42, 6.13]])
print("\nSample Prediction for Respiratory Cases:", sample_prediction)

# Optional: Visualize the relationships using Seaborn
# Plot Respiratory Cases vs AQI
sns.lmplot(x='AQI', y='RespiratoryCases', data=df)
plt.title('Respiratory Cases vs AQI')
plt.show()

# Plot Respiratory Cases vs Temperature
sns.lmplot(x='Temperature', y='RespiratoryCases', data=df)
plt.title('Respiratory Cases vs Temperature')
plt.show()
