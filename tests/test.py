import sys
import os
import unittest
from app import app, validate_input
import json

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class TestHousePriceAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_validate_input_valid(self):
        # Test valid input data
        data = {
            'bedrooms': 3,
            'bathrooms': 2,
            'sqft_living': 1500,
            'floors': 2,
            'yr_built': 1990
        }
        expected_output = [3.0, 2.0, 1500.0, 2.0, 1990.0]
        self.assertEqual(validate_input(data), expected_output)

    def test_validate_input_invalid_bedrooms(self):
        # Test invalid bedrooms value
        data = {
            'bedrooms': 20,  # Invalid value
            'bathrooms': 2,
            'sqft_living': 1500,
            'floors': 2,
            'yr_built': 1990
        }
        with self.assertRaises(ValueError):
            validate_input(data)

    def test_api_predict_success(self):
        # Test the /predict API with valid data
        data = {
            'bedrooms': 3,
            'bathrooms': 2,
            'sqft_living': 1500,
            'floors': 2,
            'yr_built': 1990
        }
        response = self.client.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertIn('prediction', json_data)

    def test_api_predict_invalid(self):
        # Test the /predict API with invalid data (invalid bedrooms)
        data = {
            'bedrooms': 20,  # Invalid value
            'bathrooms': 2,
            'sqft_living': 1500,
            'floors': 2,
            'yr_built': 1990
        }
        response = self.client.post('/predict', json=data)
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertIn('error', json_data)

if __name__ == '__main__':
    unittest.main()
