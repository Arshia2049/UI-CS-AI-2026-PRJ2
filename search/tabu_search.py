from search.local_search_base import LocalSearchBase

class TabuSearch(LocalSearchBase):
    def run(self, initial_state):
        max_iters = 400
        num_neighbors = 25
        tabu_limit = 300

        curr_state = list(initial_state)
        curr_cost = self.evaluate(curr_state)
        best_state = list(curr_state)
        best_cost = curr_cost
        evals = []
        history = []
        tabu_list = [frozenset(curr_state)]

        for i in range(max_iters):
            evals.append(curr_cost)
            history.append(list(curr_state))

            neighbors = []
            for j in range(num_neighbors):
                neighbors.append(self.get_neighbor(curr_state))

            best_n = None
            best_n_cost = float('inf')
            
            for n in neighbors:
                cost = self.evaluate(n)
                is_tabu = False
                
                if frozenset(n) in tabu_list:
                    is_tabu = True
                if is_tabu == True and cost >= best_cost:
                    continue
                if cost < best_n_cost:
                    best_n = n
                    best_n_cost = cost
                    
            if best_n == None:
                break

            curr_state = best_n
            curr_cost = best_n_cost

            tabu_list.append(frozenset(curr_state))
            
            if len(tabu_list) > tabu_limit:
                tabu_list.pop(0)
            if curr_cost < best_cost:
                best_cost = curr_cost
                best_state = list(curr_state)

        return best_state, best_cost, evals, history