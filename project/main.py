from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import math

from customer import Customer
from route import Route
from utils import calculate_distance


def nearest_customers_by_distance(curr_x: int, curr_y: int, customers: np.ndarray):
    nearest = np.sqrt(
        np.sum(
            np.square(
                customers - np.array([curr_x, curr_y])
            ),
            axis=1)
    ).argsort()
    return nearest


def make_route(
    base: Customer,
    customers: List[Customer],
    capacity: int,
) -> Route:
    route = Route(base, capacity)
    customers = sorted(customers, key=lambda c: c.ready_t)
    current_c = customers[0]
    if route.can_add_customer(current_c):
        route.add_customer(current_c)
    customers.remove(current_c)
    coords = np.array([[c.x, c.y] for c in customers])
    nearest = nearest_customers_by_distance(
        current_c.x,
        current_c.y,
        coords,
    )
    # how many neighbors were searched but they do not satisfy
    # some of the conditions
    searched = 0
    # how many neighbors were searched but their demand would
    # break constraint on total capacity
    cargo_miss = 0
    n = 3
    while True:
        # if searched == len(nearest):
        #     break
        # next_c_idx = nearest[searched]
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
            coords = np.array([[c.x, c.y] for c in customers])
            nearest = nearest_customers_by_distance(
                current_c.x,
                current_c.y,
                coords,
            )
        else:
            break
        # if truck gets there before closing
        # if current_time <= next_c.due_t:
        #     # if truck has any more capacity
        #     if next_c.demand + current_demand <= capacity:
        #         route.append(next_c)
        #         current_c = next_c
        #         customers.remove(next_c)
        #         current_demand += current_c.demand
        #         current_time = max(
        #             current_time + current_c.service_t,
        #             current_c.ready_t - current_time + current_c.service_t,
        #         )
        #         # reset distances because another customer was visited
        #         coords = np.array([[c.x, c.y] for c in customers])
        #         nearest = nearest_customers_by_distance(
        #             current_c.x,
        #             current_c.y,
        #             coords,
        #         )
        #         searched = 0
        #         cargo_miss = 0
        #     else:
        #         cargo_miss += 1
        #         if cargo_miss >= 5:
        #             break
        # else:
        #     searched += 1

    return route


def greedy(veh_num: int, capacity: int, customers: List[Customer]):
    base = customers[0]
    customers = customers[1:]
    all_customers = [c.copy() for c in customers]
    x_c = list(map(lambda c: c.x, all_customers))
    y_c = list(map(lambda c: c.y, all_customers))

    # for c in customers:
    #     print(c)
    # print()
    route1 = make_route(base, customers, capacity)
    for c in route1.customers:
        if c.no == base.no:
            continue
        customers.remove(c)

    print(route1.time)
    print(calculate_distance(route1.customers[-1], base))

    # r_c = route1.customers
    # x_r = list(map(lambda c: c.x, r_c))
    # y_r = list(map(lambda c: c.y, r_c))

    # plt.plot(x_c, y_c, 'bo')
    # plt.plot(base.x, base.y, 'ro')
    # plt.plot(x_r, y_r, 'r-')
    # plt.show()
    # print(route1)
    # print(route1.time)

    # print(len(customers))
    # print(len(route1))

    # for c in customers:
    #     print(c)
    # coords = np.array([[c.x, c.y] for c in customers])
    # nearest = nearest_customers_by_distance(base.x, base.y, coords)
    # nearest = customers[nearest[1]]
    # r_x = list(map(lambda r: r.x, route1))
    # r_y = list(map(lambda r: r.y, route1))
    # x = list(map(lambda c: c.x, customers))
    # y = list(map(lambda c: c.y, customers))
    # plt.plot(x, y, 'bo')
    # plt.plot(base.x, base.y, 'ro')
    # plt.plot(r_x, r_y, 'r-')
    # # plt.show()
    # for c in route1:
    #     customers.remove(c)
    # route2 = make_route(customers, capacity)
    # r_x = list(map(lambda r: r.x, route2))
    # r_y = list(map(lambda r: r.y, route2))
    # plt.plot(r_x, r_y, 'r-')
    # # plt.show()

    # for c in route2:
    #     customers.remove(c)
    # route3 = make_route(customers, capacity)
    # r_x = list(map(lambda r: r.x, route3))
    # r_y = list(map(lambda r: r.y, route3))
    # plt.plot(r_x, r_y, 'r-')
    # plt.show()


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


if __name__ == '__main__':
    instance_path = r'C:\Users\tonkec\Documents\hmu\project\data\i1.txt'
    veh_num, capacity, customers = read_instance(instance_path)
    greedy(veh_num, capacity, customers)
