# Customer Segmentation using RFM Analysis and K-Means

## Project Overview

This project explores customer segmentation using transaction-level retail data. The goal is to group customers based on the purchasing behavior and identify which types of customers may drive the most business value.

The project will use RFM analysis:

- **Recency:** how recently a customer purchased
- **Frequency:** how often a customer purchased
- **Monetary Value:** how much a customer spent

These features will later be used for K-means clustering.

---

## Dataset

Dataset: UCI Online Retail Dataset

Source: https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transaction-level data from a UK-based online retailer. It includes information such as invoices, quantities, prices, customer IDs, and countries.

---

## Methodology

### 1. Data Cleaning
- Removed missing 'CustomerID' values
- Excluded cancelled invoices
- Removed invalid transactions (negative quantities and prices)
- Dropped duplicate records

### 2. Feature Engineering (RFM)
- **Recency:** Days since last purchase
- **Frequency:** Number of unique transactions
- **Monetary:** Total spend

### 3. Data Transformation
- Applied log transformation to reduce skewness
- Standardized features using scaling

---

## Current Status

The following stages have been completed:

- Data loading and inspection  
- Data cleaning and preprocessing  
- RFM feature engineering  
- Exploratory data analysis  
- Data transformation (log transformation and scaling)  
- K-Means clustering  
- Cluster profiling and segment labeling  

Current customer segments identified:

- High-Value Loyal Customers
- Inactive Low-Value Customers
- Recent Occasional Customers
- Mid-Value Regular Customers

Next steps:

- Revenue contribution analysis
- Segment visualization
- Business insights and recommendations
- Power BI dashboard development

---

## Tools

- Python (pandas, NumPy)
- matplotlib
- sckit-learn (K-Means clustering)
- Power BI
- Jupyter Notebook

---

## Project Structure
```
customer-segmentation-rfm/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
│   ├── figures/
│   └── tables/
├── src/
├── README.md
├── requirements.txt
└── .gitignore
```
