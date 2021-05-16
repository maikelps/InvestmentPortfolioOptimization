import pandas as pd

df = pd.read_csv('data/extracted_prices_at_30042021.csv', encoding ='latin1')

stocks_index = list(range(len(df)))

stocks_symbols = [ df.symbol.loc[i] for i in range(len(df))]

stock_prices = [round(df.closingprice.loc[i],2) for i in range(len(df))]

budget = 1000