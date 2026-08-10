from pathlib import Path

import pandas as pd
import streamlit as st

from utils.constants import SEGMENT_ORDER


@st.cache_data
def load_data():
    base_path = Path(__file__).resolve().parents[2]

    rfm_path = base_path / "data" / "processed" / "rfm_customer_segments.csv"
    cluster_path = base_path / "data" / "processed" / "cluster_profile.csv"

    rfm = pd.read_csv(rfm_path)
    cluster_profile = pd.read_csv(cluster_path)

    # Clean segment labels to avoid filtering issues caused by hidden spaces
    rfm["Segment"] = rfm["Segment"].str.strip()
    cluster_profile["Segment"] = cluster_profile["Segment"].str.strip()

    fix = {"Recent Occassional Customers": "Recent Occasional Customers"}
    rfm["Segment"] = rfm["Segment"].replace(fix)
    cluster_profile["Segment"] = cluster_profile["Segment"].replace(fix)

    # Keep a stable, business-meaningful ordering everywhere in the app.
    order = {name: i for i, name in enumerate(SEGMENT_ORDER)}
    cluster_profile = (
        cluster_profile.assign(_o=cluster_profile["Segment"].map(order))
        .sort_values("_o")
        .drop(columns="_o")
        .reset_index(drop=True)
    )

    return rfm, cluster_profile


@st.cache_data
def compute_kpis(rfm, cluster_profile):
    """Headline numbers used across the executive surfaces."""
    total_customers = int(len(rfm))
    total_revenue = float(rfm["Monetary"].sum())

    top = cluster_profile[
        cluster_profile["Segment"] == "High-Value Loyal Customers"
    ].iloc[0]

    return {
        "total_customers": total_customers,
        "total_revenue": total_revenue,
        "avg_order_value": float(rfm["Monetary"].sum() / rfm["Frequency"].sum()),
        "avg_monetary": float(rfm["Monetary"].mean()),
        "median_recency": float(rfm["Recency"].median()),
        "avg_frequency": float(rfm["Frequency"].mean()),
        "top_segment_revenue_share": float(top["Revenue_Share_%"]),
        "top_segment_customer_share": float(top["Customer_Share_%"]),
        "segments": int(cluster_profile.shape[0]),
    }


@st.cache_data
def scatter_sample(rfm, n=900, seed=7):
    """A deterministic sample of customers for the 3D RFM point cloud."""
    if len(rfm) <= n:
        sample = rfm
    else:
        sample = rfm.sample(n=n, random_state=seed)

    return sample[["Recency", "Frequency", "Monetary", "Segment"]].to_dict("records")
