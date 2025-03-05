# Importing necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
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
        state, zipcode = statezip.split(' ', 1)
    except ValueError:
        state, zipcode = 'Unknown', 'Unknown'
    return pd.Series([state, zipcode])

def main():
    """
    Main function to execute the data processing, model training, 
    and evaluation tasks.
    """
    # Loading the dataset
    # Assuming the dataset is a CSV file, load it into a DataFrame
    #df = pd.read_csv('data/house_pred_Datasset/data.csv')
    df = pd.read_csv(r'E:/mlops_ass1/MLOps_ass1/data/house_pred_Datasset/data.csv')

    # Selecting the required fields and other fields for the model
    fields = [
        'price', 'bedrooms', 'bathrooms', 'sqft_living', 'floors', 'yr_built'
    ]

    # Subset the dataframe with the selected fields
    df = df[fields]

    # Removing outliers based on price using Interquartile Range (IQR)
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[
        (df['price'] >= (Q1 - 1.5 * IQR)) & 
        (df['price'] <= (Q3 + 1.5 * IQR))
    ]

    # Separating the target variable (price) from the feature variables
    X = df.drop('price', axis=1)
    y = df['price']

    # Feature Scaling (Standardizing)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    joblib.dump(scaler, 'scaler.pkl')
    print("Scaler saved as 'scaler.pkl'")

    # Splitting the data into train and test sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Creating and training a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Saving the trained model
    joblib.dump(model, 'linear_regression_model.pkl')
    print("Model saved as 'linear_regression_model.pkl'")

    # Making predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluating the model using Mean Squared Error and R-squared
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    print(f'Root Mean Squared Error: {rmse}')
    print(f'R-squared: {r2}')

    # Visualizing the results
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6, color='b')
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Actual vs Predicted Prices")
    plt.show()

    # Plotting Residuals
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True, bins=30, color='r')
    plt.title("Distribution of Residuals")
    plt.xlabel("Residuals")
    plt.show()

    # Loading the model (for demonstration purposes)
  

if __name__ == "__main__":
    main()
