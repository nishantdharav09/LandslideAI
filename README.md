# 🌋 LandslideAI

### AI-Based Landslide Risk Monitoring and Early Warning System

LandslideAI is an AI-powered monitoring system that analyzes **14-channel satellite/geospatial data** using a trained **U-Net deep learning segmentation model** to identify potential landslide regions and generate preliminary risk indicators.

The system combines **deep learning, geospatial image processing, a risk engine, and an interactive web dashboard** to support landslide monitoring and prioritization.

> ⚠️ **Disclaimer:** LandslideAI provides preliminary AI-derived indicators for monitoring and prioritization. It is not an official government hazard classification or a replacement for professional field assessment and official warnings.

---

## 🚀 Features

* 🛰️ 14-channel H5 satellite/geospatial image processing
* 🧠 U-Net based pixel-level landslide segmentation
* 📊 Predicted landslide area calculation
* 📈 Mean and maximum prediction probability
* ⚡ AI-derived risk score from 0–100
* 🚦 Risk classification: Low, Moderate, High, Very High
* 📤 User H5 image upload and real-time prediction
* 🔥 High-risk and very-high-risk alerts
* 🗺️ Prediction visualization
* 📊 Risk analytics and distribution
* 🛡️ Risk-level based precaution recommendations
* 🌐 React + FastAPI web application

---

## 🏗️ System Architecture

```text
                User
                 │
                 ▼
        Upload H5 Satellite Data
                 │
                 ▼
         React Frontend
                 │
                 ▼
          FastAPI Backend
                 │
                 ▼
       Input Validation
                 │
                 ▼
     128 × 128 × 14 Data
                 │
                 ▼
          Preprocessing
       HWC → CHW + Normalize
                 │
                 ▼
          Trained U-Net
                 │
                 ▼
        Probability Map
                 │
                 ▼
       Threshold (> 0.5)
                 │
                 ▼
        Landslide Mask
                 │
                 ▼
         Risk Calculation
          ┌──────┴──────┐
          ▼             ▼
      Area Score    Confidence Score
          └──────┬──────┘
                 ▼
            Risk Score
                 │
                 ▼
         Risk Classification
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Dashboard  Alerts  Precautions
                 │
                 ▼
          Visualization
```

---

## 🧠 AI Model

LandslideAI uses a **U-Net convolutional neural network** for semantic segmentation.

### Input

The model expects:

```text
128 × 128 × 14
```

The 14 channels represent multiple geospatial/satellite data layers stored in an H5 file.

### Output

The model generates a single-channel prediction map:

```text
128 × 128 × 1
```

A sigmoid function converts the model output into probabilities between 0 and 1.

A threshold of `0.5` is then used:

```text
Probability > 0.5  → Landslide pixel
Probability ≤ 0.5 → Non-landslide pixel
```

---

## 📊 Risk Calculation

The system calculates three important prediction indicators.

### Predicted Area

The percentage of image pixels classified as potential landslide pixels.

```text
Predicted Area =
(Landslide Pixels / Total Pixels) × 100
```

### Mean Probability

The average probability of pixels classified as landslide.

### Maximum Probability

The highest prediction probability found anywhere in the image.

---

## ⚡ Risk Engine

The final risk score is calculated using predicted area and model confidence.

### Area Contribution

```text
Area Score = min(Predicted Area × 1.5, 60)
```

### Confidence Contribution

```text
Confidence Score = Mean Probability × 40
```

### Final Risk Score

```text
Risk Score =
Area Score + Confidence Score
```

The final score is limited to the range:

```text
0–100
```

### Risk Levels

| Risk Score | Risk Level |
| ---------- | ---------- |
| 0 – <20    | Low        |
| 20 – <45   | Moderate   |
| 45 – <70   | High       |
| 70 – 100   | Very High  |

---

## 🖥️ Dashboard

The React dashboard provides:

### Dashboard

Overall prediction summary and current monitoring indicators.

### AI Predictions

Displays the latest uploaded prediction or stored high-risk prediction records.

### Risk Alerts

Highlights High and Very High preliminary risk predictions.

### Analytics

Shows risk distribution, average score, maximum score, and operational summaries.

### Prediction Explorer

Displays:

1. Satellite image
2. AI landslide mask
3. Prediction probability map

### Recommended Precautions

Provides risk-level based monitoring guidance for the current uploaded prediction.

---

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn

### AI / Machine Learning

* PyTorch
* U-Net
* NumPy

### Geospatial / Data Processing

* H5PY
* Pandas

### Visualization

* Matplotlib

---

## 📁 Project Structure

```text
LandslideAI/
│
├── frontend-react/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Predictions.jsx
│   │   ├── RiskAlerts.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── frontend/
│
├── src/
│   ├── api.py
│   ├── unet_model.py
│   ├── train.py
│   ├── train_cpu.py
│   ├── dataset.py
│   ├── dataloader.py
│   ├── loss.py
│   ├── predict_one.py
│   ├── predict_test.py
│   ├── evaluate_model.py
│   ├── risk_assessment.py
│   ├── risk_analysis.py
│   └── ...
│
├── models/
│
├── predictions/
│   └── landslide_risk_report.csv
│
├── screenshots/
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nishantdharav09/LandslideAI.git
cd LandslideAI
```

### 2. Backend dependencies

Install the required Python packages:

```bash
pip install torch fastapi uvicorn h5py matplotlib numpy pandas python-multipart
```

### 3. Frontend dependencies

```bash
cd frontend-react
npm install
```

---

## ▶️ Running the Project

### Start Backend

From the project root:

```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

Backend:

```text
http://127.0.0.1:8010
```

Swagger API documentation:

```text
http://127.0.0.1:8010/docs
```

### Start Frontend

Open another terminal:

```bash
cd frontend-react
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 📤 Input Format

The current prediction pipeline expects an H5 file containing:

```text
dataset name: img
shape: (128, 128, 14)
```

Example:

```text
image_677.h5
```

The system validates the H5 file before running inference.

---

## 🔄 Prediction Workflow

```text
Upload .h5
     ↓
Validate file
     ↓
Read "img" dataset
     ↓
Check shape
     ↓
HWC → CHW
     ↓
Normalize input
     ↓
Load trained U-Net
     ↓
Generate model output
     ↓
Apply sigmoid
     ↓
Create landslide mask
     ↓
Calculate area and probabilities
     ↓
Calculate risk score
     ↓
Assign risk level
     ↓
Display result
```

---

## 📌 Example Prediction

Example output:

```text
Image: image_677.h5

Risk Level: High

Predicted Area: 7.40%
Mean Probability: 85.41%
Max Probability: 99.90%
Risk Score: 45.27 / 100
```

The dashboard then updates the analytics, prediction table, alerts, visualization and precautions according to the current prediction.

---

## 🎯 Use Cases

LandslideAI can be used as a prototype for:

* Landslide monitoring
* Satellite image analysis
* Risk prioritization
* Geospatial AI research
* Disaster management research
* Early-warning workflow prototypes
* Academic and hackathon demonstrations

---

## ⚠️ Limitations

* The system currently expects a specific **14-channel H5 input format**.
* Normal JPG/PNG images are not directly supported by the current model pipeline.
* The risk score is a custom preliminary indicator.
* Predictions should be validated using real-world observations and professional assessment.
* The system should not be treated as an official emergency or government hazard classification system.

---

## 🏆 Project Highlights

* Deep learning based segmentation
* 14-channel geospatial data processing
* Pixel-level landslide detection
* Real-time H5 inference
* Risk scoring engine
* Interactive monitoring dashboard
* Visualization of AI predictions
* Automatic risk-level precautions

---

## 👨‍💻 Project

**LandslideAI**

AI-Based Landslide Risk Monitoring and Early Warning System

GitHub:
https://github.com/nishantdharav09/LandslideAI
