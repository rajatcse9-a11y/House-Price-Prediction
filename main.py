import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="House Price Prediction API",
    description="ML API for house price prediction",
    version="1.0",
)

# ---------------------------------------------------------
# Load model + preprocessing info
# ---------------------------------------------------------
model = joblib.load("model.pkl")
feature_info = joblib.load("preprocessor.pkl")

features = feature_info["features"]
cat_cols = feature_info["cat_cols"]


# ---------------------------------------------------------
# Input schema
# ---------------------------------------------------------
class HouseData(BaseModel):
    OverallQual: int = Field(ge=1, le=10)
    GrLivArea: float
    GarageCars: float
    GarageArea: float
    TotalBsmtSF: float
    firstFlrSF: float
    FullBath: int
    BedroomAbvGr: int
    YearBuilt: int
    Neighborhood: str
    KitchenQual: str
    GarageType: str
    SaleCondition: str


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.get("/")
def home():
    return {"message": "House Price Prediction API is running"}


@app.get("/features")
def get_features():
    return {
        "features": features,
        "categorical_features": cat_cols,
    }


@app.post("/predict")
def predict(data: HouseData):
    input_data = pd.DataFrame([{
        "OverallQual": data.OverallQual,
        "GrLivArea": data.GrLivArea,
        "GarageCars": data.GarageCars,
        "GarageArea": data.GarageArea,
        "TotalBsmtSF": data.TotalBsmtSF,
        "1stFlrSF": data.firstFlrSF,   # model ke training column ka naam
        "FullBath": data.FullBath,
        "BedroomAbvGr": data.BedroomAbvGr,
        "YearBuilt": data.YearBuilt,
        "Neighborhood": data.Neighborhood,
        "KitchenQual": data.KitchenQual,
        "GarageType": data.GarageType,
        "SaleCondition": data.SaleCondition,
    }])

    try:
        prediction = model.predict(input_data)[0]
    except Exception as e:
        # Unknown category ya column mismatch hone par 500 crash ki jagah saaf message
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")

    return {"predicted_price": round(float(prediction), 2)}