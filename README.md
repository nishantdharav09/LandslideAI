# 🌍 LandslideAI

LandslideAI is an AI-based project that detects possible landslide areas from image data and shows the risk level.

## 🚀 Features

* Landslide detection using AI
* U-Net deep learning model
* Risk score calculation
* Risk levels: Low, Moderate, High, Very High
* Prediction visualization
* Simple web dashboard

## 🛠️ Technologies

* Python
* PyTorch
* FastAPI
* React.js
* U-Net
* H5 Dataset

## 📂 Dataset

This project uses the **Landslide4Sense Dataset** from Kaggle.

🔗 https://www.kaggle.com/datasets/tekbahadurkshetri/landslide4sense?resource=download

## ▶️ Run Project

### Backend

```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

### Frontend

```bash
cd frontend-react
npm install
npm run dev
```

Open:

```text
http://localhost:5173/
```

## 📊 Risk Levels

| Score  | Risk      |
| ------ | --------- |
| 0–19   | Low       |
| 20–44  | Moderate  |
| 45–69  | High      |
| 70–100 | Very High |

## 👨‍💻 Author

**Nishant Dharav**

GitHub:
https://github.com/nishantdharav09/LandslideAI
