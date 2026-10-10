import streamlit as st
import requests


st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠"
)


st.title("🏠 House Price Prediction")

st.write(
    "Enter house details to predict the estimated sale price."
)


OverallQual = st.slider(
    "Overall Quality",
    min_value=1,
    max_value=10,
    value=5
)


GrLivArea = st.number_input(
    "Living Area (sq ft)",
    min_value=100.0,
    max_value=5000.0,
    value=1500.0
)


GarageCars = st.number_input(
    "Garage Cars",
    min_value=0.0,
    max_value=5.0,
    value=2.0
)


GarageArea = st.number_input(
    "Garage Area",
    min_value=0.0,
    max_value=1500.0,
    value=500.0
)


TotalBsmtSF = st.number_input(
    "Basement Area",
    min_value=0.0,
    max_value=3000.0,
    value=800.0
)


firstFlrSF = st.number_input(
    "First Floor Area",
    min_value=100.0,
    max_value=4000.0,
    value=1000.0
)


FullBath = st.number_input(
    "Full Bathrooms",
    min_value=0,
    max_value=5,
    value=2
)


BedroomAbvGr = st.number_input(
    "Bedrooms",
    min_value=0,
    max_value=10,
    value=3
)


YearBuilt = st.number_input(
    "Year Built",
    min_value=1800,
    max_value=2026,
    value=2000
)


Neighborhood = st.selectbox(
    "Neighborhood",
    [
        "CollgCr",
        "Veenker",
        "Crawfor",
        "NoRidge",
        "Mitchel",
        "Somerst",
        "NWAmes",
        "OldTown",
        "BrkSide",
        "Sawyer"
    ]
)


KitchenQual = st.selectbox(
    "Kitchen Quality",
    ["Ex", "Gd", "TA", "Fa"]
)


GarageType = st.selectbox(
    "Garage Type",
    ["Attchd", "Detchd", "BuiltIn", "Basment", "CarPort"]
)


SaleCondition = st.selectbox(
    "Sale Condition",
    ["Normal", "Abnorml", "Partial", "AdjLand", "Alloca", "Family"]
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
        "SaleCondition": SaleCondition
    }
    
    import os 
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            price = result["predicted_price"]

            st.success(
                f"Estimated House Price: ${price:,.2f}"
            )

        else:

            st.error(
                f"API Error: {response.text}"
            )

    except Exception as e:

        st.error(
            f"Could not connect to FastAPI: {e}"
        )
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("FastAPI server is not running.")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")

    except (KeyError, ValueError):
        st.error("Invalid response received from the API.")    