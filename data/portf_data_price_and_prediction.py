import pandas as pd

df = pd.read_csv('data/performance_now_and_in_15.csv', encoding ='latin1')

stocks_index = list(df.index)

stocks_symbols = [ df.symbol.loc[i] for i in stocks_index]

stock_before = [round(df.PerformanceBefore.loc[i],2) for i in stocks_index]

stock_after = [round(df.PerformancePredicted.loc[i],2) for i in stocks_index]

budget = 100000