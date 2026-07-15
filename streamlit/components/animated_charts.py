import math
import streamlit.components.v1 as components
import numpy as np

from utils.constants import SEGMENT_COLORS


def polar_to_cartesian(cx, cy, r, angle_degrees):
    angle_radians = math.radians(angle_degrees - 90)
    return (
        cx + r * math.cos(angle_radians),
        cy + r * math.sin(angle_radians),
    )


def describe_arc(cx, cy, r, start_angle, end_angle):
    start = polar_to_cartesian(cx, cy, r, end_angle)
    end = polar_to_cartesian(cx, cy, r, start_angle)
    large_arc_flag = 1 if end_angle - start_angle > 180 else 0

    return (
        f"M {start[0]} {start[1]} "
        f"A {r} {r} 0 {large_arc_flag} 0 {end[0]} {end[1]}"
    )


def animated_distribution_panel(cluster_profile):
    data = cluster_profile.sort_values("Revenue_Share_%", ascending=False)

    total_customers = int(cluster_profile["Customer_Count"].sum())
    total_segments = cluster_profile["Segment"].nunique()
    total_revenue = int(
        (cluster_profile["Customer_Count"] * cluster_profile["Avg_Monetary"]).sum()
    )

    insights = {
        "High-Value Loyal Customers": "This segment is the business-critical retention group. They represent a small share of customers but generate most revenue, so loyalty rewards, early access, and personalized engagement should be prioritized.",
        "Mid-Value Regular Customers": "This segment is the strongest growth opportunity. They already purchase regularly and contribute meaningful revenue, so campaigns should focus on increasing basket size, bundles, and cross-sell opportunities.",
        "Recent Occasional Customers": "This segment is active but not yet loyal. The business should focus on converting them into repeat buyers through onboarding, related product recommendations, and second-purchase incentives.",
        "Inactive Low-Value Customers": "This segment should be managed with cost discipline. Because they contribute limited revenue, re-engagement should rely on low-cost automation rather than heavy personalized marketing spend.",
    }

    insight_titles = {
        "High-Value Loyal Customers": "Retention Priority",
        "Mid-Value Regular Customers": "Growth Opportunity",
        "Recent Occasional Customers": "Conversion Opportunity",
        "Inactive Low-Value Customers": "Cost-Efficient Reactivation",
    }

    rows_html = ""
    donut_segments = ""
    donut_labels = ""
    table_rows = ""

    total_share = data["Customer_Share_%"].sum()
    start_angle = 0

    for _, row in data.iterrows():
        segment = row["Segment"]
        segment_id = segment.replace(" ", "-").lower()
        color = SEGMENT_COLORS[segment]

        revenue = float(row["Revenue_Share_%"])
        customer_share = float(row["Customer_Share_%"])
        customers = int(row["Customer_Count"])
        avg_recency = float(row["Avg_Recency"])
        avg_frequency = float(row["Avg_Frequency"])
        avg_monetary = float(row["Avg_Monetary"])
        segment_revenue_amount = int(customers * avg_monetary)

        rows_html += f"""
        <div
            class="dist-row"
            data-segment="{segment_id}"
            data-name="{segment}"
            data-title="{insight_titles[segment]}"
            data-insight="{insights[segment]}"
            data-color="{color}"
            data-customers="{customers:,}"
            data-revenue="{revenue:.2f}%"
            data-revenue-amount="£{segment_revenue_amount:,.0f}"
        >
            <div class="dist-label">{segment}</div>
            <div class="dist-track">
                <div class="dist-fill" style="--width:{revenue}%; --color:{color};"></div>
            </div>
            <div class="dist-value">{revenue:.2f}%</div>
        </div>
        """

        angle = (customer_share / total_share) * 360
        end_angle = start_angle + angle
        path = describe_arc(100, 100, 70, start_angle, end_angle)

        mid_angle = start_angle + (angle / 2)
        label_x, label_y = polar_to_cartesian(100, 100, 70, mid_angle)

        donut_segments += f"""
        <path
            class="donut-segment"
            data-segment="{segment_id}"
            data-name="{segment}"
            data-title="{insight_titles[segment]}"
            data-share="{customer_share:.2f}"
            data-customers="{customers:,}"
            data-insight="{insights[segment]}"
            data-color="{color}"
            data-revenue="{revenue:.2f}%"
            data-revenue-amount="£{segment_revenue_amount:,.0f}"
            d="{path}"
            fill="none"
            stroke="{color}"
            stroke-width="34"
            stroke-linecap="butt"
        ></path>
        """

        donut_labels += f"""
        <div
            class="donut-html-label"
            style="left:{label_x / 2}%; top:{label_y / 2}%;"
        >
            {customer_share:.1f}%
        </div>
        """

        table_rows += f"""
        <tr data-segment="{segment_id}">
            <td><span class="segment-dot" style="background:{color};"></span>{segment}</td>
            <td>{customers:,}</td>
            <td>{customer_share:.2f}%</td>
            <td>{revenue:.2f}%</td>
            <td>{avg_recency:.1f}</td>
            <td>{avg_frequency:.1f}</td>
            <td>£{avg_monetary:,.0f}</td>
        </tr>
        """

        start_angle = end_angle

    components.html(
        f"""
        <div class="executive-panel">

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div id="kpi-label-1" class="kpi-label">Total Customers</div>
                    <div id="kpi-customers" class="kpi-value">{total_customers:,}</div>
                </div>

                <div class="kpi-card">
                    <div id="kpi-label-2" class="kpi-label">Customer Segments</div>
                    <div id="kpi-segments" class="kpi-value">{total_segments}</div>
                </div>

                <div class="kpi-card">
                    <div id="kpi-label-3" class="kpi-label">Total Revenue</div>
                    <div id="kpi-revenue" class="kpi-value">£{total_revenue:,.0f}</div>
                </div>
            </div>

            <div class="distribution-panel">
                <div class="dist-card">
                    <div class="card-title">Revenue Distribution</div>
                    <div class="card-subtitle">Click a segment to isolate its revenue contribution.</div>
                    <div class="dist-body">{rows_html}</div>
                </div>

                <div class="dist-card">
                    <div class="card-title">Customer Distribution</div>
                    <div class="card-subtitle">Hover over a slice to view customer share.</div>

                    <div class="donut-wrap">
                        <div class="donut-stage">
                            <svg viewBox="0 0 200 200">
                                {donut_segments}
                                <circle cx="100" cy="100" r="44" fill="#FFFFFF"></circle>
                            </svg>

                            {donut_labels}
                        </div>
                    </div>

                    <div id="tooltip" class="tooltip"></div>
                </div>
            </div>

            <div id="status-banner" class="status-banner">
                Click any segment in the charts above to explore customer-specific insights.
            </div>

            <div class="insight-card">
                <div class="insight-label">Executive Insight</div>
                <div id="insight-title" class="insight-title">Overall Revenue Concentration</div>
                <div id="insight-text" class="insight-text">
                    High-Value Loyal Customers represent 16.44% of customers but generate
                    64.89% of total revenue. This shows that business value is highly
                    concentrated within a relatively small customer segment.
                </div>
            </div>

            <div class="table-card">
                <div class="table-title">Segment Performance Summary</div>
                <table>
                    <thead>
                        <tr>
                            <th>Segment</th>
                            <th>Customers</th>
                            <th>Customer Share</th>
                            <th>Revenue Share</th>
                            <th>Avg Recency</th>
                            <th>Avg Frequency</th>
                            <th>Avg Monetary</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows}</tbody>
                </table>
            </div>

        </div>

        <style>
            .executive-panel {{
                font-family: Inter, Arial, sans-serif;
                box-sizing: border-box;
                padding-top: 4px;
            }}

            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1.6rem;
                margin-bottom: 1.3rem;
            }}

            .kpi-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 18px 22px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, .04);
                min-height: 105px;
                box-sizing: border-box;
            }}

            .kpi-label {{
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                color: #6B7280;
                margin-bottom: 10px;
            }}

            .kpi-value {{
                font-size: 34px;
                font-weight: 800;
                color: #111827;
                line-height: 1;
                white-space: nowrap;
            }}

            .distribution-panel {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1.6rem;
                margin-bottom: 1rem;
            }}

            .dist-card,
            .insight-card,
            .table-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, .04);
            }}

            .dist-card {{
                height: 360px;
                padding: 22px 24px;
                box-sizing: border-box;
            }}

            .card-title,
            .table-title {{
                font-size: 18px;
                font-weight: 800;
                color: #111827;
                margin-bottom: 4px;
            }}

            .card-subtitle {{
                font-size: 13px;
                color: #6B7280;
                margin-bottom: 28px;
            }}

            .dist-row {{
                display: grid;
                grid-template-columns: 165px 1fr 58px;
                gap: 14px;
                align-items: center;
                margin-bottom: 20px;
                cursor: pointer;
                transition: opacity .2s ease, transform .2s ease;
            }}

            .dist-row:hover {{
                transform: translateX(3px);
            }}

            .dist-label {{
                font-size: 12px;
                font-weight: 800;
                color: #1F2937;
                line-height: 1.25;
            }}

            .dist-track {{
                height: 14px;
                background: #EEF2F7;
                border-radius: 999px;
                overflow: hidden;
            }}

            .dist-fill {{
                height: 100%;
                width: 0%;
                background: var(--color);
                border-radius: 999px;
                animation: growBar 1.1s cubic-bezier(.16, 1, .3, 1) forwards;
            }}

            .dist-value {{
                font-size: 12px;
                font-weight: 800;
                color: #111827;
                text-align: right;
            }}

            .donut-wrap {{
                height: 245px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .donut-stage {{
                position: relative;
                width: 245px;
                height: 245px;
            }}

            svg {{
                width: 245px;
                height: 245px;
                overflow: visible;
            }}

            .donut-segment {{
                cursor: pointer;
                transition: opacity .2s ease, filter .2s ease;
                animation: donutFade 1.2s cubic-bezier(.16, 1, .3, 1) forwards;
            }}

            .donut-segment:hover {{
                filter: brightness(1.08);
            }}

            .donut-html-label {{
                position: absolute;
                transform: translate(-50%, -50%);
                font-size: 10px;
                font-weight: 800;
                color: #FFFFFF;
                pointer-events: none;
                text-shadow: 0 1px 2px rgba(0,0,0,.25);
            }}

            .dist-row.dimmed {{
                opacity: .18 !important;
            }}

            .dist-row.selected {{
                opacity: 1 !important;
            }}

            .donut-segment.dimmed {{
                opacity: .18 !important;
                filter: grayscale(.25);
            }}

            .donut-segment.selected {{
                opacity: 1 !important;
                filter: brightness(1.08);
            }}

            .status-banner {{
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
                padding: 12px 16px;
                margin-bottom: 1rem;
                font-size: 13px;
                font-weight: 700;
                color: #6B7280;
                transition: color .2s ease, border-color .2s ease;
            }}

            .insight-card {{
                padding: 20px 24px;
                margin-bottom: 1.4rem;
                border-left: 5px solid #C97A28;
                transition: border-left-color .2s ease;
            }}

            .insight-label {{
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                color: #C97A28;
                margin-bottom: 6px;
                transition: color .2s ease;
            }}

            .insight-title {{
                font-size: 18px;
                font-weight: 800;
                color: #111827;
                margin-bottom: 6px;
            }}

            .insight-text {{
                font-size: 14px;
                line-height: 1.6;
                color: #374151;
            }}

            .table-card {{
                padding: 20px 24px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 14px;
                font-size: 12px;
            }}

            th {{
                text-align: left;
                color: #6B7280;
                font-weight: 800;
                padding: 10px 8px;
                border-bottom: 1px solid #E5E7EB;
            }}

            td {{
                padding: 11px 8px;
                border-bottom: 1px solid #F1F5F9;
                color: #111827;
                font-weight: 600;
            }}

            tr.table-hidden {{
                display: none;
            }}

            .segment-dot {{
                width: 9px;
                height: 9px;
                display: inline-block;
                border-radius: 3px;
                margin-right: 8px;
            }}

            .tooltip {{
                position: fixed;
                pointer-events: none;
                background: #111827;
                color: #FFFFFF;
                padding: 10px 12px;
                border-radius: 10px;
                font-size: 12px;
                line-height: 1.45;
                opacity: 0;
                transform: translateY(6px);
                transition: opacity .15s ease, transform .15s ease;
                z-index: 9999;
                box-shadow: 0 12px 30px rgba(15, 23, 42, .30);
            }}

            @keyframes growBar {{
                from {{ width: 0%; }}
                to {{ width: var(--width); }}
            }}

            @keyframes donutFade {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>

        <script>
            const rows = document.querySelectorAll(".dist-row");
            const segments = document.querySelectorAll(".donut-segment");
            const tableRows = document.querySelectorAll("tbody tr");
            const tooltip = document.getElementById("tooltip");

            const label1 = document.getElementById("kpi-label-1");
            const label2 = document.getElementById("kpi-label-2");
            const label3 = document.getElementById("kpi-label-3");

            const kpiCustomers = document.getElementById("kpi-customers");
            const kpiSegments = document.getElementById("kpi-segments");
            const kpiRevenue = document.getElementById("kpi-revenue");

            const statusBanner = document.getElementById("status-banner");

            const insightCard = document.querySelector(".insight-card");
            const insightLabel = document.querySelector(".insight-label");
            const insightTitle = document.getElementById("insight-title");
            const insightText = document.getElementById("insight-text");

            let active = null;

            const defaultTitle = "Overall Revenue Concentration";
            const defaultInsight =
                "High-Value Loyal Customers represent 16.44% of customers but generate 64.89% of total revenue. This shows that business value is highly concentrated within a relatively small customer segment.";

            const defaultCustomers = "{total_customers:,}";
            const defaultSegments = "{total_segments}";
            const defaultRevenue = "£{total_revenue:,.0f}";

            function applySelection(id, name, title, insight, color, customers, revenue, revenueAmount) {{
                active = active === id ? null : id;

                rows.forEach(row => {{
                    row.classList.toggle("dimmed", active !== null && row.dataset.segment !== active);
                    row.classList.toggle("selected", active !== null && row.dataset.segment === active);
                }});

                segments.forEach(seg => {{
                    seg.classList.toggle("dimmed", active !== null && seg.dataset.segment !== active);
                    seg.classList.toggle("selected", active !== null && seg.dataset.segment === active);
                }});

                tableRows.forEach(row => {{
                    row.classList.toggle("table-hidden", active !== null && row.dataset.segment !== active);
                }});

                if (active === null) {{
                    label1.textContent = "Total Customers";
                    label2.textContent = "Customer Segments";
                    label3.textContent = "Total Revenue";

                    kpiCustomers.textContent = defaultCustomers;
                    kpiSegments.textContent = defaultSegments;
                    kpiRevenue.textContent = defaultRevenue;

                    statusBanner.textContent =
                        "Click any segment in the charts above to explore customer-specific insights.";
                    statusBanner.style.color = "#6B7280";
                    statusBanner.style.borderColor = "#E5E7EB";

                    insightTitle.textContent = defaultTitle;
                    insightText.textContent = defaultInsight;
                    insightCard.style.borderLeftColor = "#C97A28";
                    insightLabel.style.color = "#C97A28";
                }} else {{
                    label1.textContent = "Customers";
                    label2.textContent = "Selected Segment";
                    label3.textContent = "Segment Revenue";

                    kpiCustomers.textContent = customers;
                    kpiSegments.textContent = name;
                    kpiRevenue.textContent = revenueAmount;

                    statusBanner.textContent =
                        "Showing detailed analysis for " + name + ".";
                    statusBanner.style.color = color;
                    statusBanner.style.borderColor = color;

                    insightTitle.textContent = title;
                    insightText.textContent = insight;
                    insightCard.style.borderLeftColor = color;
                    insightLabel.style.color = color;
                }}
            }}

            rows.forEach(row => {{
                row.addEventListener("click", () => {{
                    applySelection(
                        row.dataset.segment,
                        row.dataset.name,
                        row.dataset.title,
                        row.dataset.insight,
                        row.dataset.color,
                        row.dataset.customers,
                        row.dataset.revenue,
                        row.dataset.revenueAmount
                    );
                }});
            }});

            segments.forEach(seg => {{
                seg.addEventListener("click", () => {{
                    applySelection(
                        seg.dataset.segment,
                        seg.dataset.name,
                        seg.dataset.title,
                        seg.dataset.insight,
                        seg.dataset.color,
                        seg.dataset.customers,
                        seg.dataset.revenue,
                        seg.dataset.revenueAmount
                    );
                }});

                seg.addEventListener("mousemove", event => {{
                    tooltip.innerHTML = `
                        <strong>${{seg.dataset.name}}</strong><br>
                        Customer Share: ${{seg.dataset.share}}%<br>
                        Customers: ${{seg.dataset.customers}}
                    `;

                    tooltip.style.left = event.clientX + 16 + "px";
                    tooltip.style.top = event.clientY + 16 + "px";
                    tooltip.style.opacity = "1";
                    tooltip.style.transform = "translateY(0)";
                }});

                seg.addEventListener("mouseleave", () => {{
                    tooltip.style.opacity = "0";
                    tooltip.style.transform = "translateY(6px)";
                }});
            }});
        </script>
        """,
        height=960,
        scrolling=False,
    )

