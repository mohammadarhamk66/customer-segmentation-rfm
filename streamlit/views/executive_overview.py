from components import viz
from components.shell import render
from utils.constants import SEGMENT_ORDER, SEGMENT_COLORS, SEGMENT_SHORT


def show_executive_overview(rfm, cluster_profile, kpis, sample):
    cp = cluster_profile

    cust_rows = [(r["Segment"], float(r["Customer_Share_%"])) for _, r in cp.iterrows()]
    rev_rows = [(r["Segment"], float(r["Revenue_Share_%"])) for _, r in cp.iterrows()]
    cmp_rows = [
        (r["Segment"], float(r["Customer_Share_%"]), float(r["Revenue_Share_%"]))
        for _, r in cp.iterrows()
    ]

    top = cp[cp["Segment"] == "High-Value Loyal Customers"].iloc[0]

    # value concentration table
    table_rows = []
    for _, r in cp.iterrows():
        seg = r["Segment"]
        c = SEGMENT_COLORS.get(seg, "#94A3B8")
        intensity = float(r["Revenue_Share_%"]) / float(r["Customer_Share_%"])
        table_rows.append(f"""
<tr>
  <td><div class="seg-cell"><span class="bar" style="background:{c};box-shadow:0 0 10px {c}"></span>
      {SEGMENT_SHORT.get(seg, seg)}</div></td>
  <td class="num">{int(r['Customer_Count']):,}</td>
  <td class="num">{r['Avg_Recency']:.0f} d</td>
  <td class="num">{r['Avg_Frequency']:.1f}</td>
  <td class="num">£{r['Avg_Monetary']:,.0f}</td>
  <td class="num">£{r['Total_Revenue']/1_000_000:.2f}M</td>
  <td class="num" style="color:{c}">{intensity:.2f}×</td>
</tr>""")

    cloud_html, cloud_js = viz.scatter_3d(sample, height=400, canvas_id="execCloud")

    body = f"""
{viz.page_head(
    "Executive Overview",
    'Where the <span class="grad-amber">value</span> actually sits',
    "A single view of how 4,338 customers split into four behavioural segments, and "
    "how unevenly those segments carry revenue."
)}

<div class="row row-4 mt-32">
  {viz.kpi("Total customers", kpis['total_customers'], "Across all four segments",
           spark=100, color="#60A5FA", delay=0)}
  {viz.kpi("Total revenue", kpis['total_revenue'] / 1_000_000, "Sum of customer monetary value",
           decimals=2, prefix="£", suffix="M", spark=94, color="#34D399", delay=90)}
  {viz.kpi("Average customer value", kpis['avg_monetary'], "Mean spend per customer",
           decimals=0, prefix="£", spark=52, color="#F3A64A", delay=180)}
  {viz.kpi("Median recency", kpis['median_recency'], "Days since last purchase",
           decimals=0, suffix=" d", spark=38, color="#8B5CF6", delay=270)}
</div>

{viz.section("Customers versus revenue",
             "The two distributions are close to inverted — the concentration that "
             "defines the entire commercial strategy.")}

<div class="row row-2 mt-20">
  <div class="glass pad-lg" data-tilt="6" data-reveal="0">
    <div class="lift-sm">
      <h3 class="card-title">Share of customers</h3>
      <p class="body" style="margin-bottom:8px">How the base splits by headcount.</p>
      {viz.donut(cust_rows, f"{cust_rows[0][1]:.1f}%", "High-Value Loyal")}
    </div>
  </div>
  <div class="glass pad-lg" data-tilt="6" data-reveal="120">
    <div class="lift-sm">
      <h3 class="card-title">Share of revenue</h3>
      <p class="body" style="margin-bottom:8px">How the same base splits by money.</p>
      {viz.donut(rev_rows, f"{rev_rows[0][1]:.1f}%", "High-Value Loyal")}
    </div>
  </div>
</div>

<div class="mt-20" data-reveal="0">{viz.legend(SEGMENT_ORDER)}</div>

<div class="glass pad-lg mt-32" data-tilt="4" data-reveal="0">
  <div class="lift-sm">
    <h3 class="card-title">Customer share against revenue share</h3>
    <p class="body" style="margin-bottom:24px">
      Where the revenue bar overshoots the customer bar, the segment is punching
      above its weight. Where it falls short, the segment costs more to serve than
      it returns.
    </p>
    {viz.compare_bars(cmp_rows)}
  </div>
</div>

{viz.section("Value concentration",
             "Revenue intensity is revenue share divided by customer share — how many "
             "times more revenue a segment carries than its headcount would imply.")}

<div class="glass pad-lg mt-20" data-reveal="0">
  <table class="data">
    <thead><tr>
      <th>Segment</th><th style="text-align:right">Customers</th>
      <th style="text-align:right">Avg recency</th><th style="text-align:right">Avg frequency</th>
      <th style="text-align:right">Avg value</th><th style="text-align:right">Total revenue</th>
      <th style="text-align:right">Intensity</th>
    </tr></thead>
    <tbody>{''.join(table_rows)}</tbody>
  </table>
</div>

{viz.section("Average revenue per customer",
             "The same story on a per-head basis.")}

<div class="glass pad-lg mt-20" data-tilt="4" data-reveal="0">
  <div class="lift-sm">
    {viz.hbars([(r["Segment"], float(r["Avg_Monetary"])) for _, r in cp.iterrows()],
               value_fmt="£{:,.0f}")}
  </div>
</div>

{viz.section("The segmented base, in space",
             "Recency on X, Monetary on Y, Frequency on Z — the separation K-Means found.")}

<div class="glass mt-20" data-reveal="0" style="padding:20px 20px 8px 20px">
  {cloud_html}
</div>

<div class="glass pad-lg mt-44" data-reveal="0"
     style="background:linear-gradient(120deg,rgba(52,211,153,.11),rgba(139,92,246,.09))">
  <h2 class="section" style="font-size:22px">The headline</h2>
  <p class="body" style="max-width:66ch">
    <strong>{int(top['Customer_Count']):,} customers</strong> — {top['Customer_Share_%']:.1f}% of
    the base — generate <strong>£{top['Total_Revenue']/1_000_000:.2f}M</strong>, or
    {top['Revenue_Share_%']:.1f}% of all revenue. Retention effort aimed at this group has
    roughly <strong>{float(top['Revenue_Share_%'])/float(top['Customer_Share_%']):.1f}×</strong>
    the revenue leverage of effort spread evenly across the base.
  </p>
</div>
"""

    render(body, height=3160, css=viz.VIZ_CSS, js=viz.VIZ_JS + cloud_js)
