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
from data.portf_data_final import stocks_index, stocks_symbols, stock_before, stock_after, budget
from random import choice, random
from copy import deepcopy

# Warnings for Arima
warnings.filterwarnings("ignore")

def evaluate(self, days_in_the_future = 15):
    """
    A function to calculate the predicted price in days = 15.
    
    Assess if there would be profit or not
    """
    
    # Copy of the selected stocks:
    portfolio = self.representation
    portfolio_value_now = 0
    portfolio_value_then = 0

    for i in portfolio:

        # Select stock symbol
        current_stock_symbol = stocks_symbols[i]
        #print(current_stock_symbol)

        # Add the performance of each stock
        valuenow, valuethen = stock_before[i], stock_after[i]
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
    Getting neighbours.
    Keeping one fixed, making a random choice for the others
    """
    neigh = []
    #n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]
    for stock in self.representation:
        neigh.append([stock] + [choice(self.valid_set) for i in range(len(self.representation)-1)])

    neigh = [Individual(i) for i in neigh]
    return neigh


# Monkey Patching
Individual.evaluate = evaluate
Individual.get_neighbours = get_neighbours

# Variable for population size:
popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=100, 
    valid_set=[i for i in stocks_index],
    replacement=False
)

#for i in range(popsize):
    #print(pop[i].representation,pop[i])

pop.evolve(
    gens = 1000, 
    select = fps,
    crossover = single_point_co,
    mutate = swap_mutation,
    co_p=0.7,
    mu_p=0.2,
    elitism=True
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