def animated_rfm_distributions(rfm, selected_segment):

    segment_data = rfm[rfm["Segment"] == selected_segment].copy()

    metrics = [
        {
            "column": "Recency",
            "title": "Recency Distribution",
            "subtitle": "Days since last purchase",
            "color_top": "#2563EB",
            "color_bottom": "#1D4ED8",
            "insight": "Lower recency means customers purchased more recently. This helps identify how active or dormant the selected segment is.",
        },
        {
            "column": "Frequency",
            "title": "Frequency Distribution",
            "subtitle": "Number of purchases",
            "color_top": "#16A34A",
            "color_bottom": "#15803D",
            "insight": "Frequency shows how often customers return. Higher frequency usually indicates stronger loyalty and repeat behavior.",
        },
        {
            "column": "Monetary",
            "title": "Monetary Distribution",
            "subtitle": "Customer spend (£)",
            "color_top": "#C97A28",
            "color_bottom": "#9A5A1F",
            "insight": "Monetary value shows customer spend. This helps separate low-value activity from revenue-driving behavior.",
        },
    ]

    cards_html = ""

    for metric in metrics:
        column = metric["column"]
        values = segment_data[column].dropna()

        counts, bin_edges = np.histogram(values, bins=10)
        max_count = counts.max() if len(counts) and counts.max() > 0 else 1

        avg_value = values.mean() if len(values) else 0
        median_value = values.median() if len(values) else 0
        max_value = values.max() if len(values) else 0

        bars_html = ""

        for count, left, right in zip(counts, bin_edges[:-1], bin_edges[1:]):
            height = (count / max_count) * 100 if max_count else 0

            bars_html += f"""
            <div class="rfm-bar-group">
                <div
                    class="rfm-bar"
                    style="
                        --bar-height:{height}%;
                        --top:{metric["color_top"]};
                        --bottom:{metric["color_bottom"]};
                    "
                    data-count="{int(count)}"
                    data-range="{left:.0f} - {right:.0f}"
                ></div>
            </div>
            """

        cards_html += f"""
        <div class="rfm-card" style="--accent:{metric["color_top"]};">
            <div class="rfm-header">
                <div>
                    <div class="rfm-title">{metric["title"]}</div>
                    <div class="rfm-subtitle">{metric["subtitle"]}</div>
                </div>
                <div class="rfm-pill">{column}</div>
            </div>

            <div class="rfm-chart">
                {bars_html}
            </div>

            <div class="rfm-stats">
                <div><span>Average</span><strong>{avg_value:,.1f}</strong></div>
                <div><span>Median</span><strong>{median_value:,.1f}</strong></div>
                <div><span>Max</span><strong>{max_value:,.1f}</strong></div>
            </div>

            <div class="rfm-insight">
                {metric["insight"]}
            </div>
        </div>
        """

    components.html(
        f"""
        <div class="rfm-grid">
            {cards_html}
        </div>

        <div id="rfm-tooltip" class="rfm-tooltip"></div>

        <style>
            .rfm-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1.2rem;
                font-family: Inter, Arial, sans-serif;
            }}

            .rfm-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 20px 22px;
                height: 450px;
                box-sizing: border-box;
                box-shadow: 0 8px 24px rgba(15, 23, 42, .04);
                border-top: 4px solid var(--accent);
            }}

            .rfm-header {{
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                align-items: flex-start;
                margin-bottom: 16px;
            }}

            .rfm-title {{
                font-size: 17px;
                font-weight: 800;
                color: #111827;
                margin-bottom: 4px;
            }}

            .rfm-subtitle {{
                font-size: 12px;
                color: #6B7280;
            }}

            .rfm-pill {{
                font-size: 10px;
                font-weight: 800;
                color: var(--accent);
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 999px;
                padding: 5px 9px;
                white-space: nowrap;
            }}

            .rfm-chart {{
                height: 145px;
                display: flex;
                align-items: flex-end;
                gap: 8px;
                padding-top: 8px;
                border-bottom: 1px solid #E5E7EB;
                margin-bottom: 16px;
            }}

            .rfm-bar-group {{
                flex: 1;
                height: 100%;
                display: flex;
                align-items: flex-end;
            }}

            .rfm-bar {{
                width: 100%;
                height: 0%;
                border-radius: 8px 8px 0 0;
                background: linear-gradient(180deg, var(--top), var(--bottom));
                animation: growRfmBar .95s cubic-bezier(.16, 1, .3, 1) forwards;
                cursor: pointer;
                transition: filter .2s ease, transform .2s ease;
            }}

            .rfm-bar:hover {{
                filter: brightness(1.08);
                transform: translateY(-3px);
            }}

            .rfm-stats {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 8px;
                margin-bottom: 14px;
            }}

            .rfm-stats div {{
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 9px;
            }}

            .rfm-stats span {{
                display: block;
                font-size: 10px;
                font-weight: 700;
                color: #6B7280;
                margin-bottom: 3px;
            }}

            .rfm-stats strong {{
                font-size: 13px;
                color: #111827;
            }}

            .rfm-insight {{
                font-size: 12px;
                line-height: 1.45;
                color: #374151;
            }}

            .rfm-tooltip {{
                position: fixed;
                pointer-events: none;
                background: #111827;
                color: #FFFFFF;
                padding: 9px 11px;
                border-radius: 10px;
                font-size: 12px;
                line-height: 1.45;
                opacity: 0;
                transform: translateY(6px);
                transition: opacity .15s ease, transform .15s ease;
                z-index: 9999;
                box-shadow: 0 12px 30px rgba(15, 23, 42, .30);
            }}

            @keyframes growRfmBar {{
                from {{ height: 0%; }}
                to {{ height: var(--bar-height); }}
            }}
        </style>

        <script>
            const tooltip = document.getElementById("rfm-tooltip");

            document.querySelectorAll(".rfm-bar").forEach(bar => {{
                bar.addEventListener("mousemove", event => {{
                    tooltip.innerHTML = `
                        <strong>${{bar.dataset.count}} customers</strong><br>
                        Range: ${{bar.dataset.range}}
                    `;

                    tooltip.style.left = event.clientX + 16 + "px";
                    tooltip.style.top = event.clientY + 16 + "px";
                    tooltip.style.opacity = "1";
                    tooltip.style.transform = "translateY(0)";
                }});

                bar.addEventListener("mouseleave", () => {{
                    tooltip.style.opacity = "0";
                    tooltip.style.transform = "translateY(6px)";
                }});
            }});
        </script>
        """,
        height=470,
        scrolling=False,
    )

