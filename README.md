# Customer Intelligence Platform

An interactive Business Intelligence dashboard that combines **RFM Analysis**, **K-Means Clustering**, and **executive-focused storytelling** to transform customer transaction data into actionable business insights.

🚀 **Live Application:**  
https://customer-segmentation-rfm-customer-intelligence.streamlit.app/

---

# Project Overview

The Customer Intelligence Platform helps businesses understand customer behaviour through intelligent customer segmentation and interactive visual analytics.

Using **Recency, Frequency, and Monetary (RFM) Analysis** together with **K-Means Clustering**, customers are segmented into meaningful business groups that executives can easily explore and act upon.

Rather than presenting only analytical results, the dashboard focuses on translating data into business decisions through an interactive executive experience.

---

# Dashboard Modules

## About Project

Provides an overview of the project including:

- Business problem
- Analytical workflow
- Methodology
- Technology stack
- Dashboard architecture

---

## Executive Overview

Designed for executive stakeholders to quickly understand customer performance.

Features include:

- Executive KPI cards
- Revenue distribution
- Customer distribution
- Segment performance
- Interactive segment filtering
- Executive business insights

Selecting a customer segment automatically updates the dashboard with segment-specific insights.

---

## Segment Explorer

Allows users to investigate individual customer segments in greater detail.

Features include:

- Interactive segment selector
- RFM distributions
- Customer segment profile
- Recommended business actions
- Sample customer records
- Top monetary customers
- Lowest monetary customers

---

## Business Strategy Simulator

A scenario-based decision support tool designed for business users.

Users can evaluate four strategic approaches:

- Retain
- Grow
- Convert
- Re-engage

Each strategy presents:

- Business objective
- Estimated business impact
- Recommended actions
- Expected business outcomes
- Success criteria

The simulator demonstrates how different customer strategies may influence business performance.

---


## AI Analyst

An analyst powered by the Claude API, connected live to the customer dataset.

It answers questions in business terms and backs every figure with a real query.
Three tools run against the dataframe on request:

- `segment_overview` — the full profile of all four segments
- `query_customers` — filters customers by recency, frequency, spend and segment
- `compute_statistic` — medians, percentiles, standard deviations, correlations

The model never receives the raw customer rows. It calls these tools, which run
pandas locally and return compact summaries, so **every number it quotes is
computed on request rather than recalled** — and token cost stays flat regardless
of dataset size.

Without an API key the page still works: it reports the pre-computed segment
profile and states plainly that it is running offline.

---

# Machine Learning Workflow

```
Customer Transaction Data
            │
            ▼
      Data Cleaning
            │
            ▼
   Feature Engineering
            │
            ▼
        RFM Analysis
            │
            ▼
    Feature Scaling
            │
            ▼
     K-Means Clustering
            │
            ▼
 Customer Segmentation
            │
            ▼
 Interactive Dashboard
            │
            ▼
 Executive Decision Support
```

---

# Technologies Used

### Programming

- Python

### Machine Learning

- Scikit-learn

### Data Analysis

- Pandas
- NumPy

### Data Visualisation

- Plotly

### Dashboard Development

- Streamlit

### Front-End

- HTML
- CSS
- JavaScript (custom design system — no chart or animation libraries)

### AI

- Anthropic Claude API (`claude-opus-5`) with tool use

---

# Key Features

- Interactive Executive Dashboard
- Customer Segmentation using RFM Analysis
- K-Means Customer Clustering
- Dynamic KPI Cards
- Interactive Segment Filtering
- Executive Business Insights
- Strategy Recommendation Simulator
- Modern Custom UI Components
- Glassmorphic 3D Interface with Motion Design
- Interactive 3D RFM Customer Cloud
- AI Analyst with Live Dataset Access
- Responsive Desktop Experience

---

# Business Value

The platform enables organisations to:

- Identify high-value customers
- Detect customers at risk of churn
- Understand customer purchasing behaviour
- Prioritise marketing investment
- Improve customer retention strategies
- Support executive decision-making
- Transform analytics into actionable business recommendations

---

# Project Status

**Version:** v2.0

**Status:** ✅ Completed

This project has been successfully developed, tested, documented, and deployed as a portfolio project.

**v2.0** rebuilt the interface on a custom glassmorphic 3D design system and added
the AI Analyst. **v1.0** delivered the segmentation analysis and the original
dashboard.

Future enhancements will be released as future versions.

---

# Future Improvements

Potential future enhancements include:

- Predictive customer lifetime value
- Revenue forecasting
- Multi-currency business metrics
- Advanced scenario simulation
- AI-generated executive summaries

---

# Run Locally

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure the AI Analyst (optional)

```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

On Streamlit Community Cloud, add the same key under **Settings → Secrets**.
The app runs without it — the AI Analyst falls back to offline mode.

Run the application

```bash
streamlit run streamlit/app.py
```

---

# Screenshots

*Dashboard screenshots can be added here.*

---

# Author

Mohammad Arham Khan

Business Intelligence • Data Analytics • Machine Learning

