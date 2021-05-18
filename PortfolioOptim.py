import investpy
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import warnings

from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from charles.selection import fps, tournament, rank
from charles.mutation import swap_mutation, inversion_mutation
from charles.crossover import single_point_co, cycle_co, pmx_co
from data.portf_data import stocks_index, stocks_symbols, stock_prices, budget
from random import choice, random
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

        # Predicted profit on "days_in_the_future"
        pred = round(yhat[days::].sum(),2)

        # ----- Getting the price for investment: -----
        # Price position
        index_symbol = stocks_symbols.index(stock_symbol)

        # Value of stock NOW
        value0 = stock_prices[index_symbol]

        # Value of stock THEN
        value1 = value0 + pred

        #if pred < 0:
            #price = price * -1
        
        return value0, value1
    
    # Copy of the selected stocks:
    portfolio = self.representation
    portfolio_value_now = 0
    portfolio_value_then = 0

    for i in portfolio:

        # Select stock symbol
        current_stock_symbol = stocks_symbols[i]
        #print(current_stock_symbol)

        # Add the performance of each stock
        valuenow, valuethen = stock_performance(current_stock_symbol)
        portfolio_value_now += valuenow
        portfolio_value_then += valuethen

    # Limiting for the budget, 
    if portfolio_value_now > budget:
        # but only when the predicted value of the portfolio is worse than 0 to better evolve
        if portfolio_value_then > 0:
            portfolio_value_then = -1 * portfolio_value_then
        
        #print(portfolio_performance)
    
    return round(portfolio_value_then,2)


def get_neighbours(self):
    """

    """
    portf = []
    #n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]
    for stock in self.representation:
        portf.append([stock] + [choice(self.valid_set) for i in range(len(self.representation)-1)])

    portf = [Individual(i) for i in portf]
    return portf


# Monkey Patching
Individual.evaluate = evaluate
Individual.get_neighbours = get_neighbours

# Variable for population size:
popsize = 10

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=5, 
    valid_set=[i for i in stocks_index],
    replacement=False
)

for i in range(popsize):
    print(pop[i].representation,pop[i])

pop.evolve(
    gens = 10, 
    select = fps,
    crossover = single_point_co,
    mutate = swap_mutation,
    co_p=0.7,
    mu_p=0.2,
    elitism=False
)

"""
# Slow evolving, no bugs.
pop.evolve(
    gens = 10, 
    select = fps,
    crossover = single_point_co,
    mutate = inversion_mutation, #swap_mutation
    co_p=0.7,
    mu_p=0.2,
    elitism=False
)
"""
