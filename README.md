here is link for drive where you can find the project video [google drive]('https://drive.google.com/drive/folders/1PU_i-CGYICOdbiwI6BX2D4Q9M2rPlEr0?usp=sharing')

AI Trending Product Detector

This is a web application built with Streamlit that uses AI to analyze sales data, provide business insights, and forecast future bestselling products.

Features
1. Interactive Dashboard: Get a quick overview of your total sales, unique products, and top bestsellers.
2. AI-Powered Forecasting: Predict which products are likely to be your next bestsellers using the Prophet forecasting model.
3. Deep Dive Analysis: Select a specific product to get a detailed sales forecast and visualize its future trend.
4. Flexible Data Mapping: Upload your own CSV file and easily map your columns to the required format.

How It Works

The application takes a sales data CSV file as input. It requires columns for product names, order dates, and sales values. If you only have quantity and price, it can calculate the sales for you.

Once the data is prepared, the app provides three main sections:
1. Dashboard: Shows high-level metrics and charts.
2. Forecast Bestseller: Runs a comprehensive analysis on all products to predict the top 5 future bestsellers.
3. Product Deep Dive: Allows you to get a detailed forecast for any single product from your dataset.

Installation

1. Clone the repository:
git clone [https://github.com/1udaypawar/ai-trending-product-detector.git](https://github.com/1udaypawar/ai-trending-product-detector.git)
cd ai-trending-product-detector

2. Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:
pip install -r requirements.txt

## 📂 Dataset
Download the dataset from [Google Drive Link](https://drive.google.com/drive/folders/1PMj1HKFWa2dwTruAS0-veu4ZLyYaWTCu?usp=sharing).
Place it in the `data/` folder before running the app.


Usage

1. Run the Streamlit application:
   streamlit run app4.py

2. pen your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

3. Upload your sales CSV file. You can use the sample_data/sales_data.csv file to test the application.

4. Map your columns in the sidebar to match your dataset.

5. Explore the dashboard and run the AI forecast!

Project Structure

 1. app4.py                 # Main Streamlit application file
 2. product_predictor.py    # Contains the forecasting logic
 3. requirements.txt        # Python dependencies
 4. logo.jpg                # Application logo
 5. sample_data/
  └── sales_data.csv      # Sample sales data
 6. README.md               # This file
