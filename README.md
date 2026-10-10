# 🏠 House Price Prediction

An end-to-end Machine Learning project that predicts house prices based on property features. The project uses **Scikit-learn** for machine learning, **FastAPI** for the prediction API, **Streamlit** for the user interface, and **Docker Compose** to run both services.

## 🚀 Features

* Predict house prices using property details.
* Machine Learning model with a preprocessing pipeline.
* REST API built using FastAPI.
* Interactive web interface built using Streamlit.
* Dockerized frontend and backend.
* API testing through Swagger UI.

## 🛠️ Tech Stack

* **Language:** Python
* **Machine Learning:** Scikit-learn
* **Data Processing:** Pandas, NumPy
* **Backend:** FastAPI, Uvicorn
* **Frontend:** Streamlit
* **API Requests:** Requests
* **Model Serialization:** Joblib
* **Containerization:** Docker, Docker Compose

## 📁 Project Structure

```text
House-project/
├── api.py
├── app.py
├── model.pkl
├── preprocessor.pkl
├── requirements.txt
├── Dockerfile
├── Dockerfile.streamlit
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## ⚙️ Run the Project with Docker

### Prerequisites

* Docker Desktop
* Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/rajatcse9-a11y/House-Price-Prediction.git
cd House-Price-Prediction
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Start the application

```bash
docker compose up -d
```

### 3. Open the application

**Streamlit Web App:**
http://localhost:8501

**FastAPI Swagger Documentation:**
http://localhost:8000/docs

### 4. Stop the application

```bash
docker compose down
```

## 🖥️ Run Locally Without Docker

### 1. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the FastAPI backend

Open a terminal in the project directory:

```bash
uvicorn api:app --reload
```

### 4. Start the Streamlit frontend

Open a second terminal and run:

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

**Note:** When running locally, the Streamlit application uses the FastAPI endpoint configured in `app.py`. Ensure that the API URL points to `http://127.0.0.1:8000/predict` for local execution.

## 🔄 How It Works

1. The user enters house features in the Streamlit interface.
2. Streamlit sends the input to the FastAPI prediction endpoint.
3. The preprocessing component transforms the input.
4. The trained Machine Learning model generates a prediction.
5. FastAPI returns the predicted price.
6. Streamlit displays the result to the user.

## 🧪 API Testing

FastAPI provides interactive API documentation through Swagger UI.

Open:

http://localhost:8000/docs

Select the `/predict` endpoint, enter the required input fields, and execute the request to test the prediction API.

## 📌 Learning Outcomes

* Building an end-to-end Machine Learning application.
* Integrating a trained model with FastAPI.
* Connecting a Streamlit frontend to a REST API.
* Using Docker to containerize application services.
* Running multiple services using Docker Compose.
* Testing API endpoints and debugging integration issues.

## 👨‍💻 Author

**Rajat Maurya**

B.Tech Computer Science Engineering

Interested in Machine Learning, Artificial Intelligence, and building practical ML applications.

---

⭐ If you find this project useful, consider giving the repository a star.
