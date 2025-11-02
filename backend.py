from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    try:
        file = request.files['file']
        y, sr = librosa.load(file, sr=None)

        pitch = float(np.mean(librosa.yin(y, fmin=50, fmax=500)))
        energy = float(np.mean(y ** 2))

        if energy > 0.02 or pitch > 150:
            stress_level = "High Stress"
        else:
            stress_level = "Low Stress"

        return jsonify({
            "stress_level": stress_level,
            "pitch": pitch,
            "energy": energy
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
