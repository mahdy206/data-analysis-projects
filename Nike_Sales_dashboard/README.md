# 👟 Nike Sales Dashboard

An interactive Power BI dashboard analyzing Nike product sales across India, featuring comprehensive data cleaning, transformation, and visualization of sales performance, product categories, regional distribution, and profitability metrics.

---

## 📊 Dashboard Overview

This Power BI report provides end-to-end analysis of Nike sales data, including:
- **Sales Performance KPIs** - Revenue, units sold, profit margins
- **Product Analysis** - Performance by product line and category
- **Regional Insights** - Sales distribution across Indian cities
- **Channel Analytics** - Online vs. Retail performance comparison
- **Temporal Trends** - Sales patterns over time (2024-2025)
- **Customer Segmentation** - Analysis by gender category

---

## 📁 Project Files

### **1. Nike_Sales_Uncleaned__1_.csv**
- **Description:** Raw, uncleaned sales transaction data
- **Size:** 2,500 records
- **Status:** Contains data quality issues (intentional for practice)

### **2. Nike_Sales_Report.pbix**
- **Description:** Power BI report with cleaned data and visualizations
- **Status:** Complete dashboard with all transformations applied

---

## 📈 Dataset Description

### **Dataset Stats:**
- **Total Transactions:** 2,500 records
- **Date Range:** March 2024 - June 2025
- **Product Lines:** 5 categories (Training, Basketball, Lifestyle, Running, Soccer)
- **Gender Categories:** 3 types (Men, Women, Kids)
- **Sales Channels:** 2 types (Online, Retail)
- **Regions Covered:** 5 major Indian cities

---

## 🗂️ Data Structure

### **Columns Overview:**

| Column Name | Data Type | Description | Sample Values |
|-------------|-----------|-------------|---------------|
| **Order_ID** | Integer | Unique order identifier | 2000, 2001, 2002... |
| **Gender_Category** | Text | Target customer segment | Men, Women, Kids |
| **Product_Line** | Text | Product category | Training, Basketball, Soccer, Running, Lifestyle |
| **Product_Name** | Text | Specific product name | Air Jordan, React Infinity, Waffle One |
| **Size** | Text/Number | Product size | M, L, XL, 6, 9, 11, 12 |
| **Units_Sold** | Integer | Quantity of units sold | 0-4 (including negatives for returns) |
| **MRP** | Decimal | Maximum Retail Price | ₹3,000 - ₹10,000 |
| **Discount_Applied** | Decimal | Discount percentage | 0.16 - 1.17 (16% - 117%) |
| **Revenue** | Decimal | Total transaction revenue | ₹0 - ₹37,000 (including negatives) |
| **Order_Date** | Date | Date of transaction | Multiple formats: DD-MM-YYYY, YYYY/MM/DD, etc. |
| **Sales_Channel** | Text | Where sale occurred | Online, Retail |
| **Region** | Text | City/Location | Delhi, Mumbai, Bangalore, Kolkata, Pune, Hyderabad |
| **Profit** | Decimal | Profit from transaction | -₹1,120 to ₹3,929 |

---

## 🛠️ Data Quality Issues (The "Uncleaned" Data)

This dataset contains **intentional data quality issues** for cleaning practice:

### **1. Missing Values:**
- ✅ **Units_Sold:** ~40% missing values
- ✅ **MRP:** ~35% missing values
- ✅ **Discount_Applied:** ~30% missing values
- ✅ **Order_Date:** 616 blank records (24.6%)
- ✅ **Revenue:** 2,334 records showing 0.0 (93.4%)

### **2. Inconsistent Date Formats:**
- ❌ `2024-03-09` (YYYY-MM-DD)
- ❌ `04-10-2024` (DD-MM-YYYY)
- ❌ `2024/09/12` (YYYY/MM/DD)
- ❌ `11-10-2024` (DD-MM-YYYY)
- ❌ `31-05-2025` (DD-MM-YYYY)

### **3. Inconsistent Region Names:**
- ❌ `Bangalore` vs `bengaluru` (case inconsistency)
- ❌ `Hyderabad` vs `Hyd` vs `hyderbad` (spelling variations)

