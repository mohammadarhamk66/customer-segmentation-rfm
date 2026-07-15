import streamlit as st

from components.animated_charts import animated_business_insights


def show_business_insights(rfm, cluster_profile):
    animated_business_insights()