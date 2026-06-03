from search.local_search_base import LocalSearchBase


class HillClimbing(LocalSearchBase):
    def run(self, initial_state):
        max_iters = 300
        num_neighbors = 25
        max_side = 12

        evals = []
        history = []

        currentstate = list(initial_state)
        currentcost = self.evaluate(currentstate)
        sidemoves = 0

        for i in range(max_iters):
            evals.append(currentcost)
            history.append(list(currentstate))

            neighbors = []

            for j in range(num_neighbors):
                neighbors.append(self.get_neighbor(currentstate))

            bestN = neighbors[0]
            bestNcost = self.evaluate(bestN)

            for k in range(1, len(neighbors)):
                cost = self.evaluate(neighbors[k])

                if cost < bestNcost:
                    bestN = neighbors[k]
                    bestNcost = cost

            if bestNcost < currentcost:
                currentstate = bestN
                currentcost = bestNcost
                sidemoves = 0

            elif bestNcost == currentcost and sidemoves < max_side:
                currentstate = bestN
                currentcost = bestNcost
                sidemoves += 1

            else:
                break

        return currentstate, currentcost, evals, history
