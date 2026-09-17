"""Lightweight, dependency-free inference layer.

The scoring function is intentionally explicit and replaceable by a trained model
without changing the HTTP contract. Inputs are normalized evidence signals in [0, 1].
"""


def predict(features: dict) -> tuple[float, str]:
    weights = {"geology": 0.45, "geophysics": 0.35, "remote_sensing": 0.20}
    score = sum(features[key] * weight for key, weight in weights.items())
    probability = round(score, 6)
    classification = "high" if probability >= 0.70 else "medium" if probability >= 0.40 else "low"
    return probability, classification
