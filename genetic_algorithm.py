import random
from search.local_search_base import LocalSearchBase

class GeneticAlgorithm(LocalSearchBase):

    def run(self, initial_state):

        size = 40
        best_count = 4
        parent_size = 3
        mutation_possibility = 0.7
        how_many_generations = 150

        population = [list(initial_state)]
        
        while len(population) < size:
            population.append(self.initialize_state())


        evaluations = []
        history = []
        best_state = list(initial_state)
        best_cost = self.evaluate(best_state)
        


        for level in range(how_many_generations):
            
            costs = []
            for p in population:
                costs.append(self.evaluate(p))

            ranked = []
            for i in range(len(population)):
                ranked.append(i)

            def cost_of_index(i):
                return costs[i]
            ranked.sort(key=cost_of_index)

            bestIndex = ranked[0]
            if costs[bestIndex] < best_cost:
                best_cost = costs[bestIndex]
                best_state = list(population[bestIndex])

            evaluations.append(best_cost)
            history.append(list(best_state))

            next = []
            
            for i in range(best_count):
                next.append(list(population[ranked[i]]))

            while len(next) < size:

                parent1 = self.select_parents(population, costs, parent_size)
                parent2 = self.select_parents(population, costs, parent_size)

                child = self.crossover(parent1, parent2)

                random_num = random.random()
                if random_num < mutation_possibility:
                    child = self.get_neighbor(child)

                    if random.random() < 0.5:
                        child = self.get_neighbor(child)
                        
                next.append(child)

            population = next

        return best_state, best_cost, evaluations, history
    


    def select_parents(self, population, costs, k):

        size = k
        if len(population) < k:
            size = len(population)
            
        chosen = random.sample(range(len(population)), size)

        winner = chosen[0]
        for index in chosen:
            if costs[index] < costs[winner]:
                winner = index

        return population[winner]
    


    def crossover(self, p1, p2):

        genes = []

        for gene in p1:
            if gene not in genes:
                genes.append(gene)

        for gene in p2:
            if gene not in genes:
                genes.append(gene)

        if len(genes) == 0:
            allgenes = p1 + p2
            genes = [random.choice(allgenes)]

        if len(genes) > self.world.max_sensors:
            genes = random.sample(genes, self.world.max_sensors)

        return genes