### **4. Data Anomalies:**
- ⚠️ **Negative Units_Sold:** -1 values (likely returns)
- ⚠️ **Zero Units_Sold:** 0.0 values (cancelled orders?)
- ⚠️ **Negative Revenue:** Multiple negative values (returns/refunds)
- ⚠️ **Negative Profit:** Multiple loss-making transactions
- ⚠️ **Invalid Discount:** Values > 1.0 (117% discount - data error)
- ⚠️ **Mixed Size Formats:** Text (M, L, XL) and Numbers (6, 9, 11, 12)

### **5. Calculation Issues:**
- ⚠️ Revenue field mostly shows 0.0 (needs recalculation)
- ⚠️ Formula should be: `Units_Sold × MRP × (1 - Discount_Applied)`

---

## 📊 Data Distribution

### **Product Line Distribution:**
| Product Line | Count | Percentage |
|--------------|-------|------------|
| Training | 546 | 21.8% |
| Basketball | 507 | 20.3% |
| Lifestyle | 501 | 20.0% |
| Running | 474 | 19.0% |
| Soccer | 472 | 18.9% |

### **Sales Channel Distribution:**
| Channel | Count | Percentage |
|---------|-------|------------|
| Online | 1,255 | 50.2% |
| Retail | 1,245 | 49.8% |

### **Region Distribution:**
| Region | Count | Notes |
|--------|-------|-------|
| Delhi | 438 | 17.5% |
| Mumbai | 418 | 16.7% |
| Kolkata | 417 | 16.7% |
| Pune | 388 | 15.5% |
| Bangalore/bengaluru | 436 | 17.4% (needs consolidation) |
| Hyderabad/Hyd/hyderbad | 403 | 16.1% (needs consolidation) |

---

## 🔧 Power BI Data Cleaning Steps

### **Step 1: Data Import**
1. Imported CSV file using "Get Data" → "Text/CSV"
2. Loaded into Power Query Editor

### **Step 2: Standardize Region Names**

**Power Query M Code:**
```M
= Table.ReplaceValue(
    #"Changed Type",
    each [Region],
    each if Text.Lower([Region]) = "bengaluru" or Text.Lower([Region]) = "bangalore" then "Bangalore"
         else if Text.Contains(Text.Lower([Region]), "hyd") then "Hyderabad"
         else [Region],
    Replacer.ReplaceValue,
    {"Region"}
)
```

**Standardization Rules:**
- `bengaluru` → `Bangalore`
- `Hyd`, `hyderbad` → `Hyderabad`
- Title case applied to all regions

### **Step 3: Fix Date Formats**

**Power Query Steps:**
```M
// Replace date format variations
= Table.TransformColumns(
    #"Standardized Regions",
    {{"Order_Date", each 
        try Date.From(_) 
        otherwise try Date.FromText(_, "en-US")
        otherwise null, 
        type date}}
)
```

**Result:** All dates converted to standard format: `YYYY-MM-DD`

### **Step 4: Handle Missing Values**

**Strategy:**
- **Units_Sold:** Replace nulls with 0
- **MRP:** Keep nulls for analysis (identify incomplete records)
- **Discount_Applied:** Replace nulls with 0 (no discount)
- **Revenue:** Will be recalculated

```M
= Table.ReplaceValue(
    #"Fixed Dates",
    null,
    0,
    Replacer.ReplaceValue,
    {"Units_Sold", "Discount_Applied"}
)
```

### **Step 5: Recalculate Revenue**

**Added Calculated Column:**
```M
= Table.AddColumn(
    #"Handled Nulls",
    "Revenue_Calculated",
    each [Units_Sold] * [MRP] * (1 - [Discount_Applied]),
    type number
)
```

**Formula:** `Revenue = Units_Sold × MRP × (1 - Discount_Applied)`

### **Step 6: Add Date Intelligence Columns**

```M
= Table.AddColumn(#"Previous Step", "Year", each Date.Year([Order_Date]), Int64.Type)
= Table.AddColumn(#"Added Year", "Month", each Date.MonthName([Order_Date]), type text)
= Table.AddColumn(#"Added Month", "Quarter", each "Q" & Number.ToText(Date.QuarterOfYear([Order_Date])), type text)
= Table.AddColumn(#"Added Quarter", "Weekday", each Date.DayOfWeekName([Order_Date]), type text)
```

