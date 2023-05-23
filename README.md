# Retail Sales Dashboard

This project provides a retail sales dashboard, allowing users to interactively explore the sales data at both a monthly and weekly level, and across various stores and departments.

## Project Structure

The project consists of two main Python files:
1. `app.py`: This file contains the code for creating a Dash application that displays the sales data in a user-friendly, interactive dashboard. 
2. `data_loader.py`: This file loads and preprocesses the retail sales data, preparing it for visualization in the dashboard.

## Description of Python Files

### `app.py`

This file contains the code for creating a Dash application. The application includes a navigation bar and a body which contains several cards. Each card shows different sales figures (total sales, sales by month, sales by department, etc.) for a particular store. 

Users can select the desired store, base month, and comparison month from dropdown menus. The selection will automatically update the figures on the cards.

### `data_loader.py`

This file loads and preprocesses the retail sales data from a CSV file. The preprocessing steps include:

- Calculating the monthly sales for each store
- Calculating the holiday sales for each store
- Merging the monthly sales and holiday sales into one dataframe
- Calculating the weekly sales for each store
- Aggregating the sales data at the department level for each store

## How to Run the Project

1. Ensure that you have the necessary Python packages installed, which include pandas, numpy, plotly, dash, and dash_bootstrap_components.

2. Run `data_loader.py` to load and preprocess the data.

3. Run `app.py` to start the Dash application. 

4. Open a web browser and navigate to the local URL where the Dash app is running (by default, this is usually `http://127.0.0.1:8050/`).

## Data

The retail sales data used in this project is expected to be in CSV format, with the following columns:

- Store: The ID of the store
- Date: The date of sales record, in the format 'YYYY-MM-DD'
- Weekly_Sales: The total sales for the given store in the given week
- Holiday_Flag: A flag indicating whether the week included a holiday
- Temperature: The average temperature in the region for the given week
- Fuel_Price: The cost of fuel in the region for the given week
- CPI: The consumer price index for the given week
- Unemployment: The unemployment rate for the given week
- IsHoliday: A boolean indicating whether the given week is a holiday week

The CSV file is expected to be located in the same directory as `data_loader.py`. The name of the file is 'retail_sales.csv'. 

Please note that this project was developed and tested using Python 3.7.
