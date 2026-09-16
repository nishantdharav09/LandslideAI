from pathlib import Path
import h5py
import numpy as np
import torch
from unet_model import UNet

TEST_IMAGE = Path(
    r"C:\Users\Nishant Dharav\Downloads\TestData\img\image_101.h5"
)

MODEL_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop\LandslideAI\models\best_unet.pth"
)

STATS_PATH = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop\LandslideAI\models\channel_stats.npz"
)

device = torch.device("cpu")

# Load normalization statistics
stats = np.load(STATS_PATH)

mean = stats["mean"].astype(np.float32)
std = stats["std"].astype(np.float32)

std = np.maximum(std, 1e-6)

mean = mean.reshape(14, 1, 1)
std = std.reshape(14, 1, 1)

# Load model
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

# Load actual input
with h5py.File(TEST_IMAGE, "r") as file:
    image = file["img"][:]

print("INPUT")
print("File:", TEST_IMAGE.name)
print("Shape:", image.shape)

# HWC -> CHW
image = np.transpose(
    image,
    (2, 0, 1)
).astype(np.float32)

# Normalize
image = (image - mean) / std

# Tensor
image_tensor = torch.from_numpy(image).unsqueeze(0)

# Prediction
with torch.no_grad():

    output = model(
        image_tensor.to(device)
    )

    probability = torch.sigmoid(output)

    prediction = (
        probability > 0.5
    ).float()

# Convert to numpy
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

# Calculate area
landslide_pixels = int(
    prediction.sum()
)

total_pixels = prediction.size

predicted_area = (
    landslide_pixels / total_pixels
) * 100

mean_probability = float(
    probability[prediction == 1].mean()
) if landslide_pixels > 0 else 0.0

max_probability = float(
    probability.max()
)

# Risk score
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

# Risk level
if risk_score < 20:
    risk_level = "Low"
elif risk_score < 45:
    risk_level = "Moderate"
elif risk_score < 70:
    risk_level = "High"
else:
    risk_level = "Very High"

print("\nOUTPUT")
print("Predicted Area      :", round(predicted_area, 2), "%")
print("Mean Probability    :", round(mean_probability, 4))
print("Max Probability     :", round(max_probability, 4))
print("Risk Score          :", round(risk_score, 2), "/ 100")
print("Risk Level          :", risk_level)