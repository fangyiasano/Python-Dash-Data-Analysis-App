import pandas as pd
# retail sales dataset
retail_sales_df = pd.read_csv('/Users/jonas/retail_sales.csv', sep=',')
retail_sales_df['Date'] = pd.to_datetime(retail_sales_df['Date'], format='%Y-%m-%d')

# Monthly sales for each store
store_sales_df = retail_sales_df.groupby(['Store', 'Month']).agg({'Weekly_Sales': 'sum'}).reset_index()
store_sales_df.columns = ['Store', 'Month', 'Monthly_Sales']
store_sales_df = store_sales_df.round(1)

# Holiday Sales
holiday_sales_df = retail_sales_df[retail_sales_df['IsHoliday'] == True].groupby(['Store', 'Month']).agg({'Weekly_Sales': 'sum'}).reset_index()
holiday_sales_df.columns = ['Store', 'Month', 'Holiday_Sales_Monthly']
holiday_sales_df = holiday_sales_df.round(1)

# Merge
Monthly_sales_df = pd.merge(store_sales_df, holiday_sales_df, on=['Store', 'Month'], how='left')
Monthly_sales_df = Monthly_sales_df.fillna(0)
Monthly_sales_df = Monthly_sales_df.round(1)

# Weekly sales for each store
weekly_sales_df = retail_sales_df.groupby(['Store', 'Month', 'Date']).agg({'Weekly_Sales': 'sum'}).reset_index()
weekly_sales_df['week_no'] = weekly_sales_df.groupby(['Store', 'Month'])['Date'].rank(method='min')
weekly_sales_df = weekly_sales_df.round(1)

# Department level sales
dept_df = retail_sales_df.groupby(['Store', 'Month', 'Dept']).agg({'Weekly_Sales': 'sum'}).reset_index()
dept_df['Dept'] = dept_df['Dept'].apply(lambda x: 'Dept' + " " + str(x))
dept_df = dept_df.round(1)
