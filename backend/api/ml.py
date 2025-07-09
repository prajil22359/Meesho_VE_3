import json
import uuid
import os

class FashionClassifier:
    def __init__(self):
        pass  # Nothing to load for now

    def predict(self, image_path):
        # Instead of real model, return dummy data
        prediction = {
            "color": "1",
            "pattern": "1",
            "category": "1",
            "confidence": "1"
        }

        # Save output to JSON file
        output_filename = f"prediction_{uuid.uuid4().hex}.json"
        output_path = os.path.join("predictions", output_filename)

        # Make sure the folder exists
        os.makedirs("predictions", exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(prediction, f)

        return prediction, output_path
