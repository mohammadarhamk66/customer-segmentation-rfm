from pathlib import Path

import pandas as pd
import streamlit as st

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

    rfm["Segment"] = rfm["Segment"].replace({
        "Recent Occassional Customers": "Recent Occasional Customers"
    })

    return rfm, cluster_profile