def animated_segment_details(selected_segment, profile_text, recommended_actions, segment_customers):
    import streamlit.components.v1 as components
    from utils.constants import SEGMENT_COLORS

    color = SEGMENT_COLORS.get(selected_segment, "#C97A28")

    actions_html = ""
    for action in recommended_actions:
        actions_html += f"""
        <div class="action-item">
            <span class="action-dot"></span>
            <div>{action}</div>
        </div>
        """

    table_rows = ""
    for _, row in segment_customers.iterrows():
        table_rows += f"""
        <tr>
            <td>{row["CustomerID"]}</td>
            <td>{row["Recency"]}</td>
            <td>{row["Frequency"]}</td>
            <td>£{row["Monetary"]:,.0f}</td>
            <td>{row["Segment"]}</td>
        </tr>
        """

    components.html(
        f"""
        <div class="segment-details">

            <div class="details-grid">

                <div class="detail-card">
                    <div class="detail-eyebrow" style="color:{color};">
                        Segment Profile
                    </div>
                    <div class="detail-title">{selected_segment}</div>
                    <div class="detail-text">
                        {profile_text}
                    </div>
                </div>

                <div class="detail-card">
                    <div class="detail-eyebrow" style="color:{color};">
                        Recommended Actions
                    </div>
                    <div class="detail-title">What the business should do</div>
                    <div class="actions-list">
                        {actions_html}
                    </div>
                </div>

            </div>

            <div class="records-card">

                <div class="records-header">
                    <div>
                        <div class="detail-eyebrow" style="color:{color};">
                            Customer Records
                        </div>
                        <div class="detail-title">Customers in this segment</div>
                    </div>

                    <div class="records-actions">
                        <div class="records-pill" style="color:{color}; border-color:{color};">
                            {len(segment_customers):,} customers
                        </div>
                        <button id="fullscreen-btn" class="fullscreen-btn">
                            Full Screen
                        </button>
                    </div>
                </div>

                <input
                    id="table-search"
                    class="table-search"
                    placeholder="Search customer records..."
                />

                <div id="table-wrapper" class="table-wrapper">
                    <table id="records-table">
                        <thead>
                            <tr>
                                <th>Customer ID</th>
                                <th>Recency</th>
                                <th>Frequency</th>
                                <th>Monetary</th>
                                <th>Segment</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>

            </div>

        </div>

        <style>
            .segment-details {{
                font-family: Inter, Arial, sans-serif;
                animation: fadeIn .45s ease both;
            }}

            .details-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1.3rem;
                margin-bottom: 1.3rem;
            }}

            .detail-card,
            .records-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, .04);
                box-sizing: border-box;
            }}

            .detail-card {{
                min-height: 205px;
                padding: 22px 24px;
                border-left: 5px solid {color};
            }}

            .detail-eyebrow {{
                font-size: 12px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: .08em;
                margin-bottom: 8px;
            }}

            .detail-title {{
                font-size: 20px;
                font-weight: 800;
                color: #111827;
                margin-bottom: 10px;
                line-height: 1.25;
            }}

            .detail-text {{
                font-size: 14px;
                line-height: 1.6;
                color: #374151;
            }}

            .actions-list {{
                display: grid;
                gap: 11px;
                margin-top: 14px;
            }}

            .action-item {{
                display: flex;
                align-items: flex-start;
                gap: 10px;
                font-size: 14px;
                line-height: 1.45;
                color: #374151;
                font-weight: 600;
            }}

            .action-dot {{
                width: 9px;
                height: 9px;
                border-radius: 999px;
                background: {color};
                margin-top: 6px;
                flex-shrink: 0;
            }}

            .records-card {{
                padding: 22px 24px;
                border-top: 4px solid {color};
            }}

            .records-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 1rem;
                margin-bottom: 14px;
            }}

            .records-actions {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .records-pill {{
                font-size: 12px;
                font-weight: 800;
                border: 1px solid;
                border-radius: 999px;
                padding: 7px 11px;
                background: #F8FAFC;
                white-space: nowrap;
            }}

            .fullscreen-btn {{
                border: 1px solid #E5E7EB;
                background: #111827;
                color: #FFFFFF;
                border-radius: 999px;
                padding: 7px 12px;
                font-size: 12px;
                font-weight: 800;
                cursor: pointer;
            }}

            .table-search {{
                width: 100%;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 10px 12px;
                font-size: 13px;
                margin-bottom: 12px;
                outline: none;
                box-sizing: border-box;
            }}

            .table-search:focus {{
                border-color: {color};
            }}

            .table-wrapper {{
                max-height: 310px;
                overflow-y: auto;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
            }}

            .table-wrapper:fullscreen {{
                background: #FFFFFF;
                padding: 28px;
                box-sizing: border-box;
            }}

            .table-wrapper:fullscreen table {{
                font-size: 15px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
            }}

            thead th {{
                position: sticky;
                top: 0;
                background: #F8FAFC;
                z-index: 2;
            }}

            th {{
                text-align: left;
                color: #6B7280;
                font-weight: 800;
                padding: 11px 10px;
                border-bottom: 1px solid #E5E7EB;
            }}

            td {{
                padding: 11px 10px;
                border-bottom: 1px solid #F1F5F9;
                color: #111827;
                font-weight: 600;
            }}

            tbody tr:hover {{
                background: #F8FAFC;
            }}

            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(10px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        </style>

        <script>
            const searchInput = document.getElementById("table-search");
            const rows = document.querySelectorAll("#records-table tbody tr");
            const fullscreenBtn = document.getElementById("fullscreen-btn");
            const tableWrapper = document.getElementById("table-wrapper");

            searchInput.addEventListener("input", () => {{
                const query = searchInput.value.toLowerCase();

                rows.forEach(row => {{
                    row.style.display = row.textContent.toLowerCase().includes(query)
                        ? ""
                        : "none";
                }});
            }});

            fullscreenBtn.addEventListener("click", () => {{
                if (tableWrapper.requestFullscreen) {{
                    tableWrapper.requestFullscreen();
                }}
            }});
        </script>
        """,
        height=760,
        scrolling=False,
    )

