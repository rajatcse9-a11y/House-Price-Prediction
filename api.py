from fastapi import FastAPI
from pydantic import BaseModel,Field
import pandas as pd
import joblib

app=FastAPI(
    title="House Price PRediction API",
    description="ML API for House price  prediction",
    version="1.0"
)
model=joblib.load("model.pkl")
feature_info=joblib.load("preprocessor.pkl")

features=feature_info["features"]
cat_cols=feature_info["cat_cols"]

class HouseData(BaseModel):
    
    OverallQual: int = Field(ge=1, le=10)
    GrLivArea:float
    GarageCars:float
    GarageArea:float
    TotalBsmtSF:float
    firstFlrSF:float
    FullBath:int
    BedroomAbvGr:int
    YearBuilt:int
    Neighborhood:str
    KitchenQual:str
    GarageType:str
    SaleCondition:str


@app.get("/")
def home():
    return {
        "message":"House price PRediction API is running"
            }    
@app.get("/features")
def get_features():
    return {
        "features":features,
        "categorical_features":cat_cols
    }


    
@app.post("/predict")
def predict(data: HouseData):

    input_data = pd.DataFrame([{
        "OverallQual": data.OverallQual,
        "GrLivArea": data.GrLivArea,
        "GarageCars": data.GarageCars,
        "GarageArea": data.GarageArea,
        "TotalBsmtSF": data.TotalBsmtSF,
        "1stFlrSF": data.firstFlrSF,
        "FullBath": data.FullBath,
        "BedroomAbvGr": data.BedroomAbvGr,
        "YearBuilt": data.YearBuilt,
        "Neighborhood": data.Neighborhood,
        "KitchenQual": data.KitchenQual,
        "GarageType": data.GarageType,
        "SaleCondition": data.SaleCondition
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_price": round(float(prediction), 2)
    }       
