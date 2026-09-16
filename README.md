# 🌋 LandslideAI

## AI-Based Landslide Risk Monitoring System

LandslideAI is a web-based AI system that analyzes **14-channel satellite data** using a **U-Net deep learning model** to detect potential landslide regions and generate a preliminary risk score.

---

## 🚀 Features

* 🛰️ 14-channel H5 satellite data
* 🧠 U-Net deep learning model
* 📊 Predicted landslide area
* 📈 Mean and maximum probability
* ⚡ Risk score from 0–100
* 🚦 Low, Moderate, High and Very High risk levels
* 📤 H5 image upload
* 🚨 Risk alerts
* 📊 Analytics dashboard
* 🖼️ Prediction visualization
* 🛡️ Risk-based precautions

---

## 🔄 How It Works

```text
H5 Satellite Image
        ↓
Preprocessing
        ↓
U-Net Model
        ↓
Landslide Prediction
        ↓
Probability + Area
        ↓
Risk Score
        ↓
Risk Level
        ↓
Dashboard + Alerts + Precautions
```

---

## 🧠 AI Model

The project uses a **U-Net segmentation model**.

### Input

```text
128 × 128 × 14
```

### Output

The model generates a pixel-level landslide prediction map.

A probability above `0.5` is treated as a predicted landslide pixel.

---

## 📊 Risk Levels

| Risk Score | Level     |
| ---------- | --------- |
| 0 – <20    | Low       |
| 20 – <45   | Moderate  |
| 45 – <70   | High      |
| 70 – 100   | Very High |

---

## 🛠️ Technology Used

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn

### AI / ML

* PyTorch
* U-Net
* NumPy
* Pandas
* H5PY

### Visualization

* Matplotlib

---

## 📁 Project Structure

```text
LandslideAI/
│
├── frontend-react/
├── frontend/
├── src/
│   ├── api.py
│   ├── unet_model.py
│   ├── train.py
│   ├── dataset.py
│   ├── dataloader.py
│   ├── loss.py
│   └── ...
│
├── models/
├── predictions/
├── screenshots/
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the project

```bash
git clone https://github.com/nishantdharav09/LandslideAI.git
cd LandslideAI
```

### 2. Install Python packages

```bash
pip install torch fastapi uvicorn h5py matplotlib numpy pandas python-multipart
```

### 3. Install frontend packages

```bash
cd frontend-react
npm install
cd ..
```

---

## 📦 Required Model Files

The trained model and large data files are not included in the GitHub repository.

You need:

```text
models/
├── best_unet.pth
└── channel_stats.npz
```

Download them from:

* **Model:** `YOUR_MODEL_LINK`
* **Statistics:** `YOUR_STATS_LINK`

Place both files inside the `models` folder.

---

## 📤 Sample H5 File

The system expects an H5 file containing:

```text
dataset: img
shape: (128, 128, 14)
```

Sample file:

```text
image_677.h5
```

Download:

`YOUR_H5_LINK`

You can select the H5 file directly from the dashboard.

---

## ▶️ Run the Project

### Start Backend

From the project root:

```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

Backend:

```text
http://127.0.0.1:8010
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

## 📌 Example Result

```text
Image: image_677.h5

Predicted Area: 7.40%
Mean Probability: 85.41%
Max Probability: 99.90%
Risk Score: 45.27
Risk Level: High
```

---

## ⚠️ Important Note

LandslideAI provides a **preliminary AI-based risk indicator**.

It should be used for monitoring and prioritization and should not be considered an official government hazard classification or a replacement for professional assessment and official warnings.

---

## 👨‍💻 Project

**LandslideAI**

AI-Based Landslide Risk Monitoring System

GitHub:

https://github.com/nishantdharav09/LandslideAI
