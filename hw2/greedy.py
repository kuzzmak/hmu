import random
import sys
from typing import List

from common import Player, POSITION, Solution, MAX_BY_POSITION, read_file


def greedy(players: List[Player], budget: float) -> Solution:
    by_points = players
    random.shuffle(by_points)
    total_price = 0
    total_points = 0
    selected_players = []
    all_prices = list(map(lambda player: player.price, players))
    median_price = sum(all_prices) / len(all_prices)
    all_points = list(map(lambda player: player.points, players))
    median_points = sum(all_points) / len(all_points)
    # how many players currently are on some position
    occupied_positions = dict()
    players_of_same_club = dict()
    for pos in POSITION:
        occupied_positions[pos] = 0
    for player in by_points:
        # 1. condition: total value of team must be below budget
        if total_price + player.price <= budget:
            # 2. condition: number of players on this position must be less than
            # max number of players for this position
            if occupied_positions[player.position] < MAX_BY_POSITION[player.position]:
                try:
                    num_of_same_club_players = players_of_same_club[player.club]
                    if num_of_same_club_players > 2:
                        continue
                except KeyError:
                    players_of_same_club[player.club] = 0

                if player.price > median_price:
                    if player.points > median_points:
                        selected_players.append(player)
                        total_points += player.points
                        total_price += player.price
                        occupied_positions[player.position] += 1
                        players_of_same_club[player.club] += 1
    solution = Solution(selected_players)
    return solution


if __name__ == '__main__':
    file_path = sys.argv[1]
    players = read_file(file_path)
    budget = 100
    population_size = 10
    solution = greedy(players, budget)
    solution.save()
