import datetime
from decimal import Decimal

import pytest

from pypara.currencies import Currencies
from pypara.monetary import IncompatibleCurrencyError, Money, NoMoney, NoneMoney, Price, SomeMoney

## Define some currencies:
eur = Currencies["EUR"]
usd = Currencies["USD"]

## Defines some Decimal quantities:
zero = Decimal("0")
half = Decimal("0.5")
one = Decimal("1")
two = Decimal("2")

## Define some dates:
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)


def test_implementation() -> None:
    ## Define instances:
    smoney = SomeMoney(usd, one, today)
    nmoney = NoneMoney()

    ## Check structure:
    assert smoney.__slots__ == ()
    assert nmoney.__slots__ == ()
    assert not hasattr(smoney, "__dict__")
    assert not hasattr(nmoney, "__dict__")

    ## Check types
    assert isinstance(Money.na(), Money)
    assert isinstance(Money.na(), NoneMoney)
    assert not isinstance(Money.na(), SomeMoney)
    assert not isinstance(Money.na(), Price)

    assert isinstance(smoney, Money)
    assert isinstance(smoney, SomeMoney)
    assert not isinstance(smoney, NoneMoney)

    assert isinstance(nmoney, Money)
    assert not isinstance(nmoney, SomeMoney)
    assert isinstance(nmoney, NoneMoney)


def test_of() -> None:
    assert Money.of(usd, one, None) == Money.na()
    assert Money.of(usd, None, today) == Money.na()
    assert Money.of(usd, one, None) == Money.na()
    assert Money.of(usd, one, today) == SomeMoney(usd, one, today)
    assert Money.of(usd, Decimal("0.055"), today) == Money.of(usd, Decimal("0.06"), today)
    assert Money.of(usd, Decimal("0.045"), today) == Money.of(usd, Decimal("0.04"), today)


def test_is_equal() -> None:
    ## Vanilla:
    assert Money.na().is_equal(NoMoney)
    assert Money.na().is_equal(NoneMoney())
    assert not Money.na().is_equal(Money.of(usd, zero, today))
    assert Money.of(usd, zero, today).is_equal(Money.of(usd, zero, today))
    assert Money.of(usd, half, today).is_equal(Money.of(usd, half, today))
    assert not Money.of(usd, zero, today).is_equal(Money.of(eur, zero, today))
    assert not Money.of(usd, zero, today).is_equal(Money.of(usd, half, today))
    assert not Money.of(usd, zero, today).is_equal(Money.of(usd, zero, yesterday))

    ## With operator overload:
    assert Money.na() == NoneMoney()
    assert Money.na() != Money.of(usd, zero, today)
    assert Money.of(usd, zero, today) == Money.of(usd, zero, today)
    assert Money.of(usd, half, today) == Money.of(usd, half, today)
    assert Money.of(usd, zero, today) != Money.of(eur, zero, today)
    assert Money.of(usd, zero, today) != Money.of(usd, half, today)
    assert Money.of(usd, zero, today) != Money.of(usd, zero, yesterday)


def test_to_boolean() -> None:
    ## Vanilla:
    assert not Money.na().as_boolean()
    assert not Money.of(usd, zero, today).as_boolean()
    assert Money.of(usd, half, today).as_boolean()
    assert Money.of(usd, -half, today).as_boolean()

    ## With semantic overload
    assert not bool(Money.na())
    assert not Money.of(usd, zero, today)
    assert Money.of(usd, half, today)
    assert Money.of(usd, -half, today)


def test_to_float() -> None:
    ## Vanilla:
    with pytest.raises(TypeError):
        Money.na().as_float()
    assert Money.of(usd, half, today).as_float() == 0.5
    assert type(Money.of(usd, half, today).as_float()) == float

    ## With overload:
    with pytest.raises(TypeError):
        float(Money.na())
    assert float(Money.of(usd, half, today)) == 0.5
    assert type(float(Money.of(usd, half, today))) == float


def test_to_integer() -> None:
    ## Vanilla:
    with pytest.raises(TypeError):
        int(Money.na())
    assert int(Money.of(usd, half, today)) == 0
    assert type(int(Money.of(usd, half, today))) == int

    ## With overload:
    with pytest.raises(TypeError):
        Money.na().as_integer()
    assert Money.of(usd, half, today).as_integer() == 0
    assert type(Money.of(usd, half, today).as_integer()) == int


