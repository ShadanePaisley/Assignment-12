# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9
    
    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday
    
    for store in stores:
        store_factor = store_performance[store]
        
        for dept in departments:
            dept_factor = dept_performance[dept]
            
            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)
                
                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise
                
                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range
                
                # Calculate profit
                profit = sales_amount * profit_margin
                
                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range
    
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    
    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income
    
    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)
    
    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)
    
    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    
    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"
    
    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]
    
    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * 
                                (store_performance[store] ** 0.5))
    
    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    # Calculate aggregate totals across the full dataset
    total_sales = float(sales_df["Sales"].sum())
    total_profit = float(sales_df["Profit"].sum())
    avg_profit_margin = float(sales_df["ProfitMargin"].mean())

    # Group sales by store and department for comparison
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    # Print a formatted summary of the key descriptive statistics
    print("\n--- Sales Performance Summary ---")
    print(f"  Total Annual Sales:      ${total_sales:,.2f}")
    print(f"  Total Annual Profit:     ${total_profit:,.2f}")
    print(f"  Average Profit Margin:   {avg_profit_margin:.2%}")

    # Additional descriptive statistics for deeper understanding
    print("\n  Sales Descriptive Statistics:")
    print(f"    Mean Daily Sales (per record):  ${sales_df['Sales'].mean():,.2f}")
    print(f"    Median Daily Sales:             ${sales_df['Sales'].median():,.2f}")
    print(f"    Std Dev of Sales:               ${sales_df['Sales'].std():,.2f}")
    print(f"    Min Sales:                      ${sales_df['Sales'].min():,.2f}")
    print(f"    Max Sales:                      ${sales_df['Sales'].max():,.2f}")

    print("\n  Annual Sales by Store:")
    for store, val in sales_by_store.items():
        print(f"    {store:<15}: ${val:>15,.2f}")

    print("\n  Annual Sales by Department:")
    for dept, val in sales_by_dept.items():
        print(f"    {dept:<20}: ${val:>15,.2f}")

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept
    }

# 1.2 Create visualizations showing sales distribution by store, department, and time
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # --- Figure 1: Sales by Store (horizontal bar chart) ---
    store_sales = sales_df.groupby("Store")["Sales"].sum().sort_values()
    store_fig, ax1 = plt.subplots(figsize=(9, 5))
    colors_store = ["#4CAF50" if s == store_sales.index[-1] else "#81C784" for s in store_sales.index]
    bars = ax1.barh(store_sales.index, store_sales.values, color=colors_store, edgecolor="white")
    ax1.set_xlabel("Total Annual Sales ($)", fontsize=11)
    ax1.set_title("GreenGrocer: Annual Sales by Store", fontsize=13, fontweight="bold")
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    # Add value labels to each bar for readability
    for bar in bars:
        ax1.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                 f"${bar.get_width():,.0f}", va="center", fontsize=9)
    ax1.spines[["top", "right"]].set_visible(False)
    store_fig.tight_layout()

    # --- Figure 2: Sales and Profit Margin by Department (grouped bar) ---
    dept_sales = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    dept_margin = sales_df.groupby("Department")["ProfitMargin"].mean() * 100
    dept_fig, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: total sales per department
    ax2a.bar(dept_sales.index, dept_sales.values, color="#388E3C", edgecolor="white")
    ax2a.set_title("Annual Sales by Department", fontsize=12, fontweight="bold")
    ax2a.set_ylabel("Total Sales ($)")
    ax2a.set_xticklabels(dept_sales.index, rotation=20, ha="right")
    ax2a.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax2a.spines[["top", "right"]].set_visible(False)

    # Right panel: average profit margin per department
    margin_colors = ["#2E7D32" if m == dept_margin.max() else "#66BB6A" for m in dept_margin]
    ax2b.bar(dept_margin.index, dept_margin.values, color=margin_colors, edgecolor="white")
    ax2b.set_title("Avg Profit Margin by Department (%)", fontsize=12, fontweight="bold")
    ax2b.set_ylabel("Average Profit Margin (%)")
    ax2b.set_xticklabels(dept_margin.index, rotation=20, ha="right")
    ax2b.spines[["top", "right"]].set_visible(False)
    dept_fig.suptitle("GreenGrocer: Department Performance Overview", fontsize=13, fontweight="bold")
    dept_fig.tight_layout()

    # --- Figure 3: Monthly Sales Trend (line chart with weekend shading) ---
    sales_df["Month"] = sales_df["Date"].dt.month
    monthly_sales = sales_df.groupby("Month")["Sales"].sum()
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    time_fig, ax3 = plt.subplots(figsize=(11, 5))
    ax3.plot(monthly_sales.index, monthly_sales.values, marker="o", color="#2E7D32",
             linewidth=2.5, markersize=7, label="Monthly Sales")
    ax3.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.15, color="#4CAF50")

    # Highlight peak months: summer and December
    for peak_month in [6, 7, 8, 12]:
        ax3.axvline(x=peak_month, color="#FFA726", linestyle="--", linewidth=1, alpha=0.6)

    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels(month_labels)
    ax3.set_xlabel("Month", fontsize=11)
    ax3.set_ylabel("Total Sales ($)", fontsize=11)
    ax3.set_title("GreenGrocer: Monthly Sales Trend (2023)", fontsize=13, fontweight="bold")
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax3.legend(["Monthly Sales", "Peak Season Markers"], fontsize=9)
    ax3.spines[["top", "right"]].set_visible(False)
    time_fig.tight_layout()

    return store_fig, dept_fig, time_fig

