# 🌍 LandslideAI

### AI-Powered Landslide Risk Monitoring & Prediction System

LandslideAI is an AI-based landslide monitoring system that uses **Deep Learning and U-Net segmentation** to detect potential landslide regions from multi-channel geospatial image data and estimate the corresponding risk level.

The system provides a web-based dashboard for uploading H5 image data, generating AI predictions, visualizing results, monitoring risk levels, and displaying recommended precautions.

---

## 🚀 Features

* 🧠 AI-based landslide segmentation using **U-Net**
* 🛰️ Supports multi-channel H5 geospatial image data
* 🔍 Pixel-level landslide prediction
* 📊 Predicted landslide area calculation
* 📈 Probability and risk score calculation
* 🚨 Automatic risk classification
* 🎨 Interactive visualization of prediction results
* 📋 AI Predictions dashboard
* ⚠️ Risk Alerts
* 🛡️ Recommended precautions
* 🌐 React-based modern web interface
* ⚡ FastAPI backend for AI inference

---

## 🏗️ System Workflow

```text
H5 Geospatial Image
        ↓
128 × 128 × 14 Input
        ↓
Preprocessing & Normalization
        ↓
U-Net Deep Learning Model
        ↓
Pixel-Level Segmentation
        ↓
Probability Map
        ↓
Landslide Mask
        ↓
Risk Calculation
        ↓
Risk Classification
        ↓
Dashboard & Alerts
```

---

## 🧠 AI Model

LandslideAI uses a **U-Net Convolutional Neural Network** for semantic segmentation.

### Model Input

```text
Input Shape: 128 × 128 × 14
```

The 14 channels contain multi-source information used by the segmentation model.

### Model Output

```text
Output Shape: 128 × 128 × 1
```

Each pixel receives a probability indicating how likely it is to belong to a landslide region.

---

## 📊 Risk Calculation

The system calculates the risk using:

### Predicted Area

The percentage of pixels classified as landslide.

```text
Predicted Area =
(Landslide Pixels / Total Pixels) × 100
```

### Mean Probability

Average prediction probability of pixels classified as landslide.

### Maximum Probability

Highest landslide probability detected in the image.

### Risk Score

The system combines predicted landslide area and model probability to generate a risk score between:

```text
0 – 100
```

---

## 🚨 Risk Levels

| Risk Score | Risk Level   |
| ---------- | ------------ |
| 0 – 19.99  | 🟢 Low       |
| 20 – 44.99 | 🟡 Moderate  |
| 45 – 69.99 | 🟠 High      |
| 70 – 100   | 🔴 Very High |

> **Note:** These risk levels are part of the project's preliminary risk engine and are not an official government hazard classification.

---

## 🖥️ Dashboard

The web application contains:

### Dashboard

Displays the current prediction summary and risk statistics.

### Analytics

Provides visual information about prediction and risk results.

### AI Predictions

Displays prediction results with:

* Image name
* Predicted area
* Mean probability
* Maximum probability
* Risk score
* Risk level
* Visualization

### Risk Alerts

Displays alerts for high-risk predictions.

### Recommended Precautions

Provides general precautions according to the detected risk level.

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn

### Machine Learning

* PyTorch
* U-Net
* NumPy
* h5py

### Data Visualization

* Matplotlib
* React-based dashboard components

---

## 📂 Project Structure

```text
LandslideAI/
│
├── frontend-react/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Predictions.jsx
│   │   ├── RiskAlerts.jsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── src/
│   ├── api.py
│   ├── unet_model.py
│   ├── train.py
│   ├── test_model.py
│   ├── dataset.py
│   └── ...
│
├── models/
│   ├── best_unet.pth
│   └── channel_stats.npz
│
├── predictions/
│   └── ...
│
├── TestData/
│   └── img/
│
├── screenshots/
│   └── ...
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 📚 Dataset

This project uses the **Landslide4Sense** dataset.

### Kaggle Dataset

https://www.kaggle.com/datasets/tekbahadurkshetri/landslide4sense?resource=download

The dataset provides the geospatial image data used for training, validation, and testing of the landslide segmentation model.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nishantdharav09/LandslideAI.git
```

```bash
cd LandslideAI
```

---

## 🐍 Backend Setup

Create a Python environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI backend:

```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

Backend will run at:

```text
http://127.0.0.1:8010
```

Swagger API documentation:

```text
http://127.0.0.1:8010/docs
```

---

## ⚛️ Frontend Setup

Open a new terminal:

```powershell
cd frontend-react
```

Install dependencies:

```powershell
npm install
```

Start the React application:

```powershell
npm run dev
```

Frontend will run at:

```text
http://localhost:5173/
```

---

## ▶️ Running the Project

Run both servers:

### Backend

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

### Frontend

```powershell
cd frontend-react
npm run dev
```

Then open:

```text
http://localhost:5173/
```

---

## 📤 Prediction Process

1. Open the LandslideAI web application.
2. Upload a valid `.h5` image file.
3. The backend reads the `img` dataset.
4. The image is converted from HWC to CHW format.
5. Input channels are normalized.
6. The trained U-Net model performs segmentation.
7. A probability map is generated.
8. Pixels above the prediction threshold are classified as landslide.
9. The system calculates:

   * Predicted Area
   * Mean Probability
   * Maximum Probability
   * Risk Score
10. The final risk level is displayed on the dashboard.

---

## 📈 Example Prediction

Example output:

```text
Input Shape      : 128 × 128 × 14
Predicted Area   : 7.40%
Mean Probability : 85.41%
Max Probability  : 99.90%
Risk Score       : 45.27 / 100
Risk Level       : High
```

---

## 🔬 Model Performance

During model training, the project evaluates the segmentation model using validation data.

The project can be extended with additional metrics such as:

* Dice Score
* IoU
* Precision
* Recall
* F1 Score

---

## 🌐 API Endpoints

### Health Check

```text
GET /api/health
```

### Prediction

```text
POST /api/predict
```

### Risk Summary

```text
GET /api/risk-summary
```

### Top Risk Predictions

```text
GET /api/top-risk
```

### Prediction Visualization

```text
GET /api/prediction/{image_id}/visualization
```

---

## 🔮 Future Improvements

* Real-time satellite data integration
* Weather and rainfall integration
* Geographic mapping using GIS
* Real-time monitoring
* Improved risk calibration
* Larger and more diverse training datasets
* Cloud deployment
* Mobile application
* Automated early-warning notifications

---

## ⚠️ Disclaimer

LandslideAI is an **AI-based research and educational prototype**.

The predictions and risk scores generated by this system should not be treated as official geological, governmental, or emergency warnings.

Actual landslide assessment should be performed using appropriate geological, environmental, meteorological, and field data by qualified authorities and experts.

---

## 👨‍💻 Author

**Nishant Dharav**

GitHub:

https://github.com/nishantdharav09/LandslideAI

---

## ⭐ Project Objective

The main objective of LandslideAI is to demonstrate how **Artificial Intelligence, Deep Learning, Computer Vision, and Web Technologies** can be combined to build a preliminary landslide monitoring and risk prediction system.

---
