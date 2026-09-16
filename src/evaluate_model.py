from pathlib import Path

import torch
import numpy as np

from dataloader import val_loader
from unet_model import UNet


# ============================================================
# Paths
# ============================================================

MODEL_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI\models\best_unet.pth"
)


# ============================================================
# Device
# ============================================================

device = torch.device("cpu")


print("=" * 60)
print("LandslideAI - Validation Model Evaluation")
print("=" * 60)
print("Device:", device)


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

print("✅ Trained model loaded successfully.")


# ============================================================
# Metric Variables
# ============================================================

total_intersection = 0
total_union = 0
total_ground_truth = 0
total_prediction = 0

total_true_positive = 0
total_false_positive = 0
total_false_negative = 0

total_images = 0


# ============================================================
# Validation Evaluation
# ============================================================

with torch.no_grad():

    for batch_index, (images, masks) in enumerate(val_loader):

        images = images.to(device)
        masks = masks.to(device)

        # Model prediction
        outputs = model(images)

        probabilities = torch.sigmoid(outputs)

        predictions = (probabilities > 0.5).float()

        # Convert to boolean
        predictions_bool = predictions.bool()
        masks_bool = masks.bool()

        # Pixel statistics
        intersection = (
            predictions_bool & masks_bool
        ).sum().item()

        union = (
            predictions_bool | masks_bool
        ).sum().item()

        ground_truth_pixels = masks_bool.sum().item()
        predicted_pixels = predictions_bool.sum().item()

        # TP / FP / FN
        true_positive = (
            predictions_bool & masks_bool
        ).sum().item()

        false_positive = (
            predictions_bool & ~masks_bool
        ).sum().item()

        false_negative = (
            ~predictions_bool & masks_bool
        ).sum().item()

        total_intersection += intersection
        total_union += union
        total_ground_truth += ground_truth_pixels
        total_prediction += predicted_pixels

        total_true_positive += true_positive
        total_false_positive += false_positive
        total_false_negative += false_negative

        total_images += images.size(0)

        if (batch_index + 1) % 20 == 0:

            print(
                f"Processed "
                f"[{total_images}/760]"
            )


# ============================================================
# Calculate Metrics
# ============================================================

dice = (
    2 * total_intersection
    / (total_ground_truth + total_prediction + 1e-8)
)

iou = (
    total_intersection
    / (total_union + 1e-8)
)

precision = (
    total_true_positive
    / (total_true_positive + total_false_positive + 1e-8)
)

recall = (
    total_true_positive
    / (total_true_positive + total_false_negative + 1e-8)
)


# ============================================================
# Display Results
# ============================================================

print("\n" + "=" * 60)
print("Overall Validation Results")
print("=" * 60)

print(
    f"Validation Images       : {total_images}"
)

print(
    f"Ground Truth Pixels     : {total_ground_truth}"
)

print(
    f"Predicted Pixels        : {total_prediction}"
)

print(
    f"True Positive Pixels    : {total_true_positive}"
)

print(
    f"False Positive Pixels   : {total_false_positive}"
)

print(
    f"False Negative Pixels   : {total_false_negative}"
)

print("\n" + "-" * 60)

print(
    f"Dice Score              : {dice:.4f}"
)

print(
    f"IoU Score               : {iou:.4f}"
)

print(
    f"Precision               : {precision:.4f}"
)

print(
    f"Recall                  : {recall:.4f}"
)

print("-" * 60)

print("\n✅ Overall validation evaluation completed!")

print("=" * 60)