### **Step 7: Standardize Size Field**

```M
= Table.TransformColumns(
    #"Previous Step",
    {{"Size", Text.Upper, type text}}
)
```

**Result:** All sizes uppercase (M, L, XL, etc.)

### **Step 8: Filter Invalid Records**

**Removed:**
- Orders with negative Units_Sold (returns - handled separately)
- Orders with discount > 100% (data errors)
- Orders without MRP or Product_Name

```M
= Table.SelectRows(
    #"Previous Step",
    each [Units_Sold] >= 0 
        and [Discount_Applied] <= 1.0
        and [MRP] <> null
        and [Product_Name] <> null
)
```

---

## 📐 Data Model

### **Fact Table:**
- `Nike_Sales` (cleaned transactions)

### **Dimension Tables Created:**

**1. DateTable (Calendar):**
```DAX
DateTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2024, 1, 1), DATE(2025, 12, 31)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNum", MONTH([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Weekday", FORMAT([Date], "dddd"),
    "Day", DAY([Date])
)
```

**2. Products Table:**
```DAX
Products = 
SUMMARIZE(
    Nike_Sales,
    Nike_Sales[Product_Line],
    Nike_Sales[Product_Name]
)
```

**3. Regions Table:**
```DAX
Regions = 
DISTINCT(
    SELECTCOLUMNS(
        Nike_Sales,
        "Region", Nike_Sales[Region]
    )
)
```

**4. Gender_Category Table:**
```DAX
Gender_Categories = 
DISTINCT(
    SELECTCOLUMNS(
        Nike_Sales,
        "Gender_Category", Nike_Sales[Gender_Category]
    )
)
```

### **Relationships:**
- `Nike_Sales[Order_Date]` → `DateTable[Date]` (Many-to-One)
- `Nike_Sales[Product_Name]` → `Products[Product_Name]` (Many-to-One)
- `Nike_Sales[Region]` → `Regions[Region]` (Many-to-One)
- `Nike_Sales[Gender_Category]` → `Gender_Categories[Gender_Category]` (Many-to-One)

---

## 📊 DAX Measures Created

### **Revenue Metrics:**

```DAX
// Total Revenue
Total Revenue = 
SUM(Nike_Sales[Revenue_Calculated])

// Total Revenue (Original - for comparison)
Total Revenue Original = 
SUM(Nike_Sales[Revenue])

// Average Transaction Value
Avg Transaction Value = 
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)

// Revenue Growth %
Revenue Growth % = 
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue = CALCULATE([Total Revenue], DATEADD(DateTable[Date], -1, MONTH))
RETURN
    DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0)
```

### **Sales Metrics:**

```DAX
// Total Units Sold
Total Units Sold = 
SUM(Nike_Sales[Units_Sold])

// Total Orders
Total Orders = 
COUNTROWS(Nike_Sales)

// Average Units Per Order
Avg Units Per Order = 
DIVIDE(
    [Total Units Sold],
    [Total Orders],
    0
)

// Distinct Products Sold
Distinct Products = 
DISTINCTCOUNT(Nike_Sales[Product_Name])
```

### **Profit Metrics:**

```DAX
// Total Profit
Total Profit = 
SUM(Nike_Sales[Profit])

// Profit Margin %
Profit Margin % = 
DIVIDE(
    [Total Profit],
    [Total Revenue],
    0
)

// Average Profit Per Order
Avg Profit Per Order = 
DIVIDE(
    [Total Profit],
    [Total Orders],
    0
)
```

### **Discount Metrics:**

```DAX
// Average Discount
Avg Discount % = 
AVERAGE(Nike_Sales[Discount_Applied])

// Total Discount Amount
Total Discount Amount = 
SUMX(
    Nike_Sales,
    [Units_Sold] * [MRP] * [Discount_Applied]
)

// Orders With Discount
Orders With Discount = 
CALCULATE(
    [Total Orders],
    Nike_Sales[Discount_Applied] > 0
)
```