def animated_business_insights():
    import streamlit.components.v1 as components

    components.html(
        """
        <div class="strategy-app">

            <div class="strategy-header">
                <div class="strategy-eyebrow">Strategy Simulator</div>
                <div class="strategy-title">Choose a business strategy</div>
                <div class="strategy-subtitle">
                    Explore estimated business impact for each customer strategy. These are scenario-based estimates, not predictive model outputs.
                </div>
            </div>

            <div class="strategy-tabs">
                <button class="strategy-tab active" data-key="retain">Retain</button>
                <button class="strategy-tab" data-key="grow">Grow</button>
                <button class="strategy-tab" data-key="convert">Convert</button>
                <button class="strategy-tab" data-key="reengage">Re-engage</button>
            </div>

            <div class="strategy-panel">

                <div class="main-card">
                    <div id="strategy-label" class="strategy-label">Retention Priority</div>
                    <div id="strategy-name" class="strategy-name">Retain High-Value Loyal Customers</div>
                    <div id="strategy-objective" class="strategy-objective">
                        Protect the customer group generating the majority of revenue by strengthening loyalty and reducing churn risk.
                    </div>

                    <div class="impact-grid">
                        <div class="impact-card">
                            <span id="impact-label-1">Revenue Stability</span>
                            <strong id="impact-1">+10–15%</strong>
                        </div>
                        <div class="impact-card">
                            <span id="impact-label-2">Customer Lifetime Value</span>
                            <strong id="impact-2">+8–12%</strong>
                        </div>
                        <div class="impact-card">
                            <span id="impact-label-3">Churn Risk</span>
                            <strong id="impact-3">-10–15%</strong>
                        </div>
                    </div>

                    <div class="impact-note">
                        Estimated directional impact based on business strategy assumptions, not a forecasting model.
                    </div>
                </div>

                <div class="actions-card">
                    <div class="section-title">Recommended Actions</div>
                    <div id="actions-list" class="actions-list"></div>
                </div>

                <div class="outcome-card">
                    <div class="section-title">Expected Impact Table</div>
                    <div class="impact-table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Expected Movement</th>
                                    <th>Business Meaning</th>
                                </tr>
                            </thead>
                            <tbody id="impact-table"></tbody>
                        </table>
                    </div>
                </div>

                <div class="summary-card">
                    <div class="section-title">What success looks like</div>
                    <div id="outcome-text" class="outcome-text"></div>
                </div>

            </div>

        </div>

        <style>
            .strategy-app {
                font-family: Inter, Arial, sans-serif;
                animation: fadeIn .45s ease both;
            }

            .strategy-header {
                margin-bottom: 1.4rem;
            }

            .strategy-eyebrow {
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                color: #C97A28;
                margin-bottom: 6px;
            }

            .strategy-title {
                font-size: 28px;
                font-weight: 900;
                color: #111827;
                margin-bottom: 6px;
            }

            .strategy-subtitle {
                font-size: 14px;
                color: #6B7280;
                line-height: 1.5;
                max-width: 860px;
            }

            .strategy-tabs {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 1rem;
                margin-bottom: 1.4rem;
            }

            .strategy-tab {
                border: 1px solid #E5E7EB;
                background: #FFFFFF;
                border-radius: 16px;
                padding: 16px;
                font-size: 15px;
                font-weight: 850;
                color: #374151;
                cursor: pointer;
                box-shadow: 0 8px 24px rgba(15,23,42,.04);
                transition: all .22s ease;
            }

            .strategy-tab:hover {
                transform: translateY(-3px);
            }

            .strategy-tab.active {
                color: #FFFFFF;
                background: var(--active-color);
                border-color: var(--active-color);
            }

            .strategy-panel {
                display: grid;
                grid-template-columns: 1.2fr 1fr;
                gap: 1.3rem;
            }

            .main-card,
            .actions-card,
            .outcome-card,
            .summary-card {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(15,23,42,.04);
                box-sizing: border-box;
                padding: 22px 24px;
            }

            .main-card {
                border-left: 5px solid var(--active-color);
            }

            .actions-card {
                min-height: 235px;
                max-height: 250px;
                overflow-y: auto;
            }

            .outcome-card {
                height: 365px;
                overflow: hidden;
            }

            .impact-table-wrapper {
                height: 285px;
                overflow-y: auto;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            .impact-table-wrapper thead th {
                position: sticky;
                top: 0;
                background: #F8FAFC;
                z-index: 2;
            }

            .strategy-label {
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                color: var(--active-color);
                margin-bottom: 8px;
            }

            .strategy-name {
                font-size: 24px;
                font-weight: 900;
                color: #111827;
                margin-bottom: 12px;
                line-height: 1.25;
            }

            .strategy-objective {
                font-size: 15px;
                line-height: 1.6;
                color: #374151;
                margin-bottom: 22px;
            }

            .impact-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }

            .impact-card {
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
                padding: 14px;
            }

            .impact-card span {
                display: block;
                font-size: 11px;
                font-weight: 800;
                color: #6B7280;
                margin-bottom: 6px;
                text-transform: uppercase;
                line-height: 1.3;
            }

            .impact-card strong {
                font-size: 18px;
                color: var(--active-color);
            }

            .impact-note {
                margin-top: 16px;
                font-size: 12px;
                line-height: 1.5;
                color: #6B7280;
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 10px 12px;
            }

            .section-title {
                font-size: 17px;
                font-weight: 850;
                color: #111827;
                margin-bottom: 14px;
            }

            .actions-list {
                display: grid;
                gap: 11px;
            }

            .action-row {
                display: flex;
                gap: 10px;
                align-items: flex-start;
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                line-height: 1.45;
            }

            .action-dot {
                width: 9px;
                height: 9px;
                border-radius: 999px;
                background: var(--active-color);
                margin-top: 6px;
                flex-shrink: 0;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
            }

            th {
                text-align: left;
                color: #6B7280;
                font-weight: 850;
                padding: 12px 10px;
                border-bottom: 1px solid #E5E7EB;
            }

            td {
                padding: 13px 10px;
                border-bottom: 1px solid #F1F5F9;
                color: #111827;
                font-weight: 600;
                line-height: 1.4;
                vertical-align: top;
            }

            td:nth-child(2) {
                color: var(--active-color);
                font-weight: 900;
                white-space: nowrap;
            }

            .summary-card {
                grid-column: span 2;
                border-top: 4px solid var(--active-color);
            }

            .outcome-text {
                font-size: 14px;
                line-height: 1.6;
                color: #374151;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>

        <script>
            const strategies = {
                retain: {
                    color: "#16A34A",
                    label: "Retention Priority",
                    name: "Retain High-Value Loyal Customers",
                    objective: "Protect the customer group generating the majority of revenue by strengthening loyalty and reducing churn risk.",
                    impactLabels: ["Revenue Stability", "Customer Lifetime Value", "Churn Risk"],
                    impacts: ["+10–15%", "+8–12%", "-10–15%"],
                    table: [
                        ["Revenue Stability", "+10–15%", "Protects the largest revenue-driving segment from decline."],
                        ["Customer Lifetime Value", "+8–12%", "Encourages continued spending from the most valuable customers."],
                        ["Churn Risk", "-10–15%", "Reduces the chance of losing the business-critical group."]
                    ],
                    actions: [
                        "Offer loyalty rewards and exclusive benefits.",
                        "Provide early access to new products.",
                        "Use personalized recommendations.",
                        "Monitor signs of reduced purchase activity."
                    ],
                    outcome: "Success means the business protects its highest-value customers, keeps revenue stable, and reduces dependence on acquiring replacement customers."
                },

                grow: {
                    color: "#2563EB",
                    label: "Growth Opportunity",
                    name: "Grow Mid-Value Regular Customers",
                    objective: "Increase revenue from customers who already purchase regularly but have not yet reached high-value behavior.",
                    impactLabels: ["Basket Size", "Revenue Share", "Repeat Purchase"],
                    impacts: ["+8–12%", "+6–10%", "+5–8%"],
                    table: [
                        ["Basket Size", "+8–12%", "Bundles and cross-sell offers can increase average spend."],
                        ["Revenue Share", "+6–10%", "Mid-value customers can contribute more without requiring new acquisition."],
                        ["Repeat Purchase", "+5–8%", "Regular buyers become more consistent and higher value."]
                    ],
                    actions: [
                        "Promote product bundles.",
                        "Use cross-sell campaigns.",
                        "Encourage larger basket sizes.",
                        "Send targeted upgrade offers."
                    ],
                    outcome: "Success means more mid-value customers move toward high-value behavior through larger purchases and stronger repeat activity."
                },

                convert: {
                    color: "#C97A28",
                    label: "Conversion Strategy",
                    name: "Convert Recent Occasional Customers",
                    objective: "Turn recently active customers into repeat buyers before they become inactive.",
                    impactLabels: ["Repeat Purchase", "Customer Activation", "Dormancy Risk"],
                    impacts: ["+12–18%", "+10–15%", "-8–12%"],
                    table: [
                        ["Repeat Purchase", "+12–18%", "Second-purchase incentives can convert active customers into repeat buyers."],
                        ["Customer Activation", "+10–15%", "Onboarding and recommendations can increase engagement."],
                        ["Dormancy Risk", "-8–12%", "Timely follow-up reduces the chance of customers becoming inactive."]
                    ],
                    actions: [
                        "Send second-purchase incentives.",
                        "Recommend related products.",
                        "Use welcome campaigns.",
                        "Create onboarding journeys."
                    ],
                    outcome: "Success means recent customers build stronger buying habits and begin moving toward regular customer behavior."
                },

                reengage: {
                    color: "#6B7280",
                    label: "Cost-Control Strategy",
                    name: "Re-engage Inactive Low-Value Customers",
                    objective: "Reactivate customers cautiously while avoiding excessive marketing spend on low-return groups.",
                    impactLabels: ["Recovery Rate", "Marketing Cost", "Campaign Efficiency"],
                    impacts: ["+3–6%", "-15–25%", "+8–12%"],
                    table: [
                        ["Recovery Rate", "+3–6%", "A small share of inactive customers may return through low-cost campaigns."],
                        ["Marketing Cost", "-15–25%", "Automation reduces spend on low-return customers."],
                        ["Campaign Efficiency", "+8–12%", "Suppressing unresponsive users improves campaign quality."]
                    ],
                    actions: [
                        "Use low-cost automated campaigns.",
                        "Test limited-time offers.",
                        "Suppress customers who remain unresponsive.",
                        "Avoid expensive personalized campaigns."
                    ],
                    outcome: "Success means the business recovers some inactive customers while preventing unnecessary spend on low-value, low-response segments."
                }
            };

            const root = document.querySelector(".strategy-app");
            const tabs = document.querySelectorAll(".strategy-tab");

            const label = document.getElementById("strategy-label");
            const name = document.getElementById("strategy-name");
            const objective = document.getElementById("strategy-objective");

            const impactLabel1 = document.getElementById("impact-label-1");
            const impactLabel2 = document.getElementById("impact-label-2");
            const impactLabel3 = document.getElementById("impact-label-3");

            const impact1 = document.getElementById("impact-1");
            const impact2 = document.getElementById("impact-2");
            const impact3 = document.getElementById("impact-3");

            const actionsList = document.getElementById("actions-list");
            const outcomeText = document.getElementById("outcome-text");
            const impactTable = document.getElementById("impact-table");

            function renderStrategy(key) {
                const s = strategies[key];

                root.style.setProperty("--active-color", s.color);

                tabs.forEach(tab => {
                    tab.classList.toggle("active", tab.dataset.key === key);
                });

                label.textContent = s.label;
                name.textContent = s.name;
                objective.textContent = s.objective;

                impactLabel1.textContent = s.impactLabels[0];
                impactLabel2.textContent = s.impactLabels[1];
                impactLabel3.textContent = s.impactLabels[2];

                impact1.textContent = s.impacts[0];
                impact2.textContent = s.impacts[1];
                impact3.textContent = s.impacts[2];

                actionsList.innerHTML = s.actions.map(action => `
                    <div class="action-row">
                        <span class="action-dot"></span>
                        <div>${action}</div>
                    </div>
                `).join("");

                impactTable.innerHTML = s.table.map(row => `
                    <tr>
                        <td>${row[0]}</td>
                        <td>${row[1]}</td>
                        <td>${row[2]}</td>
                    </tr>
                `).join("");

                outcomeText.textContent = s.outcome;
            }

            tabs.forEach(tab => {
                tab.addEventListener("click", () => renderStrategy(tab.dataset.key));
            });

            renderStrategy("retain");
        </script>
        """,
        height=860,
        scrolling=False,
    )

