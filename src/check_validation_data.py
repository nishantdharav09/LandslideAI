from pathlib import Path


# ============================================================
# DATASET ROOT
# ============================================================

DATASET_ROOT = Path(
    r"C:\Users\Nishant Dharav\Downloads"
)


# ============================================================
# SPLITS
# ============================================================

splits = {
    "TRAIN": DATASET_ROOT / "TrainData",
    "VALIDATION": DATASET_ROOT / "ValidData",
    "TEST": DATASET_ROOT / "TestData"
}


# ============================================================
# INSPECTION
# ============================================================

print("=" * 70)
print("Landslide4Sense Dataset Structure")
print("=" * 70)


for split_name, split_path in splits.items():

    print("\n" + "-" * 70)
    print(f"{split_name} DATA")
    print("-" * 70)

    print("Path:", split_path)

    if not split_path.exists():

        print("❌ Folder not found")
        continue


    # Show folders
    folders = [
        item
        for item in split_path.iterdir()
        if item.is_dir()
    ]

    print("\nFolders:")

    if folders:

        for folder in folders:
            print("  └──", folder.name)

    else:

        print("  No subfolders found")


    # Count H5 files recursively
    h5_files = list(
        split_path.rglob("*.h5")
    )

    print("\nTotal H5 files:", len(h5_files))


    # Count files inside each subfolder
    for folder in folders:

        files = list(
            folder.glob("*.h5")
        )

        print(
            f"  {folder.name}: {len(files)} H5 files"
        )


    # First few H5 files
    print("\nSample files:")

    for file in sorted(h5_files)[:5]:

        print(
            "  └──",
            file.relative_to(split_path)
        )


print("\n" + "=" * 70)
print("Inspection Completed")
print("=" * 70)