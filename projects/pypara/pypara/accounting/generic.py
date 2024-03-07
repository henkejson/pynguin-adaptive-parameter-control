"""
This module provides definitions and functionality applicable to the broader accounting scope.
"""

__all__ = ["Balance"]

import datetime
from dataclasses import dataclass

from pypara.commons.numbers import Quantity


@dataclass(frozen=True)
class Balance:
    """
    Provides a value object model for encoding dated balances.
    """

    #: Date of the balance.
    date: datetime.date

    #: Value of the balance.
    value: Quantity
