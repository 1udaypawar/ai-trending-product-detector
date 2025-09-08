import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional
from prophet import Prophet
import plotly.graph_objs as go
import logging

# --- Suppress informational messages to keep the output clean ---
logging.getLogger('prophet').setLevel(logging.ERROR)
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

# --- Data structure to hold results for a single product ---
@dataclass
class ProductForecast:
    product_name: str
    historical_data: pd.DataFrame
    forecast_data: pd.DataFrame
    peak_info: Dict

def analyze_single_product(product_name, product_data):
    """Trains a Prophet model for a single product and returns its forecast."""
    df = product_data[['Order Date', 'Sales']].copy()
    df.rename(columns={'Order Date': 'ds', 'Sales': 'y'}, inplace=True)
    
    # Aggregate data to have one row per day
    daily_df = df.groupby('ds').sum().reset_index()

    # Prophet needs at least 2 data points, but more is much better.
    if len(daily_df) < 10:
        return None

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(daily_df)
    
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    
    # Find the future peak
    last_historical_date = daily_df['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_historical_date]
    
    if not future_forecast.empty:
        peak_row = future_forecast.loc[future_forecast['yhat'].idxmax()]
        peak_info = {
            'peak_date': peak_row['ds'],
            'peak_sales': peak_row['yhat'],
            'peak_month': peak_row['ds'].strftime('%B %Y')
        }
    else:
        peak_info = {'peak_date': None, 'peak_sales': 0, 'peak_month': 'N/A'}
        
    return ProductForecast(
        product_name=product_name,
        historical_data=daily_df,
        forecast_data=forecast,
        peak_info=peak_info
    )

def run_comprehensive_analysis(data):
    """
    Runs forecasting for all products and returns a leaderboard and detailed results.
    """
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    products = data['Product Name'].unique()
    
    all_product_details = {}
    leaderboard_data = []

    for product in products:
        product_data = data[data['Product Name'] == product]
        forecast_result = analyze_single_product(product, product_data)
        
        if forecast_result:
            all_product_details[product] = forecast_result
            leaderboard_data.append({
                'Product Name': product,
                'Predicted Peak Month': forecast_result.peak_info['peak_month'],
                'Estimated Peak Sales': forecast_result.peak_info['peak_sales']
            })

    if not leaderboard_data:
        return {'leaderboard': pd.DataFrame(), 'product_details': {}}
        
    # Create and sort the leaderboard
    leaderboard = pd.DataFrame(leaderboard_data)
    leaderboard.sort_values(by='Estimated Peak Sales', ascending=False, inplace=True)
    leaderboard['Estimated Peak Sales'] = leaderboard['Estimated Peak Sales'].map('${:,.2f}'.format)
    
    return {
        'leaderboard': leaderboard.head(5),
        'product_details': all_product_details
    }

def plot_single_product_forecast(product_forecast: ProductForecast):
    """Generates a Plotly graph for a single product's forecast."""
    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(
        x=product_forecast.historical_data['ds'], 
        y=product_forecast.historical_data['y'], 
        mode='lines', 
        name='Historical Sales'
    ))
    
    # Forecast line
    fig.add_trace(go.Scatter(
        x=product_forecast.forecast_data['ds'], 
        y=product_forecast.forecast_data['yhat'], 
        mode='lines', 
        name='Forecasted Sales',
        line=dict(color='red', dash='dash')
    ))

    # Uncertainty interval
    fig.add_trace(go.Scatter(
        x=product_forecast.forecast_data['ds'].tolist() + product_forecast.forecast_data['ds'].tolist()[::-1],
        y=product_forecast.forecast_data['yhat_upper'].tolist() + product_forecast.forecast_data['yhat_lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    ))

    # Highlight peak month
    peak_date = product_forecast.peak_info['peak_date']
    if peak_date:
        peak_sales = product_forecast.peak_info['peak_sales']
        peak_month = product_forecast.peak_info['peak_month']
        fig.add_vline(x=peak_date, line_width=2, line_dash="dash", line_color="green")
        fig.add_annotation(
            x=peak_date, y=peak_sales, 
            text=f"Peak Month: {peak_month}", 
            showarrow=True, arrowhead=1, yshift=10
        )

    fig.update_layout(
        title=f"Sales Forecast for '{product_forecast.product_name}'",
        xaxis_title="Date",
        yaxis_title="Sales",
        legend_title="Legend"
    )
    return fig

