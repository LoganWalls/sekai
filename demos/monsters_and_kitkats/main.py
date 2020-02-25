from math import copysign
from random import choice, random

from sekai import AsciimaticsEngine, AsciimaticsRenderer, EpisodeTerminated, SekaiObject, State, direction_vectors


class Agent(SekaiObject):

    def __init__(self, energy: int = 3, metabolism: float = 0.1):
        self._energy = energy
        self.metabolism = metabolism
        self.can_swim = False

    @property
    def display(self):
        # display depends on energy level
        return {3: "🙂", 2: "😐", 1: "😣", 0: "😵"}.get(self.energy, "😐")

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value: int):
        self._energy = value
        if self._energy <= 0:
            raise EpisodeTerminated("Agent ran out of energy")

    def tick(self, state: State, x: int, y: int):
        # Decrease energy stochastically rate as time passes
        if random() < self.metabolism:
            self.energy -= 1

        # See if the agent died of hunger
        if self.energy <= 0:
            state.reward -= 100
            state.terminal_state = True

        # Select a direction to move at random.
        step = choice(direction_vectors)
        target = (x + step[0], y + step[1])
        # Move in that direction.
        moved = state.move((x, y), target)
        if moved:
            state.agent_pos = target


class Water(SekaiObject):
    display = "🌊"

    def collide(self, other, state: State, x: int, y: int):
        if isinstance(other, Agent):
            other.energy = 0
            state.reward -= 100
        return other.can_swim


class Forest(SekaiObject):
    display = "🌳"


class KitKat(SekaiObject):
    display = "🍫"

    def __init__(self, deliciousness: int = 100):
        self.deliciousness = deliciousness

    def collide(self, other, state: State, x: int, y: int):
        if isinstance(other, Agent):
            state.reward += self.deliciousness
        return True


class Monster(SekaiObject):
    display = "👹"

    def __init__(self, intelligence: int = 0.5):
        self.intelligence = intelligence
        self.can_swim = False

    def tick(self, state: State, x: int, y: int):
        agent_x, agent_y = state.agent_pos
        chase_x = agent_x - x
        chase_y = agent_y - y

        # Chase the agent
        if random() < self.intelligence:
            if abs(chase_x) > abs(chase_y):
                move = (copysign(1, chase_x), 0)
            else:
                move = (0, copysign(1, chase_y))
        # Take a random step
        else:
            move = choice(direction_vectors)
        state.move((x, y), (x + move[0], y + move[1]))

    def collide(self, other, state: State, x: int, y: int):
        if isinstance(other, Agent):
            other.energy = 0
            state.reward -= 100
        return False


class Field(SekaiObject):
    def collide(self, other, state: State, x: int, y: int):
        return not isinstance(other, Monster)


if __name__ == '__main__':

    # Define a state
    state = State(16, 10, default_tile=Field())
    for x in range(state.n_columns - (state.n_columns // 2), state.n_columns):
        for y in range(0, (state.n_rows // 2)):
            state.tiles[x, y] = Forest()
    for x in range(7, 11):
        for y in range(4, 8):
            state.tiles[x, y] = Water()
    state.objects[15, 9] = KitKat()
    state.objects[13, 1] = Monster()
    state.objects[2, 2] = Agent()
    state.agent_pos = (2, 2)

    engine = AsciimaticsEngine(state, renderer=AsciimaticsRenderer())
    engine.run(wait_time=0.5)
