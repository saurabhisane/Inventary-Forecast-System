import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime, timedelta

def create_prophet_forecast(df, target_column, periods=30):
    try:
        prophet_df = df[['Date', target_column]].copy()
        prophet_df.columns = ['ds', 'y']
        
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )
        model.fit(prophet_df)
        
        future_dates = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future_dates)
        
        return forecast
    except Exception as e:
        print(f"Error in Prophet forecast: {str(e)}")
        return None

def process_inventory_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.sort_values('Date')
        
        numeric_df = df.select_dtypes(include=['number'])
        imputer = SimpleImputer(strategy='mean')
        df_imputed = pd.DataFrame(imputer.fit_transform(numeric_df), columns=numeric_df.columns)
        
        target_column = 'Quantity' if 'Quantity' in df_imputed.columns else 'Sales'
        
        last_date = df['Date'].max()
        start_date = last_date - timedelta(days=90)
        mask = df['Date'] >= start_date
        df_recent = df[mask].copy()
        df_imputed_recent = df_imputed[mask].copy()
        
        forecast = create_prophet_forecast(df_recent, target_column)
        if forecast is None:
            raise ValueError("Failed to generate forecast")
        
        plt.style.use('classic')
        plt.figure(figsize=(15, 8))
        
        plt.plot(df_recent['Date'], df_imputed_recent[target_column], 
                marker='o', linestyle='-', color='#2196F3', 
                label='Actual Data', markersize=6, alpha=0.7)
        
        plt.plot(forecast['ds'].iloc[-30:], forecast['yhat'].iloc[-30:], 
                color='#FF5722', linestyle='--', 
                label='30-Day Forecast', linewidth=2)
        
        plt.fill_between(forecast['ds'].iloc[-30:],
                        forecast['yhat_lower'].iloc[-30:],
                        forecast['yhat_upper'].iloc[-30:],
                        color='#FF5722', alpha=0.1,
                        label='Confidence Interval')
        
        plt.title(f'{target_column} Trend and Forecast (Last 3 Months)', 
                 fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel(target_column, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.legend(loc='upper left', fontsize=12)
        
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        stats = df_imputed_recent[target_column].describe().round(2)
        
        forecast_table = forecast.iloc[-30:][['ds', 'yhat']].round(2)
        forecast_table.columns = ['Date', 'Forecast']
        
        last_value = df_imputed_recent[target_column].iloc[-1]
        avg_forecast = forecast_table['Forecast'].mean()
        trend = 'increasing' if avg_forecast > last_value else 'decreasing'
        percent_change = abs(((avg_forecast - last_value) / last_value) * 100)
        
        weekly_pattern = forecast['weekly'].iloc[:7]
        weekly_strongest_day = weekly_pattern.idxmax()
        weekly_weakest_day = weekly_pattern.idxmin()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        df['Month'] = df['Date'].dt.month
        monthly_avg = df.groupby('Month')[target_column].mean()
        peak_month = monthly_avg.idxmax()
        low_month = monthly_avg.idxmin()
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        current_year_avg = df[df['Date'].dt.year == df['Date'].dt.year.max()][target_column].mean()
        prev_year_avg = df[df['Date'].dt.year == df['Date'].dt.year.max() - 1][target_column].mean()
        yoy_growth = ((current_year_avg - prev_year_avg) / prev_year_avg * 100) if prev_year_avg != 0 else 0
        
        prediction_summary = f"""
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Comprehensive Forecast Analysis</h5>
            </div>
            <div class="card-body">
                <h6 class="text-primary mb-3">Short-Term Forecast (Next 30 Days)</h6>
                <p>Based on recent trends, {target_column.lower()} is expected to be {trend} by 
                approximately {percent_change:.1f}% over the next 30 days. The current value is {last_value:.0f} 
                with an average forecast of {avg_forecast:.0f}.</p>
                
                <h6 class="text-primary mb-3 mt-4">Weekly Patterns</h6>
                <p>Historical data shows strongest performance on {days[weekly_strongest_day]} and 
                lowest on {days[weekly_weakest_day]}. Consider adjusting inventory levels accordingly.</p>
                
                <h6 class="text-primary mb-3 mt-4">Seasonal Trends</h6>
                <p>Peak activity typically occurs in {month_names[peak_month-1]}, while 
                {month_names[low_month-1]} shows historically lower numbers. Year-over-year growth 
                is currently at {yoy_growth:.1f}%.</p>
                
                <h6 class="text-primary mb-3 mt-4">Key Recommendations</h6>
                <ul>
                    <li>Plan for {trend} demand in the immediate future</li>
                    <li>Optimize stock levels for {days[weekly_strongest_day]} peaks</li>
                    <li>Prepare for seasonal peak in {month_names[peak_month-1]}</li>
                    <li>Consider reduced inventory during {month_names[low_month-1]}</li>
                </ul>
                
                <div class="alert alert-info mt-3">
                    <strong>Long-term Outlook:</strong> Based on the year-over-year growth of {yoy_growth:.1f}%, 
                    maintain a {yoy_growth > 0 and 'progressive' or 'conservative'} inventory strategy. 
                    {
                    'Consider increasing storage capacity and stock levels.' if yoy_growth > 5 
                    else 'Maintain current inventory levels with minor adjustments.' if yoy_growth > 0 
                    else 'Focus on optimizing existing inventory and reducing holding costs.'
                    }
                </div>
            </div>
        </div>
        """
        
        final_html = f"""
        <div class="row">
            <div class="col-12">
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">{target_column} Analysis</h5>
                    </div>
                    <div class="card-body">
                        <img src="data:image/png;base64,{plot_url}" class="img-fluid">
                    </div>
                </div>
                {prediction_summary}
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">30-Day Forecast</h5>
                    </div>
                    <div class="card-body">
                        <table class="table table-striped">
                            <tr><th>Date</th><th>Forecast</th></tr>
                            {forecast_table.to_html(index=False, header=False, classes='table table-striped')}
                        </table>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return final_html
        
    except Exception as e:
        print(f"Error in process_inventory_data: {str(e)}")
        raise
