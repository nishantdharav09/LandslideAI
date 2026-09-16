from pathlib import Path
import re

import h5py
import numpy as np
import torch
from torch.utils.data import Dataset


class LandslideDataset(Dataset):

    def __init__(
        self,
        image_dir,
        mask_dir,
        stats_path=None
    ):

        self.image_dir = Path(image_dir)
        self.mask_dir = Path(mask_dir)

        self.samples = self._build_pairs()

        if len(self.samples) == 0:
            raise RuntimeError(
                "No valid image-mask pairs found."
            )

        # Load normalization statistics
        self.mean = None
        self.std = None

        if stats_path is not None:

            stats_path = Path(stats_path)

            if not stats_path.exists():
                raise FileNotFoundError(
                    f"Normalization statistics not found:\n"
                    f"{stats_path}"
                )

            stats = np.load(stats_path)

            self.mean = stats["mean"].astype(
                np.float32
            )

            self.std = stats["std"].astype(
                np.float32
            )

            self.std = np.maximum(
                self.std,
                1e-6
            )

            print(
                "✅ Channel normalization loaded."
            )

        print(
            f"Loaded {len(self.samples)} "
            f"image-mask pairs."
        )


    def _get_id(self, filename):

        match = re.search(
            r"(\d+)",
            filename.stem
        )

        if match is None:
            return None

        return int(match.group(1))


    def _build_pairs(self):

        image_files = list(
            self.image_dir.glob("*.h5")
        )

        mask_files = list(
            self.mask_dir.glob("*.h5")
        )

        image_map = {
            self._get_id(file): file
            for file in image_files
            if self._get_id(file) is not None
        }

        mask_map = {
            self._get_id(file): file
            for file in mask_files
            if self._get_id(file) is not None
        }

        common_ids = sorted(
            set(image_map.keys())
            &
            set(mask_map.keys())
        )

        samples = [
            (
                image_map[sample_id],
                mask_map[sample_id]
            )
            for sample_id in common_ids
        ]

        return samples


    def __len__(self):

        return len(self.samples)


    def __getitem__(self, index):

        image_path, mask_path = (
            self.samples[index]
        )

        # Load image
        with h5py.File(
            image_path,
            "r"
        ) as file:

            image = file["img"][:]

        # Load mask
        with h5py.File(
            mask_path,
            "r"
        ) as file:

            mask = file["mask"][:]

        # Validate image shape
        if image.shape != (
            128,
            128,
            14
        ):

            raise ValueError(
                f"Unexpected image shape: "
                f"{image.shape}"
            )

        # H, W, C -> C, H, W
        image = np.transpose(
            image,
            (2, 0, 1)
        )

        image = image.astype(
            np.float32
        )

        # Normalize 14 channels
        if self.mean is not None:

            mean = self.mean.reshape(
                14,
                1,
                1
            )

            std = self.std.reshape(
                14,
                1,
                1
            )

            image = (
                image - mean
            ) / std

        # Mask
        mask = mask.astype(
            np.float32
        )

        # Convert to tensors
        image = torch.from_numpy(
            image
        )

        mask = torch.from_numpy(
            mask
        )

        # H, W -> 1, H, W
        mask = mask.unsqueeze(0)

        return image, mask