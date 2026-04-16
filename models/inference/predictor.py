# Auto-generated file
from detoxify import Detoxify

class ToxicityPredictor:
    def __init__(self):
        # load pretrained model
        self.model = Detoxify("original")

    def predict(self, text: str) -> dict:
        results = self.model.predict(text)

        # aggregate toxicity score
        toxicity_score = max(results.values())

        return {
            "score": float(toxicity_score),
            "details": results
        }

# singleton instance
predictor = ToxicityPredictor()
