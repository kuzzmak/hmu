import random
import time
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from customer import Customer
from route import Route
from solution import Solution
from utils import calculate_distance


def nearest_customers_by_distance(
    curr_x: int,
    curr_y: int,
    customers: np.ndarray,
) -> List[int]:
    nearest = np.sqrt(
        np.sum(
            np.square(
                customers - np.array([curr_x, curr_y])
            ),
            axis=1)
    ).argsort()
    return nearest


def initial_sort(customers: List[Customer], base: Customer) -> List[Customer]:
    funcs = [
        lambda c: c.ready_t,
        lambda c: calculate_distance(c, base),
        lambda c: (calculate_distance(c, base), c.ready_t),
    ]
    reverse = False
    idx = random.choice([0, 1, 2])
    if idx == 1:
        if random.random() < 0.5:
            reverse = True
    return sorted(customers, key=funcs[idx], reverse=reverse)


def make_route(
    base: Customer,
    customers: List[Customer],
    capacity: int,
) -> Route:
    route = Route(base, capacity)
    customers = initial_sort(customers, base)
    current_c = customers[0]
    if route.can_add_customer(current_c):
        route.add_customer(current_c)
    customers.remove(current_c)
    if len(customers) == 0:
        return route
    coords = np.array([[c.x, c.y] for c in customers])
    nearest = nearest_customers_by_distance(
        current_c.x,
        current_c.y,
        coords,
    )
    n = 10
    while True:
        nearest_n = nearest[:n]
        found = False
        for idx in nearest_n:
            next_c = customers[idx]
            if route.can_add_customer(next_c):
                route.add_customer(next_c)
                found = True
                break
        if found:
            customers.remove(next_c)
            if len(customers) == 0:
                break
            coords = np.array([[c.x, c.y] for c in customers])
            nearest = nearest_customers_by_distance(
                current_c.x,
                current_c.y,
                coords,
            )
        else:
            break
    return route


def draw_route(route: Route) -> None:
    x_r = list(map(lambda r: r.x, route.customers))
    y_r = list(map(lambda r: r.y, route.customers))
    plt.plot(x_r, y_r, 'r-')


def draw_customers(customers: List[Customer]) -> None:
    x_c = list(map(lambda c: c.x, customers))
    y_c = list(map(lambda c: c.y, customers))
    plt.plot(x_c, y_c, 'bo')


def draw_base(base: Customer) -> None:
    plt.plot(base.x, base.y, 'ro')


def greedy(veh_num: int, capacity: int, customers: List[Customer]) -> Solution:
    base = customers[0]
    customers = customers[1:]
    solution = Solution()
    while len(customers) > 0:
        route = make_route(base, customers, capacity)
        route.add_customer(base)
        for c in route.customers:
            if c.no == base.no:
                continue
            customers.remove(c)
        solution.add_route(route)
    return solution


def read_instance(instance_path: str) -> Tuple[int, int, List[Customer]]:
    with open(instance_path, 'r') as f:
        rows = f.readlines()
    rows = [row.strip() for row in rows]
    split = rows[2].split()
    veh_num, capacity = tuple(map(int, split))
    rows = [row for row in rows[7:] if len(row) > 0]
    int_rows = [list(map(int, row.split())) for row in rows]
    customers = [Customer(*row) for row in int_rows]
    return veh_num, capacity, customers


def merge_routes(r1: Route, r2: Route) -> List[Route]:
    tries = 0
    while True:
        if tries >= 100:
            return [r1, r2]
        base = r1.customers[0]
        customers = [*r1.customers[1:-1], *r2.customers[1:-1]]
        new_routes = []
        r1_new = make_route(base, customers, r1._capacity)
        r1_new.add_customer(base)
        new_routes.append(r1_new)
        for c in r1_new.customers:
            if c.no == base.no:
                continue
            customers.remove(c)
        if len(customers) == 0:
            return new_routes
        r2_new = make_route(base, customers, r1._capacity)
        r2_new.add_customer(base)
        new_routes.append(r2_new)
        if len(r1.customers) + len(r2.customers) == len(r1_new.customers) + len(r2_new.customers):
            break
        else:
            tries += 1
    return new_routes


