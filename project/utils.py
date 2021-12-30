import math

from customer import Customer


def calculate_distance(c1: Customer, c2: Customer) -> int:
    return math.ceil(math.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2))
