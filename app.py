from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

# Initialize the Flask application
app = Flask(__name__)

# Define model path
MODEL_PATH = "/content/drive/MyDrive/AIML/Projects/backend_sources/superkart_sales_model.joblib"

# Load the pre-trained pipeline model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
else:
    model = None
    print(f"Warning: Model file not found at {MODEL_PATH}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the SuperKart Sales Forecasting API!"})

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model is not loaded on server."}), 500

    try:
        # Retrieve the JSON payload
        data = request.get_json(force=True)

        # Convert payload into a pandas DataFrame (handles both single dict or list of dicts)
        if isinstance(data, dict):
            df_input = pd.DataFrame([data])
        else:
            df_input = pd.DataFrame(data)

        # Generate predictions using the loaded pipeline
        predictions = model.predict(df_input)

        # Return predictions as list in JSON response
        return jsonify({"predictions": predictions.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Run Flask on localhost, port 5000
    app.run(host='0.0.0.0', port=5000)
