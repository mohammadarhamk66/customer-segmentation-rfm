from components import viz
from components.shell import render
from utils.constants import SEGMENT_ORDER


METHOD_STEPS = [
    ("Data cleaning &amp; preprocessing",
     "Removed missing Customer IDs, cancelled invoices, invalid transactions and "
     "duplicate records, then engineered a TotalSpend feature."),
    ("RFM feature engineering",
     "Summarised each customer's behaviour into Recency (days since last order), "
     "Frequency (order count) and Monetary (total spend)."),
    ("Transformation",
     "Applied a log transformation to correct heavy right-skew, then standardised "
     "the features with StandardScaler so no dimension dominates the distance metric."),
    ("K-Means clustering",
     "Ran K-Means across a range of k, selecting the final solution with the Elbow "
     "Method and Silhouette Score. Four segments gave the cleanest separation."),
    ("Segment profiling &amp; insights",
     "Profiled each cluster on size, revenue contribution and behaviour, then "
     "translated the statistics into recommended commercial actions."),
]

STACK = ["Python", "pandas", "NumPy", "scikit-learn", "matplotlib", "seaborn",
         "Jupyter", "Streamlit", "Claude API"]


def show_about_project(rfm, cluster_profile, kpis, sample):
    cloud_html, cloud_js = viz.scatter_3d(sample, height=400, canvas_id="aboutCloud")

    steps = "".join(
        f'<div class="step"><div class="st-title">{t}</div>'
        f'<div class="st-body">{b}</div></div>'
        for t, b in METHOD_STEPS
    )

    chips = "".join(f'<span class="chip">{s}</span>' for s in STACK)

    body = f"""
{viz.page_head(
    "Customer Intelligence Platform",
    'Four segments.<br><span class="grad-amber">One revenue story.</span>',
    "An end-to-end customer segmentation study on 4,338 customers of a UK online "
    "retailer — from raw transaction records through RFM feature engineering and "
    "K-Means clustering, to the commercial actions each segment deserves."
)}

<div class="row row-4 mt-32">
  {viz.kpi("Customers analysed", kpis['total_customers'], "Unique customers after cleaning",
           spark=100, color="#60A5FA", delay=0)}
  {viz.kpi("Revenue explained", kpis['total_revenue'] / 1_000_000, "Total monetary value in the base",
           decimals=2, prefix="£", suffix="M", spark=92, color="#34D399", delay=90)}
  {viz.kpi("Behavioural segments", kpis['segments'], "Chosen via elbow + silhouette",
           spark=45, color="#F3A64A", delay=180)}
  {viz.kpi("Revenue from the top segment", kpis['top_segment_revenue_share'],
           f"From just {kpis['top_segment_customer_share']:.1f}% of customers",
           decimals=1, suffix="%", spark=65, color="#8B5CF6", delay=270)}
</div>

{viz.section("The customer base in three dimensions",
             "Every dot is a real customer, positioned by Recency, Frequency and "
             "Monetary value on a log scale and coloured by segment. Drag to explore.")}

<div class="glass mt-20" data-reveal="0" style="padding:20px 20px 8px 20px">
  {cloud_html}
</div>
<div class="mt-20" data-reveal="80">{viz.legend(SEGMENT_ORDER)}</div>

{viz.section("How the segments were built",
             "A reproducible pipeline — each step is documented in the project notebook.")}

<div class="row row-21 mt-20">
  <div class="glass pad-lg" data-tilt="5" data-reveal="0">
    <div class="lift-sm">
      <h3 class="card-title">The business problem</h3>
      <p class="body">
        Not all customers contribute equally to business performance. Without a
        behavioural view of the base, retention budget gets spread evenly across
        customers whose value differs by two orders of magnitude.
      </p>
      <p class="body" style="margin-top:16px">
        This project identifies distinct customer groups from purchasing behaviour
        alone, quantifies how each group contributes to revenue, and highlights
        where retention, growth and re-engagement effort should actually go.
      </p>
      <div class="divider" style="margin:26px 0"></div>
      <h3 class="card-title">Dataset</h3>
      <p class="body">
        <strong>UCI Online Retail</strong> — transaction-level records from a
        UK-based online retailer, covering roughly one year of trading.
      </p>
      <div class="chips" style="margin-top:18px">{chips}</div>
    </div>
  </div>

  <div class="glass pad-lg" data-tilt="5" data-reveal="120">
    <div class="lift-sm">
      <h3 class="card-title">Methodology</h3>
      <div class="steps" style="margin-top:18px">{steps}</div>
    </div>
  </div>
</div>

{viz.section("What the analysis found",
             "Three findings that change where the marketing budget should sit.")}

<div class="row row-3 mt-20">
  <div class="glass pad" data-tilt="7" data-reveal="0">
    <div class="lift">
      <h3 class="card-title">Revenue is heavily concentrated</h3>
      <p class="body">
        High-Value Loyal Customers are 16.4% of the base but generate
        <strong>64.9% of revenue</strong>. Losing a small number of them costs more
        than losing an entire low-value segment.
      </p>
    </div>
  </div>
  <div class="glass pad" data-tilt="7" data-reveal="110">
    <div class="lift">
      <h3 class="card-title">The largest group is the least valuable</h3>
      <p class="body">
        Inactive Low-Value Customers are the biggest segment at 37.4% of customers,
        yet contribute only <strong>6.2% of revenue</strong>. They warrant automation,
        not personalised spend.
      </p>
    </div>
  </div>
  <div class="glass pad" data-tilt="7" data-reveal="220">
    <div class="lift">
      <h3 class="card-title">There is a clear growth pocket</h3>
      <p class="body">
        Recent Occasional Customers bought recently but haven't repeated. Converting
        them to a second purchase is the highest-leverage <strong>growth</strong>
        opportunity in the base.
      </p>
    </div>
  </div>
</div>

<div class="glass pad-lg mt-44" data-reveal="0"
     style="background:linear-gradient(120deg,rgba(243,166,74,.12),rgba(139,92,246,.09))">
  <h2 class="section" style="font-size:23px">Ask the data directly</h2>
  <p class="body" style="max-width:64ch">
    The <strong>AI Analyst</strong> in the sidebar is connected to this dataset. It can
    filter the 4,338 customers, compare segments and size opportunities on request —
    then explain the answer in business terms.
  </p>
</div>
"""

    render(body, height=2610, css=viz.VIZ_CSS, js=viz.VIZ_JS + cloud_js)
