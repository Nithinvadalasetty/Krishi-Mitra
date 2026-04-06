# ai_engine/fertilizer_engine.py

def recommend_fertilizer(soil_type, crop, season):

    soil_type = soil_type.lower()
    crop = crop.lower()
    season = season.lower()

    database = {
        "rice": {
            "black": {
                "kharif": {
                    "fertilizer": "Urea + DAP",
                    "quantity": "50 kg/acre",
                    "timing": "Apply during early vegetative stage"
                }
            }
        },
        "wheat": {
            "red": {
                "rabi": {
                    "fertilizer": "NPK (10:26:26)",
                    "quantity": "45 kg/acre",
                    "timing": "Apply before irrigation"
                }
            }
        }
    }

    try:
        result = database[crop][soil_type][season]
        return {
            "status": "success",
            "data": result
        }
    except KeyError:
        return {
            "status": "error",
            "message": "No recommendation available for given inputs."
        }
