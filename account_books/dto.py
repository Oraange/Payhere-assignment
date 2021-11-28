from dataclasses import dataclass


@dataclass
class CreateAccoutBookInputDTO:
    type: int
    amount: int
    category: str
    memo: str
    