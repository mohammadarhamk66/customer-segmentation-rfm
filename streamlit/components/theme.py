"""Parent-document styling.

The page bodies live inside iframes (see `shell.py`); this module styles the
Streamlit chrome around them — background, sidebar, navigation, chat surface —
so the two read as one continuous product.
"""

import streamlit as st
import streamlit.components.v1 as components

PARENT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }

/* Base canvas. Deliberately flat and identical to the *base* layer of the page
   iframes (components/shell.py → .bg-mesh) — the iframes paint their orbs on top
   of this same colour, so the joins between iframe and parent stay invisible. */
.stApp {
    background: linear-gradient(175deg, #070B14 0%, #0C1322 55%, #070B14 100%);
    background-attachment: fixed;
    color: #F1F5F9;
}

/* full bleed — the page iframes carry their own padding, so any container
   padding here shows up as a visible seam around them */
.main .block-container,
.stMainBlockContainer,
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding: 0 0 1.5rem 0 !important;
}
[data-testid="stMain"] { background: transparent; }
/* views that need native widgets inset them with `gutter()` (see components/layout) */

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

h1, h2, h3, h4 { color: #FFFFFF; font-family: 'Sora','Inter',sans-serif; letter-spacing: -.025em; }
p, span, label, li { color: #CBD5E1; }

/* ---------------- sidebar ---------------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(12,19,34,.94) 0%, rgba(7,11,20,.97) 100%);
    border-right: 1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
}
[data-testid="stSidebar"] * { color: #E2E8F0; }
[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

.sidebar-brand { display: flex; gap: 14px; align-items: center; padding: 6px 2px 20px 2px; }

.brand-logo {
    width: 50px; height: 50px; border-radius: 16px; flex: 0 0 50px;
    background: radial-gradient(circle at 30% 25%, #F3A64A 0%, #D9822B 48%, #8B4A16 100%);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 14px 34px rgba(217,130,43,.34), inset 0 1px 0 rgba(255,255,255,.4);
    position: relative; overflow: hidden;
    animation: logoFloat 5.5s ease-in-out infinite;
}
@keyframes logoFloat {
    0%,100% { transform: translateY(0) rotate(0deg); }
    50%     { transform: translateY(-5px) rotate(2.5deg); }
}
.brand-logo::before {
    content: ""; position: absolute; width: 32px; height: 32px;
    border: 2px solid rgba(255,255,255,.62); border-radius: 10px; transform: rotate(18deg);
}
.brand-logo::after {
    content: "CI"; position: relative; font-weight: 900; font-size: 14px;
    color: #FFF; letter-spacing: .04em;
}

.brand-title { font-size: 15.5px; font-weight: 800; line-height: 1.2; color: #FFFFFF; }
.brand-subtitle { font-size: 11.5px; color: #94A3B8; margin-top: 5px; line-height: 1.4; }

.sidebar-divider { height: 1px; background: rgba(255,255,255,.10); margin: 4px 0 20px 0; }

.nav-label {
    font-size: 10px; font-weight: 800; color: #64748B;
    text-transform: uppercase; letter-spacing: .16em; margin: 0 0 12px 3px;
}

/* nav buttons */
[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    width: 100%; border: 1px solid transparent; background: rgba(255,255,255,.02);
    color: #CBD5E1; text-align: left; justify-content: flex-start;
    padding: 13px 15px; border-radius: 15px;
    font-size: 14px; font-weight: 700; letter-spacing: -.01em;
    transition: transform .3s cubic-bezier(.2,.8,.25,1), background .3s ease,
                color .3s ease, border-color .3s ease, box-shadow .3s ease;
    box-shadow: none;
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: rgba(255,255,255,.07);
    border-color: rgba(255,255,255,.14);
    color: #FFFFFF;
    transform: translateX(5px) translateZ(0);
    box-shadow: 0 10px 26px rgba(0,0,0,.34);
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button:focus { box-shadow: none; outline: none; }

/* active page — Streamlit stamps kind="primary" on the button element */
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(100deg, rgba(243,166,74,.22), rgba(139,92,246,.14));
    border-color: rgba(243,166,74,.38);
    color: #FFFFFF;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.14), 0 10px 26px rgba(217,130,43,.16);
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(100deg, rgba(243,166,74,.30), rgba(139,92,246,.18));
    border-color: rgba(243,166,74,.55);
}
[data-testid="stSidebar"] div[data-testid="stButton"] { margin-bottom: 9px; }

.sidebar-foot {
    margin-top: 26px; padding: 15px 16px; border-radius: 16px;
    background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.08);
    font-size: 11.5px; line-height: 1.6; color: #94A3B8;
}
.sidebar-foot b { color: #E2E8F0; font-weight: 700; }

/* ---------------- widgets ---------------- */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 14px; color: #F1F5F9;
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    transition: border-color .3s ease, box-shadow .3s ease;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
    border-color: rgba(243,166,74,.45);
    box-shadow: 0 10px 28px rgba(0,0,0,.3);
}
[data-testid="stSelectbox"] label { color: #94A3B8 !important; font-size: 11px !important;
    font-weight: 800 !important; letter-spacing: .13em; text-transform: uppercase; }
div[data-baseweb="popover"] div { background: #0F172A; color: #E2E8F0; }

/* ---------------- chat ---------------- */
[data-testid="stChatMessage"] {
    background: linear-gradient(150deg, rgba(255,255,255,.07), rgba(255,255,255,.035));
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 20px; padding: 16px 20px; margin-bottom: 14px;
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    box-shadow: 0 16px 40px rgba(0,0,0,.32), inset 0 1px 0 rgba(255,255,255,.08);
    transition: transform .45s cubic-bezier(.2,.8,.25,1), box-shadow .45s ease;
    animation: msgIn .5s cubic-bezier(.2,.8,.25,1) both;
}
[data-testid="stChatMessage"]:hover {
    transform: translateY(-3px) translateZ(0);
    box-shadow: 0 26px 60px rgba(0,0,0,.44), inset 0 1px 0 rgba(255,255,255,.12);
}
@keyframes msgIn {
    from { opacity: 0; transform: translate3d(0, 20px, -40px); }
    to   { opacity: 1; transform: none; }
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { color: #E2E8F0; font-size: 14.5px; line-height: 1.7; }
[data-testid="stChatMessage"] strong { color: #FFFFFF; }
[data-testid="stChatMessage"] code {
    background: rgba(243,166,74,.13); color: #FCD9A0;
    padding: 2px 7px; border-radius: 6px; font-size: 13px;
}
[data-testid="stChatMessage"] table { width: 100%; border-collapse: collapse; font-size: 13px; }
[data-testid="stChatMessage"] th, [data-testid="stChatMessage"] td {
    padding: 9px 12px; border-bottom: 1px solid rgba(255,255,255,.08); text-align: left;
}

[data-testid="stChatInput"] {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 18px;
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}
[data-testid="stChatInput"] textarea { color: #F1F5F9 !important; }

/* expander (AI reasoning trace) */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px; overflow: hidden;
}
[data-testid="stExpander"] summary { color: #94A3B8; font-size: 12.5px; font-weight: 700; }

/* alerts */
[data-testid="stAlert"] {
    background: rgba(243,166,74,.09);
    border: 1px solid rgba(243,166,74,.26);
    border-radius: 16px; color: #E2E8F0;
}

/* scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,.13); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(243,166,74,.42); }

iframe { border: none !important; color-scheme: normal; }
</style>
"""


MOBILE_GATE = """
<script>
    const doc = window.parent.document;
    const isMobile =
        /Android|iPhone|iPad|iPod|Opera Mini|IEMobile|Mobile/i.test(navigator.userAgent)
        || window.parent.innerWidth < 900;

    if (isMobile && !doc.getElementById('desktop-gate')) {
        const gate = doc.createElement('div');
        gate.id = 'desktop-gate';
        gate.style.cssText = `
            position:fixed; inset:0; z-index:99999;
            display:flex; align-items:center; justify-content:center;
            padding:24px; box-sizing:border-box;
            background:linear-gradient(175deg,#070B14 0%,#0C1322 55%,#070B14 100%);
            font-family:Inter,-apple-system,sans-serif;`;
        gate.innerHTML = `
            <div style="
                max-width:430px; padding:36px 32px; text-align:center;
                background:linear-gradient(150deg,rgba(255,255,255,.075),rgba(255,255,255,.045));
                border:1px solid rgba(255,255,255,.12); border-radius:26px;
                box-shadow:0 24px 60px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.10);
                backdrop-filter:blur(22px); -webkit-backdrop-filter:blur(22px);">
                <div style="font-size:52px;line-height:1">🖥️</div>
                <h2 style="margin:18px 0 0;color:#FFF;font-size:22px;
                           font-weight:800;letter-spacing:-.02em">
                    Desktop experience recommended
                </h2>
                <p style="color:#94A3B8;line-height:1.7;font-size:14.5px;margin-top:14px">
                    This Customer Intelligence Platform is built around 3D visualisations,
                    hover interactions and animation designed for larger screens.
                    <br><br>
                    Please open it on a desktop or laptop browser for the full experience.
                </p>
            </div>`;
        doc.body.appendChild(gate);
    }
</script>
"""


def apply_theme():
    st.markdown(PARENT_CSS, unsafe_allow_html=True)


def apply_mobile_gate():
    """Show a desktop-recommended screen on small viewports.

    Carried over from the previous version of the app: this interface depends on
    hover, 3D tilt and wide multi-column layouts, so it degrades badly below
    ~900px rather than merely looking cramped.
    """
    components.html(MOBILE_GATE, height=0)
