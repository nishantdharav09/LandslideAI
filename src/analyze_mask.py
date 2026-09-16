import h5py
import numpy as np

mask_path = r"C:\Users\Nishant Dharav\Downloads\TrainData\mask\mask_5.h5"

with h5py.File(mask_path, "r") as f:
    mask = f["mask"][:]

print("Mask Shape:", mask.shape)
print("Unique Values:", np.unique(mask))

total_pixels = mask.size
landslide_pixels = np.sum(mask > 0)

percentage = (landslide_pixels / total_pixels) * 100

print("Total Pixels:", total_pixels)
print("Landslide Pixels:", landslide_pixels)
print("Landslide Percentage:", round(percentage, 2), "%")