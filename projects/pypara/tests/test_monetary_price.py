import datetime
from decimal import Decimal

import pytest

from pypara.currencies import Currencies
from pypara.monetary import IncompatibleCurrencyError, Money, NonePrice, NoPrice, Price, SomePrice

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
    sprice = SomePrice(usd, one, today)
    nprice = NonePrice()

    ## Check structure:
    assert sprice.__slots__ == ()
    assert nprice.__slots__ == ()
    assert not hasattr(sprice, "__dict__")
    assert not hasattr(nprice, "__dict__")

    ## Check types
    assert isinstance(Price.na(), Price)
    assert isinstance(Price.na(), NonePrice)
    assert not isinstance(Price.na(), SomePrice)
    assert not isinstance(Price.na(), Money)

    assert isinstance(sprice, Price)
    assert isinstance(sprice, SomePrice)
    assert not isinstance(sprice, NonePrice)

    assert isinstance(nprice, Price)
    assert not isinstance(nprice, SomePrice)
    assert isinstance(nprice, NonePrice)


def test_of() -> None:
    assert Price.of(usd, one, None) == Price.na()
    assert Price.of(usd, None, today) == Price.na()
    assert Price.of(usd, one, None) == Price.na()
    assert Price.of(usd, one, today) == SomePrice(usd, one, today)


def test_is_equal() -> None:
    ## Vanilla:
    assert Price.na().is_equal(NoPrice)
    assert Price.na().is_equal(NonePrice())
    assert not Price.na().is_equal(Price.of(usd, zero, today))
    assert Price.of(usd, zero, today).is_equal(Price.of(usd, zero, today))
    assert Price.of(usd, half, today).is_equal(Price.of(usd, half, today))
    assert not Price.of(usd, zero, today).is_equal(Price.of(eur, zero, today))
    assert not Price.of(usd, zero, today).is_equal(Price.of(usd, half, today))
    assert not Price.of(usd, zero, today).is_equal(Price.of(usd, zero, yesterday))

    ## With operator overload:
    assert Price.na() == NonePrice()
    assert Price.na() != Price.of(usd, zero, today)
    assert Price.of(usd, zero, today) == Price.of(usd, zero, today)
    assert Price.of(usd, half, today) == Price.of(usd, half, today)
    assert Price.of(usd, zero, today) != Price.of(eur, zero, today)
    assert Price.of(usd, zero, today) != Price.of(usd, half, today)
    assert Price.of(usd, zero, today) != Price.of(usd, zero, yesterday)


def test_to_boolean() -> None:
    ## Vanilla:
    assert not Price.na().as_boolean()
    assert not Price.of(usd, zero, today).as_boolean()
    assert Price.of(usd, half, today).as_boolean()
    assert Price.of(usd, -half, today).as_boolean()

    ## With semantic overload
    assert not bool(Price.na())
    assert not Price.of(usd, zero, today)
    assert Price.of(usd, half, today)
    assert Price.of(usd, -half, today)


def test_to_float() -> None:
    ## Vanilla:
    with pytest.raises(TypeError):
        Price.na().as_float()
    assert Price.of(usd, half, today).as_float() == 0.5
    assert type(Price.of(usd, half, today).as_float()) == float

    ## With overload:
    with pytest.raises(TypeError):
        float(Price.na())
    assert float(Price.of(usd, half, today)) == 0.5
    assert type(float(Price.of(usd, half, today))) == float


def test_to_integer() -> None:
    ## Vanilla:
    with pytest.raises(TypeError):
        int(Price.na())
    assert int(Price.of(usd, half, today)) == 0
    assert type(int(Price.of(usd, half, today))) == int

    ## With overload:
    with pytest.raises(TypeError):
        Price.na().as_integer()
    assert Price.of(usd, half, today).as_integer() == 0
    assert type(Price.of(usd, half, today).as_integer()) == int