def test_abs() -> None:
    ## Vanilla:
    assert Money.na().abs() == Money.na()
    assert Money.of(usd, zero, today).abs() == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today).abs() == Money.of(usd, +one, today)
    assert Money.of(usd, +one, today).abs() == Money.of(usd, +one, today)

    ## With overload:
    assert abs(Money.na()) == Money.na()
    assert abs(Money.of(usd, zero, today)) == Money.of(usd, zero, today)
    assert abs(Money.of(usd, -one, today)) == Money.of(usd, +one, today)
    assert abs(Money.of(usd, +one, today)) == Money.of(usd, +one, today)


def test_negative() -> None:
    ## Vanilla:
    assert Money.na().negative() == Money.na()
    assert Money.of(usd, zero, today).negative() == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today).negative() == Money.of(usd, +one, today)
    assert Money.of(usd, +one, today).negative() == Money.of(usd, -one, today)

    ## With overload:
    assert -Money.na() == Money.na()
    assert -Money.of(usd, zero, today) == Money.of(usd, zero, today)
    assert -Money.of(usd, -one, today) == Money.of(usd, +one, today)
    assert -Money.of(usd, +one, today) == Money.of(usd, -one, today)


def test_positive() -> None:
    ## Vanilla:
    assert Money.na().positive() == Money.na()
    assert Money.of(usd, zero, today).positive() == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today).positive() == Money.of(usd, -one, today)
    assert Money.of(usd, +one, today).positive() == Money.of(usd, +one, today)

    ## With overload:
    assert +Money.na() == Money.na()
    assert +Money.of(usd, zero, today) == Money.of(usd, zero, today)
    assert +Money.of(usd, -one, today) == Money.of(usd, -one, today)
    assert +Money.of(usd, +one, today) == Money.of(usd, +one, today)


def test_round() -> None:
    ## Vanilla:
    assert Money.na().round(2) == Money.na()
    assert Money.of(usd, zero, today).round(2) == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today).round(2) == Money.of(usd, -one, today)
    assert Money.of(usd, +one, today).round(2) == Money.of(usd, +one, today)

    ## Quick tests:
    assert Money.of(usd, Decimal("1.555"), today).round(2) == Money.of(usd, Decimal("1.56"), today)
    assert Money.of(usd, Decimal("1.545"), today).round(2) == Money.of(usd, Decimal("1.54"), today)

    ## With overload:
    assert round(Money.na(), 2) == Money.na()
    assert round(Money.of(usd, zero, today), 2) == Money.of(usd, zero, today)
    assert round(Money.of(usd, -one, today), 2) == Money.of(usd, -one, today)
    assert round(Money.of(usd, +one, today), 2) == Money.of(usd, +one, today)
    assert round(Money.of(usd, Decimal("1.555"), today), 2) == Money.of(usd, Decimal("1.56"), today)
    assert round(Money.of(usd, Decimal("1.545"), today), 2) == Money.of(usd, Decimal("1.54"), today)

    ## Extras:
    assert round(Money.of(usd, Decimal("0.545"), today), 0) == Money.of(usd, Decimal("1"), today)
    assert round(Money.of(usd, Decimal("1.545"), today), 0) == Money.of(usd, Decimal("2"), today)
    assert round(Money.of(usd, Decimal("0.545"), today), 1) == Money.of(usd, Decimal("0.5"), today)
    assert round(Money.of(usd, Decimal("1.545"), today), 1) == Money.of(usd, Decimal("1.5"), today)
    assert round(Money.of(usd, Decimal("0.45"), today), 1) == Money.of(usd, Decimal("0.4"), today)
    assert round(Money.of(usd, Decimal("1.45"), today), 1) == Money.of(usd, Decimal("1.4"), today)

    ## TODO: Following two are not really what round function signature says. mypy can't detect it!
    assert round(Money.of(usd, Decimal("1.4"), today)) == Money.of(usd, Decimal("1"), today)
    assert round(Money.of(usd, Decimal("1.5"), today)) == Money.of(usd, Decimal("2"), today)


