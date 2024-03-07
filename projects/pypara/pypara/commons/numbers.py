"""
This module provides common numeric type definitions, constants and functions.
"""

__all__ = [
    "Amount",
    "CENT",
    "DecimalLike",
    "HUNDRED",
    "isum",
    "make_quantizer",
    "MaxPrecision",
    "MaxPrecisionQuantizer",
    "NaturalNumber",
    "Numeric",
    "ONE",
    "PositiveInteger",
    "Quantity",
    "quantize12",
    "quantize2",
    "quantize4",
    "quantize8",
    "Quantizer12",
    "Quantizer2",
    "Quantizer4",
    "Quantizer8",
    "sign",
    "ZERO",
]

import sys
from decimal import Decimal
from typing import Callable, Iterable, NewType, Optional, TypeVar, cast


class NaturalNumber(int):
    """
    Provides a *newtype* for natural numbers ``[0, 1, ...)``.

    Call-site should ensure that the constructor does not throw assertion errors.
    """

    def __new__(cls, value: int) -> "NaturalNumber":
        """
        Attempts to create a new instance.

        :param value: A non-negative integer.
        :raises AssertionError: If ``value`` is not a non-negative integer.
        """
        assert value >= 0
        return int(value)  # type: ignore


class PositiveInteger(int):
    """
    Provides a *newtype* for positive integers ``[1, ...)``.

    Call-site should ensure that the constructor does not throw assertion errors.
    """

    def __new__(cls, value: int) -> "PositiveInteger":
        """
        Attempts to create a new instance.

        :param value: A positive integer.
        :raises AssertionError: If ``value`` is not a positive integer.
        """
        assert value > 0
        return int(value)  # type: ignore


#: Defines a new-type for non-negative (absolute, unsigned)
#: :py:class:`decimal.Decimal` values as *amount*.
#:
#: This is just a convenience for adding further semantics to type signatures.
Amount = NewType("Amount", Decimal)

#: Defines a new-type for :py:class:`decimal.Decimal` values as *quantities*.
#:
#: This is just a convenience for adding further semantics to type signatures.
Quantity = NewType("Quantity", Decimal)

#: Defines a type alias for numeric values.
Numeric = TypeVar("Numeric", int, float, Decimal, Amount, Quantity)

#: Defines a type variable for values of type either :py:class:`decimal.Decimal`
#: or a sub-class or new-type based on : py:class:`Decimal` such as
#: :py:class:`Amount` and a :py:class:`Quantity`.
DecimalLike = TypeVar("DecimalLike", bound=Decimal)

#: Defines the constant for :py:class:`decimal.Decimal` value ``0``.
ZERO = Decimal("0")

#: Defines the constant for :py:class:`decimal.Decimal` value ``0.01``.
CENT = Decimal("0.01")

#: Defines the constant for :py:class:`decimal.Decimal` value ``1``.
ONE = Decimal("1")

#: Defines the constant for :py:class:`decimal.Decimal` value ``100``.
HUNDRED = Decimal("100")


def make_quantizer(precision: int) -> Decimal:
    """
    Creates a quantifier as per the given precision.
    """
    return Decimal(f"0.{''.join(['0' * precision])}")


def make_quantize_func(quantizer: Decimal) -> Callable[[Decimal], Decimal]:
    """
    Creates a quantize function with the given quantizer.
    """
    return lambda x: x.quantize(quantizer)


#: Defines the maximum precision of the monetary values and operations in this library.
MaxPrecision: int = 12

#: Defines the maximum precision quantifier.
MaxPrecisionQuantizer: Decimal = make_quantizer(MaxPrecision)

#: Defines a quantizer with 2 decimals.
Quantizer2 = make_quantizer(2)

#: Defines a quantizer with 4 decimals.
Quantizer4 = make_quantizer(4)

#: Defines a quantizer with 8 decimals.
Quantizer8 = make_quantizer(8)

#: Defines a quantizer with 12 decimals.
Quantizer12 = make_quantizer(12)


quantize2 = make_quantize_func(Quantizer2)
quantize2.__doc__ = """
Quantizes the given decimal (by 2 decimals).

>>> quantize2(Decimal("0.005"))
Decimal('0.00')
>>> quantize2(Decimal("0.015"))
Decimal('0.02')
"""