def test_abs() -> None:
    ## Vanilla:
    assert Price.na().abs() == Price.na()
    assert Price.of(usd, zero, today).abs() == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today).abs() == Price.of(usd, +one, today)
    assert Price.of(usd, +one, today).abs() == Price.of(usd, +one, today)

    ## With overload:
    assert abs(Price.na()) == Price.na()
    assert abs(Price.of(usd, zero, today)) == Price.of(usd, zero, today)
    assert abs(Price.of(usd, -one, today)) == Price.of(usd, +one, today)
    assert abs(Price.of(usd, +one, today)) == Price.of(usd, +one, today)


def test_negative() -> None:
    ## Vanilla:
    assert Price.na().negative() == Price.na()
    assert Price.of(usd, zero, today).negative() == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today).negative() == Price.of(usd, +one, today)
    assert Price.of(usd, +one, today).negative() == Price.of(usd, -one, today)

    ## With overload:
    assert -Price.na() == Price.na()
    assert -Price.of(usd, zero, today) == Price.of(usd, zero, today)
    assert -Price.of(usd, -one, today) == Price.of(usd, +one, today)
    assert -Price.of(usd, +one, today) == Price.of(usd, -one, today)


def test_positive() -> None:
    ## Vanilla:
    assert Price.na().positive() == Price.na()
    assert Price.of(usd, zero, today).positive() == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today).positive() == Price.of(usd, -one, today)
    assert Price.of(usd, +one, today).positive() == Price.of(usd, +one, today)

    ## With overload:
    assert +Price.na() == Price.na()
    assert +Price.of(usd, zero, today) == Price.of(usd, zero, today)
    assert +Price.of(usd, -one, today) == Price.of(usd, -one, today)
    assert +Price.of(usd, +one, today) == Price.of(usd, +one, today)


def test_round() -> None:
    ## Vanilla:
    assert Price.na().round(2) == Price.na()
    assert Price.of(usd, zero, today).round(2) == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today).round(2) == Price.of(usd, -one, today)
    assert Price.of(usd, +one, today).round(2) == Price.of(usd, +one, today)

    ## Quick tests:
    assert Price.of(usd, Decimal("1.555"), today).round(2) == Price.of(usd, Decimal("1.56"), today)
    assert Price.of(usd, Decimal("1.545"), today).round(2) == Price.of(usd, Decimal("1.54"), today)

    ## With overload:
    assert round(Price.na(), 2) == Price.na()
    assert round(Price.of(usd, zero, today), 2) == Price.of(usd, zero, today)
    assert round(Price.of(usd, -one, today), 2) == Price.of(usd, -one, today)
    assert round(Price.of(usd, +one, today), 2) == Price.of(usd, +one, today)
    assert round(Price.of(usd, Decimal("1.555"), today), 2) == Price.of(usd, Decimal("1.56"), today)
    assert round(Price.of(usd, Decimal("1.545"), today), 2) == Price.of(usd, Decimal("1.54"), today)

    ## TODO: Following two are not really what round function signature says. mypy can't detect it!
    assert round(Price.of(usd, Decimal("1.4"), today)) == Price.of(usd, Decimal("1"), today)
    assert round(Price.of(usd, Decimal("1.5"), today)) == Price.of(usd, Decimal("2"), today)


def test_addition() -> None:
    ## First use `Price.na()`s:
    assert Price.na().add(Price.na()) == Price.na()
    assert Price.na().add(Price.of(usd, zero, today)) == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today).add(Price.na()) == Price.of(usd, zero, today)

    ## Vanilla addition:
    assert Price.of(usd, zero, today).add(Price.of(usd, zero, today)) == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today).add(Price.of(usd, one, today)) == Price.of(usd, one, today)
    assert Price.of(usd, one, today).add(Price.of(usd, one, today)) == Price.of(usd, two, today)
    assert Price.of(usd, one, today).add(Price.of(usd, -one, today)) == Price.of(usd, zero, today)

    ## Carry dates forward:
    assert Price.of(usd, zero, today).add(Price.of(usd, one, yesterday)) == Price.of(usd, one, today)
    assert Price.of(usd, zero, yesterday).add(Price.of(usd, one, today)) == Price.of(usd, one, today)

    ## Incompatible currency errors:
    with pytest.raises(IncompatibleCurrencyError):
        Price.of(usd, zero, today).add(Price.of(eur, zero, today))

    ## Operator overload:
    assert Price.na() + Price.na() == Price.na()
    assert Price.na() + Price.of(usd, zero, today) == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today) + Price.na() == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today) + Price.of(usd, one, today) == Price.of(usd, one, today)


