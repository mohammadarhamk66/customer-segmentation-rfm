import streamlit as st

def open_section_card():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

def close_section_card():
    st.markdown('</div>', unsafe_allow_html=True)