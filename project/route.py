import math
from typing import List

from customer import Customer
from utils import calculate_distance


class Route:

    def __init__(self, base: Customer, capacity: int):
        self._base = base
        self._capacity = capacity
        self._customers = [self._base]
        self._length = 0
        self._real_length = 0
        self._demand = 0
        self._time = 0
        self._times = [self._time]

    @property
    def customers(self) -> List[Customer]:
        return self._customers

    @property
    def time(self) -> int:
        return self._time

    @property
    def length(self) -> int:
        return self._length

    @property
    def real_length(self) -> float:
        return self._real_length

    def can_add_customer(self, customer: Customer):
        dist = math.ceil(calculate_distance(self._customers[-1], customer))
        new_time = self._time + dist
        if new_time < customer.ready_t:
            new_time = customer.ready_t
        time_constraint_customer = new_time <= customer.due_t
        dist = math.ceil(calculate_distance(self._base, customer))
        time_constraint_base = new_time + dist <= self._base.due_t
        demand_constraint = self._demand + customer.demand <= self._capacity
        return time_constraint_customer and \
            time_constraint_base and \
            demand_constraint

    def add_customer(self, customer: Customer) -> None:
        dist = calculate_distance(self._customers[-1], customer)
        self._real_length += dist
        self._length += math.ceil(dist)
        self._time = max(self._time + math.ceil(dist), customer.ready_t) + \
            customer.service_t
        self._times.append(self._time - customer.service_t)
        self._demand += customer.demand
        self._customers.append(customer)

    def __str__(self) -> str:
        s = ''
        for i, c in enumerate(self.customers):
            s += str(c.no) + f'({self._times[i]})'
            if i < len(self.customers) - 1:
                s += '->'
        return s

    def __eq__(self, other: "Route") -> bool:
        if self._length != other._length:
            return False
        if self.time != other._time:
            return False
        for c1, c2 in zip(self.customers, other.customers):
            if c1 != c2:
                return False
        return True
