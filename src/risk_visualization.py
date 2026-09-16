from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from risk_assessment import calculate_risk


# ============================================================
# Paths
# ============================================================

PREDICTION_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)

SCREENSHOT_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\screenshots"
)


# ============================================================
# Main Function
# ============================================================

def main():

    # --------------------------------------------------------
    # Find prediction files
    # --------------------------------------------------------

    prediction_files = sorted(
        PREDICTION_DIR.glob("*_prediction.npz")
    )

    print("=" * 60)
    print("LandslideAI - Risk Distribution")
    print("=" * 60)

    print(
        f"Prediction Files Found: "
        f"{len(prediction_files)}"
    )

    if len(prediction_files) == 0:

        raise RuntimeError(
            "No prediction files found."
        )

    # --------------------------------------------------------
    # Risk counters
    # --------------------------------------------------------

    low = 0
    moderate = 0
    high = 0
    very_high = 0

    # --------------------------------------------------------
    # Analyze all predictions
    # --------------------------------------------------------

    for prediction_file in prediction_files:

        data = np.load(
            prediction_file
        )

        prediction_mask = data["mask"]

        probability_map = data["probability"]

        result = calculate_risk(
            prediction_mask,
            probability_map
        )

        risk_level = result["risk_level"]

        if risk_level == "Low":

            low += 1

        elif risk_level == "Moderate":

            moderate += 1

        elif risk_level == "High":

            high += 1

        elif risk_level == "Very High":

            very_high += 1

    # --------------------------------------------------------
    # Print risk summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Risk Level Summary")
    print("=" * 60)

    print(
        f"Low        : {low}"
    )

    print(
        f"Moderate   : {moderate}"
    )

    print(
        f"High       : {high}"
    )

    print(
        f"Very High  : {very_high}"
    )

    # --------------------------------------------------------
    # Chart data
    # --------------------------------------------------------

    labels = [
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]

    values = [
        low,
        moderate,
        high,
        very_high
    ]

    # --------------------------------------------------------
    # Create chart
    # --------------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    bars = plt.bar(
        labels,
        values
    )

    plt.title(
        "LandslideAI - Risk Distribution",
        fontsize=16
    )

    plt.xlabel(
        "Risk Level",
        fontsize=12
    )

    plt.ylabel(
        "Number of Test Images",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    # --------------------------------------------------------
    # Add values above bars
    # --------------------------------------------------------

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=11
        )

    # --------------------------------------------------------
    # Save chart
    # --------------------------------------------------------

    SCREENSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    chart_path = (
        SCREENSHOT_DIR
        / "risk_distribution.png"
    )

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    print("\n" + "=" * 60)
    print("Chart Saved Successfully")
    print("=" * 60)

    print(
        f"Location:\n{chart_path}"
    )

    # --------------------------------------------------------
    # Show chart
    # --------------------------------------------------------

    plt.show()

    print("\n" + "=" * 60)
    print(
        "✅ Risk visualization completed!"
    )
    print("=" * 60)


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    main()