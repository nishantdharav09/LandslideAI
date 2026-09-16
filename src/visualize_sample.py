import h5py
import matplotlib.pyplot as plt
import numpy as np

# Image and mask paths
image_path = r"C:\Users\Nishant Dharav\Downloads\TrainData\img\image_5.h5"
mask_path = r"C:\Users\Nishant Dharav\Downloads\TrainData\mask\mask_5.h5"

# Load image
with h5py.File(image_path, "r") as f:
    image = f["img"][:]

# Load mask
with h5py.File(mask_path, "r") as f:
    mask = f["mask"][:]

print("Image shape:", image.shape)
print("Mask shape:", mask.shape)

# Use first 3 channels for visualization
rgb = image[:, :, :3]

# Normalize RGB for display
rgb = rgb.astype(np.float32)

for i in range(3):
    channel = rgb[:, :, i]
    min_val = channel.min()
    max_val = channel.max()

    if max_val > min_val:
        rgb[:, :, i] = (channel - min_val) / (max_val - min_val)

# Plot
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(rgb)
plt.title("Satellite Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(mask, cmap="gray")
plt.title("Landslide Mask")
plt.axis("off")

plt.tight_layout()
plt.show()