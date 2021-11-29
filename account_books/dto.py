from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class BookCreateDTO:
    type: int
    amount: int
    category: str
    memo: str


@dataclass
class BookUpdateDTO:
    type: int
    amount: int
    category: str
    memo: str
    

@dataclass
class BookOutputDTO:
    id: int
    updated_at: datetime
    type: str
    amount: int
    category: str
    memo: str


@dataclass
class BookListOutputDTO:
    books: List[BookOutputDTO]
    total_income: int
    total_outlay: int
    total_count: int


@dataclass
class ParamsDTO:
    offset: int
    limit: int


@dataclass
class BookIdDTO:
    id: int


@dataclass
class TreshListOutputDTO:
    books: List[BookOutputDTO]
    total_count: int
