import h5py
import numpy as np
import torch
import matplotlib.pyplot as plt

from unet_model import UNet


# ============================================================
# PATHS
# ============================================================

IMAGE_PATH = (
    r"C:\Users\Nishant Dharav\Downloads"
    r"\TrainData\img\image_5.h5"
)

MASK_PATH = (
    r"C:\Users\Nishant Dharav\Downloads"
    r"\TrainData\mask\mask_5.h5"
)

MODEL_PATH = (
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\best_unet.pth"
)

STATS_PATH = (
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\channel_stats.npz"
)


# ============================================================
# DEVICE
# ============================================================

device = torch.device("cpu")

print("=" * 60)
print("LandslideAI - Normalized Prediction Test")
print("=" * 60)

print("Device:", device)


# ============================================================
# LOAD NORMALIZATION STATISTICS
# ============================================================

stats = np.load(STATS_PATH)

mean = stats["mean"].astype(np.float32)
std = stats["std"].astype(np.float32)

std = np.maximum(std, 1e-6)

print("✅ Channel normalization statistics loaded.")


# ============================================================
# LOAD IMAGE
# ============================================================

with h5py.File(
    IMAGE_PATH,
    "r"
) as file:

    image = file["img"][:]


# ============================================================
# LOAD GROUND TRUTH MASK
# ============================================================

with h5py.File(
    MASK_PATH,
    "r"
) as file:

    mask = file["mask"][:]


print(
    "Original Image Shape:",
    image.shape
)

print(
    "Original Mask Shape :",
    mask.shape
)


# ============================================================
# PREPARE IMAGE
# ============================================================

# H, W, C -> C, H, W

image = np.transpose(
    image,
    (2, 0, 1)
).astype(np.float32)


# ============================================================
# NORMALIZE IMAGE
# ============================================================

mean = mean.reshape(
    14,
    1,
    1
)

std = std.reshape(
    14,
    1,
    1
)

normalized_image = (
    image - mean
) / std


print(
    "Normalized Mean:",
    normalized_image.mean()
)

print(
    "Normalized Std :",
    normalized_image.std()
)


# ============================================================
# CREATE MODEL INPUT
# ============================================================

image_tensor = torch.from_numpy(
    normalized_image
).unsqueeze(0)


print(
    "Model Input Shape:",
    image_tensor.shape
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

print(
    "✅ Trained normalized model loaded successfully!"
)


# ============================================================
# PREDICTION
# ============================================================

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


# ============================================================
# CONVERT TO NUMPY
# ============================================================

prediction = (
    prediction
    .squeeze()
    .cpu()
    .numpy()
)

probability = (
    probability
    .squeeze()
    .cpu()
    .numpy()
)


# ============================================================
# CREATE MASKS
# ============================================================

ground_truth = (
    mask > 0
).astype(np.uint8)

predicted_mask = (
    prediction > 0
).astype(np.uint8)


# ============================================================
# METRICS
# ============================================================

intersection = np.logical_and(
    ground_truth,
    predicted_mask
).sum()

union = np.logical_or(
    ground_truth,
    predicted_mask
).sum()

ground_truth_pixels = (
    ground_truth.sum()
)

predicted_pixels = (
    predicted_mask.sum()
)


# ============================================================
# DICE
# ============================================================

dice = (
    2 * intersection
    /
    (
        ground_truth_pixels
        + predicted_pixels
        + 1e-8
    )
)


# ============================================================
# IOU
# ============================================================

iou = (
    intersection
    /
    (
        union
        + 1e-8
    )
)


# ============================================================
# PRECISION
# ============================================================

precision = (
    intersection
    /
    (
        predicted_pixels
        + 1e-8
    )
)


# ============================================================
# RECALL
# ============================================================

recall = (
    intersection
    /
    (
        ground_truth_pixels
        + 1e-8
    )
)


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 60)

print("Prediction Results")

print("=" * 60)

print(
    f"Ground Truth Landslide Pixels : "
    f"{ground_truth_pixels}"
)

print(
    f"Predicted Landslide Pixels    : "
    f"{predicted_pixels}"
)

print(
    f"Dice Score                    : "
    f"{dice:.4f}"
)

print(
    f"IoU Score                     : "
    f"{iou:.4f}"
)

print(
    f"Precision                     : "
    f"{precision:.4f}"
)

print(
    f"Recall                        : "
    f"{recall:.4f}"
)

print(
    f"Maximum Probability           : "
    f"{probability.max():.4f}"
)

print("=" * 60)


# ============================================================
# RGB DISPLAY IMAGE
# ============================================================

rgb = image[:3]

rgb = np.transpose(
    rgb,
    (1, 2, 0)
).astype(np.float32)


# Normalize only for visualization

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


# ============================================================
# VISUALIZATION
# ============================================================

plt.figure(
    figsize=(15, 5)
)


plt.subplot(
    1,
    3,
    1
)

plt.imshow(rgb)

plt.title(
    "Satellite Image"
)

plt.axis("off")


plt.subplot(
    1,
    3,
    2
)

plt.imshow(
    ground_truth,
    cmap="gray"
)

plt.title(
    "Ground Truth"
)

plt.axis("off")


plt.subplot(
    1,
    3,
    3
)

plt.imshow(
    predicted_mask,
    cmap="gray"
)

plt.title(
    "AI Prediction"
)

plt.axis("off")


plt.tight_layout()

plt.show()