# 1.3 Analyze customer segments and their spending patterns
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    # Count of customers in each segment
    segment_counts = customer_df["Segment"].value_counts()

    # Average monthly spend by segment — reveals which segments drive the most revenue
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)

    # Cross-tabulation of segment vs. loyalty tier — shows the quality of each customer segment
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    # Print summary
    print("\n--- Customer Segment Analysis ---")
    print("\n  Segment Counts:")
    for seg, cnt in segment_counts.items():
        print(f"    {seg:<22}: {cnt} customers ({cnt/len(customer_df)*100:.1f}%)")

    print("\n  Average Monthly Spend by Segment:")
    for seg, spend in segment_avg_spend.items():
        print(f"    {seg:<22}: ${spend:>7.2f}")

    print("\n  Loyalty Tier Distribution by Segment:")
    print(segment_loyalty.to_string())

    # Visualization: pie chart for segment size + bar for avg spend
    seg_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    palette = ["#2E7D32", "#43A047", "#66BB6A", "#A5D6A7", "#C8E6C9"]

    ax1.pie(segment_counts.values, labels=segment_counts.index, autopct="%1.1f%%",
            colors=palette, startangle=140, pctdistance=0.82)
    ax1.set_title("Customer Segment Distribution", fontsize=12, fontweight="bold")

    ax2.barh(segment_avg_spend.index, segment_avg_spend.values, color=palette, edgecolor="white")
    ax2.set_xlabel("Avg Monthly Spend ($)")
    ax2.set_title("Avg Monthly Spend by Segment", fontsize=12, fontweight="bold")
    ax2.spines[["top", "right"]].set_visible(False)
    seg_fig.suptitle("GreenGrocer: Customer Segment Insights", fontsize=13, fontweight="bold")
    seg_fig.tight_layout()

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
    }


# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    # Merge store characteristics with operational metrics for a full picture
    merged = operational_df.merge(store_df, on="Store")

    # Build correlation matrix across all numeric operational columns
    numeric_cols = ["AnnualSales", "AnnualProfit", "SalesPerSqFt", "SalesPerStaff",
                    "InventoryTurnover", "CustomerSatisfaction",
                    "SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    store_correlations = merged[numeric_cols].corr()

    # Extract and rank factors by their correlation with AnnualSales
    sales_corr = store_correlations["AnnualSales"].drop("AnnualSales").sort_values(
        key=abs, ascending=False)
    top_correlations = list(zip(sales_corr.index, sales_corr.values))

    print("\n--- Correlation Analysis: Factors vs. Annual Sales ---")
    for factor, corr in top_correlations:
        direction = "positive" if corr > 0 else "negative"
        print(f"  {factor:<25}: r = {corr:+.4f}  ({direction})")

    # Visualization: heatmap of full correlation matrix
    correlation_fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(store_correlations.values, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")
    plt.colorbar(im, ax=ax, label="Pearson r")
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(numeric_cols, fontsize=8)
    # Annotate each cell with its correlation value
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            ax.text(j, i, f"{store_correlations.values[i, j]:.2f}",
                    ha="center", va="center", fontsize=7,
                    color="black" if abs(store_correlations.values[i, j]) < 0.8 else "white")
    ax.set_title("GreenGrocer: Correlation Matrix — Store & Operational Metrics",
                 fontsize=12, fontweight="bold")
    correlation_fig.tight_layout()

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig
    }

# 2.2 Compare stores based on operational metrics

def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    # Pull efficiency metrics from the operational dataframe
    efficiency_metrics = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff",
                                         "ProfitPerSqFt", "InventoryTurnover",
                                         "CustomerSatisfaction"]].set_index("Store")

    # Rank stores by total annual profit — a holistic bottom-line measure
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    print("\n--- Store Efficiency Metrics ---")
    print(efficiency_metrics.to_string())
    print("\n  Store Performance Ranking by Annual Profit:")
    for rank, (store, profit) in enumerate(performance_ranking.items(), 1):
        print(f"    #{rank} {store:<15}: ${profit:,.2f}")

    # Visualization: radar-style grouped bar chart across key efficiency indicators
    comparison_fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    store_names = efficiency_metrics.index.tolist()
    colors = ["#1B5E20", "#2E7D32", "#388E3C", "#43A047", "#66BB6A"]

    # Panel 1: Sales per Sq Ft
    axes[0].bar(store_names, efficiency_metrics["SalesPerSqFt"], color=colors, edgecolor="white")
    axes[0].set_title("Sales per Sq Ft ($)", fontsize=11, fontweight="bold")
    axes[0].set_xticklabels(store_names, rotation=20, ha="right")
    axes[0].spines[["top", "right"]].set_visible(False)

    # Panel 2: Sales per Staff Member
    axes[1].bar(store_names, efficiency_metrics["SalesPerStaff"], color=colors, edgecolor="white")
    axes[1].set_title("Sales per Staff Member ($)", fontsize=11, fontweight="bold")
    axes[1].set_xticklabels(store_names, rotation=20, ha="right")
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
    axes[1].spines[["top", "right"]].set_visible(False)

    # Panel 3: Customer Satisfaction Score (out of 5)
    axes[2].bar(store_names, efficiency_metrics["CustomerSatisfaction"],
                color=colors, edgecolor="white")
    axes[2].set_title("Customer Satisfaction (/ 5)", fontsize=11, fontweight="bold")
    axes[2].set_xticklabels(store_names, rotation=20, ha="right")
    axes[2].set_ylim(0, 5)
    axes[2].spines[["top", "right"]].set_visible(False)

    comparison_fig.suptitle("GreenGrocer: Store Efficiency Comparison", fontsize=13, fontweight="bold")
    comparison_fig.tight_layout()

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig
    }

# 2.3 Analyze seasonal patterns and their impact
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    # Aggregate sales by calendar month (1–12)
    sales_df["Month"] = sales_df["Date"].dt.month
    monthly_sales = sales_df.groupby("Month")["Sales"].sum()

    # Aggregate sales by day of week (0 = Monday, 6 = Sunday)
    sales_df["DayOfWeek"] = sales_df["Date"].dt.dayofweek
    dow_sales = sales_df.groupby("DayOfWeek")["Sales"].sum()

    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    print("\n--- Seasonal Pattern Analysis ---")
    print("  Monthly Sales (Total):")
    for m, val in monthly_sales.items():
        print(f"    {month_labels[m-1]}: ${val:,.2f}")

    print("\n  Sales by Day of Week:")
    for d, val in dow_sales.items():
        print(f"    {dow_labels[d]}: ${val:,.2f}")

    # Visualization: two-panel figure for month and day-of-week patterns
    seasonal_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Monthly trend — line with fill to emphasize peaks and troughs
    ax1.plot(monthly_sales.index, monthly_sales.values, marker="o", color="#2E7D32",
             linewidth=2.5, markersize=8)
    ax1.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.15, color="#4CAF50")
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(month_labels, rotation=30)
    ax1.set_title("Monthly Sales Pattern", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Total Sales ($)")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    # Mark summer and December peaks for clarity
    for peak in [6, 7, 8, 12]:
        ax1.axvspan(peak - 0.5, peak + 0.5, alpha=0.10, color="#FF8F00")
    ax1.spines[["top", "right"]].set_visible(False)

    # Day-of-week pattern — bar chart, weekend bars highlighted
    bar_colors = ["#66BB6A" if d < 5 else "#2E7D32" for d in range(7)]
    ax2.bar(dow_labels, dow_sales.values, color=bar_colors, edgecolor="white")
    ax2.set_title("Sales by Day of Week", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Total Sales ($)")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    # Add a legend distinguishing weekdays from weekends
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor="#66BB6A", label="Weekday"),
                       Patch(facecolor="#2E7D32", label="Weekend")]
    ax2.legend(handles=legend_elements, fontsize=9)
    ax2.spines[["top", "right"]].set_visible(False)

    seasonal_fig.suptitle("GreenGrocer: Seasonal & Weekly Sales Patterns", fontsize=13, fontweight="bold")
    seasonal_fig.tight_layout()

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig
    }


# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    # Merge store characteristics with operational totals for the regression dataset
    model_data = operational_df.merge(store_df, on="Store")
    features = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    target = "AnnualSales"

    X = model_data[features].values
    y = model_data[target].values

    # Standardize features (z-score) so coefficients are on a comparable scale
    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0)
    X_scaled = (X - X_mean) / X_std

    # Add an intercept column for the normal equation solution
    X_b = np.column_stack([np.ones(len(X_scaled)), X_scaled])

    # Ordinary Least Squares via numpy's least-squares solver
    coeffs_raw, _, _, _ = np.linalg.lstsq(X_b, y, rcond=None)
    intercept = coeffs_raw[0]
    coeffs = coeffs_raw[1:]

    # Build a readable dictionary mapping each feature to its coefficient
    coefficients = {"intercept": intercept}
    for feat, coef in zip(features, coeffs):
        coefficients[feat] = coef

    # Generate predictions and compute R-squared
    y_pred = X_b @ coeffs_raw
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot

    # Wrap predictions in a Series indexed by store name
    predictions = pd.Series(y_pred, index=model_data["Store"], name="PredictedSales")

    print("\n--- Linear Regression Model: Predicting Annual Sales ---")
    print(f"  R-Squared: {r_squared:.4f}  ({r_squared*100:.1f}% of variance explained)")
    print("\n  Model Coefficients (standardized features):")
    for feat, coef in coefficients.items():
        print(f"    {feat:<25}: {coef:>+12,.2f}")

    print("\n  Actual vs. Predicted Annual Sales:")
    for store, actual, pred in zip(model_data["Store"], y, y_pred):
        error = abs(actual - pred)
        print(f"    {store:<15}: Actual = ${actual:>12,.2f}  |  Predicted = ${pred:>12,.2f}  |  Error = ${error:>10,.2f}")

    # Visualization: actual vs. predicted scatter + coefficient bar chart
    model_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: Actual vs. Predicted — diagonal reference line shows perfect fit
    ax1.scatter(y, y_pred, color="#2E7D32", s=100, zorder=3)
    min_val, max_val = min(y.min(), y_pred.min()), max(y.max(), y_pred.max())
    ax1.plot([min_val, max_val], [min_val, max_val], "k--", linewidth=1.5, label="Perfect Fit")
    for i, store in enumerate(model_data["Store"]):
        ax1.annotate(store, (y[i], y_pred[i]), textcoords="offset points",
                     xytext=(6, 4), fontsize=8)
    ax1.set_xlabel("Actual Annual Sales ($)")
    ax1.set_ylabel("Predicted Annual Sales ($)")
    ax1.set_title(f"Actual vs. Predicted (R² = {r_squared:.4f})", fontsize=11, fontweight="bold")
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax1.legend()
    ax1.spines[["top", "right"]].set_visible(False)

    # Right: feature importance via coefficient magnitude
    feat_names = list(coefficients.keys())[1:]  # Exclude intercept
    feat_coefs = [coefficients[f] for f in feat_names]
    bar_colors = ["#2E7D32" if c >= 0 else "#C62828" for c in feat_coefs]
    ax2.barh(feat_names, feat_coefs, color=bar_colors, edgecolor="white")
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.set_xlabel("Standardized Coefficient")
    ax2.set_title("Feature Importance (Standardized Coefficients)", fontsize=11, fontweight="bold")
    ax2.spines[["top", "right"]].set_visible(False)

    model_fig.suptitle("GreenGrocer: Sales Prediction Model", fontsize=13, fontweight="bold")
    model_fig.tight_layout()

    return {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig
    }

