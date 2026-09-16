from pathlib import Path
import io
import re
import uuid

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.unet_model import UNet


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="LandslideAI API",
    description="AI-Based Landslide Risk Monitoring System",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

RISK_REPORT_PATH = (
    BASE_DIR
    / "predictions"
    / "landslide_risk_report.csv"
)

TEST_IMAGE_DIR = Path(
    r"C:\Users\Nishant Dharav\Downloads\TestData\img"
)

PREDICTION_DIR = (
    BASE_DIR
    / "predictions"
)

VISUALIZATION_DIR = (
    PREDICTION_DIR
    / "visualizations"
)

VISUALIZATION_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# MODEL
# =========================================================

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "best_unet.pth"
)

STATS_PATH = (
    BASE_DIR
    / "models"
    / "channel_stats.npz"
)

DEVICE = torch.device(
    "cpu"
)


# =========================================================
# CURRENT USER UPLOAD MEMORY
# =========================================================

UPLOAD_PREDICTIONS = {}


# =========================================================
# NORMALIZATION
# =========================================================

stats = np.load(
    STATS_PATH
)

MEAN = stats[
    "mean"
].astype(
    np.float32
)

STD = stats[
    "std"
].astype(
    np.float32
)

STD = np.maximum(
    STD,
    1e-6
)

MEAN = MEAN.reshape(
    14,
    1,
    1
)

STD = STD.reshape(
    14,
    1,
    1
)


# =========================================================
# LOAD U-NET
# =========================================================

MODEL = UNet(
    in_channels=14,
    out_channels=1
)

MODEL.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)

MODEL = MODEL.to(
    DEVICE
)

MODEL.eval()


# =========================================================
# RISK CALCULATION
# =========================================================

def calculate_risk(
    prediction_mask,
    probability_map
):

    if (
        prediction_mask.shape
        != probability_map.shape
    ):
        raise ValueError(
            "Prediction mask and probability map "
            "must have the same shape."
        )

    total_pixels = (
        prediction_mask.size
    )

    landslide_pixels = int(
        prediction_mask.sum()
    )

    predicted_area = (
        landslide_pixels
        / total_pixels
    ) * 100

    predicted_probabilities = (
        probability_map[
            prediction_mask == 1
        ]
    )

    if (
        predicted_probabilities.size
        > 0
    ):
        mean_probability = float(
            predicted_probabilities.mean()
        )
    else:
        mean_probability = 0.0

    max_probability = float(
        probability_map.max()
    )

    area_score = min(
        predicted_area * 1.5,
        60
    )

    confidence_score = (
        mean_probability * 40
    )

    risk_score = (
        area_score
        + confidence_score
    )

    risk_score = min(
        max(risk_score, 0),
        100
    )

    if risk_score < 20:
        risk_level = "Low"

    elif risk_score < 45:
        risk_level = "Moderate"

    elif risk_score < 70:
        risk_level = "High"

    else:
        risk_level = "Very High"

    return {
        "predicted_area_percent":
            round(
                predicted_area,
                2
            ),

        "mean_probability":
            round(
                mean_probability,
                4
            ),

        "max_probability":
            round(
                max_probability,
                4
            ),

        "risk_score":
            round(
                risk_score,
                2
            ),

        "risk_level":
            risk_level
    }


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "system": "LandslideAI",
        "status": "online",
        "message":
            "LandslideAI API is running"
    }


# =========================================================
# STATUS
# =========================================================

@app.get("/api/status")
def system_status():
    return {
        "status": "online",
        "model": "U-Net",
        "input_channels": 14,
        "dataset_predictions": 800,
        "risk_engine": "Active"
    }


# =========================================================
# RISK SUMMARY
# =========================================================