def test_scalar_addition() -> None:
    ## First use `Price.na()`s:
    assert Price.na().scalar_add(1) == Price.na()

    ## Vanilla addition:
    assert Price.of(usd, zero, today).scalar_add(1) == Price.of(usd, one, today)
    assert Price.of(usd, zero, today).scalar_add(1.0) == Price.of(usd, one, today)
    assert Price.of(usd, zero, today).scalar_add(one) == Price.of(usd, one, today)
    assert Price.of(usd, zero, today).scalar_add(-1) == Price.of(usd, -one, today)


def test_subtraction() -> None:
    ## First use `Price.na()`s:
    assert Price.na().subtract(Price.na()) == Price.na()
    assert Price.na().subtract(Price.of(usd, zero, today)) == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today).subtract(Price.na()) == Price.of(usd, zero, today)

    ## Vanilla subtraction:
    assert Price.of(usd, zero, today).subtract(Price.of(usd, zero, today)) == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today).subtract(Price.of(usd, one, today)) == Price.of(usd, -one, today)
    assert Price.of(usd, one, today).subtract(Price.of(usd, one, today)) == Price.of(usd, zero, today)
    assert Price.of(usd, one, today).subtract(Price.of(usd, -one, today)) == Price.of(usd, two, today)

    ## Carry dates forward:
    assert Price.of(usd, zero, today).subtract(Price.of(usd, one, yesterday)) == Price.of(usd, -one, today)
    assert Price.of(usd, zero, yesterday).subtract(Price.of(usd, one, today)) == Price.of(usd, -one, today)

    ## Incompatible currency errors:
    with pytest.raises(IncompatibleCurrencyError):
        Price.of(usd, zero, today).subtract(Price.of(eur, zero, today))

    ## Operator overload:
    assert Price.of(usd, zero, today) - Price.of(usd, one, today) == Price.of(usd, -one, today)
    assert Price.na() - Price.na() == Price.na()
    assert Price.na() - Price.of(usd, zero, today) == Price.of(usd, zero, today)
    assert Price.of(usd, zero, today) - Price.na() == Price.of(usd, zero, today)


def test_scalar_subtraction() -> None:
    ## First use `Price.na()`s:
    assert Price.na().scalar_subtract(1) == Price.na()

    ## Vanilla subtraction:
    assert Price.of(usd, zero, today).scalar_subtract(1) == Price.of(usd, -one, today)
    assert Price.of(usd, zero, today).scalar_subtract(1.0) == Price.of(usd, -one, today)
    assert Price.of(usd, zero, today).scalar_subtract(one) == Price.of(usd, -one, today)
    assert Price.of(usd, zero, today).scalar_subtract(-1) == Price.of(usd, one, today)

    ## Operator overload:
    assert Price.of(usd, zero, today).scalar_subtract(1) == Price.of(usd, -one, today)
    assert Price.of(usd, zero, today).scalar_subtract(-1) == Price.of(usd, one, today)


