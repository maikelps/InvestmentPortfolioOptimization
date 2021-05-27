from statsmodels.tsa.arima.model import ARIMA
import warnings

from data.portf_data import stocks_symbols, stock_prices
import investpy
import csv

# Warnings for Arima
warnings.filterwarnings("ignore")

"""
This script extracts the predicted price of each stock 15 days in the future using MA15
"""


# Function to predict the value of a stock using its daily changes
def stock_performance(stock_symbol, days = 15):
        # Getting historical for the stock (USA)
        df = investpy.get_stock_historical_data(stock = stock_symbol,
                                            country = 'United States',
                                            from_date = '01/01/2021',
                                            to_date = '30/04/2021')
        
        # NetDiff per day
        df['NetDiff'] = df.Close - df.Open

        # Creating and fitting standard ARIMA model, MA15.
        model = ARIMA(df['NetDiff'], order=(0, 0, 15)).fit()
        # Make prediction
        yhat = model.predict( begin = len(df), end = len(df) + days )

        # For indexing:
        days = -1 * days 

        # Predicted profit on "days_in_the_future" = 15
        pred = round(yhat[days::].sum(),2)

        # ----- Getting the price for investment: -----
        # Price position
        index_symbol = stocks_symbols.index(stock_symbol)

        # Value of stock NOW
        value0 = stock_prices[index_symbol]

        # Value of stock THEN
        value1 = value0 + pred
        
        return value0, round(value1,2)

for i, stock in enumerate(stocks_symbols):
    """
    Saving the results using the function above
    """
    value0, value1 = stock_performance(stock)

    with open(f"data/performance_now_and_in_15.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            if i == 0:
                writer.writerow(['symbol', 'PerformanceBefore', 'PerformancePredicted'])
                writer.writerow([stock, value0, value1])
            else:
                writer.writerow([stock, value0, value1])
        
    print(i, stock, value0, value1)