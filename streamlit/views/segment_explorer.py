import streamlit as st

from components.kpi_cards import render_kpi_card
from components.animated_charts import (
    animated_rfm_distributions,
    animated_segment_details,
)


SEGMENT_PROFILES = {
    "High-Value Loyal Customers": "These customers purchased recently, buy frequently, and spend significantly more than other customer groups.",
    "Mid-Value Regular Customers": "These customers purchase consistently and contribute meaningful revenue, but still have room to grow in value.",
    "Recent Occasional Customers": "These customers purchased recently but do not yet show strong repeat behavior or high spending.",
    "Inactive Low-Value Customers": "These customers have not purchased recently, buy infrequently, and contribute relatively little revenue.",
}


RECOMMENDED_ACTIONS = {
    "High-Value Loyal Customers": [
        "Prioritize retention efforts",
        "Offer loyalty rewards",
        "Provide early access to new products",
        "Use personalized recommendations",
    ],
    "Mid-Value Regular Customers": [
        "Increase basket size through bundles",
        "Use cross-sell campaigns",
        "Encourage repeat purchases",
        "Test targeted upgrade offers",
    ],
    "Recent Occasional Customers": [
        "Encourage second purchase",
        "Send onboarding-style campaigns",
        "Recommend related products",
        "Use limited-time conversion offers",
    ],
    "Inactive Low-Value Customers": [
        "Use low-cost automated re-engagement",
        "Avoid heavy personalized marketing spend",
        "Test limited-time offers",
        "Suppress from expensive campaigns if unresponsive",
    ],
}


def show_segment_explorer(rfm, cluster_profile):
    st.subheader("Segment Explorer")

    filter_col, _ = st.columns([1.4, 2.6])

    with filter_col:
        selected_segment = st.selectbox(
            "Select a Customer Segment",
            cluster_profile["Segment"].tolist(),
        )

    selected_profile = cluster_profile[
        cluster_profile["Segment"] == selected_segment
    ].iloc[0]

    segment_customers = rfm[rfm["Segment"] == selected_segment].copy()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        render_kpi_card(
            "Customers",
            f"{int(selected_profile['Customer_Count']):,}",
        )

    with kpi2:
        render_kpi_card(
            "Customer Share",
            f"{selected_profile['Customer_Share_%']:.2f}%",
        )

    with kpi3:
        render_kpi_card(
            "Revenue Share",
            f"{selected_profile['Revenue_Share_%']:.2f}%",
        )

    with kpi4:
        render_kpi_card(
            "Avg Monetary Value",
            f"£{selected_profile['Avg_Monetary']:,.0f}",
        )

    st.markdown("---")

    st.subheader("Segment Distributions")

    animated_rfm_distributions(
        rfm,
        selected_segment,
    )

    profile_text = SEGMENT_PROFILES.get(
        selected_segment,
        "This segment has a distinct customer behavior profile based on recency, frequency, and monetary value.",
    )

    recommended_actions = RECOMMENDED_ACTIONS.get(
        selected_segment,
        ["Review segment behavior and define targeted actions."],
    )

    animated_segment_details(
        selected_segment,
        profile_text,
        recommended_actions,
        segment_customers,
    )