"""
This module provides account types, accounts and a chart of accounts model definitions.

Account's are identified by unique :py:class:`Code` instances which is a :py:class:`typing.NewType` of :py:class:`str`.

A chart of accounts (:py:class:`COA`) is initialized with 5 core accounts of types:

#. :py:attr:`AccountType.ASSETS`
#. :py:attr:`AccountType.LIABILITIES`
#. :py:attr:`AccountType.EQUITIES`
#. :py:attr:`AccountType.REVENUES`
#. :py:attr:`AccountType.EXPENSES`

A simple chart of accounts can be initialized as follows:

>>> coa = COA()
>>> for code, acct in coa:
...     print((code, acct.name))
('1', 'Assets')
('2', 'Liabilities')
('3', 'Equities')
('4', 'Revenues')
('5', 'Expenses')

We can retrieve accounts by account code:

>>> coa.find(Code("1")).name
'Assets'
>>> coa.find(Code("2")).name
'Liabilities'
>>> coa.find(Code("3")).name
'Equities'
>>> coa.find(Code("4")).name
'Revenues'
>>> coa.find(Code("5")).name
'Expenses'
>>> coa.find(Code("boguscode")) is None
True

We can add further accounts:

>>> liquidity = coa.add(Code("1"), Code("1000"), "Liquidity")
>>> bankaccnt = coa.add(liquidity.code, Code("1001"), "Bank Account")
>>> for code, acct in coa:
...     print((code, acct.name))
('1', 'Assets')
('2', 'Liabilities')
('3', 'Equities')
('4', 'Revenues')
('5', 'Expenses')
('1000', 'Liquidity')
('1001', 'Bank Account')
>>> coa.find(Code("1001")).parent.name
'Liquidity'
>>> coa.find(Code("1001")).name
'Bank Account'

We can also print the chart of accounts in a tree-like structure.

>>> coa.print()
[1] Assets
    [1000] Liquidity
        [1001] Bank Account
[2] Liabilities
[3] Equities
[4] Revenues
[5] Expenses
"""

__all__ = [
    "Account",
    "AccountType",
    "COA",
    "Code",
    "ReadChartOfAccounts",
]

from abc import abstractmethod
from collections import OrderedDict
from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Dict, Iterable, Iterator, List, NewType, Optional, Protocol, Tuple, runtime_checkable

#: Defines a new-type for account codes.
Code = NewType("Code", str)


class AccountType(Enum):
    """
    Provides an enumeration of types of accounts in balance sheet and income statement.
    """

    #: Indicates asset accounts related to economic resources which are beneficial to the entity.
    ASSETS = "ASSETS"

    #: Indicates liability accounts related to debts and future obligations to the entity.
    LIABILITIES = "LIABILITIES"

    #: Indicates equity accounts related to claims of owners and/or shareholders of the entity.
    EQUITIES = "EQUITIES"

    #: Indicates accounts for revenues resulting in increase in :py:attr:`AccountType.EQUITIES`.
    REVENUES = "REVENUES"

    #: Indicates accounts for expenses resulting in decrease in :py:attr:`AccountType.EQUITIES`.
    EXPENSES = "EXPENSES"

    def __lt__(self, other: "AccountType") -> bool:
        """
        Provides a comparison for account type enums.
        """
        ## Provides the order of enums:
        order: Dict["AccountType", int] = {
            AccountType.ASSETS: 0,
            AccountType.LIABILITIES: 1,
            AccountType.EQUITIES: 2,
            AccountType.REVENUES: 3,
            AccountType.EXPENSES: 4,
        }

        ## Compare and return the order of enums:
        return order[self] < order[other]


@runtime_checkable
class Account(Protocol):
    """
    Provides a base account model.
    """

    @property
    @abstractmethod
    def code(self) -> Code:
        """
        Code of the account.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the account.
        """
        ...

    @property
    @abstractmethod
    def type(self) -> AccountType:
        """
        Type of the account.
        """
        ...

    @property
    @abstractmethod
    def coa(self) -> "COA":
        """
        Chart of accounts of the account.
        """
        ...

    @property
    @abstractmethod
    def parent(self) -> Optional["Account"]:
        """
        Parent of the account, if any.
        """
        ...


@dataclass(frozen=True)
class RootAccount:
    """
    Provides root account model.
    """

    #: Code of the account.
    code: Code

    #: Name of the account.
    name: str

    #: Type of the account.
    type: AccountType

    #: Chart of accounts the account belongs to.
    coa: "COA"

    @property
    def parent(self) -> Optional["Account"]:
        """
        Parent account.
        """
        ## I wish I could do `parent: ClassVar[Optional["Account"]] = None` instead!
        return None


@dataclass(frozen=True)
class SubAccount:
    """
    Provides sub-account model.
    """

    #: Code of the account.
    code: Code

    #: Name of the account.
    name: str

    #: Parent account.
    parent: "Account"

    @property
    def type(self) -> AccountType:
        """
        Type of the account.
        """
        return self.parent.type

    @property
    def coa(self) -> "COA":
        """
        Chart of accounts the account belongs to.
        """
        return self.parent.coa


