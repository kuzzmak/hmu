import random
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
    base = r1.customers[0]
    customers = [*r1.customers[1:], *r2.customers[1:]]
    new_routes = []
    r1_new = make_route(base, customers, r1._capacity)
    new_routes.append(r1_new)
    for c in r1_new.customers:
        if c.no == base.no:
            continue
        customers.remove(c)
    if len(customers) == 0:
        return new_routes
    r2_new = make_route(base, customers, r1._capacity)
    new_routes.append(r2_new)
    return new_routes


def random_swap_two_customers(solution: Solution) -> Solution:
    base = solution.routes[0].customers[0]
    ok = True
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
        if len(r1.customers) == len(new_r_1.customers):
            ok = True
        else:
            ok = False
        new_r_2 = make_route(base, cs_2, capacity)
        new_r_2.add_customer(base)
        if len(r2.customers) == len(new_r_2.customers):
            ok = ok & True
        else:
            ok = False
        if ok:
            solution.routes.remove(r1)
            solution.routes.remove(r2)
            solution.add_route(new_r_1)
            solution.add_route(new_r_2)
            break
    return solution


if __name__ == '__main__':
    instance_path = r'C:\Users\tonkec\Documents\hmu\project\data\i1.txt'
    veh_num, capacity, customers = read_instance(instance_path)
    solution = greedy(veh_num, capacity, customers)
    # print(solution)
    # print()
    solution = random_swap_two_customers(solution)
    # print(solution)
    solution.save()

    # r1 = random.choice(solution.routes)
    # r2 = random.choice(solution.routes)
    # while r1 == r2:
    #     r2 = random.choice(solution.routes)
    # cs_1 = r1.customers[1:-1]
    # cs_2 = r2.customers[1:-1]
    # # print(cs_1)
    # rnd_idx_1 = random.randint(1, len(cs_1) - 1)
    # rnd_idx_2 = random.randint(1, len(cs_2) - 1)
    # r_c_1 = cs_1[rnd_idx_1]
    # r_c_2 = cs_2[rnd_idx_2]

    # cs_1.remove(r_c_1)
    # cs_2.remove(r_c_2)
    # cs_1.append(r_c_2)
    # cs_2.append(r_c_1)

    # new_r_1 = make_route(customers[0], cs_1, capacity)
    # new_r_2 = make_route(customers[0], cs_2, capacity)

    # print('sel 1', r_c_1)
    # print('sel 2', r_c_2)
    # print()
    # print('old 1', r1)
    # print('new 1', new_r_1)
    # print()
    # print('old 2', r2)
    # print('new 2', new_r_2)

    # solution.save()
    # r1 = random.choice(solution.routes)
    # r2 = random.choice(solution.routes)
    # while r1 == r2:
    #     r2 = random.choice(solution.routes)
    # new_routes = merge_routes(r1, r2)
    # r3 = make_route(customers[0], [*r1.customers[1:],
    #                 *r2.customers[1:]], capacity)
    # print(r1)
    # print(r2)
    # for r in new_routes:
    #     print(r)

    # draw_customers(customers[1:])
    # draw_base(customers[0])

    # r1 = solution.routes[0]
    # r2 = solution.routes[1]
    # draw_route(r1)
    # draw_route(r2)
    # plt.show()

    # by_dist = sorted(customers[1:], key=lambda c: calculate_distance(c, customers[0]))
    # print(by_dist[0])
    # a = list(map(lambda c: c.ready_t, customers))
    # bins = 10
    # hist = np.histogram(a, bins)
    # std_dev = np.std(hist[0])
    # print(std_dev)
    # print(hist)

    # print(solution)
    # draw_customers(customers[1:])
    # draw_base(customers[0])
    # for r in routes:
    #     draw_route(r)
    # plt.show()
    # # base
    # c1 = Customer(0, 0, 0, 1, 0, 999, 0)
    # # (0, 1)
    # c2 = Customer(0, 1, 0, 1, 0, 999, 2)
    # # (1, 2)
    # c3 = Customer(0, 1, 2, 1, 0, 999, 3)
    # # (2, 0)
    # c4 = Customer(0, 0, 2, 1, 0, 999, 4)

    # r = Route(c1, 999)
    # r.add_customer(c2)
    # r.add_customer(c3)
    # r.add_customer(c4)
    # print(r._times)
    # print(r.length)
