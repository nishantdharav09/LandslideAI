import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LandslideAI Monitoring",
    page_icon="🚨",
    layout="wide"
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(
    r"C:\Users\Nishant Dharav\OneDrive\Desktop"
    r"\LandslideAI"
)

REPORT_PATH = (
    BASE_DIR
    / "predictions"
    / "landslide_risk_report.csv"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        color: #64748b;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    .risk-high {
        color: #dc2626;
        font-weight: 700;
    }

    .risk-moderate {
        color: #d97706;
        font-weight: 700;
    }

    .risk-low {
        color: #16a34a;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">🚨 LandslideAI Monitoring Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'AI-powered landslide detection, prediction and preliminary risk monitoring'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD REPORT
# ============================================================

if not REPORT_PATH.exists():

    st.error(
        "Risk report not found."
    )

    st.info(
        "Run export_risk_report.py first."
    )

    st.stop()


df = pd.read_csv(REPORT_PATH)


# ============================================================
# DATA PREPARATION
# ============================================================

total_images = len(df)

average_area = df[
    "Predicted_Area_Percent"
].mean()

average_probability = df[
    "Mean_Probability"
].mean()

average_risk = df[
    "Risk_Score"
].mean()

very_high_count = (
    df["Risk_Level"] == "Very High"
).sum()

high_count = (
    df["Risk_Level"] == "High"
).sum()

moderate_count = (
    df["Risk_Level"] == "Moderate"
).sum()

low_count = (
    df["Risk_Level"] == "Low"
).sum()


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Images Analyzed",
        f"{total_images:,}"
    )

with col2:
    st.metric(
        "Average Landslide Area",
        f"{average_area:.2f}%"
    )

with col3:
    st.metric(
        "Average Confidence",
        f"{average_probability:.2%}"
    )

with col4:
    st.metric(
        "Average Risk Score",
        f"{average_risk:.2f}/100"
    )


st.divider()


# ============================================================
# RISK SUMMARY
# ============================================================

st.subheader("⚠️ Risk Distribution")

risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)

with risk_col1:
    st.metric(
        "🟢 Low",
        low_count
    )

with risk_col2:
    st.metric(
        "🟡 Moderate",
        moderate_count
    )

with risk_col3:
    st.metric(
        "🟠 High",
        high_count
    )

with risk_col4:
    st.metric(
        "🔴 Very High",
        very_high_count
    )


# ============================================================
# RISK CHART
# ============================================================

risk_counts = (
    df["Risk_Level"]
    .value_counts()
    .reindex(
        [
            "Low",
            "Moderate",
            "High",
            "Very High"
        ],
        fill_value=0
    )
)

st.bar_chart(risk_counts)


# ============================================================
# TOP HIGH-RISK IMAGES
# ============================================================

st.divider()

st.subheader("🔴 Highest-Risk Predictions")

top_risk = (
    df.sort_values(
        "Risk_Score",
        ascending=False
    )
    .head(10)
    .copy()
)

top_risk_display = top_risk[
    [
        "Image",
        "Predicted_Area_Percent",
        "Mean_Probability",
        "Risk_Score",
        "Risk_Level"
    ]
]

top_risk_display = (
    top_risk_display
    .rename(
        columns={
            "Image": "Image",
            "Predicted_Area_Percent": "Area (%)",
            "Mean_Probability": "Confidence",
            "Risk_Score": "Risk Score",
            "Risk_Level": "Risk Level"
        }
    )
)

st.dataframe(
    top_risk_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FILTER
# ============================================================

st.divider()

st.subheader("🔎 Explore Predictions")

selected_risk = st.selectbox(
    "Select Risk Level",
    [
        "All",
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
)

if selected_risk == "All":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["Risk_Level"] == selected_risk
    ].copy()


st.write(
    f"Showing **{len(filtered_df)}** predictions."
)


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "LandslideAI | AI-based landslide segmentation and "
    "preliminary risk monitoring system"
)

st.caption(
    "Note: Risk scores shown here are AI-derived preliminary "
    "indicators and should not be treated as official disaster warnings."
)