def test_scalar_multiplication() -> None:
    ## First use `Price.na()`s:
    assert Price.na().multiply(1) == Price.na()

    ## Vanilla subtraction:
    assert Price.of(usd, one, today).multiply(1) == Price.of(usd, one, today)
    assert Price.of(usd, one, today).multiply(2) == Price.of(usd, two, today)
    assert Price.of(usd, -one, today).multiply(1) == Price.of(usd, -one, today)
    assert Price.of(usd, -one, today).multiply(2) == Price.of(usd, -two, today)

    ## Other types:
    assert Price.of(usd, one, today).multiply(1) == Price.of(usd, one, today)
    assert Price.of(usd, one, today).multiply(1.0) == Price.of(usd, one, today)
    assert Price.of(usd, one, today).multiply(one) == Price.of(usd, one, today)

    ## Operator overload:
    assert Price.na() * 1 == Price.na()
    assert Price.of(usd, one, today) * 1 == Price.of(usd, one, today)
    assert Price.of(usd, one, today) * 2 == Price.of(usd, two, today)
    assert Price.of(usd, -one, today) * 1 == Price.of(usd, -one, today)
    assert Price.of(usd, -one, today) * 2 == Price.of(usd, -two, today)


def test_monetary_multiplication() -> None:
    ## First use `Price.na()`s:
    assert Price.na().times(1) == Money.na()

    ## Vanilla multiplication:
    assert Price.of(usd, one, today).times(1) == Money.of(usd, one, today)
    assert Price.of(usd, one, today).times(2) == Money.of(usd, two, today)
    assert Price.of(usd, -one, today).times(1) == Money.of(usd, -one, today)
    assert Price.of(usd, -one, today).times(2) == Money.of(usd, -two, today)

    ## Other types:
    assert Price.of(usd, one, today).times(1) == Money.of(usd, one, today)
    assert Price.of(usd, one, today).times(1.0) == Money.of(usd, one, today)
    assert Price.of(usd, one, today).times(one) == Money.of(usd, one, today)


def test_division() -> None:
    ## First use `Price.na()`s:
    assert Price.na().divide(1) == Price.na()

    ## Vanilla subtraction:
    assert Price.of(usd, one, today).divide(1) == Price.of(usd, one, today)
    assert Price.of(usd, one, today).divide(2) == Price.of(usd, half, today)
    assert Price.of(usd, -one, today).divide(1) == Price.of(usd, -one, today)
    assert Price.of(usd, -one, today).divide(2) == Price.of(usd, -half, today)

    ## Various divisor types:
    assert Price.of(usd, one, today).divide(2) == Price.of(usd, half, today)
    assert Price.of(usd, one, today).divide(2.0) == Price.of(usd, half, today)
    assert Price.of(usd, one, today).divide(two) == Price.of(usd, half, today)

    ## Division by zero:
    assert Price.of(usd, one, today).divide(0) == Price.na()
    assert Price.of(usd, one, today).divide(zero) == Price.na()
    assert Price.of(usd, one, today).divide(0.0) == Price.na()

    ## Operator overload:
    assert Price.na() / 1 == Price.na()
    assert Price.of(usd, one, today) / 1 == Price.of(usd, one, today)
    assert Price.of(usd, one, today) / 2 == Price.of(usd, half, today)
    assert Price.of(usd, -one, today) / 1 == Price.of(usd, -one, today)
    assert Price.of(usd, -one, today) / 2 == Price.of(usd, -half, today)
    assert Price.of(usd, -one, today) / 0 == Price.na()


