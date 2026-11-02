from datetime import date
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="HomeAI | House Price Studio",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# MODEL LOADING  (internal logic same)
# =====================================================

HERE = Path(__file__).resolve().parent

# model.pkl in jagahon mein se jo pehle mile wahi use hoga
CANDIDATE_DIRS = [
    HERE,
    HERE.parent,
    HERE / "models",
    HERE.parent / "models",
    HERE / "api",
    HERE.parent / "api",
]

# api/main.py wale exact column names aur order (training ke hisaab se)
FEATURE_COLUMNS = [
    "OverallQual",
    "GrLivArea",
    "GarageCars",
    "GarageArea",
    "TotalBsmtSF",
    "1stFlrSF",
    "FullBath",
    "BedroomAbvGr",
    "YearBuilt",
    "Neighborhood",
    "KitchenQual",
    "GarageType",
    "SaleCondition",
]


def find_model_file():
    for folder in CANDIDATE_DIRS:
        path = folder / "model.pkl"
        if path.exists():
            return path
    return None


@st.cache_resource(show_spinner="Model load ho raha hai...")
def load_model(path: str):
    """Model sirf ek baar load hota hai, har click pe nahi."""
    return joblib.load(path)


MODEL_PATH = find_model_file()


# =====================================================
# UI CONFIG (sirf dikhane ke liye, prediction pe asar nahi)
# =====================================================

NEIGHBORHOODS = [
    "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel",
    "Somerst", "NWAmes", "OldTown", "BrkSide", "Sawyer",
]
KITCHEN_OPTIONS = ["Ex", "Gd", "TA", "Fa"]
GARAGE_TYPES = ["Attchd", "Detchd", "BuiltIn", "Basment", "CarPort"]
SALE_CONDITIONS = ["Normal", "Abnorml", "Partial", "AdjLand", "Alloca", "Family"]

# Market position gauge ke liye approx range (apne dataset ke hisaab se badal sakte ho)
PRICE_MIN = 35_000
PRICE_MAX = 755_000
# Tier cutoffs (approx)
TIERS = [
    (130_000, "Budget", "#38bdf8"),
    (215_000, "Mid-range", "#4ade80"),
    (350_000, "Premium", "#fbbf24"),
    (float("inf"), "Luxury", "#f472b6"),
]

# Form ke default values (pehle jaise)
DEFAULTS = {
    "q": 5, "yb": 2000, "kq": "Ex",
    "gl": 1500.0, "ff": 1000.0, "bs": 800.0,
    "gc": 2.0, "ga": 500.0, "gt": "Attchd",
    "fb": 2, "bd": 3, "nb": "CollgCr", "sc": "Normal",
}

PRESETS = {
    "Starter Home": {
        "q": 4, "yb": 1960, "kq": "TA",
        "gl": 1000.0, "ff": 900.0, "bs": 700.0,
        "gc": 1.0, "ga": 280.0, "gt": "Detchd",
        "fb": 1, "bd": 2, "nb": "OldTown", "sc": "Normal",
    },
    "Family Home": {
        "q": 6, "yb": 1995, "kq": "Gd",
        "gl": 1800.0, "ff": 1000.0, "bs": 900.0,
        "gc": 2.0, "ga": 480.0, "gt": "Attchd",
        "fb": 2, "bd": 3, "nb": "CollgCr", "sc": "Normal",
    },
    "Luxury Home": {
        "q": 9, "yb": 2008, "kq": "Ex",
        "gl": 2800.0, "ff": 1600.0, "bs": 1500.0,
        "gc": 3.0, "ga": 800.0, "gt": "BuiltIn",
        "fb": 3, "bd": 4, "nb": "NoRidge", "sc": "Normal",
    },
}

for _k, _v in DEFAULTS.items():
    st.session_state.setdefault(_k, _v)


def apply_preset(name: str):
    for key, value in PRESETS[name].items():
        st.session_state[key] = value


def tier_for(price: float):
    for limit, label, color in TIERS:
        if price < limit:
            return label, color
    return TIERS[-1][1], TIERS[-1][2]


def short_money(value: float) -> str:
    return f"${value / 1000:,.0f}K"


