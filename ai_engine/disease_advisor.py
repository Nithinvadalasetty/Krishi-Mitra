DISEASE_INFO = {
    "Healthy": {
        "advice": "Your crop is healthy. Continue regular monitoring.",
        "remedy": "Maintain proper irrigation and nutrient balance."
    },

    "Bacterial Spot": {
        "advice": "Bacterial Spot spreads in warm and humid conditions.",
        "remedy": "Use copper-based bactericides and remove infected leaves."
    },

    "Early Blight": {
        "advice": "Early Blight is a fungal disease caused by poor field hygiene.",
        "remedy": "Apply fungicides like Mancozeb and practice crop rotation."
    },

    "Late Blight": {
        "advice": "Late Blight spreads rapidly in cool and wet conditions.",
        "remedy": "Use fungicides immediately and destroy infected plants."
    },

    "Leaf Curl": {
        "advice": "Leaf Curl is caused by whiteflies.",
        "remedy": "Spray neem oil or imidacloprid and control insect vectors."
    },

    "Mosaic Virus": {
        "advice": "Mosaic Virus is a viral disease spread by pests.",
        "remedy": "Remove infected plants and control aphids and whiteflies."
    }
}

def get_advice_and_remedy(disease):
    return DISEASE_INFO.get(
        disease,
        {
            "advice": "Disease information not available.",
            "remedy": "Consult an agriculture officer."
        }
    )