def test_addition() -> None:
    ## First use `Money.na()`s:
    assert Money.na().add(Money.na()) == Money.na()
    assert Money.na().add(Money.of(usd, zero, today)) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today).add(Money.na()) == Money.of(usd, zero, today)

    ## Vanilla addition:
    assert Money.of(usd, zero, today).add(Money.of(usd, zero, today)) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today).add(Money.of(usd, one, today)) == Money.of(usd, one, today)
    assert Money.of(usd, one, today).add(Money.of(usd, one, today)) == Money.of(usd, two, today)
    assert Money.of(usd, one, today).add(Money.of(usd, -one, today)) == Money.of(usd, zero, today)

    ## Carry dates forward:
    assert Money.of(usd, zero, today).add(Money.of(usd, one, yesterday)) == Money.of(usd, one, today)
    assert Money.of(usd, zero, yesterday).add(Money.of(usd, one, today)) == Money.of(usd, one, today)

    ## Incompatible currency errors:
    with pytest.raises(IncompatibleCurrencyError):
        Money.of(usd, zero, today).add(Money.of(eur, zero, today))

    ## Operator overload:
    assert Money.na() + Money.na() == Money.na()
    assert Money.na() + Money.of(usd, zero, today) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today) + Money.na() == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today) + Money.of(usd, one, today) == Money.of(usd, one, today)


def test_scalar_addition() -> None:
    ## First use `Money.na()`s:
    assert Money.na().scalar_add(1) == Money.na()

    ## Vanilla addition:
    assert Money.of(usd, zero, today).scalar_add(1) == Money.of(usd, one, today)
    assert Money.of(usd, zero, today).scalar_add(1.0) == Money.of(usd, one, today)
    assert Money.of(usd, zero, today).scalar_add(one) == Money.of(usd, one, today)
    assert Money.of(usd, zero, today).scalar_add(-1) == Money.of(usd, -one, today)

    ## Extras:
    assert Money.of(usd, zero, today).scalar_add(0.5) == Money.of(usd, half, today)
    assert Money.of(usd, zero, today).scalar_add(Decimal("0.05")) == Money.of(usd, Decimal("0.05"), today)
    assert Money.of(usd, zero, today).scalar_add(Decimal("0.005")) == Money.of(usd, Decimal("0"), today)
    assert Money.of(usd, zero, today).scalar_add(Decimal("0.015")) == Money.of(usd, Decimal("0.02"), today)


def test_subtraction() -> None:
    ## First use `Money.na()`s:
    assert Money.na().subtract(Money.na()) == Money.na()
    assert Money.na().subtract(Money.of(usd, zero, today)) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today).subtract(Money.na()) == Money.of(usd, zero, today)

    ## Vanilla subtraction:
    assert Money.of(usd, zero, today).subtract(Money.of(usd, zero, today)) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today).subtract(Money.of(usd, one, today)) == Money.of(usd, -one, today)
    assert Money.of(usd, one, today).subtract(Money.of(usd, one, today)) == Money.of(usd, zero, today)
    assert Money.of(usd, one, today).subtract(Money.of(usd, -one, today)) == Money.of(usd, two, today)

    ## Carry dates forward:
    assert Money.of(usd, zero, today).subtract(Money.of(usd, one, yesterday)) == Money.of(usd, -one, today)
    assert Money.of(usd, zero, yesterday).subtract(Money.of(usd, one, today)) == Money.of(usd, -one, today)

    ## Incompatible currency errors:
    with pytest.raises(IncompatibleCurrencyError):
        Money.of(usd, zero, today).subtract(Money.of(eur, zero, today))

    ## Operator overload:
    assert Money.of(usd, zero, today) - Money.of(usd, one, today) == Money.of(usd, -one, today)
    assert Money.na() - Money.na() == Money.na()
    assert Money.na() - Money.of(usd, zero, today) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today) - Money.na() == Money.of(usd, zero, today)


def test_scalar_subtraction() -> None:
    ## First use `Money.na()`s:
    assert Money.na().scalar_subtract(1) == Money.na()

    ## Vanilla subtraction:
    assert Money.of(usd, zero, today).scalar_subtract(1) == Money.of(usd, -one, today)
    assert Money.of(usd, zero, today).scalar_subtract(1.0) == Money.of(usd, -one, today)
    assert Money.of(usd, zero, today).scalar_subtract(one) == Money.of(usd, -one, today)
    assert Money.of(usd, zero, today).scalar_subtract(-1) == Money.of(usd, one, today)

    ## Operator overload:
    assert Money.of(usd, zero, today).scalar_subtract(1) == Money.of(usd, -one, today)
    assert Money.of(usd, zero, today).scalar_subtract(-1) == Money.of(usd, one, today)

    ## Extras:
    assert Money.of(usd, zero, today).scalar_subtract(0.5) == Money.of(usd, -half, today)
    assert Money.of(usd, zero, today).scalar_subtract(Decimal("0.05")) == -Money.of(usd, Decimal("0.05"), today)
    assert Money.of(usd, zero, today).scalar_subtract(Decimal("0.005")) == -Money.of(usd, Decimal("0"), today)
    assert Money.of(usd, zero, today).scalar_subtract(Decimal("0.015")) == -Money.of(usd, Decimal("0.02"), today)