# 3.2 Forecast departmental sales trends
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    # Build a monthly pivot table: rows = month, columns = department
    sales_df["Month"] = sales_df["Date"].dt.month
    monthly_dept = sales_df.groupby(["Month", "Department"])["Sales"].sum().reset_index()
    dept_trends = monthly_dept.pivot(index="Month", columns="Department", values="Sales")

    # Estimate simple linear trend (slope) for each department across the 12 months
    # Slope represents the monthly sales growth rate in dollars
    x = np.arange(1, 13)
    growth_rates = {}
    for dept in dept_trends.columns:
        y = dept_trends[dept].values
        slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
        growth_rates[dept] = slope  # $ change per month

    growth_rates = pd.Series(growth_rates).sort_values(ascending=False)

    print("\n--- Department Sales Trends & Forecasts ---")
    print("  Monthly Growth Rate ($/month) by Department:")
    for dept, rate in growth_rates.items():
        direction = "▲" if rate > 0 else "▼"
        print(f"    {direction} {dept:<20}: ${rate:>+8,.2f} per month")

    # Extend the trend 3 months into Q1 2024 (months 13–15) using the fitted line
    x_future = np.array([13, 14, 15])
    month_labels_all = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                        "Jan'24", "Feb'24", "Mar'24"]

    # Visualization: one line per department, with the forecast window shaded
    forecast_fig, ax = plt.subplots(figsize=(12, 6))
    dept_colors = {"Produce": "#1B5E20", "Dairy": "#2E7D32", "Bakery": "#388E3C",
                   "Grocery": "#66BB6A", "Prepared Foods": "#A5D6A7"}

    for dept in dept_trends.columns:
        y = dept_trends[dept].values
        slope, intercept, _, _, _ = stats.linregress(x, y)
        y_forecast = slope * x_future + intercept

        # Plot actual 2023 data
        ax.plot(x, y, marker="o", markersize=4, color=dept_colors.get(dept, "#4CAF50"),
                label=dept, linewidth=2)
        # Plot 2024 forecast as dashed continuation
        ax.plot(x_future, y_forecast, linestyle="--", color=dept_colors.get(dept, "#4CAF50"),
                linewidth=1.8, alpha=0.7)

    # Shade the forecast region to distinguish it from historical data
    ax.axvspan(12.5, 15.5, alpha=0.08, color="#FFA726", label="Forecast Period (Q1 2024)")
    ax.axvline(12.5, color="#FFA726", linewidth=1.2, linestyle=":")
    ax.set_xticks(list(range(1, 13)) + list(x_future))
    ax.set_xticklabels(month_labels_all, rotation=35, ha="right", fontsize=8)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Monthly Sales ($)")
    ax.set_title("GreenGrocer: Department Sales Trends & 3-Month Forecast",
                 fontsize=13, fontweight="bold")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax.legend(loc="upper left", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    forecast_fig.tight_layout()

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig
    }


# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    # Aggregate total sales, total profit, and average margin per store-department pair
    combo = sales_df.groupby(["Store", "Department"]).agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        AvgMargin=("ProfitMargin", "mean")
    ).reset_index()

    # Rank combinations and isolate the top and bottom performers
    combo_sorted = combo.sort_values("TotalProfit", ascending=False).reset_index(drop=True)
    top_combinations = combo_sorted.head(10)
    underperforming = combo_sorted.tail(10).reset_index(drop=True)

    # Opportunity score: profit efficiency index = profit per unit sales, scaled to 0–100
    store_agg = operational_df.set_index("Store")
    profit_efficiency = (store_agg["AnnualProfit"] / store_agg["AnnualSales"]) * 100
    opportunity_score = profit_efficiency.sort_values(ascending=False)

    print("\n--- Profit Opportunity Analysis ---")
    print("\n  Top 10 Store-Department Combinations by Profit:")
    print(top_combinations[["Store", "Department", "TotalSales", "TotalProfit", "AvgMargin"]]
          .to_string(index=False, float_format="%.2f"))

    print("\n  Bottom 10 Store-Department Combinations by Profit:")
    print(underperforming[["Store", "Department", "TotalSales", "TotalProfit", "AvgMargin"]]
          .to_string(index=False, float_format="%.2f"))

    print("\n  Opportunity Score by Store (Profit / Sales %):")
    for store, score in opportunity_score.items():
        print(f"    {store:<15}: {score:.2f}%")

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score
    }

# 4.2 Develop recommendations for improving performance
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    # Each recommendation is grounded in specific findings from the analysis above
    recommendations = [
        "1. PRIORITIZE PREPARED FOODS AND BAKERY EXPANSION: These two departments consistently "
        "deliver the highest profit margins (40% and 35% respectively). GreenGrocer should expand their  "
        "floor space and product variety in both departments across all stores especially in "
        "Gainesville and Jacksonville, where overall sales volume is lowest and incremental "
        "high-margin revenue would have the greatest relative impact.",

        "2. INVEST IN MIAMI AND TAMPA MARKETING: The Miami store leads in both annual sales and "
        "performance factor (1.2x baseline), while Tampa is a strong second. Increasing weekly "
        "marketing spend at these locations by 15–20% during peak seasons (summer months and "
        "December) is projected to amplify the natural sales lift and capture a larger share of "
        "seasonal consumer spending with the highest probability of return on investment.",

        "3. IMPLEMENT A FAMILY SHOPPER LOYALTY PROGRAM: Family Shoppers represent the largest "
        "customer segment (30% of the base) and carry the highest average basket size ($150). "
        "A targeted tiered rewards program  that offers bulk-purchase discounts, double-point "
        "weekends, and family meal bundles would increase visit frequency and deepen loyalty "
        "among this high-value segment, converting Silver-tier members to Gold and Platinum.",

        "4. OPTIMIZE WEEKEND STAFFING AND INVENTORY: Sales data confirms that weekend transactions "
        "are approximately 30% higher than weekday averages. GreenGrocer should ensure all five "
        "stores maintain full staff deployment on Saturdays and Sundays, with inventory pre-stocked "
        "by Friday evening. Reducing weekend stockouts in top-selling categories (Produce and "
        "Prepared Foods) could recover an estimated 3–5% in potential lost sales.",

        "5. MENTOR GAINESVILLE AND JACKSONVILLE WITH MIAMI BEST PRACTICES: The Miami store "
        "achieves superior sales per square foot ($" + 
        f"{operational_df.loc[operational_df['Store']=='Miami','SalesPerSqFt'].values[0]:,.2f}" +
        ") compared to Gainesville and Jacksonville. A structured knowledge-transfer program that  "
        "covers staff training, product placement, and local marketing tactics could help "
        "underperforming stores close the gap. Even a 10% improvement in SalesPerSqFt at "
        "Gainesville and Jacksonville would meaningfully increase total chain revenue.",

        "6. LEVERAGE HEALTH ENTHUSIAST SEGMENT WITH SUBSCRIPTION BOXES: Health Enthusiasts visit "
        "8–15 times per month, making them the most frequent shoppers. A weekly organic produce "
        "subscription box that features curated seasonal items and exclusive member discounts "
        "would lock in recurring revenue, reduce food waste through predictable demand, and "
        "strengthen the brand identity as a premium organic destination.",

        "7. REDUCE GROCERY DEPARTMENT DEPENDENCY: The Grocery department has the lowest profit "
        "margin (20%) and competes directly with conventional supermarkets. GreenGrocer should "
        "shift shelf space from commodity canned goods toward artisan, locally sourced, and "
        "specialty grocery items that command premium pricing and reinforce the organic brand "
        "targeting a margin improvement of 3–5 percentage points in this department."
    ]

    print("\n--- Strategic Recommendations ---")
    for rec in recommendations:
        print(f"\n  {rec}")

    return recommendations


