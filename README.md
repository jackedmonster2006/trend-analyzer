# 🛒 E-Commerce & TikTok Shop Trend Analyzer

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458.svg)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI-orange.svg)

An interactive Business Analytics dashboard designed to track viral e-commerce products, calculate profit margins, and utilize **Generative AI** to optimize pricing strategies for dropshippers.

[👉 **View the Live Dashboard Here**](https://trend-analyzer.streamlit.app/)

## 🚀 Key Features

*   **Mock Data Generation Engine:** Simulates real-world viral sales curves (Daily Units Sold, Retail Price, Supplier Cost) across 4 major e-commerce categories (Beauty, Tech, Home, Fitness) to demonstrate data pipeline architecture.
*   **Dynamic Financial KPIs:** Calculates Total Market Revenue, Estimated Profit, and Average Profit Margins in real-time based on the user's selected time window.
*   **Interactive Data Visualization:** Uses `Plotly` to render sleek, dark-mode Line Charts (Revenue Trends) and Bar Charts (Profit by Product).
*   **Generative AI Pricing Strategist:** Integrates the `Google Gemini 2.5 Flash` API. The app feeds supplier costs, competitor pricing, and market demand into the LLM, which outputs psychological pricing recommendations, AOV up-sells, and TikTok Ad hooks.

## 🧠 Architecture & Stack

*   **Frontend / UI:** `Streamlit` (Interactive Web App)
*   **Data Manipulation:** `Pandas`
*   **Visualization:** `Plotly Express`
*   **Artificial Intelligence:** `google-generativeai` (Gemini API)

## 🛠️ Local Installation

To run this dashboard locally:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/ecom-trend-analyzer.git
    cd ecom-trend-analyzer
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your Google Gemini API key to activate the AI Strategist tab:
    ```env
    GEMINI_API_KEY="your_api_key_here"
    ```

5.  **Run the App**
    ```bash
    streamlit run app.py
    ```