def test_scalar_multiplication() -> None:
    ## First use `Money.na()`s:
    assert Money.na().multiply(1) == Money.na()

    ## Vanilla subtraction:
    assert Money.of(usd, one, today).multiply(1) == Money.of(usd, one, today)
    assert Money.of(usd, one, today).multiply(2) == Money.of(usd, two, today)
    assert Money.of(usd, -one, today).multiply(1) == Money.of(usd, -one, today)
    assert Money.of(usd, -one, today).multiply(2) == Money.of(usd, -two, today)

    ## Other types:
    assert Money.of(usd, one, today).multiply(1) == Money.of(usd, one, today)
    assert Money.of(usd, one, today).multiply(1.0) == Money.of(usd, one, today)
    assert Money.of(usd, one, today).multiply(one) == Money.of(usd, one, today)

    ## Operator overload:
    assert Money.na() * 1 == Money.na()
    assert Money.of(usd, one, today) * 1 == Money.of(usd, one, today)
    assert Money.of(usd, one, today) * 2 == Money.of(usd, two, today)
    assert Money.of(usd, -one, today) * 1 == Money.of(usd, -one, today)
    assert Money.of(usd, -one, today) * 2 == Money.of(usd, -two, today)

    ## Extras
    assert Money.of(usd, one, today).multiply(Decimal("0.050")) == Money.of(usd, Decimal("0.05"), today)
    assert Money.of(usd, one, today).multiply(Decimal("0.005")) == Money.of(usd, Decimal("0.00"), today)
    assert Money.of(usd, one, today).multiply(Decimal("0.015")) == Money.of(usd, Decimal("0.02"), today)


def test_division() -> None:
    ## First use `Money.na()`s:
    assert Money.na().divide(1) == Money.na()

    ## Vanilla subtraction:
    assert Money.of(usd, one, today).divide(1) == Money.of(usd, one, today)
    assert Money.of(usd, one, today).divide(2) == Money.of(usd, half, today)
    assert Money.of(usd, -one, today).divide(1) == Money.of(usd, -one, today)
    assert Money.of(usd, -one, today).divide(2) == Money.of(usd, -half, today)

    ## Various divisor types:
    assert Money.of(usd, one, today).divide(2) == Money.of(usd, half, today)
    assert Money.of(usd, one, today).divide(2.0) == Money.of(usd, half, today)
    assert Money.of(usd, one, today).divide(two) == Money.of(usd, half, today)

    ## Division by zero:
    assert Money.of(usd, one, today).divide(0) == Money.na()
    assert Money.of(usd, one, today).divide(zero) == Money.na()
    assert Money.of(usd, one, today).divide(0.0) == Money.na()

    ## Operator overload:
    assert Money.na() / 1 == Money.na()
    assert Money.of(usd, one, today) / 1 == Money.of(usd, one, today)
    assert Money.of(usd, one, today) / 2 == Money.of(usd, half, today)
    assert Money.of(usd, -one, today) / 1 == Money.of(usd, -one, today)
    assert Money.of(usd, -one, today) / 2 == Money.of(usd, -half, today)
    assert Money.of(usd, -one, today) / 0 == Money.na()

    ## Extras
    assert Money.of(usd, one, today).divide(Decimal("10")) == Money.of(usd, Decimal("0.10"), today)
    assert Money.of(usd, one, today).divide(Decimal("50")) == Money.of(usd, Decimal("0.02"), today)
    assert Money.of(usd, one, today).divide(Decimal("100")) == Money.of(usd, Decimal("0.01"), today)
    assert Money.of(usd, one, today).divide(Decimal("1000")) == Money.of(usd, Decimal("0.00"), today)


