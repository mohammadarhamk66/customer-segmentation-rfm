import streamlit as st

from views.about_project import show_about_project
from views.executive_overview import show_executive_overview
from views.segment_explorer import show_segment_explorer
from views.business_insights import show_business_insights
from utils.data_loader import load_data


st.set_page_config(
    page_title="Customer Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        .stApp {
            background:
                radial-gradient(circle at 85% 8%, rgba(201,122,40,.08), transparent 28%),
                linear-gradient(180deg, #FFFFFF 0%, #F3F6FA 100%);
        }

        h1, h2, h3 {
            color: #111827;
            letter-spacing: -0.03em;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #172233 0%, #111827 100%);
        }

        [data-testid="stSidebar"] * {
            color: #F9FAFB;
        }

        .sidebar-brand {
            display: flex;
            gap: 14px;
            align-items: center;
            padding: 18px 4px 22px 4px;
        }

        .brand-logo {
            width: 52px;
            height: 52px;
            border-radius: 16px;
            background:
                radial-gradient(circle at 30% 25%, #F3A64A 0%, #D9822B 45%, #9A5A1F 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 14px 32px rgba(217,130,43,.28);
            position: relative;
            overflow: hidden;
        }

        .brand-logo::before {
            content: "";
            position: absolute;
            width: 34px;
            height: 34px;
            border: 2px solid rgba(255,255,255,.65);
            border-radius: 10px;
            transform: rotate(18deg);
        }

        .brand-logo::after {
            content: "CI";
            position: relative;
            font-weight: 900;
            font-size: 15px;
            color: #FFFFFF;
            letter-spacing: .04em;
        }

        .brand-title {
            font-size: 17px;
            font-weight: 850;
            line-height: 1.15;
            color: #FFFFFF;
        }

        .brand-subtitle {
            font-size: 12px;
            color: #CBD5E1;
            margin-top: 6px;
            line-height: 1.35;
        }

        .sidebar-divider {
            height: 1px;
            background: rgba(255,255,255,.14);
            margin: 10px 0 22px 0;
        }

        .nav-label {
            font-size: 11px;
            font-weight: 800;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: .12em;
            margin: 0 0 10px 4px;
        }

        div[data-testid="stButton"] > button {
            width: 100%;
            border: none;
            background: transparent;
            color: #E5E7EB;
            text-align: left;
            justify-content: flex-start;
            padding: 14px 16px;
            border-radius: 16px;
            font-size: 15px;
            font-weight: 800;
            transition: all .22s ease;
            box-shadow: none;
        }

        div[data-testid="stButton"] > button:hover {
            background: rgba(255,255,255,.08);
            color: #FFFFFF;
            transform: translateX(4px);
        }

        div[data-testid="stButton"] > button:focus {
            box-shadow: none;
            outline: none;
        }

        .active-nav {
            background: rgba(217,130,43,.22);
            border-left: 4px solid #D9822B;
            border-radius: 16px;
            padding: 0;
            margin-bottom: 10px;
            box-shadow: inset 0 0 0 1px rgba(217,130,43,.18);
        }

        .inactive-nav {
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    return load_data()


rfm, cluster_profile = get_data()


if "page" not in st.session_state:
    st.session_state.page = "About Project"


def set_page(page_name):
    st.session_state.page = page_name


st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="brand-logo"></div>
        <div>
            <div class="brand-title">Customer Intelligence Platform</div>
            <div class="brand-subtitle">Customer Segmentation & Insights</div>
        </div>
    </div>
    <div class="sidebar-divider"></div>
    <div class="nav-label">Navigation</div>
    """,
    unsafe_allow_html=True,
)


nav_items = [
    ("About Project", "01"),
    ("Executive Overview", "02"),
    ("Segment Explorer", "03"),
    ("Business Insights", "04"),
]


for page_name, icon in nav_items:
    wrapper_class = "active-nav" if st.session_state.page == page_name else "inactive-nav"

    st.sidebar.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)

    if st.sidebar.button(
        f"{icon}  {page_name}",
        key=f"nav_{page_name}",
        use_container_width=True,
    ):
        set_page(page_name)
        st.rerun()

    st.sidebar.markdown("</div>", unsafe_allow_html=True)


page = st.session_state.page


if page == "About Project":
    show_about_project()

elif page == "Executive Overview":
    show_executive_overview(rfm, cluster_profile)

elif page == "Segment Explorer":
    show_segment_explorer(rfm, cluster_profile)

elif page == "Business Insights":
    show_business_insights(rfm, cluster_profile)