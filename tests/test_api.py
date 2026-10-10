from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi import HTTPException
import importlib.util
from pathlib import Path

# Existing FastAPI application load karo
project_dir = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "house_api",
    project_dir / "api.py"
)

api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)

client = TestClient(api_module.app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_features_endpoint():
    response = client.get("/features")

    assert response.status_code == 200
    assert "features" in response.json()


def test_prediction_endpoint():
    payload = {
        "OverallQual": 7,
        "GrLivArea": 1800.0,
        "GarageCars": 2.0,
        "GarageArea": 500.0,
        "TotalBsmtSF": 800.0,
        "firstFlrSF": 1000.0,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "YearBuilt": 2005,
        "Neighborhood": "CollgCr",
        "KitchenQual": "Gd",
        "GarageType": "Attchd",
        "SaleCondition": "Normal"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "predicted_price" in response.json()
    assert isinstance(response.json()["predicted_price"], (int, float))


def test_missing_field():
    payload = {
        "OverallQual": 7
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_invalid_input():
    payload = {
        "OverallQual": "invalid",
        "GrLivArea": 1800.0,
        "GarageCars": 2.0,
        "GarageArea": 500.0,
        "TotalBsmtSF": 800.0,
        "firstFlrSF": 1000.0,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "YearBuilt": 2005,
        "Neighborhood": "CollgCr",
        "KitchenQual": "Gd",
        "GarageType": "Attchd",
        "SaleCondition": "Normal"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_invalid_quality():
    payload = {
        "OverallQual": 100,
        "GrLivArea": 1800.0,
        "GarageCars": 2.0,
        "GarageArea": 500.0,
        "TotalBsmtSF": 800.0,
        "firstFlrSF": 1000.0,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "YearBuilt": 2005,
        "Neighborhood": "CollgCr",
        "KitchenQual": "Gd",
        "GarageType": "Attchd",
        "SaleCondition": "Normal"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422