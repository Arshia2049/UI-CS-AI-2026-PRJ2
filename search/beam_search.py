from search.local_search_base import LocalSearchBase

class BeamSearch(LocalSearchBase):    

    def run(self, initial_state):
        bwidth = 6
        successornum = 12
        max_iters = 120

        beam = [list(initial_state)]
        
        while len(beam) < bwidth:
            beam.append(self.initialize_state())

        beam_costs = []
        for s in beam:
            beam_costs.append(self.evaluate(s))
            
        best_i = 0
        for i in range(1, len(beam)):
            if beam_costs[i] < beam_costs[best_i]:
                best_i = i
                
        best_state = list(beam[best_i])
        best_cost = beam_costs[best_i]
        evals = []
        history = []

        for i in range(max_iters):
            evals.append(best_cost)
            history.append(list(best_state))
            candidates = []
            
            for state in beam:
                neighbors = []
                for j in range(successornum):
                    neighbors.append(self.get_neighbor(state))
                    
                for n in neighbors:
                    cost = self.evaluate(n)
                    candidates.append((cost, n))

            if len(candidates) == 0:
                break

            def get_cost(item):
                return item[0]
            
            candidates.sort(key=get_cost)

            beam = []
            beam_costs = []
            
            num_to_take = bwidth
            if len(candidates) < bwidth:
                num_to_take = len(candidates)

            for j in range(num_to_take):
                c_cost, c_state = candidates[j]
                beam.append(c_state)
                beam_costs.append(c_cost)

            if beam_costs[0] < best_cost:
                best_cost = beam_costs[0]
                best_state = list(beam[0])

        return best_state, best_cost, evals, history
