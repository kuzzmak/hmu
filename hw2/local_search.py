import random
import sys
from typing import List

from common import Player, POSITION, Solution, read_file
from greedy import greedy


def local_search(players: List[Player], budget: float, population_size: int) -> Solution:
    solution = greedy(players, budget)
    while not solution.valid():
        solution = greedy(players, budget)

    # loop that runs so long as the best in current population has more points
    # than the solution from previous iteration
    while True:
        budget_left = budget - solution.price
        players_set = set(players)
        solution_set = set(solution.players)
        # available players that are not in a team
        left_players = players_set.difference(solution_set)
        # list of solutions for the next iteration
        population: List[Solution] = []
        for _ in range(population_size):
            # select some position where one player would be swapped
            random_position = random.choice([*POSITION])
            # players that are not in a team but play selected position on
            # which player swap should be made
            left_players_on_position = [
                p for p in left_players if p.position == random_position
            ]
            players_on_position = solution.players_by_position(random_position)
            # select one player in current solution to be replaced with new one
            player_to_replace = random.choice(players_on_position)
            # new player which will replace some current player
            random_left_player_on_position = random.choice(
                left_players_on_position)
            try:
                # if selected random player violates allowed 3 player from the
                # same club, take a new random player
                while solution.players_in_club[random_left_player_on_position.club] > 2:
                    random_left_player_on_position = random.choice(
                        left_players_on_position
                    )
            except KeyError:
                # player with this club is not present in current solution so it's
                # ok to add him to the current solution
                ...
            # price of the new player combined with budget that is available must be
            # less than price of a randomly selected player in current solution
            if player_to_replace.price + budget_left >= random_left_player_on_position.price:
                players_on_position.remove(player_to_replace)
                players_on_position.append(random_left_player_on_position)

            solution_players = []
            for pos in POSITION:
                # add players from solution on positions which weren't changed
                if pos != random_position:
                    solution_players.extend(solution.players_by_position(pos))
            solution_players.extend(players_on_position)
            new_solution = Solution(solution_players)
            population.append(new_solution)

        population = sorted(population, key=lambda p: p.points, reverse=True)
        best = population[0]
        if best.points >= solution.points:
            solution = best
        else:
            break

    return solution


if __name__ == '__main__':
    file_path = sys.argv[1]
    players = read_file(file_path)
    budget = 100
    population_size = 10
    solution = local_search(players, budget, population_size)
    solution.save()
