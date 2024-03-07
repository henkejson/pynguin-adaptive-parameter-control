"""
This module provides data definitions and related functionality for preparing general ledgers.
"""

__all__ = [
    "GeneralLedger",
    "GeneralLedgerProgram",
    "InitialBalances",
    "Ledger",
    "LedgerEntry",
    "ReadInitialBalances",
    "build_general_ledger",
    "compile_general_ledger_program",
]

import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Generic, Iterable, List, Optional, Protocol, TypeVar

from ..commons.numbers import Amount, Quantity
from ..commons.zeitgeist import DateRange
from .accounts import Account
from .generic import Balance
from .journaling import JournalEntry, Posting, ReadJournalEntries

#: Defines a generic type variable.
_T = TypeVar("_T")


#: Initial balances:
InitialBalances = Dict[Account, Balance]


@dataclass
class LedgerEntry(Generic[_T]):
    """
    Provides a ledger entry model.
    """

    #: Ledger the entry belongs to.
    ledger: "Ledger[_T]"

    #: Posting of the ledger entry.
    posting: Posting[_T]

    #: Balance of the ledger entry.
    balance: Quantity

    @property
    def date(self) -> datetime.date:
        """
        Date of the ledger entry.
        """
        return self.posting.date

    @property
    def description(self) -> str:
        """
        Description of the ledger entry.
        """
        return self.posting.journal.description

    @property
    def amount(self) -> Amount:
        """
        Amount of the ledger entry.
        """
        return self.posting.amount

    @property
    def cntraccts(self) -> List[Account]:
        """
        Counter accounts for the ledger entry.
        """
        return [p.account for p in self.posting.journal.postings if p.direction != self.posting.direction]

    @property
    def is_debit(self) -> bool:
        """
        Indicates if the ledger entry is a debit.
        """
        return self.posting.is_debit

    @property
    def is_credit(self) -> bool:
        """
        Indicates if the ledger entry is a credit.
        """
        return self.posting.is_credit

    @property
    def debit(self) -> Optional[Amount]:
        """
        Returns the debit amount, if any.
        """
        return self.amount if self.is_debit else None

    @property
    def credit(self) -> Optional[Amount]:
        """
        Returns the credit amount, if any.
        """
        return self.amount if self.is_credit else None


@dataclass
class Ledger(Generic[_T]):
    """
    Provides an account ledger model.
    """

    #: Account of the ledger.
    account: Account

    #: Initial balance of the ledger.
    initial: Balance

    #: Ledger entries.
    entries: List[LedgerEntry[_T]] = field(default_factory=list, init=False)

    @property
    def _last_balance(self) -> Quantity:
        """
        Returns the last balance.
        """
        try:
            return self.entries[-1].balance
        except IndexError:
            return self.initial.value

    def add(self, posting: Posting[_T]) -> LedgerEntry[_T]:
        """
        Adds a new ledger entry.

        :param posting: Posting the ledger entry is based on.
        :return: The new ledger entry.
        """
        ## Create the ledger entry.
        entry = LedgerEntry(self, posting, Quantity(self._last_balance + posting.amount * posting.direction.value))

        ## Add to the buffer:
        self.entries.append(entry)

        ## Done, return:
        return entry


@dataclass
class GeneralLedger(Generic[_T]):
    """
    Provides a general ledger model.
    """

    #: Accounting period.
    period: DateRange

    #: Individual account ledgers of the general ledger.
    ledgers: Dict[Account, Ledger[_T]]


def build_general_ledger(
    period: DateRange, journal: Iterable[JournalEntry[_T]], initial: InitialBalances
) -> GeneralLedger[_T]:
    """
    Builds a general ledger.

    :param period: Accounting period.
    :param journal: All available journal entries.
    :param initial: Opening balances for terminal accounts, if any.
    :return: A :py:class:`GeneralLedger` instance.
    """
    ## Initialize ledgers buffer as per available initial balances:
    ledgers: Dict[Account, Ledger[_T]] = {a: Ledger(a, b) for a, b in initial.items()}

    ## Iterate over journal postings and populate ledgers:
    for posting in (p for j in journal for p in j.postings if period.since <= j.date <= period.until):
        ## Check if we have the ledger yet, and create if not:
        if posting.account not in ledgers:
            ledgers[posting.account] = Ledger(posting.account, Balance(period.since, Quantity(Decimal(0))))

        ## Add the posting to the ledger:
        ledgers[posting.account].add(posting)

    ## Done, return general ledger.
    return GeneralLedger(period, ledgers)


class ReadInitialBalances(Protocol):
    """
    Type of functions which reads and returns initial balances.
    """

    def __call__(self, period: DateRange) -> InitialBalances:
        ...


class GeneralLedgerProgram(Protocol[_T]):
    """
    Type definition of the program which builds general ledger.
    """

    def __call__(self, period: DateRange) -> GeneralLedger[_T]:
        ...


def compile_general_ledger_program(
    read_initial_balances: ReadInitialBalances,
    read_journal_entries: ReadJournalEntries[_T],
) -> GeneralLedgerProgram[_T]:
    """
    Consumes implementations of the algebra and returns a program which consumes opening and closing dates and produces
    a general ledger.

    :param read_initial_balances: Algebra implementation which reads initial balances.
    :param read_journal_entries: Algebra implementation which reads journal entries.
    :return: A function which consumes opening and closing dates and produces a general ledger
    """

    def _program(period: DateRange) -> GeneralLedger[_T]:
        """
        Consumes the opening and closing dates and produces a general ledger.

        :param period: Accounting period.
        :return: A general ledger.
        """
        ## Get initial balances as of the end of previous financial period:
        initial_balances = read_initial_balances(period)

        ## Read journal entries and post each of them:
        journal_entries = read_journal_entries(period)

        ## Build the general ledger and return:
        return build_general_ledger(period, journal_entries, initial_balances)

    ## Return the compiled program.
    return _program
