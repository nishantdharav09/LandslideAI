from pathlib import Path
import csv
import numpy as np

from risk_assessment import calculate_risk


PREDICTION_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)

REPORT_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)

REPORT_PATH = REPORT_DIR / "landslide_risk_report.csv"


def main():

    print("=" * 60)
    print("LandslideAI - Risk Report Generation")
    print("=" * 60)

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

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = []

    for index, prediction_file in enumerate(
        prediction_files
    ):

        data = np.load(prediction_file)

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

        rows.append([
            image_name,
            round(
                result["predicted_area"],
                2
            ),
            round(
                result["mean_probability"],
                4
            ),
            round(
                result["max_probability"],
                4
            ),
            round(
                result["risk_score"],
                2
            ),
            result["risk_level"]
        ])

        if (index + 1) % 100 == 0:

            print(
                f"Processed "
                f"[{index + 1}/"
                f"{len(prediction_files)}]"
            )

    with open(
        REPORT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Image",
            "Predicted_Area_Percent",
            "Mean_Probability",
            "Max_Probability",
            "Risk_Score",
            "Risk_Level"
        ])

        writer.writerows(rows)

    print("\n" + "=" * 60)
    print("Risk Report Saved Successfully")
    print("=" * 60)

    print(
        f"Location:\n{REPORT_PATH}"
    )

    print("=" * 60)
    print("Total Records:", len(rows))
    print("✅ Risk report generation completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()