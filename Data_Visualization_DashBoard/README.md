# 📦 E-Commerce Sales Performance Dashboard  
### DSC 308 — Data Visualization · Project 3 · Winter 2026  

---

## Overview

An interactive analytics dashboard built with **Plotly Dash** that explores the sales performance of a U.S. retail superstore. The dashboard covers all **9 required chart types** (Weeks 1–9), organized into four analytical sections: Comparison, Relationship, Distribution, and Time-Series.

Users can filter every chart in real time by **year, product category, region, customer segment, and profit margin range** enabling drill-down exploration of business patterns across ~10,000 orders.

---

## Dataset

| Field      | Detail                                          |
|------------|-------------------------------------------------|
| Name       | Sample Superstore Dataset                       |
| Source     | [Kaggle — vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| Raw file   | `Sample - Superstore.csv`                       |
| Size       | ~10,000 rows · 21 columns                       |
| Period     | 2014 – 2017                                     |
| Key fields | Order Date, Region, Category, Sub-Category, Sales, Quantity, Discount, Profit |

---

## Project Structure

```
superstore_dashboard/
├── app.py                      # Main Dash application (all charts + callbacks)
├── data/
│   ├── raw_data.csv            # Original Superstore dataset (unmodified)
│   └── cleaned_data.csv        # Processed dataset used by the dashboard
├── notebooks/
│   └── preprocessing.ipynb     # Data cleaning & feature engineering steps
├── assets/
│   └── style.css               # Optional custom CSS overrides
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

---

## Chart Coverage

All 9 required chart types are implemented and connected to the global filter callbacks.

| Week | Category           | Chart Type              | Variable X              | Variable Y                  | Dashboard Section                  |
|------|--------------------|-------------------------|-------------------------|-----------------------------|------------------------------------|
| 1    | Comparison         | Column Chart            | Product Category        | Total Sales (USD)           | Section 1 — Comparison, Row 1 (Left)  |
| 1    | Comparison         | Bar Chart               | Total Profit (USD)      | Sub-Category                | Section 1 — Comparison, Row 1 (Right) |
| 2    | Comparison         | Stacked Column Chart    | Region                  | Total Sales by Category     | Section 1 — Comparison, Row 2 (Left)  |
| 2    | Comparison         | Stacked Bar Chart       | Total Profit by Category| Customer Segment            | Section 1 — Comparison, Row 2 (Right) |
| 2    | Comparison         | Clustered Column Chart  | Ship Mode               | Sales & Profit (USD)        | Section 1 — Comparison, Row 3 (Left)  |
| 2    | Comparison         | Clustered Bar Chart     | Sales & Profit (USD)    | Region                      | Section 1 — Comparison, Row 3 (Right) |
| 3    | Relationship       | Scatter Chart           | Order Sales (USD)       | Order Profit (USD)          | Section 2 — Relationship (Left)        |
| 4    | Relationship       | Bubble Chart            | Total Sales (USD)       | Total Profit (USD)          | Section 2 — Relationship (Right)       |
| 5    | Distribution       | Histogram               | Order Sales (USD)       | Number of Orders            | Section 3 — Distribution (Full Width)  |
| 6    | Distribution       | Box Chart               | Discount Tier           | Order Profit (USD)          | Section 3 — Distribution, Row 2 (Left) |
| 7    | Distribution       | Violin Chart            | Customer Segment        | Order Sales (USD)           | Section 3 — Distribution, Row 2 (Right)|
| 8    | Time-Series        | Line Chart              | Month                   | Monthly Sales (USD)         | Section 4 — Time-Series (Full Width)   |
| 9    | Time-Series        | Area Chart              | Month                   | Cumulative Sales & Profit   | Section 4 — Time-Series (Full Width)   |

---

## Interactive Elements

The dashboard includes **5 interactive controls**, all wired to Dash callbacks that update every chart dynamically:

| # | Control             | Type          | Effect                                                  |
|---|---------------------|---------------|---------------------------------------------------------|
| 1 | Year                | Dropdown      | Filters all charts to the selected year (or all years)  |
| 2 | Category            | Dropdown      | Narrows to a single product category                    |
| 3 | Region              | Dropdown      | Narrows to a single geographic region                   |
| 4 | Customer Segment    | Radio Buttons | Filters by Consumer, Corporate, or Home Office          |
| 5 | Profit Margin Range | Range Slider  | Filters orders by profit margin (e.g. only profitable)  |
| 6 | Histogram Bin Size  | Slider        | Adjusts bin resolution on the histogram chart only      |

Additionally, **4 KPI summary cards** (Total Sales, Total Profit, Total Orders, Avg Order Value) update dynamically with every filter change.

---

## How to Run

### Prerequisites

- Python 3.9 or higher
- pip

### Step 1 — Clone or unzip the project

```bash
unzip superstore_dashboard.zip
cd superstore_dashboard
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Prepare the data

Open the preprocessing notebook and run all cells. This reads `data/raw_data.csv`, cleans the data, engineers new features, and exports `data/cleaned_data.csv`.

```bash
jupyter notebook notebooks/preprocessing.ipynb
```

> **Note:** If `cleaned_data.csv` is already present in `data/`, you can skip this step and go directly to Step 4.

### Step 4 — Launch the dashboard

```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:8050/**

---

## Data Preprocessing (Detailed)

The preprocessing pipeline ensures the dataset is clean, consistent, and ready for analysis.

### 1. Data Loading
- Loaded using pandas with proper encoding (`latin1`)

### 2. Date Handling
- Converted `Order Date` and `Ship Date` into datetime format

### 3. Data Type Validation
- Converted Sales, Profit, Discount, and Quantity into numeric
- Dropped invalid or missing rows

### 4. Handling Invalid Values
- Clipped Discount values between 0 and 1
- Checked abnormal values but kept them for analysis

### 5. Feature Engineering
- Created:
  - Year, Month, Quarter
  - Profit Margin = Profit / Sales
  - Shipping Days
  - Discount Tier categories

### 6. Outlier Handling
- Used IQR method
- Outliers were kept to preserve real-world insights

### 7. Export
- Saved cleaned dataset as `cleaned_data.csv`

---

## Key Insights (Per Chart)

| Section        | Chart Type                        | Insight                                                                 | Business Implication                          |
|----------------|----------------------------------|-------------------------------------------------------------------------|-----------------------------------------------|
| Comparison     | Sales by Category (Column)       | Technology leads in total revenue                                       | Focus on high-value/premium products          |
| Comparison     | Profit by Sub-Category (Bar)     | Some sub-categories generate negative profit                            | Review pricing and discount strategies        |
| Comparison     | Sales by Region (Stacked Column) | West region dominates sales                                             | Strengthen high-performing regions            |
| Comparison     | Profit by Segment (Stacked Bar)  | Consumer segment contributes the most profit                            | Target marketing toward this segment          |
| Comparison     | Sales vs Profit by Ship Mode     | Faster shipping reduces profitability                                   | Optimize logistics vs cost trade-off          |
| Relationship   | Scatter Plot                    | Weak correlation between sales and profit                               | High sales do not guarantee high profit       |
| Relationship   | Bubble Chart                    | Large sales orders are not always efficient                             | Focus on profitability, not just volume       |
| Distribution   | Histogram                       | Most orders are low-value with few high-value outliers                  | Business depends on frequent small purchases  |
| Distribution   | Box Plot                        | High discounts significantly reduce profit                              | Limit excessive discounting                   |
| Distribution   | Violin Plot                     | Consumer segment shows highest variability in sales                     | Diverse customer behavior requires targeting  |
| Time-Series    | Line Chart                      | Sales peak in Q4 (Oct–Dec)                                              | Plan inventory and promotions seasonally      |
| Time-Series    | Area Chart                      | Profit grows slower than sales over time                                | Efficiency and cost structure need review     |

## Academic Integrity

This project was completed with full adherence to academic integrity policies.

- All code was written and understood by the team
- No unauthorized copying or plagiarism was involved
- External resources were used only for learning and are properly acknowledged
- Every team member can fully explain all parts of the project (code, preprocessing, and visualizations)

Any assistance tools (including AI) were used only to enhance understanding and not to replace original work.

---

## How to Run

```bash
pip install -r requirements.txt
python app.py
```