# TODO 5: Summary Report

def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    # Pull live values from the dataframes so the summary is data-driven, not hard-coded
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_margin = sales_df["ProfitMargin"].mean()
    top_store = operational_df.loc[operational_df["AnnualSales"].idxmax(), "Store"]
    top_dept_margin = sales_df.groupby("Department")["ProfitMargin"].mean().idxmax()
    top_segment = customer_df.groupby("Segment")["MonthlySpend"].mean().idxmax()
    weekend_lift = (sales_df[sales_df["DayOfWeek"] >= 5]["Sales"].mean() /
                    sales_df[sales_df["DayOfWeek"] < 5]["Sales"].mean() - 1) * 100

    print("\n" + "=" * 70)
    print("           GREENGROCER ANNUAL ANALYTICS — EXECUTIVE SUMMARY")
    print("=" * 70)

    print("""
OVERVIEW
--------
GreenGrocer completed its 2023 fiscal year with  annual sales
total of ${:,.0f} and total profit of ${:,.0f}, reflecting an average
profit margin of {:.1f}%. This analytics review examines performance across
five Florida stores — Tampa, Orlando, Miami, Jacksonville, and Gainesville —
spanning sales transactions, customer loyalty behavior, and operational
efficiency. The analysis applies descriptive, diagnostic, and predictive
techniques to surface the patterns and relationships that are most actionable
for the upcoming strategy cycle.
""".format(total_sales, total_profit, avg_margin * 100))

    print("""KEY FINDINGS
------------
  • TOP-PERFORMING STORE: {} leads all locations in annual sales and
    profitability, driven by the largest footprint (18,000 sq ft), highest
    staff count, and longest operating history of 7 years.

  • HIGHEST-MARGIN DEPARTMENT: {} delivers the strongest average profit
    margin across the chain, representing the clearest opportunity for
    margin-accretive growth through category expansion.

  • CUSTOMER SEGMENT OPPORTUNITY: {} customers spend more per month
    on average than any other segment, yet many remain at Silver loyalty
    tiers.

  • SEASONAL PEAKS: Summer (June–August) and December consistently drive
    the highest monthly sales volumes, with weekends generating approximately
    {:.1f}% more in daily revenue than weekdays
    
  • UNDERPERFORMING STORES: Gainesville and Jacksonville trail the chain
    average in Sales per Sq Ft and Customer Satisfaction, pointing to
    operational and marketing gaps that can be addressed through structured
    improvement initiatives.
""".format(top_store, top_dept_margin, top_segment, weekend_lift))

    print("""RECOMMENDATIONS
---------------
  • Expand Prepared Foods and Bakery floor space at all stores, prioritizing
    locations with the most headroom for margin improvement.

  • Increase marketing investment in Miami and Tampa during peak seasons
    (summer and December) to maximize return during the highest-traffic periods.

  • Launch a Family Shopper loyalty tier with bundle discounts and
    double-point weekends to drive frequency and basket size in the
    largest customer segment.

  • Optimize weekend staffing and Thursday/Friday inventory replenishment
    to capitalize on the consistent weekend sales premium across all locations.

  • Deploy a Miami-to-Gainesville and Jacksonville knowledge-transfer program
    focusing on visual merchandising, local marketing, and staff development
    to close the performance gap at underperforming stores.
""")

    print("""EXPECTED IMPACT
---------------
If GreenGrocer implements the recommendations above over the next 12 months,
the combined effect of margin improvement in high-profit departments, better
seasonal revenue acquistion, and elevated customer loyalty is expected
to increase chain-wide profitability by an estimated 8–12%. The underperforming
stores represent the greatest lever: closing even half the gap between
Gainesville/Jacksonville and the chain average in Sales per Sq Ft would add
meaningful incremental annual revenue without requiring additional capital
investment. For the long-term, strengthening the loyalty program and leaning into the
organic premium brand position will drive sustainable differentiation in an
increasingly competitive grocery market.
""")
    print("=" * 70)


# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)
    
    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing
    
    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()
    
    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()
    
    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()
    
    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()
    
    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()
    
    # Show all figures
    plt.show()
    
    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

# Run the main function
if __name__ == "__main__":
    results = main()
