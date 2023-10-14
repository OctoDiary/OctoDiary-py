#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from pydantic import Field

from octodiary.types.model import Type


class Item(Type):
    count: int | None = None
    title: str | None = None
    price: int | None = None
    consist: list[str] | None = None


class Transaction(Type):
    type: str | None = None
    time: str | None = None
    amount: int | None = None
    items: list[Item] | None = None


class Day(Type):
    date: str | None = None
    expense: int | None = None
    transactions: list[Transaction] | None = None


class DayBalanceInfo(Type):
    balance: int | None = None
    has_next_page: bool | None = Field(None, alias="hasNextPage")
    days: list[Day] | None = None
