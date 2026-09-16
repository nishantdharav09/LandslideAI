import h5py
import numpy as np

image_path = r"C:\Users\Nishant Dharav\Downloads\TrainData\img\image_5.h5"

with h5py.File(image_path, "r") as f:
    image = f["img"][:]

print("Image Shape:", image.shape)
print("Number of Channels:", image.shape[2])

print("\nChannel Statistics")
print("-" * 70)

for i in range(image.shape[2]):

    channel = image[:, :, i]

    print(
        f"Channel {i + 1:02d} | "
        f"Min: {channel.min():.4f} | "
        f"Max: {channel.max():.4f} | "
        f"Mean: {channel.mean():.4f} | "
        f"Std: {channel.std():.4f}"
    )