def test_floor_division() -> None:
    ## First use `Price.na()`s:
    assert Price.na().floor_divide(1) == Price.na()

    ## Vanilla subtraction:
    assert Price.of(usd, one, today).floor_divide(1) == Price.of(usd, one, today)
    assert Price.of(usd, one, today).floor_divide(2) == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today).floor_divide(1) == Price.of(usd, -one, today)
    assert Price.of(usd, -one, today).floor_divide(2) == Price.of(usd, zero, today)

    ## Various divisor types:
    assert Price.of(usd, one, today).floor_divide(2) == Price.of(usd, zero, today)
    assert Price.of(usd, one, today).floor_divide(2.0) == Price.of(usd, zero, today)
    assert Price.of(usd, one, today).floor_divide(two) == Price.of(usd, zero, today)

    ## Division by zero:
    assert Price.of(usd, one, today).floor_divide(0) == Price.na()
    assert Price.of(usd, one, today).floor_divide(zero) == Price.na()
    assert Price.of(usd, one, today).floor_divide(0.0) == Price.na()

    ## Operator overload:
    assert Price.na() / 1 == Price.na()
    assert Price.of(usd, one, today) // 1 == Price.of(usd, one, today)
    assert Price.of(usd, one, today) // 2 == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today) // 1 == Price.of(usd, -one, today)
    assert Price.of(usd, -one, today) // 2 == Price.of(usd, zero, today)
    assert Price.of(usd, -one, today) // 0 == Price.na()


def test_comparisons() -> None:
    ## First use `Price.na()`s:
    assert not (Price.na() < Price.na())
    assert Price.na() <= Price.na()
    assert not (Price.na() > Price.na())
    assert Price.na() >= Price.na()

    ## Try mixed:
    assert Price.na() < Price.of(usd, -one, today)
    assert Price.na() <= Price.of(usd, -one, today)
    assert not (Price.na() > Price.of(usd, -one, today))
    assert not (Price.na() >= Price.of(usd, -one, today))

    ## ... and:
    assert not (Price.of(usd, -one, today) < Price.na())
    assert not (Price.of(usd, -one, today) <= Price.na())
    assert Price.of(usd, -one, today) > Price.na()
    assert Price.of(usd, -one, today) >= Price.na()

    ## With defined values:
    assert not (Price.of(usd, zero, today) < Price.of(usd, zero, today))
    assert Price.of(usd, zero, today) <= Price.of(usd, zero, today)
    assert not (Price.of(usd, zero, today) > Price.of(usd, zero, today))
    assert Price.of(usd, zero, today) >= Price.of(usd, zero, today)

    ## ... and:
    assert Price.of(usd, zero, today) < Price.of(usd, one, today)
    assert Price.of(usd, zero, today) <= Price.of(usd, one, today)
    assert not (Price.of(usd, zero, today) > Price.of(usd, one, today))
    assert not (Price.of(usd, zero, today) >= Price.of(usd, one, today))

    ## ... and:
    assert not (Price.of(usd, one, today) < Price.of(usd, zero, today))
    assert not (Price.of(usd, one, today) <= Price.of(usd, zero, today))
    assert Price.of(usd, one, today) > Price.of(usd, zero, today)
    assert Price.of(usd, one, today) >= Price.of(usd, zero, today)


def test_with() -> None:
    ## First use `Price.na()`s:
    assert Price.na().with_ccy(usd) == Price.na()
    assert Price.na().with_qty(one) == Price.na()
    assert Price.na().with_dov(today) == Price.na()

    ## Now with some:
    assert Price.of(usd, zero, today).with_ccy(eur) == Price.of(eur, zero, today)
    assert Price.of(usd, zero, today).with_qty(one) == Price.of(usd, one, today)
    assert Price.of(usd, zero, today).with_dov(yesterday) == Price.of(usd, zero, yesterday)


def test_types() -> None:
    assert isinstance(Price.na(), Price)
    assert isinstance(Price.na(), NonePrice)
    assert not isinstance(Price.na(), SomePrice)
    assert not isinstance(Price.na(), Money)


def test_type_guard() -> None:
    none = Price.na()

    assert Price.is_none(none)
    assert not Price.is_some(none)

    with pytest.raises(AttributeError) as exc:
        none.ccy  # type: ignore[attr-defined]  # pylint: disable=[no-member,pointless-statement]

    assert str(exc.value) == "'NonePrice' object has no attribute 'ccy'"

    some = Price.of(usd, zero, today)

    assert not Price.is_none(some)
    assert Price.is_some(some)
    assert some.ccy == usd
    assert some.qty == zero
    assert some.dov == today
