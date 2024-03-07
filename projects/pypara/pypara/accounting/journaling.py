"""
This module provides data definitions and functionality related to journal entries and postings.
"""

__all__ = [
    "Direction",
    "JournalEntry",
    "Posting",
    "ReadJournalEntries",
]

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Generic, Iterable, List, Protocol, Set, TypeVar

from ..commons.guid import Guid, makeguid
from ..commons.numbers import Amount, Quantity, isum
from ..commons.zeitgeist import DateRange
from .accounts import Account, AccountType

#: Defines a type variable.
_T = TypeVar("_T")


class Direction(Enum):
    """
    Provides an enumeration for indicating increment and decrement events.
    """

    #: Declares the value type.
    value: int

    #: Indicates increment events.
    INC = +1

    #: Indicates decrement events.
    DEC = -1

    @classmethod
    def of(cls, quantity: Quantity) -> "Direction":
        """
        Returns the corresponding direction as per the sign of the quantity.

        :param quantity: Quantity to find the direction of.
        :return: Direction for the quantity.
        :raises AssertionError: If quantity is zero which implies a programming error.
        """
        assert not quantity.is_zero(), "Encountered a `0` quantity. This implies a programming error."
        return Direction.INC if quantity > 0 else Direction.DEC


#: Provides the mapping for DEBIT/CREDIT convention as per increment/decrement and account type.
_debit_mapping: Dict[Direction, Set[AccountType]] = {
    Direction.INC: {AccountType.ASSETS, AccountType.EQUITIES, AccountType.LIABILITIES},
    Direction.DEC: {AccountType.REVENUES, AccountType.EXPENSES},
}


@dataclass(frozen=True)
class Posting(Generic[_T]):
    """
    Provides a posting value object model.
    """

    #: Journal entry the posting belongs to.
    journal: "JournalEntry[_T]"

    #: Date of posting.
    date: datetime.date

    #: Account of the posting.
    account: Account

    #: Direction of the posting.
    direction: Direction

    #: Posted amount (in absolute value).
    amount: Amount

    @property
    def is_debit(self) -> bool:
        """
        Indicates if this posting is a debit.
        """
        return self.account.type in _debit_mapping[self.direction]

    @property
    def is_credit(self) -> bool:
        """
        Indicates if this posting is a credit.
        """
        return not self.is_debit


@dataclass(frozen=True)
class JournalEntry(Generic[_T]):
    """
    Provides a journal entry model.
    """

    #: Date of the entry.
    date: datetime.date

    #: Description of the entry.
    description: str

    #: Business object as the source of the journal entry.
    source: _T

    #: Postings of the journal entry.
    postings: List[Posting[_T]] = field(default_factory=list, init=False)

    #: Globally unique, ephemeral identifier.
    guid: Guid = field(default_factory=makeguid, init=False)

    @property
    def increments(self) -> Iterable[Posting[_T]]:
        """
        Increment event postings of the journal entry.
        """
        return (p for p in self.postings if p.direction == Direction.INC)

    @property
    def decrements(self) -> Iterable[Posting[_T]]:
        """
        Decrement event postings of the journal entry.
        """
        return (p for p in self.postings if p.direction == Direction.DEC)

    @property
    def debits(self) -> Iterable[Posting[_T]]:
        """
        Debit postings of the journal entry.
        """
        return (p for p in self.postings if p.is_debit)

    @property
    def credits(self) -> Iterable[Posting[_T]]:
        """
        Credit postings of the journal entry.
        """
        return (p for p in self.postings if p.is_credit)

    def post(self, date: datetime.date, account: Account, quantity: Quantity) -> "JournalEntry[_T]":
        """
        Posts an increment/decrement event (depending on the sign of ``quantity``) to the given account.

        If the quantity is ``0``, nothing is posted.

        :param date: Date of posting.
        :param account: Account to post the amount to.
        :param quantity: Signed-value to post to the account.
        :return: This journal entry (to be chained conveniently).
        """
        if not quantity.is_zero():
            self.postings.append(Posting(self, date, account, Direction.of(quantity), Amount(abs(quantity))))
        return self

    def validate(self) -> None:
        """
        Performs validations on the instance.

        :raises AssertionError: If the journal entry is inconsistent.
        """
        ## Get total debit and credit amounts:
        total_debit = isum(i.amount for i in self.debits)
        total_credit = isum(i.amount for i in self.credits)

        ## Check:
        assert total_debit == total_credit, f"Total Debits and Credits are not equal: {total_debit} != {total_credit}"


class ReadJournalEntries(Protocol[_T]):
    """
    Type of functions which read journal entries from a source.
    """

    def __call__(self, period: DateRange) -> Iterable[JournalEntry[_T]]:
        ...
