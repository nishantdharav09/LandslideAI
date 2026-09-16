from pathlib import Path
import numpy as np


def calculate_risk(prediction_mask, probability_map):

    if prediction_mask.shape != probability_map.shape:
        raise ValueError(
            "Prediction mask and probability map "
            "must have the same shape."
        )

    total_pixels = prediction_mask.size

    landslide_pixels = int(
        prediction_mask.sum()
    )

    predicted_area = (
        landslide_pixels / total_pixels
    ) * 100

    predicted_probabilities = probability_map[
        prediction_mask == 1
    ]

    if predicted_probabilities.size > 0:
        mean_probability = float(
            predicted_probabilities.mean()
        )
    else:
        mean_probability = 0.0

    max_probability = float(
        probability_map.max()
    )

    # Area contribution
    area_score = min(
        predicted_area * 1.5,
        60
    )

    # Model confidence contribution
    confidence_score = (
        mean_probability * 40
    )

    risk_score = (
        area_score + confidence_score
    )

    risk_score = min(
        max(risk_score, 0),
        100
    )

    if risk_score < 20:
        risk_level = "Low"

    elif risk_score < 45:
        risk_level = "Moderate"

    elif risk_score < 70:
        risk_level = "High"

    else:
        risk_level = "Very High"

    return {
        "predicted_area": predicted_area,
        "mean_probability": mean_probability,
        "max_probability": max_probability,
        "risk_score": risk_score,
        "risk_level": risk_level
    }


if __name__ == "__main__":

    prediction_path = Path(
        r"C:\Users\Nishant Dharav\OneDrive\Desktop"
        r"\LandslideAI\predictions"
        r"\image_101_prediction.npz"
    )

    if not prediction_path.exists():
        raise FileNotFoundError(
            f"Prediction file not found:\n"
            f"{prediction_path}"
        )

    data = np.load(
        prediction_path
    )

    prediction_mask = data["mask"]

    probability_map = data["probability"]

    result = calculate_risk(
        prediction_mask,
        probability_map
    )

    print("=" * 60)
    print("LandslideAI - Risk Assessment")
    print("=" * 60)

    print(
        f"Predicted Landslide Area : "
        f"{result['predicted_area']:.2f}%"
    )

    print(
        f"Mean Prediction Probability : "
        f"{result['mean_probability']:.4f}"
    )

    print(
        f"Maximum Prediction Probability : "
        f"{result['max_probability']:.4f}"
    )

    print(
        f"Preliminary Risk Score : "
        f"{result['risk_score']:.2f}/100"
    )

    print(
        f"Preliminary Risk Level : "
        f"{result['risk_level']}"
    )

    print("=" * 60)