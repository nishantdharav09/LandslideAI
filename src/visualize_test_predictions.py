from pathlib import Path

import h5py
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Paths
# ============================================================

TEST_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads\TestData\img"
)

PREDICTION_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop\LandslideAI\predictions"
)


# ============================================================
# Select Test Image
# ============================================================

IMAGE_NAMES = [
    "image_101.h5"
]


# ============================================================
# Process Images
# ============================================================

for image_name in IMAGE_NAMES:

    image_path = TEST_DIR / image_name

    prediction_path = (
        PREDICTION_DIR
        / f"{Path(image_name).stem}_prediction.npz"
    )

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not image_path.exists():
        print(f"⚠️ Image not found: {image_path}")
        continue

    if not prediction_path.exists():
        print(f"⚠️ Prediction not found: {prediction_path}")
        continue

    # --------------------------------------------------------
    # Load satellite image
    # --------------------------------------------------------

    with h5py.File(image_path, "r") as file:
        image = file["img"][:]

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if image.shape != (128, 128, 14):
        raise ValueError(
            f"Unexpected image shape: {image.shape}"
        )

    # --------------------------------------------------------
    # Load AI prediction
    # --------------------------------------------------------

    data = np.load(prediction_path)

    prediction = data["mask"]
    probability = data["probability"]

    # --------------------------------------------------------
    # Create RGB visualization
    # --------------------------------------------------------

    rgb = image[:, :, :3].astype(np.float32)

    for channel in range(3):

        current = rgb[:, :, channel]

        min_value = current.min()
        max_value = current.max()

        if max_value > min_value:

            rgb[:, :, channel] = (
                current - min_value
            ) / (
                max_value - min_value
            )

    # --------------------------------------------------------
    # Calculate predicted area
    # --------------------------------------------------------

    predicted_pixels = int(
        prediction.sum()
    )

    total_pixels = prediction.size

    predicted_area = (
        predicted_pixels / total_pixels
    ) * 100

    # --------------------------------------------------------
    # Probability values
    # --------------------------------------------------------

    mean_probability = (
        float(
            probability[prediction == 1].mean()
        )
        if predicted_pixels > 0
        else 0.0
    )

    max_probability = float(
        probability.max()
    )

    # --------------------------------------------------------
    # Risk Score
    # --------------------------------------------------------

    area_score = min(
        predicted_area * 1.5,
        60
    )

    confidence_score = (
        mean_probability * 40
    )

    risk_score = min(
        max(
            area_score + confidence_score,
            0
        ),
        100
    )

    # --------------------------------------------------------
    # Risk Level
    # --------------------------------------------------------

    if risk_score < 20:

        risk_level = "Low"

    elif risk_score < 45:

        risk_level = "Moderate"

    elif risk_score < 70:

        risk_level = "High"

    else:

        risk_level = "Very High"

    # --------------------------------------------------------
    # Print result
    # --------------------------------------------------------

    print("=" * 60)
    print("LandslideAI - Visual Prediction")
    print("=" * 60)

    print(f"Input Image        : {image_name}")
    print(f"Input Shape        : {image.shape}")

    print("-" * 60)

    print(
        f"Predicted Area     : "
        f"{predicted_area:.2f}%"
    )

    print(
        f"Mean Probability   : "
        f"{mean_probability:.4f}"
    )

    print(
        f"Max Probability    : "
        f"{max_probability:.4f}"
    )

    print(
        f"Risk Score         : "
        f"{risk_score:.2f}/100"
    )

    print(
        f"Risk Level         : "
        f"{risk_level}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # Create visualization
    # --------------------------------------------------------

    plt.figure(
        figsize=(15, 5)
    )

    # --------------------------------------------------------
    # 1. Satellite Image
    # --------------------------------------------------------

    plt.subplot(1, 3, 1)

    plt.imshow(rgb)

    plt.title(
        f"Satellite Image\n{image_name}"
    )

    plt.axis("off")

    # --------------------------------------------------------
    # 2. AI Landslide Mask
    # --------------------------------------------------------

    plt.subplot(1, 3, 2)

    plt.imshow(
        prediction,
        cmap="gray"
    )

    plt.title(
        f"AI Landslide Mask\n"
        f"Area: {predicted_area:.2f}%"
    )

    plt.axis("off")

    # --------------------------------------------------------
    # 3. Probability Map
    # --------------------------------------------------------

    plt.subplot(1, 3, 3)

    plt.imshow(
        probability,
        cmap="viridis",
        vmin=0,
        vmax=1
    )

    plt.colorbar(
        fraction=0.046,
        pad=0.04
    )

    plt.title(
        f"Prediction Probability\n"
        f"Max: {max_probability:.4f}"
    )

    plt.axis("off")

    # --------------------------------------------------------
    # Final layout
    # --------------------------------------------------------

    plt.tight_layout()

    plt.show()


# ============================================================
# Completed
# ============================================================

print("\n" + "=" * 60)
print("✅ Test visualization completed!")
print("=" * 60)