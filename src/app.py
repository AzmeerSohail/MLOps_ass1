from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import joblib
import os

app = Flask(__name__, static_folder="../frontend")  # Set frontend folder
CORS(app)  # Enable CORS for API calls


# Load the trained model and scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "linear_regression_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))


def validate_input(data):
    try:
        bedrooms = float(data.get("bedrooms", 0))  #no of bedrooms
        bathrooms = float(data.get("bathrooms", 0))
        sqft_living = float(data.get("sqft_living", 0))
        floors = float(data.get("floors", 0))
        yr_built = float(data.get("yr_built", 0))

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
    try:
        data = request.json
        features = validate_input(data)
        input_data = np.array(features).reshape(1, -1)
        scaled_data = scaler.transform(input_data)
        prediction = model.predict(scaled_data)[0]

        return jsonify({"prediction": prediction})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify(
            {"error": "An error occurred. Please check your input."}
        ), 500


@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