def animated_about_project():
    components.html(
        """
        <div class="about-app">

            <div class="about-bg"></div>

            <div class="about-hero">
                <div class="about-eyebrow">Project Context</div>
                <div class="about-title">Customer Intelligence Platform</div>
                <div class="about-subtitle">
                    This project demonstrates how customer segmentation can turn transactional data
                    into business insight. Using RFM analysis and K-Means clustering, the application
                    identifies customer groups, explains their behaviour, and connects those findings
                    to practical business strategies.
                </div>
            </div>

            <div class="about-grid">
                <div class="about-card active" data-section="problem">
                    <div class="card-number">01</div>
                    <div class="card-title">Business Problem</div>
                    <div class="card-text">
                        Customers do not contribute equally to revenue. The project identifies which
                        groups create the most value and where the business should focus action.
                    </div>
                </div>

                <div class="about-card" data-section="method">
                    <div class="card-number">02</div>
                    <div class="card-title">Methodology</div>
                    <div class="card-text">
                        RFM analysis measures recency, frequency, and monetary value. K-Means clustering
                        then groups customers based on similar purchasing behaviour.
                    </div>
                </div>

                <div class="about-card" data-section="workflow">
                    <div class="card-number">03</div>
                    <div class="card-title">Workflow</div>
                    <div class="card-text">
                        Raw transactions are cleaned, transformed into customer-level metrics, clustered,
                        profiled, visualized, and translated into business recommendations.
                    </div>
                </div>

                <div class="about-card" data-section="product">
                    <div class="card-number">04</div>
                    <div class="card-title">Application</div>
                    <div class="card-text">
                        The final application includes an executive overview, segment explorer, strategy
                        simulator, and project context module.
                    </div>
                </div>
            </div>

            <div class="workflow-card">
                <div class="workflow-title">Analytics Workflow</div>

                <div class="workflow-steps">
                    <div class="step" data-step="raw">Raw Data</div>
                    <div class="arrow">→</div>
                    <div class="step" data-step="cleaning">Cleaning</div>
                    <div class="arrow">→</div>
                    <div class="step" data-step="rfm">RFM Features</div>
                    <div class="arrow">→</div>
                    <div class="step" data-step="kmeans">K-Means</div>
                    <div class="arrow">→</div>
                    <div class="step" data-step="insights">Insights</div>
                    <div class="arrow">→</div>
                    <div class="step" data-step="strategy">Strategy</div>
                </div>
            </div>

            <div class="tech-card">
                <div class="tech-title">Tools & Techniques</div>
                <div class="tech-list">
                    <span data-tip="Used for data processing, logic, and application development.">Python</span>
                    <span data-tip="Used for cleaning, transforming, and aggregating transactional data.">Pandas</span>
                    <span data-tip="Used for K-Means clustering and customer segmentation.">Scikit-learn</span>
                    <span data-tip="Used to calculate recency, frequency, and monetary value.">RFM Analysis</span>
                    <span data-tip="Used to group customers based on behavioral similarity.">K-Means Clustering</span>
                    <span data-tip="Used to build the interactive analytics application.">Streamlit</span>
                    <span data-tip="Used for custom interactions, animation, and interface polish.">HTML/CSS/JavaScript</span>
                </div>
            </div>

            <div id="about-tooltip" class="about-tooltip"></div>

        </div>

        <style>
            .about-app {
                position: relative;
                font-family: Inter, Arial, sans-serif;
                animation: fadeIn .45s ease both;
                overflow: hidden;
            }

            .about-bg {
                position: absolute;
                inset: 0;
                pointer-events: none;
                background:
                    radial-gradient(circle at 85% 8%, rgba(201,122,40,.12), transparent 30%),
                    linear-gradient(rgba(15,23,42,.035) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(15,23,42,.035) 1px, transparent 1px);
                background-size: auto, 36px 36px, 36px 36px;
                opacity: .9;
                z-index: 0;
            }

            .about-hero,
            .about-grid,
            .workflow-card,
            .tech-card {
                position: relative;
                z-index: 1;
            }

            .about-hero {
                margin-bottom: 1.8rem;
            }

            .about-eyebrow {
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .1em;
                text-transform: uppercase;
                color: #C97A28;
                margin-bottom: 8px;
            }

            .about-title {
                font-size: 36px;
                font-weight: 900;
                color: #111827;
                margin-bottom: 10px;
                line-height: 1.1;
            }

            .about-subtitle {
                font-size: 16px;
                color: #4B5563;
                line-height: 1.7;
                max-width: 980px;
            }

            .about-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 1rem;
                margin-bottom: 1.4rem;
            }

            .about-card {
                background: rgba(255,255,255,.92);
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 20px;
                box-shadow: 0 8px 24px rgba(15,23,42,.04);
                cursor: pointer;
                transition: all .22s ease;
                border-top: 4px solid #E5E7EB;
                backdrop-filter: blur(6px);
            }

            .about-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 16px 34px rgba(15,23,42,.08);
            }

            .about-card.active {
                border-top-color: #C97A28;
            }

            .card-number {
                font-size: 12px;
                font-weight: 900;
                color: #C97A28;
                margin-bottom: 12px;
            }

            .card-title {
                font-size: 18px;
                font-weight: 850;
                color: #111827;
                margin-bottom: 10px;
            }

            .card-text {
                font-size: 13px;
                color: #374151;
                line-height: 1.55;
            }

            .workflow-card,
            .tech-card {
                background: rgba(255,255,255,.94);
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 24px;
                box-shadow: 0 8px 24px rgba(15,23,42,.04);
                margin-bottom: 1.3rem;
                backdrop-filter: blur(6px);
            }

            .workflow-title,
            .tech-title {
                font-size: 20px;
                font-weight: 850;
                color: #111827;
                margin-bottom: 18px;
            }

            .workflow-steps {
                display: flex;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
            }

            .step {
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 999px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 800;
                color: #111827;
                transition: all .25s ease;
            }

            .step.active-step {
                background: #FFF7ED;
                border-color: #C97A28;
                color: #9A5A1F;
                transform: translateY(-2px);
            }

            .arrow {
                color: #C97A28;
                font-weight: 900;
            }

            .tech-list {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            .tech-list span {
                background: #FFF7ED;
                color: #9A5A1F;
                border: 1px solid #FED7AA;
                border-radius: 999px;
                padding: 9px 13px;
                font-size: 13px;
                font-weight: 800;
                cursor: default;
            }

            .about-tooltip {
                position: fixed;
                pointer-events: none;
                background: #111827;
                color: #FFFFFF;
                padding: 9px 11px;
                border-radius: 10px;
                font-size: 12px;
                line-height: 1.45;
                opacity: 0;
                transform: translateY(6px);
                transition: opacity .15s ease, transform .15s ease;
                z-index: 9999;
                box-shadow: 0 12px 30px rgba(15,23,42,.30);
                max-width: 240px;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>

        <script>
            const cards = document.querySelectorAll(".about-card");
            const steps = document.querySelectorAll(".step");
            const tooltip = document.getElementById("about-tooltip");

            const stepGroups = {
                problem: ["raw"],
                method: ["rfm", "kmeans"],
                workflow: ["raw", "cleaning", "rfm", "kmeans", "insights", "strategy"],
                product: ["insights", "strategy"]
            };

            function highlightSteps(section) {
                steps.forEach(step => step.classList.remove("active-step"));
                const activeSteps = stepGroups[section] || [];

                activeSteps.forEach((key, index) => {
                    setTimeout(() => {
                        const step = document.querySelector(`[data-step="${key}"]`);
                        if (step) step.classList.add("active-step");
                    }, index * 120);
                });
            }

            cards.forEach(card => {
                card.addEventListener("click", () => {
                    cards.forEach(c => c.classList.remove("active"));
                    card.classList.add("active");
                    highlightSteps(card.dataset.section);
                });
            });

            document.querySelectorAll(".tech-list span").forEach(item => {
                item.addEventListener("mousemove", event => {
                    tooltip.textContent = item.dataset.tip;
                    tooltip.style.left = event.clientX + 14 + "px";
                    tooltip.style.top = event.clientY + 14 + "px";
                    tooltip.style.opacity = "1";
                    tooltip.style.transform = "translateY(0)";
                });

                item.addEventListener("mouseleave", () => {
                    tooltip.style.opacity = "0";
                    tooltip.style.transform = "translateY(6px)";
                });
            });

            highlightSteps("problem");
        </script>
        """,
        height=760,
        scrolling=False,
    )
