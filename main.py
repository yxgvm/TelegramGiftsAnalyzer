import pandas as pd
from tonnelmp import saleHistory
 
# Your authorization data (replace with your actual authorization key)
myAuthData = ""
 
def get_sales_history_df(authData, pages=5, limit=50):
    """
    Gathers sales history from the 'tonnelmp' API and returns it as a pandas DataFrame.
 
    Args:
        authData (str): Your authorization key for the 'tonnelmp' API.
        pages (int): The number of pages of sales history to retrieve. Each page contains 'limit' records.
        limit (int): The maximum number of sales records to retrieve per page (not more than 50).
 
    Returns:
        pd.DataFrame or None: A DataFrame containing the sales history, or None if an error occurs.
    """
    sales_list = []  # Initialize an empty list to store sales records
 
    # Loop through the specified number of pages
    for page in range(1, pages + 1):
        try:
            print(f"Page {page}, records collected: {len(sales_list)}")
 
            # Call the saleHistory function from the tonnelmp library to get sales data
            sales = saleHistory(authData=authData, page=page, limit=limit, type="SALE", gift_name="", model="", backdrop="", sort="latest")
 
            # If no sales are returned for the current page, break the loop
            if not sales:
                print(f"No more data available after page {page-1}")
                break
 
            # Extend the sales_list with the sales data from the current page
            sales_list.extend(sales)
 
        except Exception as e:
            print(f"Error occurred on page {page}: {e}")
            print(f"Continuing with {len(sales_list)} records collected so far...")
            # Don't break immediately - try a few more times in case it's a temporary issue
            if page <= pages - 2:  # If we're not near the end, try to continue
                continue
            else:
                break
 
    if sales_list:
        # Convert the list of sales records into a pandas DataFrame
        df = pd.DataFrame(sales_list)
        print(f"Successfully collected {len(sales_list)} sales records total")
        return df
    else:
        print("No sales data could be collected")
        return None
 
def get_all_price_statistic(df):
    """
    Calculates various price statistics for each unique 'gift_name' in the DataFrame.
 
    Args:
        df (pd.DataFrame): A DataFrame containing sales data, expected to have 'gift_name' and 'price' columns.
 
    Returns:
        pd.DataFrame: A DataFrame with aggregated price statistics (count, median, average, max, min, range).
    """
    # Group the DataFrame by 'gift_name' and apply aggregation functions to the 'price' column
    result = df.groupby('gift_name')['price'].agg([
        ('Sales count', 'count'),  # Count of sales for each gift
        ('Median price', 'median'), # Median price for each gift
        ('Average price', lambda x: x.mean().round(2)), # Average price, rounded to 2 decimal places
        ('Max price', 'max'),      # Maximum price for each gift
        ('Min price', 'min'),      # Minimum price for each gift
        ('Price range', lambda x: x.max() - x.min()) # Price range (max - min) for each gift
    ]).reset_index() # Reset the index to make 'gift_name' a regular column
 
    # Rename the first column from 'gift_name' to 'Name' for clarity in the report
    result.columns = ['Name'] + [col for col in result.columns[1:]]
 
    return result
 
def create_report():
    """
    Creates an Excel report file ('result.xlsx') containing raw sales data and aggregated statistics.
 
    This function orchestrates the data retrieval, processing, and saving to an Excel file.
    """
    print("Starting data collection, please wait...")
 
    # Get the sales history DataFrame, attempting to retrieve up to 50 pages (2500 records by default)
    df_sales = get_sales_history_df(myAuthData, pages=50)
 
    # Check if data was successfully retrieved; if not, print a message and exit
    if df_sales is None or df_sales.empty:
        print("No data available to create the report.")
        return
 
    print(f"Proceeding with {len(df_sales)} sales records to create report...")
 
    # Save the results to an Excel file
    try:
        # Use a pandas ExcelWriter to write multiple sheets to a single Excel file
        with pd.ExcelWriter("result.xlsx", engine="openpyxl") as writer:
            # Write the raw sales data to a sheet named 'Data'
            df_sales.to_excel(writer, sheet_name='Data', index=False)
            print(f"Saved {len(df_sales)} sales records to 'Data' sheet.")
 
            report = get_all_price_statistic(df_sales)
 
            # Write the statistics to a sheet named 'Statistics'
            report.to_excel(writer, sheet_name='Statistics', index=False)
            print(f"Saved statistics for {len(report)} unique gifts to 'Statistics' sheet.")
 
        print("File 'result.xlsx' saved successfully!")
    except Exception as e:
        print("Error during saving:", e)
 
 
if __name__ == "__main__":
    create_report()