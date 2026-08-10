import streamlit as st

from components.theme import apply_mobile_gate, apply_theme
from utils.constants import APP_SUBTITLE, APP_TITLE
from utils.data_loader import compute_kpis, load_data, scatter_sample
from views.about_project import show_about_project
from views.ai_analyst import show_ai_analyst
from views.business_insights import show_business_insights
from views.executive_overview import show_executive_overview
from views.segment_explorer import show_segment_explorer

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
apply_mobile_gate()

rfm, cluster_profile = load_data()
kpis = compute_kpis(rfm, cluster_profile)
sample = scatter_sample(rfm)

NAV = [
    ("About Project", "01", show_about_project),
    ("Executive Overview", "02", show_executive_overview),
    ("Segment Explorer", "03", show_segment_explorer),
    ("Business Insights", "04", show_business_insights),
    ("AI Analyst", "05", show_ai_analyst),
]

if "page" not in st.session_state:
    st.session_state.page = "About Project"

st.sidebar.markdown(
    f"""
    <div class="sidebar-brand">
        <div class="brand-logo"></div>
        <div>
            <div class="brand-title">{APP_TITLE}</div>
            <div class="brand-subtitle">{APP_SUBTITLE}</div>
        </div>
    </div>
    <div class="sidebar-divider"></div>
    <div class="nav-label">Navigation</div>
    """,
    unsafe_allow_html=True,
)

for name, num, _ in NAV:
    active = st.session_state.page == name
    # `type` drives the kind="primary"/"secondary" attribute the CSS keys off —
    # a wrapper <div> can't work here because Streamlit isolates each markdown block.
    if st.sidebar.button(
        f"{num}   {name}",
        key=f"nav_{name}",
        use_container_width=True,
        type="primary" if active else "secondary",
    ):
        st.session_state.page = name
        st.rerun()

st.sidebar.markdown(
    f"""
    <div class="sidebar-foot">
        <b>{kpis['total_customers']:,} customers</b> · <b>{kpis['segments']} segments</b><br>
        RFM analysis with K-Means clustering on the UCI Online Retail dataset.
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.session_state.page
for name, _, view in NAV:
    if name == page:
        view(rfm, cluster_profile, kpis, sample)
        break
