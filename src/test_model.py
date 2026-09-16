import torch

from unet_model import UNet


# Create model
model = UNet(
    in_channels=14,
    out_channels=1
)

print("U-Net Model Created Successfully!")

# Create dummy input
x = torch.randn(2, 14, 128, 128)

# Forward pass
with torch.no_grad():
    output = model(x)

print("Input Shape :", x.shape)
print("Output Shape:", output.shape)