from PIL import Image
import numpy as np
import io

IMG_SIZE = (224, 224)

def preprocess(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    img = np.array(img) / 255.0
    return np.expand_dims(img, axis=0)