@app.get("/api/risk-summary")
def risk_summary():

    if not RISK_REPORT_PATH.exists():
        return {
            "total_images": 0,
            "low": 0,
            "moderate": 0,
            "high": 0,
            "very_high": 0,
            "average_risk_score": 0,
            "maximum_risk_score": 0
        }

    try:

        df = pd.read_csv(
            RISK_REPORT_PATH
        )

        total = len(df)

        low = int(
            (
                df["Risk_Level"]
                == "Low"
            ).sum()
        )

        moderate = int(
            (
                df["Risk_Level"]
                == "Moderate"
            ).sum()
        )

        high = int(
            (
                df["Risk_Level"]
                == "High"
            ).sum()
        )

        very_high = int(
            (
                df["Risk_Level"]
                == "Very High"
            ).sum()
        )

        average_risk_score = float(
            df["Risk_Score"].mean()
        )

        maximum_risk_score = float(
            df["Risk_Score"].max()
        )

        return {
            "total_images":
                total,

            "low":
                low,

            "moderate":
                moderate,

            "high":
                high,

            "very_high":
                very_high,

            "average_risk_score":
                round(
                    average_risk_score,
                    2
                ),

            "maximum_risk_score":
                round(
                    maximum_risk_score,
                    2
                )
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# TOP RISK
# =========================================================

@app.get("/api/top-risk")
def top_risk(
    limit: int = 10
):

    if not RISK_REPORT_PATH.exists():
        return {
            "status": "error",
            "message":
                "Risk report file not found",
            "data": []
        }

    try:

        df = pd.read_csv(
            RISK_REPORT_PATH
        )

        df = df.sort_values(
            by="Risk_Score",
            ascending=False
        )

        df = df.head(
            limit
        )

        records = []

        for _, row in df.iterrows():

            records.append(
                {
                    "image":
                        str(
                            row["Image"]
                        ),

                    "predicted_area_percent":
                        round(
                            float(
                                row[
                                    "Predicted_Area_Percent"
                                ]
                            ),
                            2
                        ),

                    "mean_probability":
                        round(
                            float(
                                row[
                                    "Mean_Probability"
                                ]
                            ),
                            4
                        ),

                    "max_probability":
                        round(
                            float(
                                row[
                                    "Max_Probability"
                                ]
                            ),
                            4
                        ),

                    "risk_score":
                        round(
                            float(
                                row[
                                    "Risk_Score"
                                ]
                            ),
                            2
                        ),

                    "risk_level":
                        str(
                            row[
                                "Risk_Level"
                            ]
                        )
                }
            )

        return {
            "status":
                "success",

            "count":
                len(records),

            "data":
                records
        }

    except Exception as error:

        return {
            "status":
                "error",

            "message":
                str(error),

            "data":
                []
        }


# =========================================================
# USER UPLOAD PREDICTION
# =========================================================

@app.post("/api/predict")
async def predict_uploaded_image(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(
        ".h5"
    ):
        return {
            "status":
                "error",

            "message":
                "Only .h5 files are supported."
        }

    try:

        # -------------------------------------------------
        # READ H5
        # -------------------------------------------------

        with h5py.File(
            file.file,
            "r"
        ) as h5_file:

            if "img" not in h5_file:
                return {
                    "status":
                        "error",

                    "message":
                        (
                            "H5 file does not contain "
                            "'img' dataset."
                        )
                }

            original_hwc = h5_file[
                "img"
            ][:]

        # -------------------------------------------------
        # SHAPE
        # -------------------------------------------------

        if original_hwc.shape != (
            128,
            128,
            14
        ):
            return {
                "status":
                    "error",

                "message":
                    (
                        "Invalid image shape. "
                        "Expected (128, 128, 14), "
                        f"received {original_hwc.shape}."
                    )
            }

        # -------------------------------------------------
        # COPY ORIGINAL IMAGE
        # -------------------------------------------------

        original_hwc = (
            original_hwc
            .astype(
                np.float32
            )
        )

        # -------------------------------------------------
        # HWC -> CHW
        # -------------------------------------------------

        image = np.transpose(
            original_hwc,
            (2, 0, 1)
        ).astype(
            np.float32
        )

        # -------------------------------------------------
        # NORMALIZE
        # -------------------------------------------------

        image = (
            image - MEAN
        ) / STD

        # -------------------------------------------------
        # TENSOR
        # -------------------------------------------------

        image_tensor = (
            torch.from_numpy(
                image
            )
            .unsqueeze(0)
            .to(DEVICE)
        )

        # -------------------------------------------------
        # MODEL
        # -------------------------------------------------

        with torch.no_grad():

            output = MODEL(
                image_tensor
            )

            probability_tensor = (
                torch.sigmoid(
                    output
                )
            )

            prediction_tensor = (
                probability_tensor > 0.5
            ).float()

        # -------------------------------------------------
        # NUMPY
        # -------------------------------------------------

        prediction = (
            prediction_tensor
            .squeeze()
            .cpu()
            .numpy()
            .astype(
                np.uint8
            )
        )

        probability = (
            probability_tensor
            .squeeze()
            .cpu()
            .numpy()
        )

        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        result = calculate_risk(
            prediction,
            probability
        )

        # -------------------------------------------------
        # ID
        # -------------------------------------------------

        prediction_id = (
            uuid.uuid4().hex
        )

        # -------------------------------------------------
        # STORE CURRENT UPLOAD
        # -------------------------------------------------

        UPLOAD_PREDICTIONS[
            prediction_id
        ] = {
            "image":
                original_hwc,

            "mask":
                prediction,

            "probability":
                probability,

            "result":
                result,

            "filename":
                file.filename,
        }

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {
            "status":
                "success",

            "filename":
                file.filename,

            "input_shape":
                [
                    128,
                    128,
                    14
                ],

            "prediction_id":
                prediction_id,

            "prediction":
                result
        }

    except Exception as error:

        return {
            "status":
                "error",

            "message":
                str(error)
        }


# =========================================================
# CURRENT UPLOADED IMAGE VISUALIZATION
# =========================================================

@app.get(
    "/api/upload-prediction/{prediction_id}/visualization"
)
def uploaded_prediction_visualization(
    prediction_id: str
):

    if (
        prediction_id
        not in UPLOAD_PREDICTIONS
    ):
        return {
            "status":
                "error",

            "message":
                "Uploaded prediction not found"
        }

    try:

        item = (
            UPLOAD_PREDICTIONS[
                prediction_id
            ]
        )

        image = item[
            "image"
        ]

        mask = item[
            "mask"
        ]

        probability = item[
            "probability"
        ]

        # -------------------------------------------------
        # RGB
        # -------------------------------------------------

        rgb = image[
            :, :, :3
        ].astype(
            np.float32
        )

        for channel in range(3):

            channel_data = rgb[
                :, :, channel
            ]

            min_value = (
                channel_data.min()
            )

            max_value = (
                channel_data.max()
            )

            if (
                max_value
                > min_value
            ):

                rgb[
                    :, :, channel
                ] = (
                    (
                        channel_data
                        - min_value
                    )
                    /
                    (
                        max_value
                        - min_value
                    )
                )

            else:

                rgb[
                    :, :, channel
                ] = 0.0

        # -------------------------------------------------
        # FIGURE
        # -------------------------------------------------

        figure = plt.figure(
            figsize=(15, 5)
        )

        # Satellite

        plt.subplot(
            1,
            3,
            1
        )

        plt.imshow(
            rgb
        )

        plt.title(
            "Satellite Image"
        )

        plt.axis(
            "off"
        )

        # Mask

        plt.subplot(
            1,
            3,
            2
        )

        plt.imshow(
            mask,
            cmap="gray"
        )

        plt.title(
            "AI Landslide Mask"
        )

        plt.axis(
            "off"
        )

        # Probability

        plt.subplot(
            1,
            3,
            3
        )

        plt.imshow(
            probability,
            cmap="inferno"
        )

        plt.title(
            "Prediction Probability"
        )

        plt.colorbar(
            fraction=0.046,
            pad=0.04
        )

        plt.axis(
            "off"
        )

        plt.tight_layout()

        # -------------------------------------------------
        # BUFFER
        # -------------------------------------------------

        buffer = io.BytesIO()

        figure.savefig(
            buffer,
            format="png",
            dpi=140,
            bbox_inches="tight"
        )

        plt.close(
            figure
        )

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="image/png"
        )

    except Exception as error:

        return {
            "status":
                "error",

            "message":
                str(error)
        }


# =========================================================
# OLD STORED VISUALIZATION
# =========================================================

@app.get(
    "/api/prediction/{image_id}/visualization"
)
def prediction_visualization(
    image_id: str
):

    if not re.fullmatch(
        r"image_\d+",
        image_id
    ):
        return {
            "status":
                "error",

            "message":
                "Invalid image ID"
        }

    image_path = (
        TEST_IMAGE_DIR
        / f"{image_id}.h5"
    )

    prediction_path = (
        PREDICTION_DIR
        / f"{image_id}_prediction.npz"
    )

    if not image_path.exists():
        return {
            "status":
                "error",

            "message":
                (
                    f"Test image not found: "
                    f"{image_path}"
                )
        }

    if not prediction_path.exists():
        return {
            "status":
                "error",

            "message":
                (
                    f"Prediction file not found: "
                    f"{prediction_path.name}"
                )
        }

    try:

        with h5py.File(
            image_path,
            "r"
        ) as file:

            image = file[
                "img"
            ][:]

        prediction = np.load(
            prediction_path
        )

        mask = prediction[
            "mask"
        ]

        probability = prediction[
            "probability"
        ]

        rgb = image[
            :, :, :3
        ].astype(
            np.float32
        )

        for channel in range(3):

            channel_data = rgb[
                :, :, channel
            ]

            min_value = (
                channel_data.min()
            )

            max_value = (
                channel_data.max()
            )

            if (
                max_value
                > min_value
            ):

                rgb[
                    :, :, channel
                ] = (
                    (
                        channel_data
                        - min_value
                    )
                    /
                    (
                        max_value
                        - min_value
                    )
                )

            else:
                rgb[
                    :, :, channel
                ] = 0.0

        figure = plt.figure(
            figsize=(15, 5)
        )

        plt.subplot(
            1,
            3,
            1
        )

        plt.imshow(
            rgb
        )

        plt.title(
            "Satellite Image"
        )

        plt.axis(
            "off"
        )

        plt.subplot(
            1,
            3,
            2
        )

        plt.imshow(
            mask,
            cmap="gray"
        )

        plt.title(
            "AI Landslide Mask"
        )

        plt.axis(
            "off"
        )

        plt.subplot(
            1,
            3,
            3
        )

        plt.imshow(
            probability,
            cmap="inferno"
        )

        plt.title(
            "Prediction Probability"
        )

        plt.colorbar(
            fraction=0.046,
            pad=0.04
        )

        plt.axis(
            "off"
        )

        plt.tight_layout()

        buffer = io.BytesIO()

        figure.savefig(
            buffer,
            format="png",
            dpi=140,
            bbox_inches="tight"
        )

        plt.close(
            figure
        )

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="image/png"
        )

    except Exception as error:

        return {
            "status":
                "error",

            "message":
                str(error)
        }