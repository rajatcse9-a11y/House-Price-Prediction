import os

import requests
import streamlit as st

# Local: FastAPI same laptop pe chalti hai.
# Render: Streamlit service ke Environment mein API_URL = https://<api-service>.onrender.com
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
)

st.title("🏠 House Price Prediction")
st.write("Enter house details to predict the estimated sale price.")


OverallQual = st.slider("Overall Quality", min_value=1, max_value=10, value=5)

GrLivArea = st.number_input(
    "Living Area (sq ft)", min_value=100.0, max_value=5000.0, value=1500.0
)

GarageCars = st.number_input(
    "Garage Cars", min_value=0.0, max_value=5.0, value=2.0
)

GarageArea = st.number_input(
    "Garage Area", min_value=0.0, max_value=1500.0, value=500.0
)

TotalBsmtSF = st.number_input(
    "Basement Area", min_value=0.0, max_value=3000.0, value=800.0
)

firstFlrSF = st.number_input(
    "First Floor Area", min_value=100.0, max_value=4000.0, value=1000.0
)

FullBath = st.number_input("Full Bathrooms", min_value=0, max_value=5, value=2)

BedroomAbvGr = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)

YearBuilt = st.number_input("Year Built", min_value=1800, max_value=2026, value=2000)

Neighborhood = st.selectbox(
    "Neighborhood",
    [
        "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel",
        "Somerst", "NWAmes", "OldTown", "BrkSide", "Sawyer",
    ],
)

KitchenQual = st.selectbox("Kitchen Quality", ["Ex", "Gd", "TA", "Fa"])

GarageType = st.selectbox(
    "Garage Type", ["Attchd", "Detchd", "BuiltIn", "Basment", "CarPort"]
)

SaleCondition = st.selectbox(
    "Sale Condition",
    ["Normal", "Abnorml", "Partial", "AdjLand", "Alloca", "Family"],
)


if st.button("Predict House Price"):

    data = {
        "OverallQual": OverallQual,
        "GrLivArea": GrLivArea,
        "GarageCars": GarageCars,
        "GarageArea": GarageArea,
        "TotalBsmtSF": TotalBsmtSF,
        "firstFlrSF": firstFlrSF,
        "FullBath": FullBath,
        "BedroomAbvGr": BedroomAbvGr,
        "YearBuilt": YearBuilt,
        "Neighborhood": Neighborhood,
        "KitchenQual": KitchenQual,
        "GarageType": GarageType,
        "SaleCondition": SaleCondition,
    }

    try:
        with st.spinner("Predicting... (pehli baar API jaagne mein 1 minute lag sakta hai)"):
            # Timeout bada rakha hai, kyunki free tier pe API so jaati hai
            response = requests.post(f"{API_URL}/predict", json=data, timeout=90)

        if response.status_code == 200:
            price = response.json()["predicted_price"]
            st.success(f"Estimated House Price: ${price:,.2f}")

        elif response.status_code in (502, 503, 504):
            st.warning("API abhi jaag rahi hai. 1 minute ruko aur dobara try karo.")

        else:
            st.error(f"API error {response.status_code}: {response.text[:300]}")

    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error(
            f"API se connect nahi ho paya ({API_URL}). "
            "Render pe Streamlit service ke Environment mein API_URL check karo."
        )

    except (KeyError, ValueError):
        st.error("Invalid response received from the API.")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")