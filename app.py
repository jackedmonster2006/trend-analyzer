import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# We will try to use the Google Gemini SDK for AI Pricing recommendations
try:
    import google.generativeai as genai
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        ai_client = True
    else:
        ai_client = False
except Exception as e:
    print("AI Client Error:", e)
    ai_client = False

st.set_page_config(page_title="E-Commerce Trend Analyzer", layout="wide", page_icon="🛒")
st.title("🛒 E-Commerce & TikTok Shop Trend Analyzer")
st.markdown("Track viral products, calculate estimated revenues, and use AI to optimize your pricing strategy.")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
category = st.sidebar.selectbox("Product Category", ["Beauty & Personal Care", "Electronics", "Home & Kitchen", "Fitness"])
time_range = st.sidebar.slider("Analysis Window (Days)", 7, 30, 14)

# --- MOCK DATA GENERATOR ---
def generate_mock_data(category, days):
    products = {
        "Beauty & Personal Care": ["Crystal Hair Eraser", "Rosemary Hair Oil", "Heatless Hair Curler", "Ice Roller"],
        "Electronics": ["Magnetic Power Bank", "Mini Projector", "Neck Massager", "Sunset Lamp"],
        "Home & Kitchen": ["Vegetable Chopper", "Portable Blender", "Shower Filter", "Spill-proof Bowl"],
        "Fitness": ["Posture Corrector", "Ab Roller Wheel", "Grip Strength Trainer", "Resistance Bands"]
    }
    
    data = []
    base_date = datetime.now()
    
    for prod in products[category]:
        # Generate trend curve
        for day in range(days):
            date = base_date - timedelta(days=day)
            
            # Simulate viral curve: older dates have fewer sales, newer dates spike
            base_sales = 50 if day > (days/2) else 300
            daily_sales = base_sales + (hash(prod + str(day)) % 200)
            
            unit_cost = 4.50 + (hash(prod) % 10)
            sell_price = unit_cost * 3.5  # Typical dropship markup
            
            data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Product": prod,
                "Daily_Units_Sold": daily_sales,
                "Unit_Cost": round(unit_cost, 2),
                "Retail_Price": round(sell_price, 2),
                "Daily_Revenue": round(daily_sales * sell_price, 2),
                "Daily_Profit": round(daily_sales * (sell_price - unit_cost), 2)
            })
            
    return pd.DataFrame(data)

with st.spinner("Scraping E-Commerce Data..."):
    df = generate_mock_data(category, time_range)
    df['Date'] = pd.to_datetime(df['Date'])

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📈 Market Trends", "💰 Competitor Pricing", "🤖 AI Pricing Strategist"])

with tab1:
    # --- KPIs ---
    st.subheader(f"Metrics for {category} (Last {time_range} Days)")

    total_rev = df['Daily_Revenue'].sum()
    total_profit = df['Daily_Profit'].sum()
    avg_margin = (total_profit / total_rev) * 100 if total_rev > 0 else 0

    top_product = df.groupby('Product')['Daily_Revenue'].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Market Revenue", f"${total_rev:,.2f}")
    col2.metric("Total Est. Profit", f"${total_profit:,.2f}")
    col3.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
    col4.metric("Top Trending Product", top_product)

    st.divider()

    # --- CHARTS ---
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 📈 Revenue Trends Over Time")
        fig_line = px.line(df, x="Date", y="Daily_Revenue", color="Product", markers=True, template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_b:
        st.markdown("### 📊 Total Profit by Product")
        profit_df = df.groupby('Product')['Daily_Profit'].sum().reset_index()
        fig_bar = px.bar(profit_df, x="Product", y="Daily_Profit", color="Product", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Competitor Sourcing & Margins")
    st.markdown("A breakdown of supplier costs vs retail prices for the top trending items.")
    
    # Create a clean summary dataframe for pricing
    pricing_df = df.groupby('Product').agg({
        'Unit_Cost': 'mean',
        'Retail_Price': 'mean',
        'Daily_Profit': 'sum',
        'Daily_Units_Sold': 'sum'
    }).reset_index()
    
    # Calculate exact profit margin per product
    pricing_df['Margin %'] = ((pricing_df['Retail_Price'] - pricing_df['Unit_Cost']) / pricing_df['Retail_Price']) * 100
    
    # Format the dataframe for display
    display_df = pricing_df.copy()
    display_df['Unit_Cost'] = display_df['Unit_Cost'].apply(lambda x: f"${x:.2f}")
    display_df['Retail_Price'] = display_df['Retail_Price'].apply(lambda x: f"${x:.2f}")
    display_df['Daily_Profit'] = display_df['Daily_Profit'].apply(lambda x: f"${x:,.2f}")
    display_df['Margin %'] = display_df['Margin %'].apply(lambda x: f"{x:.1f}%")
    
    # Rename columns for the UI
    display_df.columns = ['Product', 'Supplier Cost (AliExpress)', 'Avg Retail Price', 'Total Profit Generated', 'Total Units Sold', 'Profit Margin']
    
    st.dataframe(display_df, use_container_width=True)
    
with tab3:
    st.subheader("🤖 Generative AI Pricing Strategist")
    st.markdown("Select a trending product and let the AI analyze the data to recommend the optimal Dropshipping/TikTok Shop pricing strategy.")
    
    selected_ai_product = st.selectbox("Select a product to analyze:", df['Product'].unique())
    
    if not ai_client:
        st.warning("⚠️ No Gemini API Key found in `.env`. Please add it to use the AI Strategist.")
    else:
        if st.button("Generate Pricing Strategy"):
            with st.spinner("Consulting AI Strategist..."):
                try:
                    # Get product specific data
                    prod_data = pricing_df[pricing_df['Product'] == selected_ai_product].iloc[0]
                    cost = prod_data['Unit_Cost']
                    retail = prod_data['Retail_Price']
                    units = prod_data['Daily_Units_Sold']
                    
                    prompt = f"""
                    You are an elite e-commerce and dropshipping strategist.
                    Analyze the following product data and provide a pricing and marketing strategy to maximize profits on TikTok Shop.
                    
                    Product: {selected_ai_product}
                    Supplier Cost (AliExpress/CJ): ${cost:.2f}
                    Current Competitor Retail Price: ${retail:.2f}
                    Total Market Demand (Units Sold Last {time_range} Days): {units}
                    
                    Instructions:
                    1. Suggest an optimal "Perceived Value" price point (e.g., $19.99 vs $24.99) and explain why based on consumer psychology.
                    2. Provide an "Offer Structure" (e.g., Buy 1 Get 1 50% Off, Free Shipping over $30) to increase Average Order Value (AOV).
                    3. Give a 1-sentence hook for a TikTok Ad that justifies the price.
                    
                    Keep it highly professional and actionable.
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("Strategy Generated Successfully")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error generating strategy: {e}")
