"""Tools that let the AI analyst query the real RFM dataset.

The model never sees the 4,338 raw rows — it calls these tools, which run pandas
locally and return compact summaries. That keeps token cost flat regardless of
dataset size and means every number the analyst quotes is computed, not recalled.
"""

import json

import pandas as pd

from utils.constants import SEGMENT_ORDER

NUMERIC_FIELDS = ["Recency", "Frequency", "Monetary"]

TOOLS = [
    {
        "name": "segment_overview",
        "description": (
            "Return the full profile of every customer segment: customer count, "
            "customer share, revenue share, total revenue, and average recency, "
            "frequency and monetary value. Call this whenever the question is about "
            "how segments compare, which segment is biggest or most valuable, or "
            "when you need the baseline numbers before reasoning further."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "query_customers",
        "description": (
            "Filter the customer-level RFM table and return aggregate statistics plus "
            "a small sample of matching customers. Call this when the question is "
            "about a specific slice of customers — for example 'customers who spent "
            "over £5,000', 'lapsed high-value customers', or 'how many people in the "
            "Mid-Value segment ordered more than 10 times'. Returns the match count, "
            "their share of the base, their total and average spend, and up to 10 "
            "example customers."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "segment": {
                    "type": "string",
                    "enum": SEGMENT_ORDER,
                    "description": "Restrict to one segment. Omit to search all customers.",
                },
                "min_recency": {"type": "number", "description": "Minimum days since last purchase."},
                "max_recency": {"type": "number", "description": "Maximum days since last purchase."},
                "min_frequency": {"type": "number", "description": "Minimum number of orders."},
                "max_frequency": {"type": "number", "description": "Maximum number of orders."},
                "min_monetary": {"type": "number", "description": "Minimum total spend in GBP."},
                "max_monetary": {"type": "number", "description": "Maximum total spend in GBP."},
                "sort_by": {
                    "type": "string",
                    "enum": ["Monetary", "Frequency", "Recency"],
                    "description": "Field used to pick the example customers. Defaults to Monetary.",
                },
                "sort_desc": {
                    "type": "boolean",
                    "description": "Sort descending (highest first). Defaults to true.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "compute_statistic",
        "description": (
            "Compute one statistic over Recency, Frequency or Monetary, optionally "
            "grouped by segment and optionally restricted to a segment. Use this for "
            "precise numbers the other tools do not already give you — medians, "
            "percentiles, standard deviations, correlations between two RFM fields, "
            "or a total across a subset. Never estimate a number you could compute here."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "field": {
                    "type": "string",
                    "enum": NUMERIC_FIELDS,
                    "description": "The RFM field to summarise.",
                },
                "statistic": {
                    "type": "string",
                    "enum": ["sum", "mean", "median", "min", "max", "std",
                             "count", "percentile", "correlation"],
                    "description": (
                        "Which statistic to compute. 'percentile' requires the "
                        "percentile argument; 'correlation' requires against_field."
                    ),
                },
                "percentile": {
                    "type": "number",
                    "description": "Percentile between 0 and 100, used when statistic is 'percentile'.",
                },
                "against_field": {
                    "type": "string",
                    "enum": NUMERIC_FIELDS,
                    "description": "Second field, used when statistic is 'correlation'.",
                },
                "group_by_segment": {
                    "type": "boolean",
                    "description": "Return one value per segment instead of one overall value.",
                },
                "segment": {
                    "type": "string",
                    "enum": SEGMENT_ORDER,
                    "description": "Restrict the computation to a single segment.",
                },
            },
            "required": ["field", "statistic"],
            "additionalProperties": False,
        },
    },
]


def _apply_filters(rfm, args):
    df = rfm
    if args.get("segment"):
        df = df[df["Segment"] == args["segment"]]
    bounds = [
        ("min_recency", "Recency", "ge"), ("max_recency", "Recency", "le"),
        ("min_frequency", "Frequency", "ge"), ("max_frequency", "Frequency", "le"),
        ("min_monetary", "Monetary", "ge"), ("max_monetary", "Monetary", "le"),
    ]
    for key, col, op in bounds:
        if args.get(key) is not None:
            df = df[getattr(df[col], op)(args[key])]
    return df


def _segment_overview(rfm, cluster_profile):
    rows = []
    for _, r in cluster_profile.iterrows():
        rows.append({
            "segment": r["Segment"],
            "customers": int(r["Customer_Count"]),
            "customer_share_pct": round(float(r["Customer_Share_%"]), 2),
            "revenue_share_pct": round(float(r["Revenue_Share_%"]), 2),
            "total_revenue_gbp": round(float(r["Total_Revenue"]), 2),
            "avg_recency_days": round(float(r["Avg_Recency"]), 1),
            "avg_frequency_orders": round(float(r["Avg_Frequency"]), 2),
            "avg_monetary_gbp": round(float(r["Avg_Monetary"]), 2),
        })
    return {
        "total_customers": int(len(rfm)),
        "total_revenue_gbp": round(float(rfm["Monetary"].sum()), 2),
        "segments": rows,
    }


def _query_customers(rfm, args):
    df = _apply_filters(rfm, args)
    if df.empty:
        return {"matches": 0, "note": "No customers match those filters."}

    sort_by = args.get("sort_by", "Monetary")
    df = df.sort_values(sort_by, ascending=not args.get("sort_desc", True))

    sample = df.head(10)[["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]]
    sample = sample.round({"Monetary": 2}).to_dict("records")

    by_segment = (
        df.groupby("Segment")
        .agg(customers=("CustomerID", "count"), revenue=("Monetary", "sum"))
        .round(2)
        .to_dict("index")
    )

    return {
        "matches": int(len(df)),
        "share_of_all_customers_pct": round(len(df) / len(rfm) * 100, 2),
        "total_spend_gbp": round(float(df["Monetary"].sum()), 2),
        "share_of_all_revenue_pct": round(
            float(df["Monetary"].sum()) / float(rfm["Monetary"].sum()) * 100, 2
        ),
        "avg_spend_gbp": round(float(df["Monetary"].mean()), 2),
        "median_spend_gbp": round(float(df["Monetary"].median()), 2),
        "avg_frequency": round(float(df["Frequency"].mean()), 2),
        "avg_recency_days": round(float(df["Recency"].mean()), 1),
        "breakdown_by_segment": by_segment,
        "sample_customers": sample,
    }


def _compute_statistic(rfm, args):
    field = args["field"]
    stat = args["statistic"]
    df = rfm[rfm["Segment"] == args["segment"]] if args.get("segment") else rfm

    def one(frame):
        s = frame[field]
        if stat == "sum":
            return round(float(s.sum()), 2)
        if stat == "mean":
            return round(float(s.mean()), 2)
        if stat == "median":
            return round(float(s.median()), 2)
        if stat == "min":
            return round(float(s.min()), 2)
        if stat == "max":
            return round(float(s.max()), 2)
        if stat == "std":
            return round(float(s.std()), 2)
        if stat == "count":
            return int(s.count())
        if stat == "percentile":
            p = args.get("percentile")
            if p is None:
                return "error: percentile statistic requires the 'percentile' argument"
            return round(float(s.quantile(p / 100)), 2)
        if stat == "correlation":
            other = args.get("against_field")
            if not other:
                return "error: correlation statistic requires 'against_field'"
            return round(float(frame[field].corr(frame[other])), 4)
        return f"error: unsupported statistic {stat}"

    if args.get("group_by_segment"):
        return {
            "field": field, "statistic": stat,
            "by_segment": {
                seg: one(df[df["Segment"] == seg])
                for seg in SEGMENT_ORDER if not df[df["Segment"] == seg].empty
            },
        }

    return {
        "field": field, "statistic": stat,
        "scope": args.get("segment", "all customers"),
        "value": one(df),
    }


def execute(name, args, rfm, cluster_profile):
    """Run a tool call and return a JSON string for the tool_result block."""
    try:
        if name == "segment_overview":
            result = _segment_overview(rfm, cluster_profile)
        elif name == "query_customers":
            result = _query_customers(rfm, args)
        elif name == "compute_statistic":
            result = _compute_statistic(rfm, args)
        else:
            return json.dumps({"error": f"unknown tool: {name}"}), True

        return json.dumps(result, default=_json_safe), False
    except Exception as exc:  # surfaced to the model so it can adjust its query
        return json.dumps({"error": f"{type(exc).__name__}: {exc}"}), True


def _json_safe(obj):
    if isinstance(obj, (pd.Timestamp,)):
        return str(obj)
    if hasattr(obj, "item"):
        return obj.item()
    return str(obj)


def build_system_prompt(cluster_profile, kpis):
    """Frozen system prompt — stable bytes so the prompt cache holds."""
    table = "\n".join(
        f"- {r['Segment']}: {int(r['Customer_Count']):,} customers "
        f"({r['Customer_Share_%']:.2f}% of base), £{r['Total_Revenue']:,.0f} revenue "
        f"({r['Revenue_Share_%']:.2f}% of total), avg recency {r['Avg_Recency']:.1f} days, "
        f"avg frequency {r['Avg_Frequency']:.2f} orders, avg value £{r['Avg_Monetary']:,.2f}"
        for _, r in cluster_profile.iterrows()
    )

    return f"""You are the AI Analyst inside a customer intelligence platform built on an \
RFM + K-Means segmentation of the UCI Online Retail dataset — {kpis['total_customers']:,} \
customers of a UK online retailer, £{kpis['total_revenue']:,.0f} in total customer value, \
split into four behavioural segments.

The segments, for reference:
{table}

Field meanings: Recency is days since the customer's last purchase (lower is better). \
Frequency is their number of orders. Monetary is their total spend in GBP over the period.

How to work:
- You have three tools over the live dataset. Use them for any question that turns on a \
number. The reference table above is a summary; the tools are the source of truth, and \
they can answer things the table cannot.
- Never estimate or recall a figure you could compute with compute_statistic or \
query_customers. If you state a number, it should have come from a tool call in this \
conversation or from the reference table above.
- Answer as an analyst talking to a commercial stakeholder: lead with the answer, then \
the number that supports it, then what to do about it. Keep responses tight — a few \
short paragraphs, or a compact markdown table when comparing segments.
- Currency is GBP. Format money as £1,234 and percentages to one decimal place.
- Be honest about the limits of the data: it is one retailer over roughly one year, it \
describes behaviour rather than cause, and it is a point-in-time snapshot. Say so when a \
question reaches past what the data can support, rather than answering anyway.
- If asked for something outside this dataset, say what you do not have and offer the \
closest question you can actually answer."""
