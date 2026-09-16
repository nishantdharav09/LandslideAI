from pathlib import Path

import h5py
import numpy as np


# ============================================================
# PATH
# ============================================================

IMAGE_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads\TrainData\img"
)


# ============================================================
# SETTINGS
# ============================================================

NUM_CHANNELS = 14

channel_sum = np.zeros(NUM_CHANNELS, dtype=np.float64)
channel_squared_sum = np.zeros(NUM_CHANNELS, dtype=np.float64)

total_pixels = 0


# ============================================================
# FIND TRAINING IMAGES
# ============================================================

image_files = sorted(
    IMAGE_DIR.glob("*.h5")
)

print("=" * 60)
print("LandslideAI - Channel Normalization")
print("=" * 60)

print(
    "Training Images:",
    len(image_files)
)

if len(image_files) == 0:
    raise RuntimeError(
        "No training H5 images found."
    )


# ============================================================
# CALCULATE STATISTICS
# ============================================================

for index, image_path in enumerate(image_files):

    with h5py.File(image_path, "r") as file:
        image = file["img"][:]

    if image.shape != (128, 128, 14):
        raise ValueError(
            f"Unexpected shape {image.shape} "
            f"in {image_path.name}"
        )

    image = image.astype(np.float64)

    # H x W x C
    pixels = image.reshape(-1, NUM_CHANNELS)

    channel_sum += pixels.sum(axis=0)

    channel_squared_sum += (
        (pixels ** 2).sum(axis=0)
    )

    total_pixels += pixels.shape[0]

    if (index + 1) % 500 == 0:
        print(
            f"Processed "
            f"[{index + 1}/{len(image_files)}]"
        )


# ============================================================
# MEAN
# ============================================================

mean = channel_sum / total_pixels


# ============================================================
# STANDARD DEVIATION
# ============================================================

variance = (
    channel_squared_sum / total_pixels
) - (mean ** 2)

variance = np.maximum(
    variance,
    0
)

std = np.sqrt(variance)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("Channel Statistics")
print("=" * 60)

for channel in range(NUM_CHANNELS):

    print(
        f"Channel {channel + 1:02d} "
        f"Mean: {mean[channel]:.6f} "
        f"Std: {std[channel]:.6f}"
    )


# ============================================================
# SAVE STATISTICS
# ============================================================

OUTPUT_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\channel_stats.npz"
)

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

np.savez(
    OUTPUT_PATH,
    mean=mean,
    std=std
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("✅ Normalization statistics saved!")
print("=" * 60)

print("Saved To:")
print(OUTPUT_PATH)