# =====================================================
# STYLING
# =====================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(900px 400px at 85% -10%, rgba(34, 211, 238, 0.10), transparent 60%),
            radial-gradient(700px 400px at -10% 10%, rgba(99, 102, 241, 0.12), transparent 60%),
            #0a0f1e;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #0f1626;
        border-right: 1px solid #22304a;
    }
    [data-testid="stHeader"] { background: rgba(10, 15, 30, 0.9); }

    /* ---------- Hero ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(125deg, #1e1b4b 0%, #0f172a 50%, #0c4a6e 100%);
        padding: 34px 36px;
        border-radius: 20px;
        border: 1px solid #334155;
        margin-bottom: 22px;
    }
    .hero::after {
        content: "";
        position: absolute;
        right: -60px; top: -60px;
        width: 240px; height: 240px;
        background: radial-gradient(circle, rgba(34, 211, 238, 0.28), transparent 70%);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(34, 211, 238, 0.12);
        border: 1px solid rgba(34, 211, 238, 0.35);
        color: #67e8f9;
        font-size: 11px; font-weight: 700;
        letter-spacing: 1.5px; text-transform: uppercase;
        padding: 5px 12px; border-radius: 999px; margin-bottom: 14px;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        color: #f8fafc; font-size: 38px; font-weight: 700; margin: 0 0 8px 0;
    }
    .hero p { color: #cbd5e1; font-size: 15px; margin: 0; max-width: 640px; }

    /* ---------- Cards ---------- */
    .kpi {
        background: rgba(17, 28, 48, 0.75);
        border: 1px solid #22304a;
        border-radius: 14px;
        padding: 16px 18px;
    }
    .kpi-label {
        color: #94a3b8; font-size: 11px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .kpi-value { color: #f8fafc; font-size: 21px; font-weight: 800; margin-top: 6px; }
    .kpi-caption { color: #94a3b8; font-size: 12px; margin-top: 3px; }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        color: #f1f5f9; font-size: 21px; font-weight: 700;
        margin: 16px 0 4px 0;
    }
    .section-description { color: #94a3b8; font-size: 13px; margin-bottom: 14px; }

    .group-title {
        display: flex; align-items: center; gap: 8px;
        color: #e2e8f0; font-size: 14px; font-weight: 700;
        margin: 4px 0 10px 0;
    }

    /* ---------- Result ---------- */
    .result-card {
        background: linear-gradient(135deg, #0b2540 0%, #111c30 60%, #14213d 100%);
        border: 1px solid #2b4a6b;
        border-radius: 20px;
        padding: 30px 32px;
        margin: 12px 0 18px 0;
    }
    .result-top {
        display: flex; justify-content: space-between;
        align-items: center; flex-wrap: wrap; gap: 10px;
    }
    .price-label {
        color: #94a3b8; font-size: 12px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.5px;
    }
    .tier-chip {
        font-size: 12px; font-weight: 700; padding: 5px 14px;
        border-radius: 999px; border: 1px solid;
    }
    .price-value {
        font-family: 'Space Grotesk', sans-serif;
        color: #f8fafc; font-size: 58px; font-weight: 700;
        margin: 10px 0 2px 0; letter-spacing: -1px;
    }
    .price-sub { color: #94a3b8; font-size: 13px; }

    .gauge-wrap { margin-top: 26px; }
    .gauge {
        position: relative; height: 10px; border-radius: 999px;
        background: linear-gradient(90deg, #38bdf8 0%, #4ade80 30%, #fbbf24 60%, #f472b6 100%);
    }
    .gauge-marker {
        position: absolute; top: -7px;
        width: 4px; height: 24px; border-radius: 4px;
        background: #ffffff;
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
        transform: translateX(-2px);
    }
    .gauge-scale {
        display: flex; justify-content: space-between;
        color: #64748b; font-size: 11px; margin-top: 10px;
    }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        width: 100%;
        background: #111c30;
        color: #e2e8f0;
        border: 1px solid #2b3d5c;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.15s ease;
    }
    div.stButton > button:hover {
        border-color: #22d3ee; color: #67e8f9; background: #12213a;
    }
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        background: linear-gradient(90deg, #4f46e5, #0891b2);
        color: white; font-weight: 700; border: none;
        border-radius: 12px; min-height: 52px; font-size: 16px;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(90deg, #4338ca, #0e7490);
        color: white; border: none;
    }

    div[data-testid="stMetric"] {
        background: rgba(17, 28, 48, 0.75);
        border: 1px solid #22304a;
        padding: 16px; border-radius: 12px;
    }
    div[data-testid="stMetricLabel"] { color: #94a3b8; }
    div[data-testid="stMetricValue"] { color: #f8fafc; }

    button[data-baseweb="tab"] { font-weight: 600; }
    hr { border-color: #22304a; }
    .footer { color: #64748b; text-align: center; font-size: 12px; padding: 20px 0; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("## 🏠 HomeAI")
    st.caption("HOUSE PRICE STUDIO")
    st.divider()

    st.markdown("### How it works")
    st.markdown("1️⃣ Pick a preset or enter details")
    st.markdown("2️⃣ Model analyses 13 features")
    st.markdown("3️⃣ Get price, market tier and what-if insights")
    st.divider()

    st.markdown("### System Information")
    st.caption("Model: House Price Regressor")
    st.caption("Inference: Local model")
    st.caption("Frontend: Streamlit")
    st.divider()

    st.markdown("### Model Status")
    if MODEL_PATH is None:
        st.error("model.pkl nahi mila.")
    else:
        st.code(MODEL_PATH.name, language="text")
        if st.button("🔌 Check Model Status"):
            try:
                load_model(str(MODEL_PATH))
                st.success("Model loaded successfully.")
            except Exception as e:
                st.error(f"Model load nahi hua: {e}")


# =====================================================
# HERO + OVERVIEW
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">AI · Real Estate</div>
    <h1>House Price Studio</h1>
    <p>
        Estimate a home's sale price with a trained machine learning model,
        see where it sits in the market, and explore what-if scenarios.
    </p>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">System</div>
        <div class="kpi-value">AI Enabled</div>
        <div class="kpi-caption">Sale price estimation</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">Input Features</div>
        <div class="kpi-value">13 Features</div>
        <div class="kpi-caption">Numeric + categorical</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">Inference</div>
        <div class="kpi-value">Local Model</div>
        <div class="kpi-caption">Loaded from model.pkl</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">Extras</div>
        <div class="kpi-value">What-if</div>
        <div class="kpi-caption">Scenario analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

if MODEL_PATH is None:
    st.error(
        "model.pkl nahi mila. File ko repo mein app.py ke saath, "
        "ya models/ folder mein rakho."
    )
    st.stop()


# =====================================================
# TABS
# =====================================================

tab_predict, tab_whatif, tab_about = st.tabs(
    ["🏠 Predict", "📈 What-if Analysis", "ℹ️ About"]
)


# =====================================================
# TAB 1: PREDICT
# =====================================================

with tab_predict:

    st.markdown(
        '<div class="section-title">Property Details</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-description">'
        'Start from a preset or fill the details manually.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- Presets ----------
    p1, p2, p3 = st.columns(3)
    with p1:
        st.button("🏡 Starter Home", on_click=apply_preset, args=("Starter Home",))
    with p2:
        st.button("👨‍👩‍👧 Family Home", on_click=apply_preset, args=("Family Home",))
    with p3:
        st.button("🏰 Luxury Home", on_click=apply_preset, args=("Luxury Home",))

    st.write("")

    # ---------- Form (same fields, same ranges, same options) ----------
    with st.form("house_form"):

        st.markdown('<div class="group-title">🏗️ Quality & Age</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            OverallQual = st.slider("Overall Quality", min_value=1, max_value=10, key="q")
        with c2:
            YearBuilt = st.number_input(
                "Year Built", min_value=1800, max_value=2026, key="yb"
            )
        with c3:
            KitchenQual = st.selectbox("Kitchen Quality", KITCHEN_OPTIONS, key="kq")

        st.divider()

        st.markdown('<div class="group-title">📐 Area (sq ft)</div>', unsafe_allow_html=True)
        a1, a2, a3 = st.columns(3)
        with a1:
            GrLivArea = st.number_input(
                "Living Area (sq ft)", min_value=100.0, max_value=5000.0, key="gl"
            )
        with a2:
            firstFlrSF = st.number_input(
                "First Floor Area", min_value=100.0, max_value=4000.0, key="ff"
            )
        with a3:
            TotalBsmtSF = st.number_input(
                "Basement Area", min_value=0.0, max_value=3000.0, key="bs"
            )

        st.divider()

        st.markdown('<div class="group-title">🚗 Garage</div>', unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1:
            GarageCars = st.number_input(
                "Garage Cars", min_value=0.0, max_value=5.0, key="gc"
            )
        with g2:
            GarageArea = st.number_input(
                "Garage Area", min_value=0.0, max_value=1500.0, key="ga"
            )
        with g3:
            GarageType = st.selectbox("Garage Type", GARAGE_TYPES, key="gt")

        st.divider()

        st.markdown('<div class="group-title">🛏️ Rooms & Location</div>', unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            FullBath = st.number_input(
                "Full Bathrooms", min_value=0, max_value=5, key="fb"
            )
        with r2:
            BedroomAbvGr = st.number_input(
                "Bedrooms", min_value=0, max_value=10, key="bd"
            )
        with r3:
            Neighborhood = st.selectbox("Neighborhood", NEIGHBORHOODS, key="nb")
        with r4:
            SaleCondition = st.selectbox("Sale Condition", SALE_CONDITIONS, key="sc")

        st.divider()

        submitted = st.form_submit_button(
            "🔍 PREDICT HOUSE PRICE", use_container_width=True
        )

    # ---------- Prediction (internal logic same) ----------
    if submitted:

        row = {
            "OverallQual": int(OverallQual),
            "GrLivArea": float(GrLivArea),
            "GarageCars": float(GarageCars),
            "GarageArea": float(GarageArea),
            "TotalBsmtSF": float(TotalBsmtSF),
            "1stFlrSF": float(firstFlrSF),   # model ke training column ka naam
            "FullBath": int(FullBath),
            "BedroomAbvGr": int(BedroomAbvGr),
            "YearBuilt": int(YearBuilt),
            "Neighborhood": Neighborhood,
            "KitchenQual": KitchenQual,
            "GarageType": GarageType,
            "SaleCondition": SaleCondition,
        }

        try:
            model = load_model(str(MODEL_PATH))

            X = pd.DataFrame([row])[FEATURE_COLUMNS]

            with st.spinner("Predicting..."):
                price = round(float(model.predict(X)[0]), 2)

            st.session_state["last"] = {"row": row, "price": price}

        except Exception as e:
            st.session_state.pop("last", None)
            st.error("Prediction fail hui. Neeche error details dekho.")
            with st.expander("View Error Details"):
                st.code(repr(e))

    # ---------- Result ----------
    last = st.session_state.get("last")

    if last:
        row = last["row"]
        price = last["price"]

        tier_label, tier_color = tier_for(price)
        position = (price - PRICE_MIN) / (PRICE_MAX - PRICE_MIN) * 100
        position = min(max(position, 0), 100)

        st.divider()
        st.markdown(
            '<div class="section-title">Prediction Result</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-top">
                    <div class="price-label">Estimated Sale Price</div>
                    <div class="tier-chip"
                         style="color:{tier_color}; border-color:{tier_color};
                                background:{tier_color}1a;">
                        {tier_label}
                    </div>
                </div>
                <div class="price-value">${price:,.2f}</div>
                <div class="price-sub">
                    {row["BedroomAbvGr"]} bed · {row["FullBath"]} bath ·
                    {row["GrLivArea"]:,.0f} sq ft · {row["Neighborhood"]}
                </div>
                <div class="gauge-wrap">
                    <div class="gauge">
                        <div class="gauge-marker" style="left:{position:.1f}%;"></div>
                    </div>
                    <div class="gauge-scale">
                        <span>{short_money(PRICE_MIN)}</span>
                        <span>Market position</span>
                        <span>{short_money(PRICE_MAX)}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        house_age = max(date.today().year - row["YearBuilt"], 0)
        total_area = row["GrLivArea"] + row["TotalBsmtSF"]

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Price per sq ft", f"${price / row['GrLivArea']:,.0f}")
        with m2:
            st.metric("House Age", f"{house_age} years")
        with m3:
            st.metric("Total Area", f"{total_area:,.0f} sq ft")
        with m4:
            st.metric("Overall Quality", f"{row['OverallQual']} / 10")

        st.markdown("#### 📊 Area Breakdown")
        area_df = pd.DataFrame(
            {
                "Area (sq ft)": [
                    row["GrLivArea"],
                    row["1stFlrSF"],
                    row["TotalBsmtSF"],
                    row["GarageArea"],
                ]
            },
            index=["Living Area", "First Floor", "Basement", "Garage"],
        )
        st.bar_chart(area_df)

        with st.expander("📋 View Input Details"):
            st.json(row)

        report = pd.DataFrame([{**row, "predicted_price": price}])
        st.download_button(
            label="📥 Download Prediction Report (CSV)",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name="house_price_prediction.csv",
            mime="text/csv",
            use_container_width=True,
        )


# =====================================================
# TAB 2: WHAT-IF ANALYSIS
# (wahi model, wahi row; ek feature badal ke dekhte hain price kaise badalta hai)
# =====================================================

WHATIF_OPTIONS = {
    "Overall Quality": ("OverallQual", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    "Living Area (sq ft)": ("GrLivArea", [float(v) for v in range(500, 4001, 500)]),
    "Year Built": ("YearBuilt", list(range(1950, 2021, 10))),
    "Garage Cars": ("GarageCars", [0.0, 1.0, 2.0, 3.0, 4.0]),
    "Basement Area (sq ft)": ("TotalBsmtSF", [float(v) for v in range(0, 2501, 500)]),
}

with tab_whatif:

    st.markdown(
        '<div class="section-title">What-if Analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-description">'
        'Same model, same inputs: sirf ek feature badal ke dekho price kaise '
        'react karta hai.'
        '</div>',
        unsafe_allow_html=True,
    )

    last = st.session_state.get("last")

    if not last:
        st.info("Pehle Predict tab mein ek prediction chalao, phir yahan scenarios dekho.")
    else:
        base_row = last["row"]
        base_price = last["price"]

        choice = st.selectbox("Kaunsa feature badalna hai?", list(WHATIF_OPTIONS.keys()))
        column, values = WHATIF_OPTIONS[choice]

        try:
            model = load_model(str(MODEL_PATH))

            rows = []
            for v in values:
                r = dict(base_row)
                r[column] = v
                rows.append(r)

            scenario_X = pd.DataFrame(rows)[FEATURE_COLUMNS]
            scenario_prices = model.predict(scenario_X)

            result_df = pd.DataFrame(
                {
                    choice: values,
                    "Predicted Price ($)": [round(float(p), 2) for p in scenario_prices],
                }
            )

            st.caption(f"Base prediction: ${base_price:,.2f}")

            chart_df = result_df.set_index(choice)
            st.line_chart(chart_df)

            display_df = result_df.copy()
            display_df["Change vs Base"] = display_df["Predicted Price ($)"] - base_price
            st.dataframe(
                display_df.style.format(
                    {
                        "Predicted Price ($)": "${:,.0f}",
                        "Change vs Base": "{:+,.0f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Ye model ka scenario estimate hai (baaki saare features fixed). "
                "Real market price ki guarantee nahi."
            )

        except Exception as e:
            st.error("What-if analysis fail hui.")
            with st.expander("View Error Details"):
                st.code(repr(e))


# =====================================================
# TAB 3: ABOUT
# =====================================================

with tab_about:

    st.markdown(
        '<div class="section-title">About this project</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
**House Price Studio** ek machine learning model se house ka estimated sale price nikalta hai.

**Model kya leta hai (13 features)**
- Quality & age: Overall Quality, Year Built, Kitchen Quality
- Area: Living Area, First Floor Area, Basement Area
- Garage: Cars, Area, Type
- Rooms & location: Full Bathrooms, Bedrooms, Neighborhood, Sale Condition

**Market position bar** price ko ek approximate range ke saamne dikhata hai
(`PRICE_MIN` aur `PRICE_MAX`, code ke top mein badal sakte ho).

**What-if tab** wahi model baar baar chalata hai, har baar sirf ek feature badal ke.

**Tech stack:** Python, scikit-learn, pandas, Streamlit.
        """
    )

    st.warning(
        "Predictions estimates hain aur formal valuation ki jagah nahi le sakte."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">
    HomeAI · House Price Studio | Machine Learning
    <br>
    Built with Python, Streamlit and scikit-learn
    <br>
    Predictions are estimates and should not be treated as a formal valuation.
</div>
""", unsafe_allow_html=True)