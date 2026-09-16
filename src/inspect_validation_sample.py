import h5py
import numpy as np


# ============================================================
# VALIDATION SAMPLE
# ============================================================

IMAGE_PATH = (
    r"C:\Users\Nishant Dharav\Downloads"
    r"\ValidData\img\image_1.h5"
)


# ============================================================
# LOAD H5 FILE
# ============================================================

with h5py.File(IMAGE_PATH, "r") as file:

    print("=" * 60)
    print("Validation Sample Inspection")
    print("=" * 60)

    print("\nDataset Keys:")
    print(list(file.keys()))

    for key in file.keys():

        data = file[key]

        print("\n" + "-" * 60)

        print("Key       :", key)
        print("Shape     :", data.shape)
        print("Data Type :", data.dtype)

        array = data[:]

        print("Min Value :", np.min(array))
        print("Max Value :", np.max(array))
        print("Mean      :", np.mean(array))
        print("Std       :", np.std(array))

        print("-" * 60)


print("\n✅ Validation sample inspection completed.")