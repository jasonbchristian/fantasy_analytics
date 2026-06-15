from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np

def run_model(X, y, model):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size= 0.20)
    X_train = X_train.to_numpy()
    X_test = X_test.to_numpy()
    y_train = y_train.to_numpy().ravel()
    y_test = y_test.to_numpy().ravel()
    
    match model:
        case "LinearRegression":
            lin_model = LinearRegression().fit(X_train, y_train)
            predictions = lin_model.predict(X_test)
            predictions_flat = predictions.ravel()

            print(f"R2 Score: {r2_score(y_test, predictions):.3f}")
            print(f"MAE: {mean_absolute_error(y_test, predictions):.2f} points")

            plt.figure(figsize=(10, 6))
            plt.scatter(y_test, predictions_flat, alpha=0.3, color='blue', label='Actual vs Predicted')

            # Define min/max based on the flattened arrays
            lims = [min(y_test.min(), predictions_flat.min()), max(y_test.max(), predictions_flat.max())]

            plt.plot(lims, lims, 'r--', lw=2, label='Perfect Prediction Line')

            plt.xlabel('Actual PPR Points')
            plt.ylabel('Predicted PPR Points')
            plt.title('Model Performance: Predicted vs. Actual PPR Points')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.show()
