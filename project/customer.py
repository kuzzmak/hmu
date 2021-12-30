from dataclasses import dataclass


@dataclass
class Customer:
    no: int
    x: int
    y: int
    demand: int
    ready_t: int
    due_t: int
    service_t: int

    def copy(self) -> "Customer":
        return Customer(
            self.no,
            self.x,
            self.y,
            self.demand,
            self.ready_t,
            self.due_t,
            self.service_t,
        )
