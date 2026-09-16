from pathlib import Path
import numpy as np


# ============================================================
# PATH
# ============================================================

PREDICTION_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)


# ============================================================
# CHECK FOLDER
# ============================================================

if not PREDICTION_DIR.exists():
    raise FileNotFoundError(
        f"Prediction folder not found:\n{PREDICTION_DIR}"
    )


# ============================================================
# FIND PREDICTIONS
# ============================================================

prediction_files = sorted(
    PREDICTION_DIR.glob("*_prediction.npz")
)


print("=" * 60)
print("LandslideAI - Prediction File Check")
print("=" * 60)

print(
    "Prediction Files:",
    len(prediction_files)
)


# ============================================================
# CHECK FILES
# ============================================================

if len(prediction_files) == 0:
    raise RuntimeError(
        "No prediction files found."
    )


for file_path in prediction_files[:5]:

    data = np.load(file_path)

    mask = data["mask"]
    probability = data["probability"]

    print("\n" + "-" * 60)

    print("File:", file_path.name)

    print("Mask Shape:", mask.shape)
    print("Mask Data Type:", mask.dtype)

    print(
        "Mask Unique Values:",
        np.unique(mask)
    )

    print(
        "Probability Shape:",
        probability.shape
    )

    print(
        "Probability Min:",
        float(probability.min())
    )

    print(
        "Probability Max:",
        float(probability.max())
    )

    print(
        "Predicted Landslide Pixels:",
        int(mask.sum())
    )


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("Prediction files checked successfully!")
print("=" * 60)