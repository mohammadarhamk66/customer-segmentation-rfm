import streamlit as st

from components import viz
from components.layout import inset
from components.shell import render
from utils.constants import (
    RECOMMENDED_ACTIONS,
    SEGMENT_COLORS,
    SEGMENT_GLOW,
    SEGMENT_ORDER,
    SEGMENT_PROFILES,
    SEGMENT_SHORT,
)


def show_segment_explorer(rfm, cluster_profile, kpis, sample):
    # Intro renders first so the picker sits under a heading rather than floating
    # at the very top of the page.
    render(
        viz.page_head(
            "Segment Explorer",
            'Inside each <span class="grad-amber">segment</span>',
            "Pick a segment to see how its customers behave, how they compare to the "
            "rest of the base, and what to do about them.",
        ),
        height=280,
        css=viz.VIZ_CSS,
        js=viz.VIZ_JS,
    )

    with inset():
        col, _ = st.columns([1.3, 2.7])
        with col:
            selected = st.selectbox("Select a customer segment", SEGMENT_ORDER, index=0)

    profile = cluster_profile[cluster_profile["Segment"] == selected].iloc[0]
    members = rfm[rfm["Segment"] == selected]

    color = SEGMENT_COLORS.get(selected, "#94A3B8")
    glow = SEGMENT_GLOW.get(selected, "#CBD5E1")

    # distribution curves for this segment
    rec = members["Recency"].tolist()
    freq = members["Frequency"].tolist()
    mon = members["Monetary"].tolist()

    c1, j1 = viz.curve("cRec", "Recency", f"Median <b>{members['Recency'].median():.0f} days</b> "
                       f"since last purchase", rec, color)
    c2, j2 = viz.curve("cFreq", "Frequency", f"Median <b>{members['Frequency'].median():.0f} orders</b> "
                       f"per customer", freq, color)
    c3, j3 = viz.curve("cMon", "Monetary", f"Median <b>£{members['Monetary'].median():,.0f}</b> "
                       f"lifetime spend", mon, color)

    actions = "".join(
        f"<li>{a}</li>" for a in RECOMMENDED_ACTIONS.get(selected, [])
    )

    # top customers in the segment
    top10 = members.nlargest(10, "Monetary")
    rows = "".join(f"""
<tr>
  <td style="color:#FFFFFF;font-weight:600">#{int(r.CustomerID)}</td>
  <td class="num">{int(r.Recency)} d</td>
  <td class="num">{int(r.Frequency)}</td>
  <td class="num" style="color:{color}">£{r.Monetary:,.0f}</td>
</tr>""" for r in top10.itertuples())

    # how this segment compares on each dimension
    def rel(field, seg_val):
        base = rfm[field].mean()
        return seg_val / base if base else 1.0

    comparisons = [
        ("Recency", f"{profile['Avg_Recency']:.0f} days", rel("Recency", profile["Avg_Recency"]), True),
        ("Frequency", f"{profile['Avg_Frequency']:.1f} orders", rel("Frequency", profile["Avg_Frequency"]), False),
        ("Monetary", f"£{profile['Avg_Monetary']:,.0f}", rel("Monetary", profile["Avg_Monetary"]), False),
    ]
    cmp_html = "".join(f"""
<div class="hbar">
  <div class="hbar-head">
    <span class="hbar-name">{name} — {val}</span>
    <span class="hbar-val" style="color:{'#F87171' if (lower_is_better and ratio > 1) or (not lower_is_better and ratio < 1) else glow}">
      {ratio:.2f}× base
    </span>
  </div>
  <div class="hbar-track">
    <div class="hbar-fill" data-w="{min(ratio / 4 * 100, 100):.1f}" data-delay="{i*120}"
         style="background:linear-gradient(90deg,{color},{glow});box-shadow:0 0 16px {color}66"></div>
  </div>
</div>""" for i, (name, val, ratio, lower_is_better) in enumerate(comparisons))

    body = f"""
<div data-reveal="0" style="padding:22px 4px 0 4px">
  <h2 class="section" style="font-size:30px">
    <span class="grad-amber">{SEGMENT_SHORT.get(selected, selected)}</span> Customers
  </h2>
  <p class="lede" style="margin-top:10px">{SEGMENT_PROFILES.get(selected, "")}</p>
</div>

<div class="row row-4 mt-32">
  {viz.kpi("Customers", int(profile['Customer_Count']), "In this segment",
           spark=float(profile['Customer_Share_%']) * 2.5, color=color, delay=0)}
  {viz.kpi("Customer share", float(profile['Customer_Share_%']), "Of the total base",
           decimals=1, suffix="%", spark=float(profile['Customer_Share_%']) * 2.5,
           color=color, delay=90)}
  {viz.kpi("Revenue share", float(profile['Revenue_Share_%']), "Of total revenue",
           decimals=1, suffix="%", spark=float(profile['Revenue_Share_%']), color=color, delay=180)}
  {viz.kpi("Average value", float(profile['Avg_Monetary']), "Mean spend per customer",
           decimals=0, prefix="£", spark=min(float(profile['Avg_Monetary']) / 90, 100),
           color=color, delay=270)}
</div>

{viz.section("Behavioural distributions",
             "How this segment's customers spread across each RFM dimension.")}

<div class="row row-3 mt-20">
  <div class="glass pad" data-tilt="6" data-reveal="0"><div class="lift-sm">{c1}</div></div>
  <div class="glass pad" data-tilt="6" data-reveal="110"><div class="lift-sm">{c2}</div></div>
  <div class="glass pad" data-tilt="6" data-reveal="220"><div class="lift-sm">{c3}</div></div>
</div>

{viz.section("How this segment compares",
             "Each dimension against the average across all 4,338 customers. For "
             "recency, lower is better.")}

<div class="row row-12 mt-20">
  <div class="glass pad-lg" data-tilt="5" data-reveal="0">
    <div class="lift-sm">{cmp_html}</div>
  </div>
  <div class="glass pad-lg" data-tilt="5" data-reveal="120">
    <div class="lift-sm">
      <h3 class="card-title">Recommended actions</h3>
      <ul class="ticks" style="margin-top:6px">{actions}</ul>
    </div>
  </div>
</div>

{viz.section("Highest-value customers in this segment",
             "The ten largest accounts by lifetime spend.")}

<div class="glass pad-lg mt-20" data-reveal="0">
  <table class="data">
    <thead><tr>
      <th>Customer</th><th style="text-align:right">Recency</th>
      <th style="text-align:right">Frequency</th><th style="text-align:right">Monetary</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<div class="glass pad-lg mt-44" data-reveal="0"
     style="background:linear-gradient(120deg,{color}1f,rgba(139,92,246,.08))">
  <h2 class="section" style="font-size:22px">Segment summary</h2>
  <p class="body" style="max-width:66ch">
    {int(profile['Customer_Count']):,} customers carrying
    <strong>£{profile['Total_Revenue']/1_000_000:.2f}M</strong> in revenue. They order on
    average <strong>{profile['Avg_Frequency']:.1f} times</strong>, last purchased
    <strong>{profile['Avg_Recency']:.0f} days ago</strong>, and spend
    <strong>£{profile['Avg_Monetary']:,.0f}</strong> each.
  </p>
</div>
"""

    render(body, height=2120, css=viz.VIZ_CSS, js=viz.VIZ_JS + j1 + j2 + j3)
