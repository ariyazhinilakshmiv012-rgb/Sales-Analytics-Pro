import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Sales & Revenue Analysis Dashboard")
st.write("Analyze sales performance, revenue trends, and products.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Revenue"] = df["Quantity"] * df["Unit_Price"]
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

products = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

# Filter the data
filtered_df = df[
    df["Region"].isin(regions)
    & df["Category"].isin(categories)
    & df["Product"].isin(products)
]

# Calculate key performance indicators
total_revenue = filtered_df["Revenue"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = len(filtered_df)
total_products = filtered_df["Product"].nunique()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Units Sold", f"{total_quantity:,}")
col3.metric("Sales Records", f"{total_orders:,}")
col4.metric("Products Sold", f"{total_products:,}")

st.divider()

# Revenue trend
st.subheader("📈 Revenue Trend")

if not filtered_df.empty:
    monthly_revenue = (
        filtered_df.groupby(
            filtered_df["Date"].dt.to_period("M").astype(str)
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue.columns = ["Month", "Revenue"]

    fig1 = px.line(
        monthly_revenue,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Product performance
    col1, col2 = st.columns(2)

    product_sales = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    with col1:
        st.subheader("🏆 Top-Performing Products")

        fig2 = px.bar(
            product_sales,
            x="Product",
            y="Revenue",
            color="Product",
            title="Revenue by Product"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Category analysis
    category_sales = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
        .reset_index()
    )

    with col2:
        st.subheader("📦 Category Analysis")

        fig3 = px.pie(
            category_sales,
            names="Category",
            values="Revenue",
            title="Revenue by Category"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Region analysis
    st.subheader("🌍 Revenue by Region")

    region_sales = (
        filtered_df.groupby("Region")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    fig4 = px.bar(
        region_sales,
        x="Region",
        y="Revenue",
        color="Region",
        title="Regional Revenue Comparison"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Sales data table
    st.subheader("📋 Sales Data")

    st.dataframe(
        filtered_df.sort_values("Date", ascending=False),
        use_container_width=True
    )

    # Download filtered data
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Sales Data",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

else:
    st.warning("No sales records match your selected filters.")

st.caption("Sales & Revenue Analysis Dashboard | Python Project")
