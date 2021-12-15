import math
import random
from typing import List

from common import Player, POSITION, read_file, Solution, random_solution
from greedy import greedy


class SA:

    def __init__(self, players: List[Player], budget: float, initial_temp: float, alpha: float):
        self._players = players
        self._budget = budget
        self._initial_temp = initial_temp
        self._current_temp = initial_temp
        self._alpha = alpha
        self._players_by_position = {
            POSITION.MID: [p for p in players if p.position == POSITION.MID],
            POSITION.FW: [p for p in players if p.position == POSITION.FW],
            POSITION.DEF: [p for p in players if p.position == POSITION.DEF],
            POSITION.GK: [p for p in players if p.position == POSITION.GK]
        }

    def _get_neighbor(self, solution: Solution) -> Solution:
        solution_players = solution.players
        while True:
            idx = random.choice(range(0, len(solution_players)))
            pos = solution_players[idx].position
            new_random_player = random.choice(self._players_by_position[pos])
            new_players = [
                *solution.players[:idx],
                new_random_player,
                *solution.players[idx + 1:],
            ]
            new_solution = Solution(new_players)
            if new_solution.valid():
                return new_solution

    def _update_temp(self) -> None:
        self._current_temp *= self._alpha

    def run(self, initial_solution: Solution) -> Solution:
        best_solution = initial_solution
        current_solution = initial_solution
        non_improving_iterations = 0
        while non_improving_iterations < 100:
            neighbor = self._get_neighbor(current_solution)
            if neighbor.points > current_solution.points:
                current_solution = neighbor
            else:
                rnd_val = random.random()
                prob = math.exp(-(current_solution.points -
                                neighbor.points) / (self._current_temp + 1e-8))
                if rnd_val < prob:
                    current_solution = neighbor
            if current_solution.points > best_solution.points:
                best_solution = current_solution
                non_improving_iterations = 0
            else:
                non_improving_iterations += 1
            self._update_temp()
        return best_solution


if __name__ == '__main__':
    budget = 100
    instance_path = r'...'
    players = read_file(instance_path)
    alpha = 0.9
    initial_temp = 300
    initial_sol_type = 'greedy'
    best_solution = random_solution(players)
    if initial_sol_type == 'random':
        initial_solution = random_solution(players)
    else:
        initial_solution = greedy(players, budget)
        while not initial_solution.valid():
            initial_solution = greedy(players, budget)
    sa = SA(players, budget, initial_temp, alpha)
    solution = sa.run(initial_solution)
    solution.save('sa.txt')
