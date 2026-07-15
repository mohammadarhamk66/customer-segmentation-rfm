import streamlit as st

from components.animated_charts import animated_distribution_panel


def show_executive_overview(rfm, cluster_profile):
    st.subheader("Executive Overview")

    animated_distribution_panel(cluster_profile)