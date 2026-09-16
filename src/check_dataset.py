from pathlib import Path

img_dir = Path(r"C:\Users\Nishant Dharav\Downloads\TrainData\img")
mask_dir = Path(r"C:\Users\Nishant Dharav\Downloads\TrainData\mask")

images = sorted(img_dir.glob("*.h5"))
masks = sorted(mask_dir.glob("*.h5"))

print("Total Images:", len(images))
print("Total Masks:", len(masks))

print("\nFirst 5 Images:")
for file in images[:5]:
    print(file.name)

print("\nFirst 5 Masks:")
for file in masks[:5]:
    print(file.name)