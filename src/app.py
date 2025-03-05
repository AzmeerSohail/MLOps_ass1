from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and scaler
model = joblib.load("linear_regression_model.pkl")
scaler = joblib.load("scaler.pkl")


def validate_input(data):
    """
    Validate the input data.
    Ensure correct data types and value ranges.
    """
    try:
        # Convert input to float and check ranges
        bedrooms = float(data.get("bedrooms", 0))
        bathrooms = float(data.get("bathrooms", 0))
        sqft_living = float(data.get("sqft_living", 0))
        floors = float(data.get("floors", 0))
        yr_built = float(data.get("yr_built", 0))

        # Check if the values are within reasonable ranges
        if not (0 <= bedrooms <= 10):
            raise ValueError("Invalid value for bedrooms")
        if not (0 <= bathrooms <= 10):
            raise ValueError("Invalid value for bathrooms")
        if not (0 <= sqft_living <= 10000):
            raise ValueError("Invalid value for sqft_living")
        if not (0 <= floors <= 10):
            raise ValueError("Invalid value for floors")
        if not (1800 <= yr_built <= 2024):
            raise ValueError("Invalid value for yr_built")

        return [bedrooms, bathrooms, sqft_living, floors, yr_built]

    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input: {str(e)}")


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Predict house prices based on user input.
    """
    try:
        data = request.json

        # Validate input data
        features = validate_input(data)

        # Prepare data for prediction
        input_data = np.array(features).reshape(1, -1)
        scaled_data = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(scaled_data)[0]

        return jsonify({"prediction": prediction})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify(
            {"error": "An error occurred. Please check your input."}
        ), 500  # ✅ Fixed: Split into multiple lines


if __name__ == "__main__":
    app.run(debug=True)
