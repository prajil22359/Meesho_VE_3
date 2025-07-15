import uuid
import os
import json

class FashionClassifier:
    def __init__(self):
        # Do not create ModelPredictor here to save memory
        self.predictor = None

    def predict(self, image_path):
        # Lazy import
        from .meesho_model import ModelPredictor

        # Initialize predictor only when first used
        if self.predictor is None:
            self.predictor = ModelPredictor()

        prediction = self.predictor.predict_image(image_path)

        # Keep only category and attributes
        result = {
            "category": prediction["category"],
            "attributes": prediction["attributes"]
        }

        # Save clean JSON
        output_dir = "predictions"
        os.makedirs(output_dir, exist_ok=True)

        output_filename = f"prediction_{uuid.uuid4().hex}.json"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        return result, output_path
