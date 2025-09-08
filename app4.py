import streamlit as st
import pandas as pd
from product_predictor import run_comprehensive_analysis, plot_single_product_forecast

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Trending product detector",
    page_icon="logo.png",
    layout="wide"
)

# --- Data Preparation (Upgraded with Interactive Mapping) ---
def map_and_prepare_data(df, product_col, date_col, sales_col, quantity_col=None, price_col=None):
    """
    Prepares the dataframe for the model using user-defined column mappings.
    The model needs: 'Product Name', 'Order Date', 'Sales'
    """
    try:
        # Create a copy to avoid modifying the original dataframe in cache
        prepared_df = df.copy()

        # Rename columns based on user mapping
        prepared_df.rename(columns={
            product_col: 'Product Name',
            date_col: 'Order Date'
        }, inplace=True)

        # Calculate 'Sales' if needed, otherwise rename
        if quantity_col and price_col:
            st.write(f"Calculating 'Sales' from '{quantity_col}' and '{price_col}'...")
            # Ensure columns are numeric before multiplication
            prepared_df[quantity_col] = pd.to_numeric(prepared_df[quantity_col], errors='coerce')
            prepared_df[price_col] = pd.to_numeric(prepared_df[price_col], errors='coerce')
            prepared_df['Sales'] = prepared_df[quantity_col] * prepared_df[price_col]
        else:
            st.write(f"Using '{sales_col}' as the 'Sales' column...")
            prepared_df.rename(columns={sales_col: 'Sales'}, inplace=True)

        # Basic cleaning
        prepared_df = prepared_df[pd.to_numeric(prepared_df['Sales'], errors='coerce') > 0]
        prepared_df.dropna(subset=['Product Name', 'Order Date', 'Sales'], inplace=True)
        
        # Convert Order Date to datetime objects
        prepared_df['Order Date'] = pd.to_datetime(prepared_df['Order Date'], errors='coerce')
        prepared_df.dropna(subset=['Order Date'], inplace=True) # Drop rows where date conversion failed

        # Ensure required columns exist
        required_cols = ['Product Name', 'Order Date', 'Sales']
        if not all(col in prepared_df.columns for col in required_cols):
             st.error("Data preparation failed. Please check your column selections.")
             return None

        st.success("✅ Data has been successfully prepared!")
        return prepared_df[required_cols]

    except Exception as e:
        st.error(f"An error occurred during data preparation: {e}")
        return None


# --- Main App ---
st.image("logo.png", width=150)
st.title("🚀 AI Trending product detector")
st.write("Upload your sales data, map your columns, and let the AI give you a complete business overview and predict future bestsellers.")

# --- Initialize session state ---
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'prepared_data' not in st.session_state:
    st.session_state.prepared_data = None
if 'data_mapped' not in st.session_state:
    st.session_state.data_mapped = False

uploaded_file = st.file_uploader("Click here to upload your sales CSV file", type="csv")

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file, encoding='windows-1252', on_bad_lines='skip')
        st.write("### Preview of Your Data")
        st.dataframe(data.head())
        
        # --- Interactive Column Mapping UI ---
        with st.expander("STEP 1: Map Your Data Columns", expanded=True):
            st.info("Tell the app which columns contain your product names, order dates, and sales values.")
            
            column_list = data.columns.tolist()
            col1, col2, col3 = st.columns(3)
            
            with col1:
                product_col = st.selectbox("Which column is the Product Name?", column_list, index=0)
            with col2:
                date_col = st.selectbox("Which column is the Order Date?", column_list, index=1)
            with col3:
                sales_method = st.radio("How is sales value represented?", ("A single 'Sales' column", "Calculate from 'Quantity' and 'Price'"))

            sales_col, quantity_col, price_col = None, None, None
            if sales_method == "A single 'Sales' column":
                sales_col = st.selectbox("Which column has the Sales Value?", column_list, index=2)
            else:
                quantity_col = st.selectbox("Which column has the Quantity?", column_list)
                price_col = st.selectbox("Which column has the Unit Price?", column_list)

            if st.button("✅ Prepare and Validate Data", key="prepare_data"):
                with st.spinner('Preparing your data...'):
                    st.session_state.prepared_data = map_and_prepare_data(data, product_col, date_col, sales_col, quantity_col, price_col)
                    if st.session_state.prepared_data is not None:
                        st.session_state.data_mapped = True

    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

# --- Display dashboard and forecasting tabs ONLY if data is prepared ---
if st.session_state.data_mapped:
    prepared_data = st.session_state.prepared_data
    
    st.markdown("---")
    st.header("STEP 2: Explore Your Business Insights")

    # --- Create Tabs ---
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔮 Forecast Bestseller", "🔍 Product Deep Dive"])

    # ================= TAB 1: DASHBOARD =================
    with tab1:
        st.header("Sales Data Overview")
        total_sales = prepared_data['Sales'].sum()
        num_products = prepared_data['Product Name'].nunique()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Sales", f"${total_sales:,.2f}")
        col2.metric("Number of Unique Products", f"{num_products:,}")

        st.subheader("Top 10 Bestselling Products (All Time)")
        top_10_products = prepared_data.groupby('Product Name')['Sales'].sum().nlargest(10)
        st.bar_chart(top_10_products)

        st.subheader("Overall Sales Trend")
        daily_sales = prepared_data.groupby(prepared_data['Order Date'].dt.date)['Sales'].sum()
        st.line_chart(daily_sales)

    # ================= TAB 2: FORECAST BESTSELLER =================
    with tab2:
        st.header("Predict Your Next Bestseller")
        if st.button("✨ Run AI Forecast!", key="forecast_button"):
            with st.spinner('The AI is analyzing every product... This might take a few minutes...'):
                analysis_results = run_comprehensive_analysis(prepared_data)
                st.session_state.analysis_results = analysis_results
            st.success("Analysis Complete!")

        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            leaderboard = results['leaderboard']
            
            st.subheader("🏆 Predicted Top 5 Bestsellers")
            st.dataframe(leaderboard)

            if not leaderboard.empty:
                top_product_name = leaderboard.iloc[0]['Product Name']
                if top_product_name in results['product_details']:
                    top_product_forecast = results['product_details'][top_product_name]
                    st.subheader(f"Detailed Forecast for '{top_product_name}'")
                    fig = plot_single_product_forecast(top_product_forecast)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Click the 'Run AI Forecast!' button to see your future bestsellers.")

    # ================= TAB 3: PRODUCT DEEP DIVE =================
    with tab3:
        st.header("Analyze a Specific Product")
        product_list = sorted(prepared_data['Product Name'].unique())
        selected_product = st.selectbox("Select a product to analyze", product_list)

        if st.button("🔍 Get Detailed Forecast", key="deep_dive_button"):
            if st.session_state.analysis_results:
                if selected_product in st.session_state.analysis_results['product_details']:
                    with st.spinner(f"Generating deep dive for '{selected_product}'..."):
                        product_forecast = st.session_state.analysis_results['product_details'][selected_product]
                        fig = plot_single_product_forecast(product_forecast)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("This product may have had too little data to be included in the main analysis. Please run the forecast on Tab 2 first or try another product.")
            else:
                st.warning("Please run the main AI forecast on the 'Forecast Bestseller' tab first.")