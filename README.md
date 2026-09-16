# 🌍 LandslideAI

LandslideAI is an **AI/ML based student project** developed to detect possible landslide areas from geospatial images and show the risk level.

The project uses a **U-Net deep learning model** for landslide segmentation and a **React + FastAPI** web application to display the prediction results.

## 📌 Features

* Landslide detection using AI
* U-Net deep learning model
* H5 image support
* Landslide area prediction
* Risk score calculation
* Risk level detection
* Prediction visualization
* Risk Alerts
* **Early Warning Alert**
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
Risk Score
   ↓
Risk Level
   ↓
Early Warning Alert
   ↓
Dashboard
```

## 🚨 Early Warning

The system provides an **Early Warning Alert** when the AI prediction shows:

* High Risk
* Very High Risk

The alert helps the user identify predictions that need additional monitoring and review.

## 🛠️ Technologies Used

* Python
* PyTorch
* U-Net
* FastAPI
* React.js
* Vite
* NumPy
* h5py
* Matplotlib

## 📂 Dataset

This project uses the **Landslide4Sense Dataset** from Kaggle.

### Kaggle Link

https://www.kaggle.com/datasets/tekbahadurkshetri/landslide4sense?resource=download

The dataset is used for training, validation and testing.

## 🤖 Model Files

The project uses the following trained model files:

```text
models/
├── best_unet.pth
└── channel_stats.npz
```

These files are required for running AI predictions.

## 📁 Project Structure

```text
LandslideAI/
│
├── frontend-react/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── src/
│   ├── api.py
│   ├── train.py
│   ├── dataset.py
│   ├── unet_model.py
│   └── ...
│
├── models/
│   ├── best_unet.pth
│   └── channel_stats.npz
│
├── TestData/
│   └── img/
│
├── predictions/
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

# 💻 How to Run

There are two ways to run the project.

## 1️⃣ Download ZIP

Open the GitHub repository:

https://github.com/nishantdharav09/LandslideAI

Click:

```text
Code → Download ZIP
```

Extract the ZIP file and open the **LandslideAI** folder in VS Code.

Open:

```text
Terminal → New Terminal
```

Install Python packages:

```powershell
pip install -r requirements.txt
```

Go to frontend:

```powershell
cd frontend-react
```

Install frontend packages:

```powershell
npm.cmd install
```

## 2️⃣ Clone Repository

Open PowerShell:

```powershell
git clone https://github.com/nishantdharav09/LandslideAI.git
```

Go to the project:

```powershell
cd LandslideAI
```

Install Python packages:

```powershell
pip install -r requirements.txt
```

Go to frontend:

```powershell
cd frontend-react
```

Install frontend packages:

```powershell
npm.cmd install
```

# ▶️ Run the Project

The backend and frontend should be run in **two terminals**.

## Terminal 1 - Backend

From the main project folder:

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

Backend:

```text
http://127.0.0.1:8010
```

API Documentation:

```text
http://127.0.0.1:8010/docs
```

## Terminal 2 - Frontend

Open another terminal:

```powershell
cd frontend-react
```

Run:

```powershell
npm.cmd run dev
```

Frontend:

```text
http://localhost:5173/
```

Open the frontend link in your browser.

## 📤 How to Use

1. Open the website.
2. Select a valid `.h5` image.
3. Click **Predict Risk**.
4. The backend processes the image.
5. The U-Net model generates the prediction.
6. The system calculates the risk score.
7. The dashboard shows the prediction result.
8. If the risk is **High** or **Very High**, an **Early Warning Alert** is displayed.
9. Recommended precautions are also shown.

## 📊 Prediction Result

The system displays:

* Predicted Area
* Mean Probability
* Maximum Probability
* Risk Score
* Risk Level
* Prediction Visualization

Example:

```text
Predicted Area    : 7.40%
Mean Probability  : 85.41%
Max Probability   : 99.90%
Risk Score        : 45.27 / 100
Risk Level        : High
```

## 🚨 Risk Levels

| Risk Score | Risk Level |
| ---------- | ---------- |
| 0 – 19     | Low        |
| 20 – 44    | Moderate   |
| 45 – 69    | High       |
| 70 – 100   | Very High  |

## 🎯 Project Objective

The main aim of this project is to use **AI and Deep Learning** to detect possible landslide regions and show the result through a simple web application.

This project helped me learn about:

* Machine Learning
* Deep Learning
* U-Net
* Image Segmentation
* Python
* FastAPI
* React.js
* AI model deployment

## 🔮 Future Scope

* Real-time satellite data
* Weather and rainfall data
* GIS map integration
* Mobile application
* Improved risk prediction
* Real-time monitoring
* Automated notifications

## ⚠️ Note

This project is developed for **educational and student project purposes**.

The prediction is an AI-based preliminary estimate and should not be considered an official government or emergency warning.

## 👨‍💻 Author

**Nishant Dharav**

GitHub:

https://github.com/nishantdharav09/LandslideAI
