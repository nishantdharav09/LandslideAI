from pathlib import Path

import h5py
import numpy as np
import torch

from unet_model import UNet


# ============================================================
# Paths
# ============================================================

TEST_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads"
    r"\TestData\img"
)

MODEL_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\best_unet.pth"
)

STATS_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\channel_stats.npz"
)

OUTPUT_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)


# ============================================================
# Device
# ============================================================

device = torch.device("cpu")


print("=" * 60)
print("LandslideAI - Test Data Prediction")
print("=" * 60)

print("Device:", device)


# ============================================================
# Check Paths
# ============================================================

if not TEST_DIR.exists():
    raise FileNotFoundError(
        f"Test directory not found:\n{TEST_DIR}"
    )

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )

if not STATS_PATH.exists():
    raise FileNotFoundError(
        f"Normalization statistics not found:\n{STATS_PATH}"
    )


# ============================================================
# Create Output Directory
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Load Normalization Statistics
# ============================================================

stats = np.load(STATS_PATH)

mean = stats["mean"].astype(np.float32)
std = stats["std"].astype(np.float32)

std = np.maximum(
    std,
    1e-6
)

mean = mean.reshape(
    14, 1, 1
)

std = std.reshape(
    14, 1, 1
)

print("✅ Normalization statistics loaded.")


# ============================================================
# Load Model
# ============================================================

model = UNet(
    in_channels=14,
    out_channels=1
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model = model.to(device)

model.eval()

print("✅ Trained U-Net model loaded.")


# ============================================================
# Find Test Images
# ============================================================

image_files = sorted(
    TEST_DIR.glob("*.h5")
)

print(
    f"Test Images Found: {len(image_files)}"
)


if len(image_files) == 0:
    raise RuntimeError(
        "No H5 test images found."
    )


# ============================================================
# Prediction
# ============================================================

for index, image_path in enumerate(image_files):

    # --------------------------------------------------------
    # Load image
    # --------------------------------------------------------

    with h5py.File(
        image_path,
        "r"
    ) as file:

        image = file["img"][:]


    # --------------------------------------------------------
    # Validate shape
    # --------------------------------------------------------

    if image.shape != (
        128,
        128,
        14
    ):

        raise ValueError(
            f"Unexpected image shape: "
            f"{image.shape}"
        )


    # --------------------------------------------------------
    # Convert HWC → CHW
    # --------------------------------------------------------

    image = np.transpose(
        image,
        (2, 0, 1)
    ).astype(np.float32)


    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    image = (
        image - mean
    ) / std


    # --------------------------------------------------------
    # Convert to Tensor
    # --------------------------------------------------------

    image_tensor = torch.from_numpy(
        image
    ).unsqueeze(0)


    # --------------------------------------------------------
    # Model Prediction
    # --------------------------------------------------------

    with torch.no_grad():

        image_tensor = image_tensor.to(
            device
        )

        output = model(
            image_tensor
        )

        probability = torch.sigmoid(
            output
        )

        prediction = (
            probability > 0.5
        ).float()


    # --------------------------------------------------------
    # Convert to NumPy
    # --------------------------------------------------------

    prediction = (
        prediction
        .squeeze()
        .cpu()
        .numpy()
        .astype(np.uint8)
    )

    probability = (
        probability
        .squeeze()
        .cpu()
        .numpy()
    )


    # --------------------------------------------------------
    # Calculate predicted area
    # --------------------------------------------------------

    predicted_pixels = int(
        prediction.sum()
    )

    total_pixels = prediction.size

    predicted_percentage = (
        predicted_pixels
        / total_pixels
    ) * 100


    # --------------------------------------------------------
    # Save prediction
    # --------------------------------------------------------

    output_name = (
        image_path.stem
        + "_prediction.npz"
    )

    output_path = (
        OUTPUT_DIR
        / output_name
    )


    np.savez_compressed(
        output_path,
        mask=prediction,
        probability=probability
    )


    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    if (index + 1) % 50 == 0:

        print(
            f"Processed "
            f"[{index + 1}/{len(image_files)}] "
            f"| Latest predicted area: "
            f"{predicted_percentage:.2f}%"
        )


# ============================================================
# Completed
# ============================================================

print("\n" + "=" * 60)
print("Test Prediction Completed!")
print("=" * 60)

print(
    f"Total Images Processed: "
    f"{len(image_files)}"
)

print(
    "Predictions Saved To:"
)

print(OUTPUT_DIR)

print("=" * 60)