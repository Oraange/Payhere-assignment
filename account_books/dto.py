from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class CreateAccoutBookInputDTO:
    type: int
    amount: int
    category: str
    memo: str
    

@dataclass
class UpdateAccountBookInputDTO:
    type: int
    amount: int
    category: str
    memo: str


@dataclass
class ReadAccountBookOutputDTO:
    updated_at: datetime
    type: str
    amount: int
    category: str
    memo: str


@dataclass
class ParamsInputDTO:
    offset: int
    limit: int


@dataclass
class DeleteBookIdDTO:
    id: int


@dataclass
class ReadAccountBookListOutputDTO:
    account_books: List[ReadAccountBookOutputDTO]
    total_income: int
    total_outlay: int
    total_count: int
