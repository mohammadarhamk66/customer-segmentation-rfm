import re
import streamlit.components.v1 as components


def _extract_number(value):
    cleaned = re.sub(r"[^\d.]", "", str(value))
    return float(cleaned) if cleaned else 0


def render_kpi_card(label, value, help_text=None):
    end_value = _extract_number(value)
    prefix = "£" if str(value).startswith("£") else ""
    suffix = "%" if str(value).endswith("%") else ""
    decimals = 2 if suffix == "%" else 0

    help_html = f"<div class='kpi-help'>{help_text}</div>" if help_text else ""

    components.html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">
                {prefix}<span id="counter">0</span>{suffix}
            </div>
            {help_html}
        </div>

        <style>
        .kpi-card {{
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 1.1rem 1.25rem;
            min-height: 100px;
            box-shadow: 0 6px 18px rgba(15,23,42,.05);
            font-family: Inter, sans-serif;
            transition: all .22s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 14px 32px rgba(15,23,42,.09);
        }}

        .kpi-label {{
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            color: #6B7280;
            font-weight: 700;
            margin-bottom: .65rem;
        }}

        .kpi-value {{
            font-size: 2.25rem;
            font-weight: 800;
            color: #111827;
            line-height: 1.05;
        }}

        .kpi-help {{
            margin-top: .75rem;
            color: #6B7280;
            font-size: .82rem;
            line-height: 1.45;
        }}
        </style>

        <script>
        const counter = document.getElementById("counter");
        const end = {end_value};
        const decimals = {decimals};
        const duration = 850;
        const startTime = performance.now();

        function formatNumber(num) {{
            return num.toLocaleString(undefined, {{
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            }});
        }}

        function animate(currentTime) {{
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = formatNumber(end * eased);

            if (progress < 1) {{
                requestAnimationFrame(animate);
            }}
        }}

        requestAnimationFrame(animate);
        </script>
        """,
        height=125,
    )