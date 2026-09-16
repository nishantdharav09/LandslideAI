from pathlib import Path
import re

img_dir = Path(r"C:\Users\Nishant Dharav\Downloads\TrainData\img")
mask_dir = Path(r"C:\Users\Nishant Dharav\Downloads\TrainData\mask")


def get_id(filename):
    match = re.search(r"(\d+)", filename.stem)
    return int(match.group(1)) if match else None


image_ids = {
    get_id(file)
    for file in img_dir.glob("*.h5")
}

mask_ids = {
    get_id(file)
    for file in mask_dir.glob("*.h5")
}

missing_masks = image_ids - mask_ids
missing_images = mask_ids - image_ids

print("Total Images:", len(image_ids))
print("Total Masks:", len(mask_ids))

print("\nMissing Masks:", len(missing_masks))
print("Missing Images:", len(missing_images))

if missing_masks:
    print("\nImage IDs without masks:")
    print(sorted(missing_masks)[:20])

if missing_images:
    print("\nMask IDs without images:")
    print(sorted(missing_images)[:20])

if not missing_masks and not missing_images:
    print("\n✅ ALL IMAGE-MASK PAIRS ARE VALID")
else:
    print("\n⚠️ PAIRING PROBLEM FOUND")