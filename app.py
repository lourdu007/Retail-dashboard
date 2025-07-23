import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="🛒 Retail Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    return df

df = load_data()

st.title("🛍️ Online Retail Dashboard")
st.markdown("Analyze customer purchasing behavior from the UK-based online retailer.")

# Filter section
country = st.sidebar.selectbox("Select Country", df["Country"].unique())
df_filtered = df[df["Country"] == country]

# KPIs
total_sales = df_filtered["ItemTotal"].sum()
unique_customers = df_filtered["CustomerID"].nunique()
total_orders = df_filtered["InvoiceNo"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"£{total_sales:,.2f}")
col2.metric("Unique Customers", unique_customers)
col3.metric("Total Orders", total_orders)

# 📊 Sales by Customer
st.subheader("Top 10 Customers by Total Spend")
top_customers = df_filtered.groupby("CustomerID")["ItemTotal"].sum().nlargest(10).reset_index()
fig1 = px.bar(top_customers, x="CustomerID", y="ItemTotal", title="Top 10 Customers")
st.plotly_chart(fig1, use_container_width=True)

# 📦 Product Demand
st.subheader("Top 10 Products by Quantity Sold")
top_products = df_filtered.groupby("Description")["Quantity"].sum().nlargest(10).reset_index()
fig2 = px.bar(top_products, x="Quantity", y="Description", orientation='h', title="Top Products")
st.plotly_chart(fig2, use_container_width=True)