@dataclass(frozen=True)
class COA:
    """
    Provides a model of chart of accounts.
    """

    @dataclass
    class Node:
        """
        Provides a node definition for the chart of accounts tree.
        """

        #: Account of the node.
        account: Account

        #: Sub-accounts of the account of the node.
        children: List["COA.Node"]

    #: Internal buffer for accounts.
    _accounts: Dict[Code, Account] = field(default_factory=OrderedDict, hash=False)

    #: Internal buffer for sub-accounts.
    _subaccounts: Dict[Account, List[Account]] = field(default_factory=OrderedDict, hash=False)

    #: Specification to initialize root accounts.
    rootspec: InitVar[Optional[Dict[AccountType, Tuple[Code, str]]]] = None

    def __post_init__(self, rootspec: Optional[Dict[AccountType, Tuple[Code, str]]]) -> None:
        """
        Initializes the root accounts buffer.
        """
        ## Do we have a rootspec?
        rootspec = rootspec or {}

        ## Iterate over account types and initialize root accounts:
        for c, t in enumerate(AccountType, start=1):
            ## Attempt to get or initialize code/name tuple for the type:
            code, name = rootspec.get(t, (Code(str(c)), t.name.capitalize()))

            ## Create the account and add to the buffer:
            self._accounts[code] = RootAccount(code, name, t, self)

    def __iter__(self) -> Iterator[Tuple[Code, Account]]:
        """
        Returns an iterable of account code and account tuples.
        """
        return ((c, a) for c, a in self._accounts.items())

    @property
    def accounts(self) -> Iterable[Account]:
        """
        All accounts of the chart of accounts.
        """
        return iter(self._accounts.values())

    @property
    def toplevel(self) -> Iterable[Account]:
        """
        Top-level accounts (balance sheet and income statement accounts) of the chart of accounts.
        """
        return (a for a in self.accounts if a.parent is None)

    @property
    def structure(self) -> Iterable["COA.Node"]:
        """
        Tree-like structure of the chart of accounts.
        """
        return map(self.nodify, self.toplevel)

    def find(self, code: Code) -> Optional[Account]:
        """
        Attempts to find and return the account by the given code.

        :param code: Code of the account we want to retrieve.
        :return: :py:class:`Account` identified by the given code if found, ``None`` otherwise.
        """
        return self._accounts.get(code, None)

    def subaccounts(self, account: Account) -> List[Account]:
        """
        Attempts to find and return sub-accounts of the given account.

        :param account: Account we want to retrieve sub-accounts of.
        :return: List of sub-accounts.
        """
        return self._subaccounts.get(account, [])

    def nodify(self, account: Account) -> "COA.Node":
        """
        Compiles a :py:class:`Node` instance for the given account.

        :param account: Account we want to compile the :py:class:`Node` for.
        :return: Account :py:class:`Node` within the chart of accounts.
        """
        return self.Node(account, [self.nodify(a) for a in self.subaccounts(account)])

    def add(self, parent: Code, code: Code, name: str) -> Account:
        """
        Attempts to add a new account to the chart of accounts.

        :param parent: Code of the parent account.
        :param code: Account code.
        :param name: Account name.
        :return: Newly created account (or existing one).
        """
        ## Check if parent and code are same:
        if parent == code:
            raise ValueError("An account can not be the parent of itself.")

        ## Attempt to get the parent instance:
        parentinstance = self._accounts.get(parent)

        ## Check if we have a parent instance:
        if parentinstance is None:
            raise ValueError("Parent account is not (yet) defined.")

        ## Check if we already have an account:
        if code in self._accounts:
            ## Get the account:
            account = self._accounts[code]

            ## Check account information is consistent:
            if account.parent == parentinstance and account.name == name and account.code == code:
                return account
            else:
                raise ValueError("Account name, code and parent do not match existing chart of accounts member.")

        ## Create the account:
        account = SubAccount(code, name, self._accounts[parent])

        ## Add to the COA:
        self._accounts[code] = account

        ## Add the account to children buffer:
        if account.parent not in self._subaccounts:
            self._subaccounts[account.parent] = []
        self._subaccounts[account.parent].append(account)

        ## Done, return the new account:
        return account

    def print(self) -> None:
        """
        Prints the chart of accounts in a tree-like form.

        :param coa: Chart of accounts to print.
        """
        for tree in self.structure:
            self._print_node(tree, 0)

    @classmethod
    def _print_node(cls, node: "COA.Node", level: int = 0) -> None:
        """
        Prints a node.

        This is an auxiliary function to :py:func:`print_coa`.

        :param node: Node to print.
        :param level: Level to print node at.
        """
        print(f"{''.join(['    '] * level)}[{node.account.code}] {node.account.name}")  # noqa: T201
        for c in node.children:
            cls._print_node(c, level + 1)


class ReadChartOfAccounts(Protocol):
    """
    Type of functions which read chart-of-accounts from a source.
    """

    def __call__(self) -> COA:
        ...
