"""Design tokens and shared copy for the Customer Intelligence Platform."""

APP_TITLE = "Customer Intelligence Platform"
APP_SUBTITLE = "Customer Segmentation & Insights"

# Dark-glass palette. Each segment carries a base colour plus a lighter
# companion used for gradients, glows and 3D depth shading.
SEGMENT_COLORS = {
    "High-Value Loyal Customers": "#34D399",
    "Mid-Value Regular Customers": "#60A5FA",
    "Recent Occasional Customers": "#FBBF24",
    "Inactive Low-Value Customers": "#94A3B8",
}

SEGMENT_GLOW = {
    "High-Value Loyal Customers": "#6EE7B7",
    "Mid-Value Regular Customers": "#93C5FD",
    "Recent Occasional Customers": "#FCD34D",
    "Inactive Low-Value Customers": "#CBD5E1",
}

SEGMENT_ORDER = [
    "High-Value Loyal Customers",
    "Mid-Value Regular Customers",
    "Recent Occasional Customers",
    "Inactive Low-Value Customers",
]

SEGMENT_SHORT = {
    "High-Value Loyal Customers": "High-Value Loyal",
    "Mid-Value Regular Customers": "Mid-Value Regular",
    "Recent Occasional Customers": "Recent Occasional",
    "Inactive Low-Value Customers": "Inactive Low-Value",
}

SEGMENT_PROFILES = {
    "High-Value Loyal Customers": (
        "Purchased recently, buy frequently, and spend significantly more than "
        "any other group. This is the revenue engine of the business."
    ),
    "Mid-Value Regular Customers": (
        "Purchase consistently and contribute meaningful revenue, but still have "
        "clear headroom to grow in both frequency and basket size."
    ),
    "Recent Occasional Customers": (
        "Purchased recently but have not yet shown repeat behaviour or high "
        "spending. The clearest growth opportunity in the base."
    ),
    "Inactive Low-Value Customers": (
        "Have not purchased recently, buy infrequently, and contribute little "
        "revenue. The largest group by headcount, the smallest by value."
    ),
}

RECOMMENDED_ACTIONS = {
    "High-Value Loyal Customers": [
        "Prioritise retention over acquisition spend",
        "Offer loyalty rewards and tiered benefits",
        "Provide early access to new products",
        "Use personalised recommendations",
    ],
    "Mid-Value Regular Customers": [
        "Increase basket size through bundles",
        "Run cross-sell campaigns on adjacent categories",
        "Encourage repeat purchases with reorder prompts",
        "Test targeted upgrade offers",
    ],
    "Recent Occasional Customers": [
        "Drive the critical second purchase",
        "Send onboarding-style campaign sequences",
        "Recommend related products post-purchase",
        "Use limited-time conversion offers",
    ],
    "Inactive Low-Value Customers": [
        "Use low-cost automated re-engagement only",
        "Avoid heavy personalised marketing spend",
        "Test a single limited-time win-back offer",
        "Suppress from expensive campaigns if unresponsive",
    ],
}

# Model used by the AI analyst.
CLAUDE_MODEL = "claude-opus-5"
