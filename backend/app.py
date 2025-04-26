# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

@app.route('/')
def home():
    return "Welcome to ArtIQ API"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']

    try:
        image = Image.open(io.BytesIO(file.read()))
        # Dummy prediction logic – replace with real model
        predicted_style = "Impressionism"
        confidence = 91.3

        return jsonify({
            "style": predicted_style,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
