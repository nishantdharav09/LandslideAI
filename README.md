# 🌍 LandslideAI

**LandslideAI** is an AI-based project developed to detect possible landslide areas from geospatial image data and predict the risk level.

The project uses a **U-Net deep learning model** for landslide segmentation and provides the prediction results through a web-based dashboard.

## 📌 Project Features

* Landslide area detection using AI
* U-Net based image segmentation
* Support for H5 image data
* Landslide probability prediction
* Predicted area calculation
* Risk score calculation
* Risk classification
* Prediction visualization
* Risk alerts
* Recommended precautions
* Interactive web dashboard

## 🧠 How the Project Works

```text
H5 Image
   ↓
Image Preprocessing
   ↓
U-Net Model
   ↓
Landslide Prediction
   ↓
Probability Map
   ↓
Risk Calculation
   ↓
Risk Level
   ↓
Dashboard
```

## 🚨 Risk Levels

| Risk Score | Risk Level |
| ---------- | ---------- |
| 0 – 19     | Low        |
| 20 – 44    | Moderate   |
| 45 – 69    | High       |
| 70 – 100   | Very High  |

## 🛠️ Technologies Used

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

## 📂 Dataset

This project uses the **Landslide4Sense Dataset**.

### Kaggle Dataset Link

https://www.kaggle.com/datasets/tekbahadurkshetri/landslide4sense?resource=download

The dataset is used for training, validation and testing of the landslide detection model.

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
│   ├── unet_model.py
│   ├── dataset.py
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
│
├── screenshots/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/nishantdharav09/LandslideAI.git
```

Go to the project folder:

```bash
cd LandslideAI
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run Backend

```bash
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

## ▶️ Run Frontend

Open another terminal:

```bash
cd frontend-react
```

Install frontend packages:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

Open the application:

```text
http://localhost:5173/
```

## 📊 Example Prediction

For an uploaded H5 image, the system shows information such as:

```text
Predicted Area
Mean Probability
Maximum Probability
Risk Score
Risk Level
```

The result is also shown on the dashboard with a visualization of the predicted landslide area.

## 🎯 Project Objective

The main objective of this project is to use **Artificial Intelligence and Deep Learning** for detecting possible landslide regions and presenting the results in an easy-to-understand web dashboard.

This project was developed as a student AI/ML project for learning and demonstrating the practical use of deep learning, image segmentation, and web technologies.

## 🔮 Future Scope

* Real-time satellite data
* Weather and rainfall data integration
* GIS map integration
* Real-time monitoring
* Mobile application
* Better risk prediction
* Automated warning notifications

## ⚠️ Disclaimer

This project is developed for **educational and project demonstration purposes**.

The predicted risk should not be considered an official geological or government warning.

## 👨‍💻 Author

**Nishant Dharav**

GitHub:
https://github.com/nishantdharav09/LandslideAI
