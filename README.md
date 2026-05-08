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
