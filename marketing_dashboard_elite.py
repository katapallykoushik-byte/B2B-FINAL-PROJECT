# ============================================================
# B2B MARKETING CAMPAIGN ANALYTICS DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
st.markdown("""
<style>
[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Marketing Dashboard", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("b2b_marketing_dataset_final-1.csv")

df = load_data()

# =========================
# CLEAN DATA
# =========================
df = df.drop_duplicates()

# =========================
# KPI CALCULATIONS
# =========================

# Total Campaigns
total_campaigns = df["Campaign_ID"].nunique()

# Conversion Rate (use existing column)
conversion_rate = df["Conversion_Rate"].mean() * 100

# ROI (use existing column)
roi = df["ROI"].mean() * 100

# Revenue
total_revenue = df["Revenue"].sum()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

channel_filter = st.sidebar.multiselect(
    "Channel",
    df["Channel"].unique(),
    default=df["Channel"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Channel"].isin(channel_filter)) &
    (df["Region"].isin(region_filter))
]

# =========================
# HEADER
# =========================
st.title("B2B Marketing Campaign Performance Dashboard")

st.write("Track campaign performance, conversion efficiency, and ROI.")

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Campaigns", total_campaigns)
col2.metric("Conversion Rate (%)", round(conversion_rate, 2))
col3.metric("ROI (%)", round(roi, 2))
col4.metric("Revenue", f"${round(total_revenue, 2)}")
st.markdown("---")
st.subheader("📊 Executive Summary")

top_channel = filtered_df.groupby("Channel")["Revenue"].sum().idxmax()
top_region = filtered_df.groupby("Region")["Conversion_Rate"].mean().idxmax()

st.success(f"Top Performing Channel: {top_channel}")
st.info(f"Best Region for Conversion: {top_region}")

if roi > 0:
    st.success("Overall Campaigns are Profitable")
else:
    st.error("Campaign ROI is Negative — Optimization Needed")

# =========================
# CHART 1: CHANNEL PERFORMANCE
# =========================
st.subheader("Channel Performance (Revenue by Channel)")

channel_perf = filtered_df.groupby("Channel")["Revenue"].sum().reset_index()

fig1 = px.bar(
    channel_perf,
    x="Channel",
    y="Revenue",
    color="Channel",
    title="Revenue by Channel"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2: CONVERSION RATE BY REGION
# =========================
st.subheader("Conversion Rate by Region")

region_conv = filtered_df.groupby("Region")["Conversion_Rate"].mean().reset_index()

fig2 = px.bar(
    region_conv,
    x="Region",
    y="Conversion_Rate",
    color="Region",
    title="Average Conversion Rate by Region"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# CHART 3: BUDGET vs REVENUE
# =========================
st.subheader("Budget vs Revenue")

fig3 = px.scatter(
    filtered_df,
    x="Budget",
    y="Revenue",
    color="Channel",
    size="Conversions",
    title="Budget vs Revenue"
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown("---")
st.subheader("🏆 Top Performing Campaigns")

top_campaigns = filtered_df.sort_values(
    "Revenue", ascending=False
).head(10)

st.dataframe(top_campaigns)
st.subheader("⚠️ Campaign Alerts")

low_perf = filtered_df[
    (filtered_df["ROI"] < 0) | (filtered_df["Conversion_Rate"] < 0.1)
]

if len(low_perf) > 0:
    st.warning(f"{len(low_perf)} campaigns need attention")
    st.dataframe(low_perf.head(5))
else:
    st.success("All campaigns performing well")

    
    st.markdown("---")
st.caption("B2B Marketing Analytics Dashboard | Built using Streamlit & Python")

# =========================
# END
# ============================================================