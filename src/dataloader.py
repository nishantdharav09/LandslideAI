from pathlib import Path

import torch
from torch.utils.data import DataLoader, random_split

from dataset import LandslideDataset


# ============================================================
# Paths
# ============================================================

IMAGE_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads"
    r"\TrainData\img"
)

MASK_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads"
    r"\TrainData\mask"
)

STATS_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\channel_stats.npz"
)


# ============================================================
# Load Dataset
# ============================================================

dataset = LandslideDataset(
    image_dir=IMAGE_DIR,
    mask_dir=MASK_DIR,
    stats_path=STATS_PATH
)


# ============================================================
# Train / Validation Split
# ============================================================

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

# Fixed seed makes the split reproducible
split_generator = torch.Generator().manual_seed(42)

train_dataset, val_dataset = random_split(
    dataset,
    [train_size, val_size],
    generator=split_generator
)


# ============================================================
# DataLoaders
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=8,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=8,
    shuffle=False,
    num_workers=0
)


# ============================================================
# Information
# ============================================================

print("=" * 60)
print("LandslideAI DataLoader")
print("=" * 60)

print("Total Dataset:", len(dataset))
print("Training Samples:", len(train_dataset))
print("Validation Samples:", len(val_dataset))

print("\nValidation split seed: 42")


# ============================================================
# Batch Test
# ============================================================

images, masks = next(iter(train_loader))

print("\n" + "=" * 60)
print("Batch Test")
print("=" * 60)

print("Images Shape:", images.shape)
print("Masks Shape:", masks.shape)

print("Images Data Type:", images.dtype)
print("Masks Data Type:", masks.dtype)

print("Batch Mean:", images.mean().item())
print("Batch Std:", images.std().item())

print("=" * 60)
