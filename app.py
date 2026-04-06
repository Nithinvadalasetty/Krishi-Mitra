import os
import cv2
import numpy as np
import subprocess
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
import os


# ================= APP SETUP =================
app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
MODEL_PATH = "models/disease_model.h5"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= GLOBAL MEMORY =================
LAST_ANALYSIS = {
    "crop": None,
    "disease": None,
    "cause": None,
    "actions": None
}

# ================= LOAD MODEL =================
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded")
print("🧠 Model input shape:", model.input_shape)

# ================= LABEL MAP =================
CLASS_NAMES = ["Healthy", "Early Blight", "Late Blight"]

DISEASE_INFO = {
    "Early Blight": {
        "cause": "Fungal infection (Alternaria)",
        "actions": [
            "Spray Chlorothalonil 2 g/L",
            "Remove infected leaves",
            "Avoid overhead irrigation",
            "Crop rotation"
        ]
    },
    "Late Blight": {
        "cause": "Fungal infection (Phytophthora)",
        "actions": [
            "Spray Mancozeb 3 g/L",
            "Destroy infected plants",
            "Avoid moisture on leaves",
            "Improve air circulation"
        ]
    },
    "Healthy": {
        "cause": "No disease detected",
        "actions": [
            "Maintain irrigation schedule",
            "Apply balanced fertilizer",
            "Monitor weekly"
        ]
    }
}

# ================= IMAGE PREPROCESS =================
def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ================= HOME =================
@app.route("/")
def index():
    return render_template("index.html")

# ================= ANALYZE =================
@app.route("/analyze", methods=["POST"])
def analyze():
    crop = request.form.get("crop")
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"})

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = preprocess_image(path)
    preds = model.predict(img)[0]
    idx = np.argmax(preds)

    disease = CLASS_NAMES[idx]
    confidence = round(float(preds[idx]) * 100, 2)
    info = DISEASE_INFO[disease]

    LAST_ANALYSIS["crop"] = crop
    LAST_ANALYSIS["disease"] = disease
    LAST_ANALYSIS["cause"] = info["cause"]
    LAST_ANALYSIS["actions"] = info["actions"]

    return jsonify({
        "crop": crop,
        "disease": disease,
        "confidence": confidence,
        "health": "Healthy" if disease == "Healthy" else "Unhealthy",
        "cause": info["cause"],
        "actions": info["actions"]
    })

# ================= CHATBOT =================
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower()

    if not LAST_ANALYSIS["disease"]:
        return jsonify({
            "reply": "Please analyze a crop image first 🌱"
        })

    prompt = f"""
You are an agriculture expert.

Crop: {LAST_ANALYSIS['crop']}
Disease: {LAST_ANALYSIS['disease']}
Cause: {LAST_ANALYSIS['cause']}
Recommended actions:
{chr(10).join(LAST_ANALYSIS['actions'])}

User question: {msg}

Rules:
- Answer briefly
- Use bullet points
- Mention spray name and dosage
- Avoid long explanations
"""

    result = subprocess.run(
        ["ollama", "run", "phi"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    reply = result.stdout.strip()
    if not reply:
        reply = "No response generated. Please try again."

    return jsonify({"reply": reply})

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)