from components import viz
from components.shell import render
from components.strategy_simulator import SIM_CSS, render_simulator, sim_js
from utils.constants import (
    RECOMMENDED_ACTIONS,
    SEGMENT_COLORS,
    SEGMENT_GLOW,
    SEGMENT_ORDER,
    SEGMENT_SHORT,
)

PRIORITY = {
    "High-Value Loyal Customers": ("Protect", "Retention"),
    "Mid-Value Regular Customers": ("Grow", "Expansion"),
    "Recent Occasional Customers": ("Convert", "Activation"),
    "Inactive Low-Value Customers": ("Automate", "Efficiency"),
}


def show_business_insights(rfm, cluster_profile, kpis, sample):
    cp = cluster_profile

    # opportunity sizing: what a modest lift in each segment is worth
    cards = []
    for i, (_, r) in enumerate(cp.iterrows()):
        seg = r["Segment"]
        color = SEGMENT_COLORS.get(seg, "#94A3B8")
        glow = SEGMENT_GLOW.get(seg, "#CBD5E1")
        verb, theme = PRIORITY[seg]
        actions = "".join(f"<li>{a}</li>" for a in RECOMMENDED_ACTIONS[seg])

        cards.append(f"""
<div class="glass pad-lg" data-tilt="6" data-reveal="{i * 110}">
  <div class="lift-sm">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:14px">
      <span class="chip" style="border-color:{color}55;background:{color}18;color:{glow}">
        <span class="swatch" style="background:{color};box-shadow:0 0 10px {color}"></span>{verb}
      </span>
      <span style="font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
                   color:#64748B;font-weight:800">{theme}</span>
    </div>
    <h3 class="card-title" style="margin-top:18px;font-size:19px">
      {SEGMENT_SHORT.get(seg, seg)}
    </h3>
    <p class="body" style="margin-bottom:18px">
      {int(r['Customer_Count']):,} customers · {r['Customer_Share_%']:.1f}% of base ·
      <strong>{r['Revenue_Share_%']:.1f}% of revenue</strong>
    </p>
    <div style="display:flex;gap:22px;margin-bottom:18px">
      <div>
        <div class="kpi-label" style="margin-bottom:6px">Avg value</div>
        <div style="font-family:Sora,Inter,sans-serif;font-size:21px;font-weight:800;color:#FFF">
          £{r['Avg_Monetary']:,.0f}</div>
      </div>
      <div>
        <div class="kpi-label" style="margin-bottom:6px">Avg orders</div>
        <div style="font-family:Sora,Inter,sans-serif;font-size:21px;font-weight:800;color:#FFF">
          {r['Avg_Frequency']:.1f}</div>
      </div>
      <div>
        <div class="kpi-label" style="margin-bottom:6px">Avg recency</div>
        <div style="font-family:Sora,Inter,sans-serif;font-size:21px;font-weight:800;color:#FFF">
          {r['Avg_Recency']:.0f}d</div>
      </div>
    </div>
    <ul class="ticks">{actions}</ul>
  </div>
</div>""")

    # --- opportunity model -------------------------------------------------
    # A deliberately conservative, clearly-stated scenario rather than a forecast.
    occ = cp[cp["Segment"] == "Recent Occasional Customers"].iloc[0]
    mid = cp[cp["Segment"] == "Mid-Value Regular Customers"].iloc[0]
    loyal = cp[cp["Segment"] == "High-Value Loyal Customers"].iloc[0]

    convert_rate = 0.10
    occ_uplift = convert_rate * occ["Customer_Count"] * (mid["Avg_Monetary"] - occ["Avg_Monetary"])
    mid_uplift = 0.05 * mid["Customer_Count"] * mid["Avg_Monetary"]
    churn_saved = 0.02 * loyal["Customer_Count"] * loyal["Avg_Monetary"]

    scenarios = [
        ("Activate 10% of Recent Occasional", occ_uplift,
         f"Move {convert_rate*occ['Customer_Count']:.0f} customers to Mid-Value average spend",
         "#FBBF24"),
        ("Lift Mid-Value spend by 5%", mid_uplift,
         f"Applied across all {int(mid['Customer_Count']):,} Mid-Value customers", "#60A5FA"),
        ("Prevent 2% of High-Value churn", churn_saved,
         f"Retaining {0.02*loyal['Customer_Count']:.0f} of the highest-value accounts", "#34D399"),
    ]
    total_opp = sum(v for _, v, _, _ in scenarios)

    scen_html = "".join(f"""
<div class="glass pad" data-tilt="7" data-reveal="{i*110}">
  <div class="lift">
    <div class="kpi-label">{name}</div>
    <div class="kpi-value" style="color:{c}">
      <span data-count="{val/1000:.1f}" data-decimals="1" data-prefix="£" data-suffix="K">£0K</span>
    </div>
    <div class="kpi-foot">{note}</div>
    <div class="kpi-spark"><i data-w="{min(val/total_opp*100*2, 100):.0f}"
      style="background:linear-gradient(90deg,{c},{c}55)"></i></div>
  </div>
</div>""" for i, (name, val, note, c) in enumerate(scenarios))

    rev_rows = [(r["Segment"], float(r["Revenue_Share_%"])) for _, r in cp.iterrows()]

    body = f"""
{viz.page_head(
    "Business Insights",
    'From segments to <span class="grad-amber">decisions</span>',
    "What each segment is worth, what it should be spent on, and where the "
    "next increment of revenue is most likely to come from."
)}

{viz.section("Business Strategy Simulator",
             "Review the scenario, select a strategy, and compare its estimated "
             "commercial impact against the alternatives.")}

{render_simulator()}

{viz.section("Priority by segment",
             "Each segment gets a different job — protecting revenue, growing it, "
             "converting it, or serving it cheaply.")}

<div class="row row-2 mt-20">
  {''.join(cards)}
</div>

{viz.section("Where the next revenue comes from",
             "Three conservative scenarios, each stated with its own assumption so the "
             "arithmetic can be checked rather than trusted.")}

<div class="row row-3 mt-20">{scen_html}</div>

<div class="glass pad-lg mt-32" data-reveal="0"
     style="background:linear-gradient(120deg,rgba(243,166,74,.13),rgba(139,92,246,.09))">
  <div class="kpi-label">Combined modelled opportunity</div>
  <div class="kpi-value" style="font-size:52px;margin-top:6px">
    <span data-count="{total_opp/1000:.0f}" data-decimals="0" data-prefix="£" data-suffix="K">£0K</span>
  </div>
  <p class="body" style="margin-top:16px;max-width:66ch">
    Roughly <strong>{total_opp / kpis['total_revenue'] * 100:.1f}%</strong> of current
    revenue, from three independent levers. These are scenario estimates built on the
    stated assumptions above — not forecasts, and they assume the behavioural averages
    hold as customers move between segments.
  </p>
</div>

{viz.section("Revenue contribution at a glance")}

<div class="row row-12 mt-20">
  <div class="glass pad-lg" data-tilt="5" data-reveal="0">
    <div class="lift-sm">
      <h3 class="card-title">Revenue share by segment</h3>
      {viz.hbars(rev_rows)}
    </div>
  </div>
  <div class="glass pad-lg" data-tilt="5" data-reveal="120">
    <div class="lift-sm">
      <h3 class="card-title">Budget allocation principle</h3>
      <p class="body">
        Marketing spend should track <strong>revenue share</strong>, not customer
        count. Allocating evenly across the base sends roughly 37% of the budget to
        a segment that returns 6% of revenue.
      </p>
      <p class="body" style="margin-top:16px">
        The practical rule: personalised, human, high-cost effort for High-Value and
        Mid-Value; automated, templated, low-cost effort for Inactive; and a focused
        conversion programme for Recent Occasional, where the marginal return is
        highest.
      </p>
    </div>
  </div>
</div>

{viz.section("Limitations worth stating",
             "What this analysis does not tell you.")}

<div class="row row-3 mt-20">
  <div class="glass pad" data-tilt="6" data-reveal="0"><div class="lift">
    <h3 class="card-title">One year, one retailer</h3>
    <p class="body">The dataset covers a single UK online retailer over roughly one
    year. Seasonality and category mix are not controlled for.</p>
  </div></div>
  <div class="glass pad" data-tilt="6" data-reveal="110"><div class="lift">
    <h3 class="card-title">Behaviour, not causation</h3>
    <p class="body">Segments describe what customers did, not why. A segment change
    after a campaign is not proof the campaign caused it.</p>
  </div></div>
  <div class="glass pad" data-tilt="6" data-reveal="220"><div class="lift">
    <h3 class="card-title">Snapshot, not lifecycle</h3>
    <p class="body">RFM is computed at a point in time. Customers move between
    segments; re-scoring on a schedule is required to keep the view live.</p>
  </div></div>
</div>
"""

    # Tallest of the four strategy panels, measured; the simulator swaps content
    # in place so the page must fit whichever strategy is selected.
    render(body, height=3980, css=viz.VIZ_CSS + SIM_CSS, js=viz.VIZ_JS + sim_js())
