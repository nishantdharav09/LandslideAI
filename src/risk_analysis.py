from pathlib import Path
import numpy as np

from risk_assessment import calculate_risk


# ============================================================
# LandslideAI - Complete Risk Analysis
# ============================================================

PREDICTION_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)


def main():

    print("=" * 60)
    print("LandslideAI - Complete Risk Analysis")
    print("=" * 60)

    # --------------------------------------------------------
    # Find prediction files
    # --------------------------------------------------------

    prediction_files = sorted(
        PREDICTION_DIR.glob("*_prediction.npz")
    )

    print(
        f"Prediction Files Found: "
        f"{len(prediction_files)}"
    )

    if len(prediction_files) == 0:
        raise RuntimeError(
            "No prediction files found."
        )

    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    results = []

    # --------------------------------------------------------
    # Analyze all predictions
    # --------------------------------------------------------

    for index, prediction_file in enumerate(
        prediction_files
    ):

        data = np.load(
            prediction_file
        )

        prediction_mask = data["mask"]

        probability_map = data["probability"]

        result = calculate_risk(
            prediction_mask,
            probability_map
        )

        image_name = prediction_file.stem.replace(
            "_prediction",
            ""
        )

        results.append(
            {
                "image": image_name,
                "area": result["predicted_area"],
                "probability": result[
                    "mean_probability"
                ],
                "risk_score": result[
                    "risk_score"
                ],
                "risk_level": result[
                    "risk_level"
                ]
            }
        )

        # Progress
        if (index + 1) % 100 == 0:

            print(
                f"Processed "
                f"[{index + 1}/"
                f"{len(prediction_files)}]"
            )

    # --------------------------------------------------------
    # Count risk levels
    # --------------------------------------------------------

    low_count = 0
    moderate_count = 0
    high_count = 0
    very_high_count = 0

    for result in results:

        if result["risk_level"] == "Low":
            low_count += 1

        elif result["risk_level"] == "Moderate":
            moderate_count += 1

        elif result["risk_level"] == "High":
            high_count += 1

        elif result["risk_level"] == "Very High":
            very_high_count += 1

    # --------------------------------------------------------
    # Sort by risk score
    # --------------------------------------------------------

    results.sort(
        key=lambda item: item["risk_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Risk Summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Risk Level Summary")
    print("=" * 60)

    print(
        f"Low          : {low_count}"
    )

    print(
        f"Moderate     : {moderate_count}"
    )

    print(
        f"High         : {high_count}"
    )

    print(
        f"Very High    : {very_high_count}"
    )

    # --------------------------------------------------------
    # Top 10
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Top 10 Highest Preliminary Risk Predictions")
    print("=" * 60)

    for index, result in enumerate(
        results[:10],
        start=1
    ):

        print(
            f"{index:02d}. "
            f"{result['image']} | "
            f"Area: "
            f"{result['area']:.2f}% | "
            f"Score: "
            f"{result['risk_score']:.2f}/100 | "
            f"Risk: "
            f"{result['risk_level']}"
        )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    areas = np.array(
        [
            result["area"]
            for result in results
        ]
    )

    scores = np.array(
        [
            result["risk_score"]
            for result in results
        ]
    )

    probabilities = np.array(
        [
            result["probability"]
            for result in results
        ]
    )

    print("\n" + "=" * 60)
    print("Overall Statistics")
    print("=" * 60)

    print(
        f"Total Images Analyzed : "
        f"{len(results)}"
    )

    print(
        f"Average Predicted Area : "
        f"{areas.mean():.2f}%"
    )

    print(
        f"Median Predicted Area  : "
        f"{np.median(areas):.2f}%"
    )

    print(
        f"Maximum Predicted Area : "
        f"{areas.max():.2f}%"
    )

    print(
        f"Average Probability    : "
        f"{probabilities.mean():.4f}"
    )

    print(
        f"Average Risk Score     : "
        f"{scores.mean():.2f}/100"
    )

    print(
        f"Maximum Risk Score     : "
        f"{scores.max():.2f}/100"
    )

    print("=" * 60)
    print("✅ Complete risk analysis finished!")
    print("=" * 60)


# ============================================================
# Run Program
# ============================================================

if __name__ == "__main__":
    main()