import random
import copy

class LocalSearchBase:
    def __init__(self, world):
        self.world = world


    def evaluate(self, state):

        """
        TODO: Implement the evaluation (Cost) function.
        Design a function that calculates the cost of the current sensor placement.
        Refer to the project documentation for the primary objectives and constraints.
        
        Returns:    
            cost (int or float): The evaluated cost of the state (lower is better).
        """

        targets = self.world.get_targets()
        sensor_range = self.world.sensor_range
        covered = 0

        for target in targets:
            x, y = target

            for sensor in state:
                xs, ys = sensor
                d = abs(ys - y) + abs(xs - x)

                if d <= sensor_range:
                    covered += 1
                    break

        not_covered_cost = (len(targets) - covered) * 100              
        sensor_cost = len(state)

        cost = not_covered_cost + sensor_cost

        return cost
        # raise NotImplementedError("Students must implement this method.")
    

    def random_position(self, used):

        for i in range(100):
            x = random.randrange(self.world.rows)
            y = random.randrange(self.world.cols)

            if self.world.is_valid_position(x, y) and (x, y) not in used:
                return (x, y)

        return False

    def get_neighbor(self, state):

        state = copy.copy(state)
        
        """
        TODO: Implement the neighbor generation function.
        
        Generate a new valid state by applying a local change to the current state.
        Ensure you include all the required operations mentioned in the project PDF
        to support a dynamic search space.
        
        Returns:
            neighbor_state (list of tuples): The newly generated valid state.
        """

        allowed_actions = ['move_sensor']
        if len(state) < self.world.max_sensors:
            allowed_actions.append('add_sensor')
        if len(state) > 1:
            allowed_actions.append('remove_sensor')

        action = random.choice(allowed_actions)

        if action == 'move_sensor':

            changed_index = random.randrange(len(state))
            possibility = random.random()

            if possibility < 0.60:

                x, y = state[changed_index]

                for i in range(20):

                    delta_x = random.randint(-self.world.sensor_range, self.world.sensor_range)
                    delta_y = random.randint(-self.world.sensor_range, self.world.sensor_range)

                    new_x, new_y = x + delta_x, y + delta_y

                    if self.world.is_valid_position(new_x, new_y) and (new_x, new_y) not in state:
                        state[changed_index] = (new_x, new_y)
                        break
                
            else:
                new_position = self.random_position(state)
                if new_position:
                    state[changed_index] = new_position

        elif action == 'add_sensor':

            new_position = self.random_position(state)
            if new_position:
                state.append(new_position)

        else:
            index = random.randrange(len(state))
            state.pop(index)

        return state
        # raise NotImplementedError("Students must implement this method.")

    def initialize_state(self):
        """
        TODO: Generate a valid initial state.
        
        Create a starting configuration of sensors within the grid boundaries,
        respecting the maximum sensor limits and obstacle placements.
        
        Returns:
            initial_state (list of tuples): The starting coordinates of the sensors.
        """

        sensor_count = random.randint(1, self.world.max_sensors)
        state = []

        while len(state) < sensor_count:

            new_position = self.random_position(state) 

            if new_position:    
                state.append(new_position)
            else:
                break

        return state
        # raise NotImplementedError("Students must implement this method.")