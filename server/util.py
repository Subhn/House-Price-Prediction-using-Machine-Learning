import pickle
import json
import numpy as np

# Global variables to store locations, data columns, and the model
locations_list = None
data_columns_list = None
price_prediction_model = None

# Function to estimate the price of a home
def get_estimated_price(location, sqft, bhk, bath):
    try:
        # Get the index of the location from the data columns
        location_index = data_columns_list.index(location.lower())
    except ValueError:
        # If location is not found, set index to -1
        location_index = -1

    # Create an input array for the model with all zeros
    input_features = np.zeros(len(data_columns_list))
    input_features[0] = sqft  # Assuming sqft is the first feature
    input_features[1] = bath   # Assuming bath is the second feature
    input_features[2] = bhk    # Assuming bhk is the third feature
    
    if location_index >= 0:
        input_features[location_index] = 1  # Set the location index to 1

    # Return the predicted price rounded to 2 decimal places
    return round(price_prediction_model.predict([input_features])[0], 2)

# Function to load saved artifacts (data columns and model)
def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global data_columns_list
    global locations_list

    # Load data columns from a JSON file
    with open("./artifacts/columns.json", "r") as f:
        data_columns_list = json.load(f)['data_columns']
        locations_list = data_columns_list[3:]  # first 3 columns are sqft, bath, bhk

    global price_prediction_model
    # Load the model if it's not already loaded
    if price_prediction_model is None:
        model_path = r"C:\Users\subha\Desktop\new\house-price-prediction\model\hyderabad_house_data_model.pickle"
        try:
            with open(model_path, 'rb') as f:
                price_prediction_model = pickle.load(f)
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}")
            raise

    print("Loading saved artifacts...done")

# Function to get location names
def get_location_names():
    return locations_list

# Function to get data columns
def get_data_columns():
    return data_columns_list

# Main function to test the module
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Nizampet', 1000, 3, 3))
    print(get_estimated_price('Nizampet', 1000, 2, 2))
    print(get_estimated_price('Kompally', 1000, 2, 2))  # Other location
    print(get_estimated_price('Kukatpally', 1000, 2, 2))  # Other location
