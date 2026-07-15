import streamlit as st

def render_page_header(eyebrow, title, subtitle):
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-eyebrow">{eyebrow}</div>
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>    
        """,
        unsafe_allow_html=True
    )