import math
import random
from search.local_search_base import LocalSearchBase

class SimulatedAnnealing(LocalSearchBase):
    def run(self, start_state):
        start_temp = 120.0
        min_temp = 0.05
        cooling_rate = 0.98
        max_loops = 4000

        working_state = list(start_state)
        working_cost = self.evaluate(working_state)
        the_best_state = list(working_state)
        the_best_cost = working_cost
        all_evals = []
        all_states = []

        temp = start_temp
        
        for step in range(max_loops):
            all_evals.append(working_cost)
            all_states.append(list(working_state))
            if temp < min_temp:
                break
            next_guess = self.get_neighbor(working_state)
            next_cost = self.evaluate(next_guess)
            difference = next_cost - working_cost
            accept_move = False
            
            if difference < 0:
                accept_move = True
            else:
                prob = math.exp(-difference / temp)
                rand_chance = random.random()
                if rand_chance < prob:
                    accept_move = True

            if accept_move == True:
                working_state = next_guess
                working_cost = next_cost
                if working_cost < the_best_cost:
                    the_best_cost = working_cost
                    the_best_state = list(working_state)

            temp = temp * cooling_rate

        return the_best_state, the_best_cost, all_evals, all_states
