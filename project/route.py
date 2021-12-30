from typing import List

from customer import Customer
from utils import calculate_distance


class Route:

    def __init__(self, base: Customer, capacity: int):
        self._base = base
        self._capacity = capacity
        self._customers = [self._base]
        self._length = 0
        self._demand = 0
        self._time = 0

    @property
    def customers(self) -> List[Customer]:
        return self._customers

    @property
    def time(self) -> int:
        return self._time

    def can_add_customer(self, customer: Customer):
        dist = calculate_distance(self._customers[-1], customer)
        new_time = self._time + dist
        time_constraint_customer = new_time <= customer.due_t
        dist = calculate_distance(self._base, customer)
        time_constraint_base = new_time + dist <= self._base.due_t
        demand_constraint = self._demand + customer.demand <= self._capacity
        return time_constraint_customer and \
            time_constraint_base and \
            demand_constraint

    def add_customer(self, customer: Customer) -> None:
        dist = calculate_distance(self._customers[-1], customer)
        self._time = self._time + dist + customer.service_t
        self._demand += customer.demand
        self._customers.append(customer)

    def __str__(self) -> str:
        s = ''
        for i, c in enumerate(self.customers):
            s += str(c.no)
            if i < len(self.customers) - 1:
                s += '->'
        return s