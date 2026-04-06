import numpy as np
import cv2
from tensorflow.keras.models import load_model
from ai_engine.disease_advisor import get_advice_and_remedy

model = load_model("models/disease_model.h5")

CLASS_NAMES = [
    "Healthy",
    "Bacterial Spot",
    "Early Blight",
    "Late Blight",
    "Leaf Curl",
    "Mosaic Virus"
]

def predict_image(image_file):
    img_bytes = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)
    idx = int(np.argmax(preds))
    confidence = float(np.max(preds) * 100)

    disease = CLASS_NAMES[idx]
    info = get_advice_and_remedy(disease)

    return {
        "disease": disease,
        "confidence": round(confidence, 2),
        "advice": info["advice"],
        "remedy": info["remedy"]
    }
