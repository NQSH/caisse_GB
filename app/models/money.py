from dataclasses import dataclass


@dataclass
class Money:
    value: float
    quantity: int = 0

    @property
    def total(self):
        return self.value * self.quantity