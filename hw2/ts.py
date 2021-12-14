import random
from typing import List

import matplotlib.pyplot as plt

from common import read_file, Player, POSITION, Solution, random_solution
from greedy import greedy
from local_search import local_search
from validator import Validator



class TS:

    def __init__(self, players: List[Player], budget: float, tabu_tenure: int):
        self._players = players
        self._budget = budget
        self._n_neighbors = 15
        self._tabu_tenure = tabu_tenure
        self._tabu = [0] * self._n_neighbors
        self._players_by_position = {
            POSITION.MID: [p for p in players if p.position == POSITION.MID],
            POSITION.FW: [p for p in players if p.position == POSITION.FW],
            POSITION.DEF: [p for p in players if p.position == POSITION.DEF],
            POSITION.GK: [p for p in players if p.position == POSITION.GK]
        }

    def _get_neighbors(self, solution: Solution) -> List[Solution]:
        """Construct neighborhood around current solution. Neighborhood in
        this problem is the current solution with replaced one player. This
        player is chosen randomly from the list of all players which play some
        particular position. If anything goes wrong when selecting one player
        like same player is selected, or this player is the 4th from same
        club, another random selection is made until solution satisfies.

        Parameters
        ----------
        solution : Solution
            current solution for which neighborhood is constructed

        Returns
        -------
        List[Solution]
            list of 15 neighborhood solutions, one for every player swapped
        """
        neighbors = []
        solution_players = solution.players
        for i in range(self._n_neighbors):
            pos = solution_players[i].position
            while True:
                random_player_on_pos = random.choice(
                    self._players_by_position[pos]
                )
                new_players = [
                    *solution.players[:i],
                    random_player_on_pos,
                    *solution.players[i + 1:],
                ]
                new_solution = Solution(new_players)
                if new_solution.valid():
                    neighbors.append(new_solution)
                    break
        return neighbors

    def _decrement_tabu(self) -> None:
        """Reduces values in tabu list on every iteration.
        """
        for i in range(len(self._tabu)):
            if self._tabu[i] > 0:
                self._tabu[i] -= 1

    def run(self, initial_solution: Solution) -> Solution:
        current_solution = initial_solution
        best_solution = initial_solution
        for _ in range(self._n_neighbors + 1):
            self._decrement_tabu()
            neighbors = self._get_neighbors(current_solution)
            indices_sorted = [
                i[0] for i in sorted(enumerate(neighbors), key=lambda x: x[1].points, reverse=True)
            ]
            for index in indices_sorted:
                # tabu neighbor, skip, move to other best neighbor
                if self._tabu[index] > 0:
                    continue
                current_solution = neighbors[index]
                # best solution yet, replace current
                if current_solution.points >= best_solution.points:
                    best_solution = current_solution
                self._tabu[index] = self._tabu_tenure
                break

        return best_solution


if __name__ == '__main__':
    instance = 'instance1'
    budget = 100
    instance_path = fr'C:\Users\tonkec\Documents\hmu\hw2\data\{instance}.txt'
    players = read_file(instance_path)

    for i in range(9):

        initial_solution = random_solution(players)
        # initial_solution = greedy(players, budget)
        # while not initial_solution.valid():
        #     initial_solution = greedy(players, budget)

        ts = TS(players, budget, 3)
        solution = ts.run(initial_solution)
        solution.save('ts.txt')
        solution = local_search(players, budget, 20, initial_solution)
        solution.save('ls.txt')

        print('exp ', str(i))
        price, points = Validator(instance_path, 'ts.txt').validate()
        print('ts points: ', points)
        price, points = Validator(instance_path, 'ls.txt').validate()
        print('ls points: ', points)
        print()

    # num_of_runs = 100
    # for instance in ['instance1', 'instance2']:
    #     instance_path = fr'C:\Users\tonkec\Documents\hmu\hw2\data\{instance}.txt'
    #     players = read_file(instance_path)
    #     for tenure in [3, 5, 7]:
    #         for rand in [True, False]:
    #             ts = TS(players, budget, tenure, rand)
    #             best = 0
    #             best_solution = None
    #             x = []
    #             y = []
    #             for i in range(num_of_runs):
    #                 if rand:
    #                     initial_solution = random_solution(players)
    #                 else:
    #                     initial_solution = greedy(players, budget)
    #                     while not initial_solution.valid():
    #                         initial_solution = greedy(players, budget)
    #                 solution = ts.run(initial_solution)
    #                 solution.save('ts.txt')
    #                 price, points = Validator(
    #                     instance_path,
    #                     'ts.txt',
    #                 ).validate()
    #                 x.append(i)
    #                 y.append(points)
    #                 if points >= best:
    #                     best = points
    #                     best_solution = solution

    #             solution_type = 'random_initial' if rand else 'greedy'
    #             save_string = f'{instance}_ts_{solution_type}_{best}_tabu_tenure_{tenure}'
    #             best_solution.save(save_string + '.txt')

    #             plt.plot(x, y, 'xr')
    #             plt.savefig(save_string + '.png')
    #             plt.clf()
