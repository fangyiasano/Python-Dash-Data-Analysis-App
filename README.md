# Retail Sales Dashboard with Python Dash

This is a dynamic dashboard for visualizing retail sales data. The application is built in Python using the Dash framework. Dash Bootstrap Components are used for structuring the layout, and Plotly for interactive charts.

## Files

main.py - This is the main Python script that runs the dashboard.

## Instructions

1. Ensure you have the necessary Python libraries installed. You will need:
   - pandas
   - numpy
   - plotly
   - dash
   - dash-bootstrap-components

2. Run the script with `python main.py`. This will start a local server and the dashboard can be accessed by navigating to `http://localhost:8050` in a web browser.

## Dashboard Components

The dashboard includes a range of components for a comprehensive view of retail sales data.

- Dropdown menus for selecting the current period, reference period, and store
- Cards displaying total monthly sales, holiday sales, and the number of departments for the selected store and period
- An interactive line chart comparing weekly sales for the current and reference period
- Bar charts showing sales by department for the current and reference period
- A bar chart showing the difference in sales between the top departments for the current and reference period
