from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from charles.selection import fps, tournament, rank
from charles.mutation import swap_mutation, inversion_mutation
from charles.crossover import single_point_co, multiple_points_co
from data.portf_data_price_and_prediction import stocks_index, stocks_symbols, stock_before, stock_after, budget
from random import choice

"""
Script to test the configurations for the maximization
"""


def evaluate(self, days_in_the_future = 15):
    """
    A function to calculate the predicted price in days = 15.
    
    Assess if there would be profit or not
    """
    
    # Copy of the selected stocks (portfolio):
    portfolio = self.representation
    portfolio_value_now = 0
    portfolio_value_then = 0

    for i in portfolio:

        # Select stock symbol (for useful for debugging)
        current_stock_symbol = stocks_symbols[i]
        #print(current_stock_symbol)

        # Add the performance of each stock (now and then)
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
#print(pop.individuals[0].representation, pop.individuals[0].fitness)
#print(pop.individuals[1].representation, pop.individuals[1].fitness)
#selected = [1617, 1596, 1617, 1596, 1596, 1617, 1617, 1617, 1617, 1617, 1617, 1596, 41, 1596, 1617, 1596, 1596, 1596, 1617, 1596, 1617, 1596, 1617, 1617, 1617, 1596, 1218, 3657, 1596, 1617, 1617, 1617, 1617, 1596, 1617, 1596, 1617, 1617, 1617, 1617, 1617, 1596, 1617, 1596, 1617, 1596, 1617, 1596, 1596, 1596]
#selected = Individual(selected)
#print(selected.evaluate)

popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens = 700, 
    select = tournament,
    crossover = multiple_points_co,
    mutate = inversion_mutation,
    co_p=0.9,
    mu_p=0.4,
    elitism=True
)


"""
model6
Interesting to look at. Converges between 7% and 9%
popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens = 700, 
    select = tournament,
    crossover = multiple_points_co,
    mutate = inversion_mutation,
    co_p=0.9,
    mu_p=0.4,
    elitism=True
)

---------
model5
Escalates really fast to 9%
popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens = 700, 
    select = rank,
    crossover = multiple_points_co,
    mutate = inversion_mutation,
    co_p=0.9,
    mu_p=0.4,
    elitism=True
)
-------------------
model4
Finds the plateu fast:
# Variable for population size:
popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens = 700, 
    select = tournament,
    crossover = single_point_co,
    mutate = swap_mutation,
    co_p=0.8,
    mu_p=0.4,
    elitism=True
)
------------------------
model3
Great performance. Almost 10%

# Variable for population size:
popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens = 700, 
    select = rank,
    crossover = single_point_co,
    mutate = swap_mutation,
    co_p=0.8,
    mu_p=0.4,
    elitism=True
)
---------------------------
model2
Awesome performance: ~+9%
Continuous grow

popsize = 300

pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)

pop.evolve(
    gens = 700, 
    select = rank,
    crossover = single_point_co,
    mutate = inversion_mutation,
    co_p=0.8,
    mu_p=0.4,
    elitism=True
)
------------------------
model1
Great performance: ~+7%
Some plateus. But it grows well.

popsize = 300
pop = Population(
    size= popsize, 
    optim="max", 
    sol_size=50,
    valid_set=[i for i in stocks_index],
    replacement=False
)
pop.evolve(
    gens = 700, 
    select = fps,
    crossover = single_point_co,
    mutate = inversion_mutation,
    co_p=0.95,
    mu_p=0.2,
    elitism=True
)
"""
