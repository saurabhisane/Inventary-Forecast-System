# Inventory Forecast System

A scalable and accurate inventory forecasting system designed to optimize stock levels, reduce carrying costs, and prevent stockouts.

## Overview

The Inventory Forecast System uses advanced forecasting algorithms to predict future inventory needs based on historical sales data, seasonality patterns, market trends, and other relevant factors. By providing accurate demand forecasts, businesses can make informed decisions about inventory management, leading to cost savings and improved customer satisfaction.

## Features

- **Multi-method Forecasting**: Implements multiple forecasting algorithms including Time Series Analysis, Machine Learning models, and statistical methods
- **Automatic Algorithm Selection**: Intelligently selects the best forecasting method based on your data patterns
- **Seasonality Detection**: Automatically identifies seasonal patterns in your sales data
- **Inventory Optimization**: Recommends optimal stock levels based on service level targets
- **Exception Reporting**: Highlights unusual patterns or potential stock issues
- **Interactive Dashboard**: Visualize forecasts, trends, and inventory metrics

## Installation

```bash
# Clone the repository
git clone https://github.com/saurabhisane/Inventary-Forecast-System.git

# Navigate to the project directory
cd Inventary-Forecast-System

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
# Example usage of the forecasting system
from inventory_forecast import Forecaster

# Initialize the forecaster
forecaster = Forecaster(data_path='path/to/your/data.csv')

# Generate forecasts
forecasts = forecaster.predict(horizon=30)  # Forecast 30 days ahead

# Get inventory recommendations
recommendations = forecaster.get_inventory_recommendations()

# Display results
forecaster.plot_forecasts()
```

## Configuration

The system can be configured through the `config.yaml` file:

```yaml
forecast_settings:
  algorithms: ['arima', 'prophet', 'lstm']
  evaluation_metric: 'rmse'
  confidence_interval: 0.95

inventory_settings:
  service_level: 0.95
  lead_time_days: 7
  safety_stock_method: 'normal_distribution'
```

## Data Format

The system expects CSV files with the following format:

```
date,product_id,sales,price,promotions
2023-01-01,A1001,120,25.99,0
2023-01-02,A1001,145,25.99,1
...
```

## Dependencies

- Python 3.8+
- Pandas
- NumPy
- Scikit-learn
- Prophet
- TensorFlow (optional, for deep learning models)
- Plotly (for visualization)
