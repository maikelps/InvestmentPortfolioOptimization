import investpy
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import warnings


from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from charles.selection import fps, tournament, rank
from charles.mutation import swap_mutation
from charles.crossover import cycle_co, pmx_co
from data.portf_data import stocks_index, stocks_symbols, stock_prices, budget
from random import choices, random
from copy import deepcopy

# Warnings for Arima
warnings.filterwarnings("ignore")

def evaluate(self, days_in_the_future = 15):
    """
    A function to calculate the predicted price in days = 15.
    
    Assess if there would be profit or not
    """
    def stock_performance(stock_symbol, days = days_in_the_future):
        # Getting historical for the stock (USA)
        df = investpy.get_stock_historical_data(stock = stock_symbol,
                                            country = 'United States',
                                            from_date = '01/01/2021',
                                            to_date = '30/04/2021')
        
        df['NetDiff'] = df.Close - df.Open

        # Creating and fitting standard ARIMA model, MA15.
        model = ARIMA(df['NetDiff'], order=(0, 0, 15)).fit()
        # Make prediction
        yhat = model.predict( begin = len(df), end = len(df) + days )

        # For indexing:
        days = -1 * days 

        # Predicted profit on "days"
        pred = round(yhat[days::].sum(),2)

        # Returning the prediction of profit in days=15
        return pred
    
    # Copy of the selected stocks:
    portfolio = self.representation
    portfolio_performance = 0

    #while 1 in portfolio:
    for i in portfolio:
        # Get the position of the stock:
        #index = portfolio.index(1)
        index = portfolio.index(i)

        # Select stock symbol
        current_stock_symbol = stocks_symbols[index]


        # Append the performance of each stock
        portfolio_performance += stock_performance(current_stock_symbol)

        #portfolio[index] = 0
    
    return portfolio_performance




def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n


# Monkey Patching
Individual.evaluate = evaluate
Individual.get_neighbours = get_neighbours


pop = Population(
    size=10, 
    optim="min", 
    sol_size=5, 
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens=100, 
    select= rank,
    crossover= cycle_co,
    mutate=swap_mutation,
    co_p=0.7,
    mu_p=0.2,
    elitism=False
)

print(pop)