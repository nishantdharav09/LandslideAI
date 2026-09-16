from pathlib import Path

import numpy as np


# ============================================================
# Paths
# ============================================================

PREDICTION_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)


# ============================================================
# Check Directory
# ============================================================

if not PREDICTION_DIR.exists():
    raise FileNotFoundError(
        f"Prediction directory not found:\n{PREDICTION_DIR}"
    )


# ============================================================
# Find Prediction Files
# ============================================================

prediction_files = sorted(
    PREDICTION_DIR.glob("*_prediction.npz")
)


if len(prediction_files) == 0:
    raise RuntimeError(
        "No prediction files found."
    )


print("=" * 60)
print("LandslideAI - Test Prediction Analysis")
print("=" * 60)

print(
    f"Prediction Files Found: "
    f"{len(prediction_files)}"
)


# ============================================================
# Statistics
# ============================================================

areas = []

images_with_landslide = 0

total_predicted_pixels = 0

total_pixels = 0


# ============================================================
# Analyze Every Prediction
# ============================================================

for file_path in prediction_files:

    data = np.load(file_path)

    mask = data["mask"]

    predicted_pixels = int(
        mask.sum()
    )

    pixels = mask.size

    area_percentage = (
        predicted_pixels
        / pixels
    ) * 100

    areas.append(area_percentage)

    total_predicted_pixels += predicted_pixels

    total_pixels += pixels

    if predicted_pixels > 0:
        images_with_landslide += 1


# ============================================================
# Convert to NumPy
# ============================================================

areas = np.array(
    areas,
    dtype=np.float32
)


# ============================================================
# Overall Statistics
# ============================================================

average_area = float(
    areas.mean()
)

minimum_area = float(
    areas.min()
)

maximum_area = float(
    areas.max()
)

median_area = float(
    np.median(areas)
)


# ============================================================
# Risk-style Groups
# ============================================================

low_count = int(
    np.sum(areas < 1)
)

moderate_count = int(
    np.sum(
        (areas >= 1)
        & (areas < 5)
    )
)

high_count = int(
    np.sum(
        (areas >= 5)
        & (areas < 20)
    )
)

very_high_count = int(
    np.sum(areas >= 20)
)


# ============================================================
# Display Results
# ============================================================

print("\n" + "=" * 60)
print("Overall Test Prediction Statistics")
print("=" * 60)

print(
    f"Total Images              : "
    f"{len(prediction_files)}"
)

print(
    f"Images With Prediction    : "
    f"{images_with_landslide}"
)

print(
    f"Average Predicted Area    : "
    f"{average_area:.2f}%"
)

print(
    f"Median Predicted Area     : "
    f"{median_area:.2f}%"
)

print(
    f"Minimum Predicted Area    : "
    f"{minimum_area:.2f}%"
)

print(
    f"Maximum Predicted Area    : "
    f"{maximum_area:.2f}%"
)

print(
    f"Total Predicted Pixels    : "
    f"{total_predicted_pixels}"
)

print(
    f"Total Pixels              : "
    f"{total_pixels}"
)


# ============================================================
# Area Distribution
# ============================================================

print("\n" + "=" * 60)
print("Predicted Area Distribution")
print("=" * 60)

print(
    f"Below 1%                 : "
    f"{low_count}"
)

print(
    f"1% - 5%                  : "
    f"{moderate_count}"
)

print(
    f"5% - 20%                 : "
    f"{high_count}"
)

print(
    f"20% or more              : "
    f"{very_high_count}"
)


# ============================================================
# Top 10 Images
# ============================================================

results = []

for file_path, area in zip(
    prediction_files,
    areas
):

    results.append(
        (
            file_path.name,
            float(area)
        )
    )


results.sort(
    key=lambda x: x[1],
    reverse=True
)


print("\n" + "=" * 60)
print("Top 10 Highest Predicted Areas")
print("=" * 60)

for rank, (filename, area) in enumerate(
    results[:10],
    start=1
):

    print(
        f"{rank:02d}. "
        f"{filename} "
        f"-> {area:.2f}%"
    )


# ============================================================
# Completed
# ============================================================

print("\n" + "=" * 60)
print("✅ Test prediction analysis completed!")
print("=" * 60)