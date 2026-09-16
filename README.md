# 🌍 LandslideAI

LandslideAI is an AI/ML project developed to detect possible landslide areas from geospatial images and show the risk level.

This project was developed as a student project to learn and apply **AI, Machine Learning, Deep Learning and Web Development**.

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

These files are required to run predictions.

## 💻 How to Download and Run

There are two ways to run this project.

---

# Option 1: Download ZIP

### Step 1: Download the Project

Open the GitHub repository:

https://github.com/nishantdharav09/LandslideAI

Click:

```text
Code → Download ZIP
```

### Step 2: Extract the ZIP

Extract the downloaded ZIP file.

### Step 3: Open in VS Code

Open the extracted **LandslideAI** folder in VS Code.

### Step 4: Open Terminal

In VS Code:

```text
Terminal → New Terminal
```

### Step 5: Install Python Dependencies

Make sure you are in the main project folder and run:

```powershell
pip install -r requirements.txt
```

### Step 6: Install Frontend Dependencies

```powershell
cd frontend-react
npm.cmd install
```

---

# Option 2: Clone the Repository

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

---

# ▶️ Run the Project

The backend and frontend should be run in **two terminals**.

## Terminal 1 - Backend

From the main project folder:

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8010
```

Backend URL:

```text
http://127.0.0.1:8010
```

API documentation:

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

Frontend URL:

```text
http://localhost:5173/
```

Open the frontend URL in your browser.

## 📤 How to Use

1. Open the website.
2. Upload an `.h5` image.
3. The image is processed by the backend.
4. The U-Net model predicts possible landslide areas.
5. The system calculates the risk.
6. The result is shown on the dashboard.

## 📊 Prediction Result

The application shows:

* Predicted Area
* Mean Probability
* Maximum Probability
* Risk Score
* Risk Level
* Prediction Visualization

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

This project is made for educational and student project purposes.

The prediction results should not be treated as an official government or emergency warning.

## 👨‍💻 Author

**Nishant Dharav**

GitHub:

https://github.com/nishantdharav09/LandslideAI