### **Channel Performance:**

```DAX
// Online Revenue
Online Revenue = 
CALCULATE(
    [Total Revenue],
    Nike_Sales[Sales_Channel] = "Online"
)

// Retail Revenue
Retail Revenue = 
CALCULATE(
    [Total Revenue],
    Nike_Sales[Sales_Channel] = "Retail"
)

// Online vs Retail %
Online % = 
DIVIDE(
    [Online Revenue],
    [Total Revenue],
    0
)
```

### **Product Line Analysis:**

```DAX
// Top Product Line
Top Product Line = 
CALCULATE(
    FIRSTNONBLANK(Nike_Sales[Product_Line], 1),
    TOPN(
        1,
        VALUES(Nike_Sales[Product_Line]),
        [Total Revenue],
        DESC
    )
)

// Product Line Revenue %
Product Line % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(Nike_Sales[Product_Line])),
    0
)
```

### **Regional Metrics:**

```DAX
// Top Region by Revenue
Top Region = 
CALCULATE(
    FIRSTNONBLANK(Nike_Sales[Region], 1),
    TOPN(
        1,
        VALUES(Nike_Sales[Region]),
        [Total Revenue],
        DESC
    )
)

// Region Contribution %
Region % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(Nike_Sales[Region])),
    0
)
```

---

## 🎨 Dashboard Design

### **Color Theme: Nike-Inspired**

```
Primary (Nike Orange): #FF6900
Secondary (Dark): #1A1A1A
Accent 1: #E85D0D
Accent 2: #FFB84D
Light Background: #F5F5F5
White: #FFFFFF
Text Dark: #2C2C2C
```

### **Canvas Setup:**
- **Dimensions:** 1280 × 720 px (16:9 ratio)
- **Background:** Clean white with subtle Nike swoosh watermark
- **Layout:** Header + 3 content rows

### **Page Structure:**

**Page 1 - Overview Dashboard:**
- Header with Nike branding
- KPI cards (Revenue, Units Sold, Profit, Avg Order Value)
- Revenue trend over time
- Product line performance
- Regional distribution
- Channel comparison

**Page 2 - Product Analysis:**
- Product line deep dive
- Best/worst selling products
- Product profitability analysis
- Size distribution

**Page 3 - Regional & Channel Insights:**
- Regional performance comparison
- Online vs Retail analysis
- Customer segment breakdown
- Discount effectiveness

---

## 📊 Key Visualizations

### **1. KPI Cards (4 cards):**
- Total Revenue
- Total Units Sold
- Total Profit
- Average Order Value

### **2. Line Chart:**
- Revenue trend by month
- X-axis: Month
- Y-axis: Total Revenue

### **3. Clustered Bar Chart:**
- Revenue by Product Line
- Sorted descending

### **4. Donut Charts:**
- Sales Channel distribution
- Gender Category distribution
- Regional distribution

### **5. Stacked Column Chart:**
- Revenue by Product Line and Gender

### **6. Map Visual:**
- Sales by Region (Indian cities)

### **7. Matrix/Table:**
- Top 10 products by revenue and profit

---

## 🎯 Key Insights from Dashboard

### **Sales Performance:**
- Overall revenue trends across 2024-2025
- Peak sales periods identification
- Product line contribution analysis

### **Product Insights:**
- Training line is top performer (21.8% of products)
- Most profitable product categories
- Size preferences by category

### **Channel Performance:**
- Nearly equal split between Online (50.2%) and Retail (49.8%)
- Channel preferences by product type
- Average order value comparison

### **Regional Analysis:**
- Delhi leads with 17.5% of transactions
- Metro city performance comparison
- Regional product preferences

### **Customer Behavior:**
- Gender-wise purchasing patterns
- Discount sensitivity analysis
- Return rate insights (negative units)

---

## 🚀 How to Use This Dashboard

### **Prerequisites:**
- Power BI Desktop (Latest version)
- Windows 10/11 or Power BI Service

### **Steps:**

1. **Download Files:**
   - `Nike_Sales_Report.pbix`
   - `Nike_Sales_Uncleaned__1_.csv` (optional - for reference)

