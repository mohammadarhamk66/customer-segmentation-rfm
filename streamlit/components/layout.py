"""Layout helper for native Streamlit widgets.

The block container is full-bleed so the page iframes render without a seam.
Native widgets therefore need their own inset to line up with the content inside
those iframes — `inset()` reproduces the `.stage` box from components/shell.py
exactly (same max-width, same horizontal padding).
"""

import streamlit as st

INSET_CSS = """
<style>
.st-key-inset {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 26px;
}
</style>
"""


def inset():
    """A container aligned with the iframe content column."""
    st.markdown(INSET_CSS, unsafe_allow_html=True)
    return st.container(key="inset")