def random_merge_two_routes(solution: Solution) -> Solution:
    routes = [*solution.routes]
    r1 = random.choice(routes)
    r2 = random.choice(routes)
    while r1 == r2:
        r2 = random.choice(routes)
    routes.remove(r1)
    routes.remove(r2)
    new_routes = merge_routes(r1, r2)
    routes = [*new_routes, *routes]
    s = Solution()
    [s.add_route(r) for r in routes]
    return s


def random_swap_two_customers(solution: Solution, capacity: int) -> Solution:
    base = solution.routes[0].customers[0]
    ok = True
    new_solution = Solution()
    while True:
        r1 = random.choice(solution.routes)
        r2 = random.choice(solution.routes)
        while r1 == r2:
            r2 = random.choice(solution.routes)
        # remove bases from the begining and the end of the route
        cs_1 = r1.customers[1:-1]
        cs_2 = r2.customers[1:-1]
        # select two random customers which will be swapped
        if len(cs_1) == 1:
            rnd_idx_1 = 0
        else:
            rnd_idx_1 = random.randint(1, len(cs_1) - 1)
        if len(cs_2) == 1:
            rnd_idx_2 = 0
        else:
            rnd_idx_2 = random.randint(1, len(cs_2) - 1)
        r_c_1 = cs_1[rnd_idx_1]
        r_c_2 = cs_2[rnd_idx_2]
        cs_1.remove(r_c_1)
        cs_2.remove(r_c_2)
        cs_1.append(r_c_2)
        cs_2.append(r_c_1)
        new_r_1 = make_route(base, cs_1, capacity)
        new_r_1.add_customer(base)
        new_r_2 = make_route(base, cs_2, capacity)
        new_r_2.add_customer(base)
        ok = len(r1.customers) + len(r2.customers) == \
            len(new_r_1.customers) + len(new_r_2.customers)
        if ok:
            routes = [*solution.routes]
            routes.remove(r1)
            routes.remove(r2)
            routes.append(new_r_1)
            routes.append(new_r_2)
            solution = Solution()
            [new_solution.add_route(r) for r in routes]
            break
    return new_solution


def make_population(
    population_size: int,
    veh_num: int,
    capacity: int,
    customers: List[Customer],
) -> List[Solution]:
    pop = [greedy(veh_num, capacity, customers)
           for _ in range(population_size)]
    return pop


def run(instance_path: str, population_size: int, seconds: int) -> Solution:
    veh_num, capacity, customers = read_instance(instance_path)
    population = make_population(population_size, veh_num, capacity, customers)
    population = sorted(population, key=lambda s: (s.vehicles, s.length))
    best = population[0]
    t = time.time()
    time_string = '{:>3}/{} seconds elapsed - '
    while time.time() - t < seconds:
        new_pop = [*population[:population_size // 2]]
        while len(new_pop) < population_size and time.time() - t < seconds:
            rnd_sol = random.choice(new_pop)
            s1 = random_swap_two_customers(rnd_sol, capacity)
            s2 = random_merge_two_routes(rnd_sol)
            s3 = random_merge_two_routes(s2)
            new_s = sorted(
                [s1, s2, s3],
                key=lambda s: (s.vehicles, s.length),
            )
            best_new_s = new_s[0]
            if best_new_s.better_than(rnd_sol):
                new_pop.append(best_new_s)
                if best_new_s.better_than(best):
                    best = best_new_s
                    print(
                        time_string.format(round(time.time() - t), seconds),
                        f'new best - routes: {best.vehicles}, length: {best.length}',
                    )
        print(time_string.format(round(time.time() - t), seconds))
        population = sorted(new_pop, key=lambda s: (s.vehicles, s.length))
    return best


if __name__ == '__main__':
    for i in range(6):
        instance = f'i{i+1}'
        instance_path = fr'...\data\{instance}.txt'
        population_size = 10
        for seconds, t in [(60, '1m'), (300, '5m'), (600, 'un')]:
            solution = run(instance_path, population_size, seconds)
            save_string = f'res-{t}-{instance}.txt'
            solution.save(save_string)
