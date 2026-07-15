import streamlit as st

def render_section_card(title, body):
    st.markdown(
        f"""
        <div class="content-card">
            <h3>{title}</h3>
            <div class="card-body">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )