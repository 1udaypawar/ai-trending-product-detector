AI Trending Product Detector
This is a web application built with Streamlit that uses AI to analyze sales data, provide business insights, and forecast future bestselling products.

Features
Interactive Dashboard: Get a quick overview of your total sales, unique products, and top bestsellers.

AI-Powered Forecasting: Predict which products are likely to be your next bestsellers using the Prophet forecasting model.

Deep Dive Analysis: Select a specific product to get a detailed sales forecast and visualize its future trend.

Flexible Data Mapping: Upload your own CSV file and easily map your columns to the required format.

How It Works
The application takes a sales data CSV file as input. It requires columns for product names, order dates, and sales values. If you only have quantity and price, it can calculate the sales for you.

Once the data is prepared, the app provides three main sections:

Dashboard: Shows high-level metrics and charts.

Forecast Bestseller: Runs a comprehensive analysis on all products to predict the top 5 future bestsellers.

Product Deep Dive: Allows you to get a detailed forecast for any single product from your dataset.

Installation
Clone the repository:

git clone [https://github.com/your-username/ai-trending-product-detector.git](https://github.com/your-username/ai-trending-product-detector.git)
cd ai-trending-product-detector

Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required dependencies:

pip install -r requirements.txt

Usage
Run the Streamlit application:

streamlit run app4.py

Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

Upload your sales CSV file. You can use the sample_data/sales_data.csv file to test the application.

Map your columns in the sidebar to match your dataset.

Explore the dashboard and run the AI forecast!

Project Structure
.
├── app4.py                 # Main Streamlit application file
├── product_predictor.py    # Contains the forecasting logic
├── requirements.txt        # Python dependencies
├── logo.jpg                # Application logo
├── sample_data/
│   └── sales_data.csv      # Sample sales data
└── README.md               # This file
