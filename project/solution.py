from typing import List

from route import Route


class Solution:

    def __init__(self):
        self._routes = []

    @property
    def routes(self) -> List[Route]:
        return self._routes

    @property
    def vehicles(self) -> int:
        return len(self.routes)

    @property
    def length(self) -> float:
        return sum([r.real_length for r in self.routes])

    def better_than(self, other: "Solution") -> bool:
        if self.vehicles < other.vehicles:
            return True
        if self.vehicles == other.vehicles and self.length < other.length:
            return True
        return False

    def add_route(self, route: Route) -> None:
        self._routes.append(route)

    def save(self, path: str = 'solution.txt') -> None:
        with open(path, 'w') as f:
            f.write(str(self))

    def __str__(self) -> str:
        s = str(len(self._routes)) + '\n'
        for i, r in enumerate(self._routes):
            s += f'{i}: {r}\n'
        s += str(sum([r.real_length for r in self._routes]))
        return s
