import tensorflow as tf
import numpy as np
from ai_engine.image_utils import preprocess
from ai_engine.disease_advisor import generate_advice

# ai_engine/router.py
import tensorflow as tf

MODELS = {}

def load_model(crop):
    if crop not in MODELS:
        MODELS[crop] = tf.keras.models.load_model(
            f"models/{crop}/disease_model.keras"
        )
    return MODELS[crop]

def predict(crop, image_bytes):
    config = MODELS[crop]
    image = preprocess(image_bytes)

    # Health check
    if config["health"]:
        health_model = tf.keras.models.load_model(config["health"])
        health_score = health_model.predict(image)[0][0]
        health = "Healthy" if health_score < 0.5 else "Diseased"
    else:
        health = "Diseased"

    # Disease detection
    disease_model = tf.keras.models.load_model(config["disease"])
    preds = disease_model.predict(image)[0]
    idx = int(np.argmax(preds))

    disease = config["classes"][idx]
    confidence = float(preds[idx])

    advice = generate_advice(crop, health, disease, confidence)

    return {
        "crop": crop,
        "health": health,
        "disease": disease if health != "Healthy" else "None",
        "confidence": round(confidence, 3),
        "advice": advice
    }
