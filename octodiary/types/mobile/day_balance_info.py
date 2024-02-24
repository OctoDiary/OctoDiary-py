#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from pydantic import Field

from octodiary.types.model import DT, Type


class Item(Type):
    count: Optional[int] = None
    title: Optional[str] = None
    price: Optional[int] = None
    consist: list[str] | None = None


class Transaction(Type):
    type: Optional[str] = None
    time: Optional[str] = None
    amount: Optional[int] = None
    items: list[Item] | None = None


class Day(Type):
    date: Optional[DT] = None
    expense: Optional[int] = None
    transactions: list[Transaction] | None = None


class DayBalanceInfo(Type):
    balance: Optional[int] = None
    has_next_page: Optional[bool] = Field(None, alias="hasNextPage")
    days: list[Day] | None = None
