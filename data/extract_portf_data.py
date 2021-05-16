import investpy
import datetime
import csv

# Setting global parameters
selected_country = 'United States'
startdate = datetime.date(2021, 1, 1).strftime('%d/%m/%Y')
endate = datetime.date(2021, 4, 30)

# Formatting dates for investpy:
date0 = ( endate - datetime.timedelta(1) ).strftime('%d/%m/%Y') # helper variable
str_endate = endate.strftime('%d/%m/%Y')

# Getting the stocks info:
stocks_info = investpy.stocks.get_stocks(country = selected_country)

# Filtering stocks with error:
#conditions = (~stocks_info.symbol.isin(['CAKFF', 'PDLI']))
#stocks_info = stocks_info[ conditions ].reset_index(drop=True)

for i in range(len(stocks_info)):
    try:
        name = stocks_info.name.loc[i]
        stocksym = stocks_info.symbol.loc[i]

        dfprices = investpy.get_stock_historical_data(stock = stocksym,
                                            country = selected_country,
                                            from_date = date0,
                                            to_date = str_endate)
        
        dfprices.reset_index(inplace=True)

        closingprice = dfprices.Close.loc[1]
        day = dfprices.Date.loc[1]
        

        with open(f"data/extracted_prices_at_{endate.strftime('%d%m%Y')}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            if i == 0:
                writer.writerow(['name', 'symbol', 'Date', 'closingprice'])
            else:
                writer.writerow([name, stocksym, day, closingprice])
        
        print(i, name, stocksym, day, closingprice)

    except:
        pass

#stocknames = [ [stocks_info.name.loc[i], stocks_info.symbol.loc[i]] for i in range(len(stocks_info))]
"""
prices = []
i = 0

for _ , stocksym in stocknames:
    try:
        dfprices = investpy.get_stock_historical_data(stock = stocksym,
                                            country = selected_country,
                                            from_date = date0,
                                            to_date = endate)
    except:
        pass
    
    print(i, _, stocksym)
    i += 1
    prices.append(dfprices.Close.loc[endate])

print(prices)
"""