def test_floor_division() -> None:
    ## First use `Money.na()`s:
    assert Money.na().floor_divide(1) == Money.na()

    ## Vanilla subtraction:
    assert Money.of(usd, one, today).floor_divide(1) == Money.of(usd, one, today)
    assert Money.of(usd, one, today).floor_divide(2) == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today).floor_divide(1) == Money.of(usd, -one, today)
    assert Money.of(usd, -one, today).floor_divide(2) == Money.of(usd, zero, today)

    ## Various divisor types:
    assert Money.of(usd, one, today).floor_divide(2) == Money.of(usd, zero, today)
    assert Money.of(usd, one, today).floor_divide(2.0) == Money.of(usd, zero, today)
    assert Money.of(usd, one, today).floor_divide(two) == Money.of(usd, zero, today)

    ## Division by zero:
    assert Money.of(usd, one, today).floor_divide(0) == Money.na()
    assert Money.of(usd, one, today).floor_divide(zero) == Money.na()
    assert Money.of(usd, one, today).floor_divide(0.0) == Money.na()

    ## Operator overload:
    assert Money.na() / 1 == Money.na()
    assert Money.of(usd, one, today) // 1 == Money.of(usd, one, today)
    assert Money.of(usd, one, today) // 2 == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today) // 1 == Money.of(usd, -one, today)
    assert Money.of(usd, -one, today) // 2 == Money.of(usd, zero, today)
    assert Money.of(usd, -one, today) // 0 == Money.na()

    ## Extras
    assert Money.of(usd, Decimal("10"), today).floor_divide(Decimal("10")) == Money.of(usd, Decimal("1.00"), today)
    assert Money.of(usd, Decimal("10"), today).floor_divide(Decimal("11")) == Money.of(usd, Decimal("0.00"), today)


def test_comparisons() -> None:
    ## First use `Money.na()`s:
    assert not (Money.na() < Money.na())
    assert Money.na() <= Money.na()
    assert not (Money.na() > Money.na())
    assert Money.na() >= Money.na()

    ## Try mixed:
    assert Money.na() < Money.of(usd, -one, today)
    assert Money.na() <= Money.of(usd, -one, today)
    assert not (Money.na() > Money.of(usd, -one, today))
    assert not (Money.na() >= Money.of(usd, -one, today))

    ## ... and:
    assert not (Money.of(usd, -one, today) < Money.na())
    assert not (Money.of(usd, -one, today) <= Money.na())
    assert Money.of(usd, -one, today) > Money.na()
    assert Money.of(usd, -one, today) >= Money.na()

    ## With defined values:
    assert not (Money.of(usd, zero, today) < Money.of(usd, zero, today))
    assert Money.of(usd, zero, today) <= Money.of(usd, zero, today)
    assert not (Money.of(usd, zero, today) > Money.of(usd, zero, today))
    assert Money.of(usd, zero, today) >= Money.of(usd, zero, today)

    ## ... and:
    assert Money.of(usd, zero, today) < Money.of(usd, one, today)
    assert Money.of(usd, zero, today) <= Money.of(usd, one, today)
    assert not (Money.of(usd, zero, today) > Money.of(usd, one, today))
    assert not (Money.of(usd, zero, today) >= Money.of(usd, one, today))

    ## ... and:
    assert not (Money.of(usd, one, today) < Money.of(usd, zero, today))
    assert not (Money.of(usd, one, today) <= Money.of(usd, zero, today))
    assert Money.of(usd, one, today) > Money.of(usd, zero, today)
    assert Money.of(usd, one, today) >= Money.of(usd, zero, today)


def test_with() -> None:
    ## First use `Money.na()`s:
    assert Money.na().with_ccy(usd) == Money.na()
    assert Money.na().with_qty(one) == Money.na()
    assert Money.na().with_dov(today) == Money.na()

    ## Now with some:
    assert Money.of(usd, zero, today).with_ccy(eur) == Money.of(eur, zero, today)
    assert Money.of(usd, zero, today).with_qty(one) == Money.of(usd, one, today)
    assert Money.of(usd, zero, today).with_dov(yesterday) == Money.of(usd, zero, yesterday)

    ## Extras:
    assert Money.of(usd, zero, today).with_qty(Decimal("0.005")) == Money.of(usd, zero, today)
    assert Money.of(usd, zero, today).with_qty(Decimal("0.054")) == Money.of(usd, Decimal("0.05"), today)


def test_type_guard() -> None:
    none = Money.na()

    assert Money.is_none(none)
    assert not Money.is_some(none)

    with pytest.raises(AttributeError) as exc:
        none.ccy  # type: ignore[attr-defined]  # pylint: disable=[no-member,pointless-statement]

    assert str(exc.value) == "'NoneMoney' object has no attribute 'ccy'"

    some = Money.of(usd, zero, today)

    assert not Money.is_none(some)
    assert Money.is_some(some)
    assert some.ccy == usd
    assert some.qty == zero
    assert some.dov == today
