# Customer Segmentation using RFM Analysis and K-Means Clustering

## Project Overview

This project applies customer segmentation techniques to transaction-level retail data to identify distinct customer groups based on purchasing behavior.

Using RFM (Recency, Frequency, Monetary) analysis and K-Means clustering, customers were grouped into segments with different behavioral and revenue characteristics.

The goal is to better understand customer value distribution and demonstrate how behavioral segmentation can support business decision-making.

---

## Business Problem

Not all customers contribute equally to business performance.

The objective of this project is to:

* Identify distinct customer segments based on purchasing behavior
* Understand how different customer groups contribute to revenue
* Highlight opportunities for retention, growth, and customer engagement
* Demonstrate an end-to-end analytics workflow from raw data to business insights

---

## Dataset

**Dataset:** UCI Online Retail Dataset

**Source:** https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transaction-level records from a UK-based online retailer.

---

## Methodology

### 1. Data Cleaning and Preprocessing

* Removed records with missing Customer IDs
* Removed cancelled invoices
* Removed invalid transactions
* Removed duplicate records
* Created a TotalSpend feature

### 2. RFM Feature Engineering

Customer behavior was summarized using:

* Recency
* Frequency
* Monetary

### 3. Data Transformation

* Log transformation
* StandardScaler

### 4. Customer Segmentation

K-Means clustering was applied to the transformed RFM dataset.

Cluster selection was supported using:

* Elbow Method
* Silhouette Score

A final solution of **4 customer segments** was selected.

---

## Key Findings

| Segment                      | Customer Share | Revenue Share |
| ---------------------------- | -------------- | ------------- |
| High-Value Loyal Customers   | 16.44%         | 64.89%        |
| Mid-Value Regular Customers  | 26.88%         | 23.64%        |
| Recent Occasional Customers  | 19.29%         | 5.25%         |
| Inactive Low-Value Customers | 37.39%         | 6.22%         |

### Insights

* High-Value Loyal Customers generate the majority of total revenue despite representing a relatively small share of customers.
* Inactive Low-Value Customers represent the largest customer segment but contribute comparatively little revenue.
* Mid-Value Regular Customers contribute nearly one-quarter of total revenue.
* Recent Occasional Customers may represent a growth opportunity.

---

## Tools Used

* Python
* pandas
* NumPy
* matplotlib
* seaborn
* scikit-learn
* Jupyter Notebook

---

## Repository Structure

```text
customer-segmentation-rfm/
├── data/
├── notebooks/
├── outputs/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Project Status

### Completed

* Data cleaning and preprocessing
* RFM feature engineering
* Exploratory data analysis
* Data transformation
* K-Means clustering
* Segment profiling
* Business insights and recommendations

### In Progress

* Power BI dashboard development
* Final project documentation
* GitHub project packaging

---

## Future Enhancements

* Interactive Power BI dashboard
* Additional customer behavior metrics
* Dashboard-based business recommendations
