from pathlib import Path

import h5py
import numpy as np
import torch

from unet_model import UNet


# ============================================================
# PATHS
# ============================================================

VALIDATION_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads\ValidData\img"
)

MODEL_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\best_unet.pth"
)

OUTPUT_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\predictions"
)


# ============================================================
# DEVICE
# ============================================================

device = torch.device("cpu")

print("=" * 60)
print("LandslideAI - Validation Prediction")
print("=" * 60)

print("Device:", device)


# ============================================================
# CHECK PATHS
# ============================================================

if not VALIDATION_DIR.exists():
    raise FileNotFoundError(
        f"Validation folder not found:\n{VALIDATION_DIR}"
    )

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained model not found:\n{MODEL_PATH}"
    )


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD MODEL
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

print("✅ Trained U-Net loaded successfully.")


# ============================================================
# FIND VALIDATION IMAGES
# ============================================================

image_files = sorted(
    VALIDATION_DIR.glob("*.h5")
)

print(
    f"Validation Images Found: {len(image_files)}"
)


if len(image_files) == 0:
    raise RuntimeError(
        "No validation H5 files found."
    )


# ============================================================
# PREDICTION
# ============================================================

for index, image_path in enumerate(image_files):

    with h5py.File(
        image_path,
        "r"
    ) as file:

        image = file["img"][:]


    # ----------------------------------------
    # Validate shape
    # ----------------------------------------

    if image.shape != (128, 128, 14):

        raise ValueError(
            f"Unexpected image shape "
            f"{image.shape} in {image_path.name}"
        )


    # ----------------------------------------
    # Convert HWC -> CHW
    # ----------------------------------------

    image = np.transpose(
        image,
        (2, 0, 1)
    )

    image = image.astype(
        np.float32
    )


    # ----------------------------------------
    # Add batch dimension
    # ----------------------------------------

    image_tensor = torch.from_numpy(
        image
    ).unsqueeze(0)


    # ----------------------------------------
    # Prediction
    # ----------------------------------------

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


    # ----------------------------------------
    # Convert prediction to NumPy
    # ----------------------------------------

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


    # ----------------------------------------
    # Save prediction
    # ----------------------------------------

    output_name = (
        image_path.stem
        + "_prediction.npz"
    )

    output_path = (
        OUTPUT_DIR / output_name
    )

    np.savez_compressed(
        output_path,
        mask=prediction,
        probability=probability
    )


    # ----------------------------------------
    # Progress
    # ----------------------------------------

    if (index + 1) % 10 == 0:

        print(
            f"Processed "
            f"[{index + 1}/{len(image_files)}]"
        )


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)

print(
    "Validation prediction completed!"
)

print(
    "Total Images Processed:",
    len(image_files)
)

print(
    "Predictions Saved To:"
)

print(
    OUTPUT_DIR
)

print("=" * 60)