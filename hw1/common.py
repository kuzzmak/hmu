from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class POSITION(Enum):
    GK = 'GK'
    DEF = 'DEF'
    MID = 'MID'
    FW = 'FW'


MAX_BY_POSITION = {
    POSITION.GK: 2,
    POSITION.DEF: 5,
    POSITION.MID: 5,
    POSITION.FW: 3,
}


@dataclass
class Player:
    id: int
    position: POSITION
    name: str
    club: str
    points: int
    price: float

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Solution:

    def __init__(self, players: List[Player]) -> None:
        self._players = players
        self._points = sum([player.points for player in self.players])
        self._price = sum([player.price for player in self.players])
        self._players_in_club = dict()
        for p in players:
            try:
                self._players_in_club[p.club] += 1
            except KeyError:
                self._players_in_club[p.club] = 1

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def points(self) -> int:
        return self._points

    @property
    def price(self) -> float:
        return self._price

    @property
    def players_in_club(self) -> Dict[str, int]:
        return self._players_in_club

    def players_by_position(self, position: POSITION) -> List[Player]:
        return [p for p in self.players if p.position == position]

    def _max_by_position_ok(self) -> bool:
        ok = True
        for pos in POSITION:
            num_of_players_on_pos = len(
                [player for player in self.players if player.position == pos]
            )
            ok = ok and MAX_BY_POSITION[pos] == num_of_players_on_pos
        return ok

    def _num_of_players_in_same_club_ok(self) -> bool:
        return max(self._players_in_club.values()) <= 3

    def valid(self) -> bool:
        num_of_players_ok = len(self.players) == 15
        price_below_budget_ok = self.price <= 100
        max_by_position_ok = self._max_by_position_ok()
        num_of_players_in_same_club_ok = self._num_of_players_in_same_club_ok()
        return num_of_players_ok and \
            price_below_budget_ok and \
            max_by_position_ok and \
            num_of_players_in_same_club_ok

    def distribute(self) -> Tuple[List[Player], List[Player]]:
        positions = dict()
        for pos in POSITION:
            positions[pos] = []
        for p in self.players:
            positions[p.position].append(p)
        gks = sorted(positions[POSITION.GK],
                     key=lambda p: p.points, reverse=True)
        # add better goalkeeper
        first_eleven = [gks[0]]
        substitutions = [gks[1]]
        defs = sorted(positions[POSITION.DEF],
                      key=lambda p: p.points, reverse=True)
        # add 3 best defs as required
        first_eleven.extend(defs[:3])
        fws = sorted(positions[POSITION.FW],
                     key=lambda p: p.points, reverse=True)
        # add best forward
        first_eleven.append(fws[0])
        # remaining players
        remaining = [*defs[3:], *fws[1:], *positions[POSITION.MID]]
        remaining = sorted(remaining, key=lambda p: p.points, reverse=True)
        # add remaining 6 players ranked by points
        first_eleven.extend(remaining[:6])
        # remaining players are substitutions
        substitutions.extend(remaining[6:])
        return first_eleven, substitutions

    def save(self):
        first_eleven, substitutions = self.distribute()
        first_eleven = list(map(lambda p: str(p.id), first_eleven))
        first_eleven = ','.join(first_eleven)
        substitutions = list(map(lambda p: str(p.id), substitutions))
        substitutions = ','.join(substitutions)
        with open('solution.txt', 'w') as f:
            f.write(first_eleven)
            f.write('\n')
            f.write(substitutions)


def read_row(row: str) -> Player:
    split = row.strip().split(',')
    id = int(split[0])
    position = POSITION[split[1]]
    name = split[2]
    club = split[3]
    points = int(split[4])
    price = float(split[5])
    return Player(id, position, name, club, points, price)


def read_file(file_path: str) -> List[Player]:
    with open(file_path, 'r') as f:
        rows = f.readlines()
    return [read_row(row) for row in rows]
