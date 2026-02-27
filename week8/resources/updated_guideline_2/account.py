from __future__ import annotations
import time
from dataclasses import dataclass

@dataclass
class Account:
    _balance: int = 0

    @property
    def balance(self) -> int:
        return self._balance

    def deposit(self, amount: int) -> None:
        current = self._balance
        time.sleep(0.0001)
        self._balance = current + amount