quantize4 = make_quantize_func(Quantizer4)
quantize4.__doc__ = """
Quantizes the given decimal (by 4 decimals).

>>> quantize4(Decimal("0.00005"))
Decimal('0.0000')
>>> quantize4(Decimal("0.00015"))
Decimal('0.0002')
"""

quantize8 = make_quantize_func(Quantizer8)
quantize8.__doc__ = """
Quantizes the given decimal (by 8 decimals).

>>> quantize8(Decimal("0.000000005"))
Decimal('0E-8')
>>> quantize8(Decimal("0.000000015"))
Decimal('2E-8')
"""


quantize12 = make_quantize_func(Quantizer12)
quantize12.__doc__ = """
Quantizes the given decimal (by 12 decimals).

>>> quantize12(Decimal("0.0000000000005"))
Decimal('0E-12')
>>> quantize12(Decimal("0.0000000000015"))
Decimal('2E-12')
"""


def isum(xs: Iterable[DecimalLike], start: Optional[DecimalLike] = None) -> DecimalLike:
    """
    Computes the sum of an iterable of :py:class:`DecimalLike` values such as :py:class:`Amount` or
    :py:class:`Quantity` including :py:class:`Decimal` itself.

    The return type is the same as the input element type. The base condition is :py:const:`ZERO` of
    :py:class:`decimal.Decimal` type but cast to the type variable if required.

    :param xs: An iterable of :py:class:`Decimal`-like values.
    :param start: Optional initial value. This defaults to :py:const:`ZERO` in the implementation.
    :return: Sum of the elements in the same type as the elements in the argument.

    >>> isum([Amount(ONE), Amount(ONE)])  # Return value is of type `Amount` during type-checking.
    Decimal('2')
    >>> isum([Quantity(ONE), Quantity(ONE)])  # Return value is of type `Quantity` during type-checking.
    Decimal('2')
    >>> isum([Amount(ONE), Amount(ONE)], Amount(ONE))  # Return value is of type `Amount` during type-checking.
    Decimal('3')
    >>> isum([Quantity(ONE), Quantity(ONE)], Quantity(ONE))  # Return value is of type `Quantity` during type-checking.
    Decimal('3')
    """
    return sum(xs, start or cast(DecimalLike, ZERO))


def sign(x: Numeric) -> int:
    """
    Defines a sign predicate for numeric values (ints, floats and Decimals).

    :param number: A number.
    :return: The sign of the given number.

    >>> sign(1)
    1
    >>> sign(0)
    0
    >>> sign(-0)
    0
    >>> sign(-1)
    -1
    >>> sign(Decimal("1"))
    1
    >>> sign(Decimal("0"))
    0
    >>> sign(-Decimal("0"))
    0
    >>> sign(Decimal("-1"))
    -1
    """
    return 1 if x > 0 else -1 if x < 0 else 0


def normalize(value: Decimal) -> Decimal:
    """
    Normalizes a given decimal value.

    :param value: The decimal value to be normalized.
    :return: The normalized decimal value.

    >>> normalize(Decimal("0.00"))
    Decimal('0')
    """
    return value.quantize(ONE) if value == value.to_integral() else value.normalize()


def weirdiv(dividend: Optional[Decimal], divisor: Optional[Decimal]) -> Decimal:
    """
    Provides a division for weirdos.

    Essentially, we are using this function at such call-sites where we don't have control over the incoming data, and
    lazy enough to bother doing it there.

    :param dividend: An optional dividend.
    :param divisor: An optional divisor.
    :return: A Decimal whether dividend and/or divisor are missing (0 in that case)

    >>> weirdiv(None, None)
    Decimal('0')
    >>> weirdiv(None, Decimal(0))
    Decimal('0')
    >>> weirdiv(None, Decimal(1))
    Decimal('0')
    >>> weirdiv(Decimal(0), None)
    Decimal('0')
    >>> weirdiv(Decimal(1), None) > 10 ** 10
    True
    >>> weirdiv(Decimal(9), Decimal(3))
    Decimal('3')
    """
    ## Check the dividend:
    if dividend is None or dividend.is_zero():
        return ZERO

    ## Check the divisor:
    if divisor is None or divisor.is_zero():
        ## Wish I could return infinity!
        return Decimal(sys.float_info.max).copy_sign(dividend)

    ## Normal division:
    return dividend / divisor
