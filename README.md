# 🌍 LandslideAI

LandslideAI is an AI/ML project for detecting possible landslide areas from geospatial images and showing the risk level.

This project was developed as a student project to learn and apply **Machine Learning, Deep Learning and Web Development**.

## 📌 Features

* Landslide detection using AI
* U-Net deep learning model
* H5 image support
* Landslide area prediction
* Risk score
* Risk level
* Prediction visualization
* Risk alerts
* Recommended precautions
* Web dashboard

## 🧠 How It Works

```text
H5 Image
   ↓
Preprocessing
   ↓
U-Net Model
   ↓
Landslide Prediction
   ↓
Risk Calculation
   ↓
Risk Level
   ↓
Dashboard
```

## 🛠️ Technologies Used

* Python
* PyTorch
* U-Net
* FastAPI
* React.js
* Vite
* NumPy
* h5py

## 📂 Dataset

This project uses the **Landslide4Sense Dataset** from Kaggle.

Kaggle Link:

https://www.kaggle.com/datasets/tekbahadurkshetri/landslide4sense?resource=download

## 📁 Project Structure

```text
LandslideAI/
│
├── frontend-react/
├── src/
├── models/
├── TestData/
├── predictions/
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

## 🤖 Model Files

The project uses:

```text
models/
├── best_unet.pth
└── channel_stats.npz
```

These files are required to run the prediction system.

## ⚙️ Installation

Clone the project:

```bash
git clone https://github.com/nishantdharav09/LandslideAI.git
```

Go to the project:

```bash
cd LandslideAI
```

Install Python packages:

```bash
pip install -r requirements.txt
```

For frontend:

```bash
cd frontend-react
npm install
```

## ▶️ Run the Project

### Backend

From the main project folder:

```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

Backend:

```text
http://127.0.0.1:8010
```

### Frontend

Open another terminal:

```bash
cd frontend-react
npm run dev
```

Frontend:

```text
http://localhost:5173/
```

## 📊 Prediction Result

The application shows:

* Predicted Area
* Mean Probability
* Maximum Probability
* Risk Score
* Risk Level
* Prediction Image

## 🚨 Risk Levels

| Score  | Risk      |
| ------ | --------- |
| 0–19   | Low       |
| 20–44  | Moderate  |
| 45–69  | High      |
| 70–100 | Very High |

## 🎯 Project Objective

The main aim of this project is to use AI and Deep Learning to detect possible landslide regions and display the result in a simple web application.

## 🔮 Future Scope

* Real-time satellite data
* Weather and rainfall data
* GIS map
* Mobile application
* Better risk prediction
* Real-time alerts

## ⚠️ Disclaimer

This project is made for **educational and student project purposes**.

The prediction results should not be treated as an official government or emergency warning.

## 👨‍💻 Author

**Nishant Dharav**

GitHub:

https://github.com/nishantdharav09/LandslideAI
