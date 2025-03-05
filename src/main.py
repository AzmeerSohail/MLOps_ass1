# Importing necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib  # For saving the model


def split_state_zip(statezip):
    """
    Splits the 'statezip' field into 'state' and 'zipcode'.

    Args:
        statezip (str): The combined state and zipcode field.

    Returns:
        pd.Series: A series containing the state and zipcode.
    """
    try:
        state, zipcode = statezip.split(" ", 1)
    except ValueError:
        state, zipcode = "Unknown", "Unknown"
    return pd.Series([state, zipcode])


def main():
    """
    Main function to execute the data processing, model training,
    and evaluation tasks.
    """
    df = pd.read_csv(
        r"E:/mlops_ass1/MLOps_ass1/data/house_pred_Datasset/data.csv"
    )

    # Selecting the required fields
    fields = [
        "price", "bedrooms", "bathrooms", "sqft_living", "floors", "yr_built"
    ]
    df = df[fields]

    # Removing outliers using Interquartile Range (IQR)
    Q1 = df["price"].quantile(0.25)
    Q3 = df["price"].quantile(0.75)
    IQR = Q3 - Q1
    df = df[
        (df["price"] >= (Q1 - 1.5 * IQR)) & (df["price"] <= (Q3 + 1.5 * IQR))
    ]

    # Separating the target variable (price) from the feature variables
    X = df.drop("price", axis=1)
    y = df["price"]

    # Feature Scaling (Standardizing)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    joblib.dump(scaler, "scaler.pkl")
    print("Scaler saved as 'scaler.pkl'")

    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Creating and training a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Saving the trained model
    joblib.dump(model, "linear_regression_model.pkl")
    print("Model saved as 'linear_regression_model.pkl'")

    # Making predictions
    y_pred = model.predict(X_test)

    # Evaluating the model
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"Root Mean Squared Error: {rmse}")
    print(f"R-squared: {r2}")


if __name__ == "__main__":
    main()
