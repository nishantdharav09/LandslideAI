from pathlib import Path

from dataset import LandslideDataset


# ============================================================
# PATHS
# ============================================================

IMAGE_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads\TrainData\img"
)

MASK_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads\TrainData\mask"
)

STATS_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\channel_stats.npz"
)


# ============================================================
# CREATE DATASET
# ============================================================

dataset = LandslideDataset(
    image_dir=IMAGE_DIR,
    mask_dir=MASK_DIR,
    stats_path=STATS_PATH
)


# ============================================================
# LOAD ONE SAMPLE
# ============================================================

image, mask = dataset[0]


# ============================================================
# DISPLAY BASIC INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("Normalized Dataset Test")
print("=" * 60)

print(
    "Dataset Length:",
    len(dataset)
)

print(
    "Image Shape:",
    image.shape
)

print(
    "Image Data Type:",
    image.dtype
)

print(
    "Mask Shape:",
    mask.shape
)

print(
    "Mask Data Type:",
    mask.dtype
)


# ============================================================
# NORMALIZATION CHECK
# ============================================================

print("\n" + "=" * 60)
print("Normalization Check")
print("=" * 60)

for channel in range(14):

    channel_data = image[channel]

    mean_value = channel_data.mean().item()
    std_value = channel_data.std().item()

    print(
        f"Channel {channel + 1:02d} "
        f"Mean: {mean_value:.4f} "
        f"Std: {std_value:.4f}"
    )


print("\n" + "=" * 60)
print("✅ Normalization test completed!")
print("=" * 60)