2. **Open Dashboard:**
   - Double-click `Nike_Sales_Report.pbix`
   - Power BI Desktop opens automatically

3. **Interact:**
   - Click on visuals to filter
   - Use slicers for date, region, product
   - Hover for detailed tooltips

4. **Refresh Data:**
   - Home → Refresh (if data source updated)

5. **Export:**
   - File → Export to PDF
   - Publish to Power BI Service for web sharing

---

## 🛠️ Technical Requirements

### **Software:**
- Power BI Desktop (Free)
- Microsoft Excel (for CSV viewing - optional)

### **Skills Demonstrated:**
- ✅ Data cleaning and transformation (Power Query)
- ✅ Data modeling (Star schema)
- ✅ DAX measure creation
- ✅ Dashboard design principles
- ✅ Data visualization best practices
- ✅ Business intelligence reporting

---

## 📚 Learning Outcomes

### **Power Query Skills:**
- Text standardization
- Date format handling
- Null value management
- Calculated columns
- Conditional transformations

### **DAX Skills:**
- Aggregation functions
- CALCULATE function
- Time intelligence
- Percentages and ratios
- TOPN and ranking

### **Visualization Skills:**
- Appropriate chart selection
- Color theory application
- Layout design
- User experience optimization

---

## 🔄 Data Cleaning Summary

### **Before Cleaning:**
- ❌ 2,500 records with multiple quality issues
- ❌ Inconsistent date formats
- ❌ Mixed region naming
- ❌ 93% of revenue values = 0.0
- ❌ Missing values across multiple columns

### **After Cleaning:**
- ✅ Standardized region names (7 regions → 5 cities)
- ✅ Unified date format
- ✅ Recalculated revenue field
- ✅ Handled missing values appropriately
- ✅ Filtered out invalid records
- ✅ Added date intelligence columns
- ✅ Created proper data model with relationships

---

## 📦 Project Structure

```
nike-sales-dashboard/
│
├── 📄 Nike_Sales_Report.pbix          # Power BI dashboard
├── 📄 Nike_Sales_Uncleaned__1_.csv    # Raw data (uncleaned)
├── 📄 README.md                       # This file
│
└── 📸 screenshots/                     # (Optional)
    ├── dashboard_overview.png
    ├── product_analysis.png
    └── regional_insights.png
```

---

## 🤝 Use Cases

### **Business Applications:**
- **Sales Management:** Track performance across regions and channels
- **Inventory Planning:** Identify best-selling products and sizes
- **Marketing Strategy:** Understand customer segments and preferences
- **Pricing Optimization:** Analyze discount effectiveness
- **Regional Expansion:** Identify high-performing markets

### **Learning & Portfolio:**
- Data cleaning practice
- Power BI skill development
- Business intelligence project showcase
- Interview portfolio piece

---

## 🔮 Future Enhancements

**Potential Improvements:**
- [ ] Add customer lifetime value analysis
- [ ] Implement predictive sales forecasting
- [ ] Add inventory stock tracking
- [ ] Create customer cohort analysis
- [ ] Add mobile-optimized view
- [ ] Implement row-level security for regions
- [ ] Add drill-through pages for detailed analysis
- [ ] Create automated email reports

---

## 📝 Notes

### **Data Source:**
- Sample/practice dataset with intentional quality issues
- Date range: 2024-2025 (includes future dates for practice)
- Currency: Indian Rupees (₹)

### **Known Limitations:**
- Some future dates present (2025 dates)
- Negative profits indicate returns or loss-making transactions
- Revenue field in original data mostly zeros (recalculated in Power BI)

---

## 🏷️ Tags

`Power BI` `Data Analytics` `Data Cleaning` `Business Intelligence` `Sales Dashboard` `Nike` `Retail Analytics` `E-commerce` `Data Visualization` `DAX` `Power Query` `Portfolio Project`

## 🙏 Acknowledgments

- Nike for brand inspiration
- Power BI community for best practices
- Indian retail market for regional context

---

**⭐ If you found this project helpful, please star this repository!**

---

*Last Updated: February 2026*
*Version: 1.0*
