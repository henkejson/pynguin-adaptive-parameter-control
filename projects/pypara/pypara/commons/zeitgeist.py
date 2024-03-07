"""
This module defines common date/time typings and functions.
"""

__all__ = [
    "Date",
    "DateRange",
    "DateTime",
    "ensure_date",
    "ensure_datetime",
    "FinancialPeriods",
    "get_month_end",
    "get_month_start",
    "get_now",
    "get_period_starts",
    "get_prev_weekday",
    "get_prev_year_end",
    "get_quarter_end_stream",
    "get_quarter_end",
    "get_quarter_start",
    "get_today",
    "get_tomorrow",
    "get_week_end",
    "get_week_start",
    "get_year_end",
    "get_year_half_end",
    "get_year_half_start",
    "get_year_start",
    "get_yesterday",
    "make_financial_periods",
    "OpenDateRange",
    "PeriodStarts",
    "Time",
    "TimeDelta",
]

from calendar import isleap
from dataclasses import dataclass
from datetime import date as Date
from datetime import datetime as DateTime
from datetime import time as Time
from datetime import timedelta as TimeDelta
from typing import Dict, Iterable, Iterator, Literal, Optional, OrderedDict, Tuple, Union

from dateutil.parser import ParserError, parse
from dateutil.relativedelta import relativedelta

from pypara.commons.numbers import NaturalNumber, PositiveInteger

#: Positive integer 1.
_POS_INT_1 = PositiveInteger(1)


class OpenDateRange:
    """
    Defines a date-range class with inclusive but optional start and end.

    For a date range with both ends open:

    >>> range = OpenDateRange()
    >>> range.start is None
    True
    >>> range.end is None
    True
    >>> range.is_finite
    False
    >>> range.has_start
    False
    >>> range.has_end
    False
    >>> list(range.range)
    []
    >>> range.endpoints
    (None, None)

    For a date range with both ends closed:

    >>> range2 = OpenDateRange(Date(2018, 1, 1), Date(2018, 1, 3))
    >>> range2.start is None
    False
    >>> range2.end is None
    False
    >>> range2.is_finite
    True
    >>> range2.has_start
    True
    >>> range2.has_end
    True
    >>> list(range2.range)
    [datetime.date(2018, 1, 1), datetime.date(2018, 1, 2), datetime.date(2018, 1, 3)]
    >>> range2.endpoints
    (datetime.date(2018, 1, 1), datetime.date(2018, 1, 3))
    """

    def __init__(self, start: Optional[Date] = None, end: Optional[Date] = None) -> None:
        ## Cast the start date:
        self.start = start

        ## Cast the end date:
        self.end = end

    @property
    def is_finite(self) -> bool:
        return self.start is not None and self.end is not None

    @property
    def has_start(self) -> bool:
        return self.start is not None

    @property
    def has_end(self) -> bool:
        return self.end is not None

    @property
    def range(self) -> Iterator[Date]:
        if self.start is None or self.end is None:
            return iter(())
        return self._drange(self.start, self.end)

    @property
    def endpoints(self) -> Tuple[Optional[Date], Optional[Date]]:
        return self.start, self.end

    @staticmethod
    def _drange(start: Date, end: Date) -> Iterator[Date]:
        """
        Returns a date range.
        """
        while start <= end:
            yield start
            start = start + TimeDelta(days=1)


@dataclass(frozen=True)
class DateRange(Iterable[Date]):
    """
    Provides an encoding for date ranges with inclusive date endpoints.

    A :py:class:`DateRange` is essentially a simple value object with two
    fields: :py:attr:`since` and :py:attr:`until`. These denote the start and
    end dates of the date range.

    Once successfully initialized, the value is guaranteed to have the property
    of :py:attr:`until` being equal to or greater than :py:attr:`since`.

    In an attempt to create a :py:class:`DateRange` instance that violates this
    condition, an :py:class:`AssertionError` is raised. In other words, the
    constructor of :py:meth:`DateRange.__init__` is unsafe. The safe alternative
    of creating :py:class:`DateRange` instances is :py:meth:`DateRange.of`. It
    returns a :py:class:`DateRange` instance if the condition is satisfied,
    ``None`` otherwise.

    Below are some examples of successful creation and erroneous attempt of
    creation:

    >>> good = DateRange(Date(2019, 1, 1), Date(2019, 1, 1))
    >>> good.since
    datetime.date(2019, 1, 1)
    >>> good.until
    datetime.date(2019, 1, 1)
    >>> list(good)
    [datetime.date(2019, 1, 1)]
    >>> better = DateRange(Date(2019, 1, 1), Date(2019, 1, 2))
    >>> better.since
    datetime.date(2019, 1, 1)
    >>> better.until
    datetime.date(2019, 1, 2)
    >>> list(better)
    [datetime.date(2019, 1, 1), datetime.date(2019, 1, 2)]
    >>> best = DateRange(Date(2019, 1, 1), Date(2019, 1, 3))
    >>> best.since
    datetime.date(2019, 1, 1)
    >>> best.until
    datetime.date(2019, 1, 3)
    >>> list(best)
    [datetime.date(2019, 1, 1), datetime.date(2019, 1, 2), datetime.date(2019, 1, 3)]

    In case of bad input:

    >>> bad = DateRange(Date(2019, 1, 2), Date(2019, 1, 1))
    Traceback (most recent call last):
    ...
        assert self.since > self.until
    AssertionError

    Therefore, it is advised to use :py:meth:`DateRange.of` instead:

    >>> DateRange.of(Date(2019, 1, 2), Date(2019, 1, 1)) is None
    True
    >>> DateRange.of(Date(2019, 1, 1), Date(2019, 1, 1))
    DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 1))
    """

    #: Date the range starts from (inclusive).
    since: Date

    #: Date the range ends on (inclusive).
    until: Date

    def __post_init__(self) -> None:
        """
        Checks whether the two date endpoints are consistent.

        :raises AssertError: If ``since`` is later than ``until``.
        """
        assert self.since <= self.until

    def __iter__(self) -> Iterator[Date]:
        """
        Returns an iterator for dates within the date-range in ascending order.

        :return: An :py:class:`typing.Iterator` of :py:class:`datetime.date` instances.
        """
        return iter((self.since + TimeDelta(days=i) for i in range(0, (self.until - self.since).days + 1)))

    @property
    def endpoints(self) -> Tuple["Date", "Date"]:
        """
        Endpoints of the date range as a 2-tuple of dates (since, until).

        >>> DateRange(Date(2019, 1, 1), Date(2019, 1, 1)).endpoints
        (datetime.date(2019, 1, 1), datetime.date(2019, 1, 1))
        >>> DateRange(Date(2019, 1, 1), Date(2019, 1, 2)).endpoints
        (datetime.date(2019, 1, 1), datetime.date(2019, 1, 2))
        >>> DateRange(Date(2019, 1, 1), Date(2019, 1, 3)).endpoints
        (datetime.date(2019, 1, 1), datetime.date(2019, 1, 3))
        """
        return (self.since, self.until)

    @classmethod
    def of(cls, since: Date, until: Date) -> Optional["DateRange"]:
        """
        Safe, smart constructor to create :py:class:`DateRange` instances.

        :param since: Start date of the date range.
        :param until: End date of the date range.
        :return: A :py:class:`DateRange` instance if the ``since <= until`` is satisfied, ``None`` otherwise.

        >>> DateRange.of(Date(2019, 1, 2), Date(2019, 1, 1))
        >>> DateRange.of(Date(2019, 1, 1), Date(2019, 1, 1))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 1))
        """
        return cls(since, until) if since <= until else None

    @classmethod
    def ordered(cls, date1: Date, date2: Date) -> "DateRange":
        """
        Safe, smart constructor to create :py:class:`DateRange` instances ensuring the order of dates.

        :param date1: First date.
        :param date2: Second date.
        :return: A :py:class:`DateRange` instance with ``(since, until)`` as ``(date1, date2)`` if ``date1 <= date2``
                 ``(date2, date1)`` otherwise.

        >>> DateRange.ordered(Date(2019, 1, 1), Date(2019, 1, 1))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 1))
        >>> DateRange.ordered(Date(2019, 1, 1), Date(2019, 1, 2))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 2))
        >>> DateRange.ordered(Date(2019, 1, 2), Date(2019, 1, 1))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 2))
        """
        return cls(date1, date2) if date1 <= date2 else cls(date2, date1)

    @classmethod
    def pivotal(cls, pivot: Date, n_prev: NaturalNumber, n_next: NaturalNumber) -> "DateRange":
        """
        Creates a :py:class:`DateRange` as per given ``pivot`` date in time to create date range since ``prev`` years
        back and ``next`` years forward.

        :param pivot: Pivot date in time.
        :param n_prev: Numbers to go back in years.
        :param n_next: Numbers to go forward in years.
        :return: A :py:class:`DateRange` instance.

        >>> DateRange.pivotal(Date(2019, 12, 31), NaturalNumber(0), NaturalNumber(0))
        DateRange(since=datetime.date(2019, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange.pivotal(Date(2019, 12, 31), NaturalNumber(0), NaturalNumber(1))
        DateRange(since=datetime.date(2019, 12, 31), until=datetime.date(2020, 12, 31))
        >>> DateRange.pivotal(Date(2019, 12, 31), NaturalNumber(1), NaturalNumber(0))
        DateRange(since=datetime.date(2018, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange.pivotal(Date(2019, 12, 31), NaturalNumber(1), NaturalNumber(1))
        DateRange(since=datetime.date(2018, 12, 31), until=datetime.date(2020, 12, 31))
        >>> DateRange.pivotal(Date(2020, 2, 29), NaturalNumber(0), NaturalNumber(0))
        DateRange(since=datetime.date(2020, 2, 29), until=datetime.date(2020, 2, 29))
        >>> DateRange.pivotal(Date(2020, 2, 29), NaturalNumber(0), NaturalNumber(1))
        DateRange(since=datetime.date(2020, 2, 29), until=datetime.date(2021, 2, 28))
        >>> DateRange.pivotal(Date(2020, 2, 29), NaturalNumber(1), NaturalNumber(0))
        DateRange(since=datetime.date(2019, 2, 28), until=datetime.date(2020, 2, 29))
        >>> DateRange.pivotal(Date(2020, 2, 29), NaturalNumber(1), NaturalNumber(1))
        DateRange(since=datetime.date(2019, 2, 28), until=datetime.date(2021, 2, 28))
        """
        ## Get the target since date:
        s_y, s_m, s_d = pivot.year - n_prev, pivot.month, pivot.day

        ## Check if (m, d) is a valid one:
        if not isleap(s_y) and s_m == 2 and s_d == 29:
            s_d = 28

        ## Get the target until date:
        u_y, u_m, u_d = pivot.year + n_next, pivot.month, pivot.day

        ## Check if (m, d) is a valid one:
        if not isleap(u_y) and u_m == 2 and u_d == 29:
            u_d = 28

        ## Create the date range and return:
        return cls(Date(s_y, s_m, s_d), Date(u_y, u_m, u_d))

    @classmethod
    def dtd(cls, date: Date) -> "DateRange":
        """
        Returns day-to-date date range as of the given date.

        :param date: To-date.
        :return: Day-to-date (DTD) date range.

        >>> DateRange.dtd(Date(2019, 1, 9))
        DateRange(since=datetime.date(2019, 1, 9), until=datetime.date(2019, 1, 9))
        >>> DateRange.dtd(Date(2020, 3, 1))
        DateRange(since=datetime.date(2020, 3, 1), until=datetime.date(2020, 3, 1))
        >>> DateRange.dtd(Date(2020, 3, 9))
        DateRange(since=datetime.date(2020, 3, 9), until=datetime.date(2020, 3, 9))
        """
        return cls(date, date)

    @classmethod
    def mtd(cls, date: Date) -> "DateRange":
        """
        Returns month-to-date date range as of the given date.

        :param date: To-date.
        :return: Month-to-date (MTD) date range.

        >>> DateRange.mtd(Date(2019, 1, 9))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 9))
        >>> DateRange.mtd(Date(2020, 3, 1))
        DateRange(since=datetime.date(2020, 3, 1), until=datetime.date(2020, 3, 1))
        >>> DateRange.mtd(Date(2020, 3, 9))
        DateRange(since=datetime.date(2020, 3, 1), until=datetime.date(2020, 3, 9))
        """
        return cls(date.replace(day=1), date)

    @classmethod
    def ytd(cls, date: Date) -> "DateRange":
        """
        Returns year-to-date date range as of the given date.

        :param date: To-date.
        :return: Year-to-date (YTD) date range.

        >>> DateRange.ytd(Date(2020, 1, 1))
        DateRange(since=datetime.date(2020, 1, 1), until=datetime.date(2020, 1, 1))
        >>> DateRange.ytd(Date(2019, 1, 9))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 1, 9))
        >>> DateRange.ytd(Date(2020, 3, 1))
        DateRange(since=datetime.date(2020, 1, 1), until=datetime.date(2020, 3, 1))
        """
        return cls(date.replace(month=1, day=1), date)

    @classmethod
    def year(cls, year: PositiveInteger) -> "DateRange":
        """
        Returns a full year date range for the given year.

        :param year: The year.
        :return: Year date range.

        >>> DateRange.year(PositiveInteger(2019))
        DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 12, 31))
        >>> DateRange.year(PositiveInteger(2020))
        DateRange(since=datetime.date(2020, 1, 1), until=datetime.date(2020, 12, 31))
        """
        return cls(Date(year, 1, 1), Date(year, 12, 31))

    @classmethod
    def cover(cls, first: "DateRange", *rest: "DateRange") -> "DateRange":
        """
        Returns the date-range that covers all given date ranges.

        :param first: First date range.
        :param rest: Rest of date ranges.
        :return: A new date range which covers all given date ranges.

        >>> DateRange.cover(DateRange.dtd(Date(2019, 4, 1)), DateRange.mtd(Date(2020, 2, 29)), DateRange.ytd(Date(2018, 3, 6)))  # noqa: E501 pylint: disable=line-too-long
        DateRange(since=datetime.date(2018, 1, 1), until=datetime.date(2020, 2, 29))
        """
        return DateRange(
            min(first, *rest, key=lambda x: x.since).since,  # pyright: ignore [reportGeneralTypeIssues]
            max(first, *rest, key=lambda x: x.until).until,  # pyright: ignore [reportGeneralTypeIssues]
        )

    def since_prev_year_end(self, years: PositiveInteger = _POS_INT_1, weekday: bool = False) -> "DateRange":
        """
        Re-creates the date range starting from the previous ``years`` number of
        years as per :py:attr:`DateRange.since`.

        >>> DateRange(Date(2019, 12, 31), Date(2019, 12, 31)).since_prev_year_end(PositiveInteger(1))
        DateRange(since=datetime.date(2018, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange(Date(2019, 12, 30), Date(2019, 12, 31)).since_prev_year_end(PositiveInteger(1))
        DateRange(since=datetime.date(2018, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange(Date(2019, 12, 30), Date(2019, 12, 31)).since_prev_year_end(PositiveInteger(2))
        DateRange(since=datetime.date(2017, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange(Date(2019, 12, 31), Date(2019, 12, 31)).since_prev_year_end(PositiveInteger(1), True)
        DateRange(since=datetime.date(2018, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange(Date(2019, 12, 30), Date(2019, 12, 31)).since_prev_year_end(PositiveInteger(1), True)
        DateRange(since=datetime.date(2018, 12, 31), until=datetime.date(2019, 12, 31))
        >>> DateRange(Date(2019, 12, 30), Date(2019, 12, 31)).since_prev_year_end(PositiveInteger(2), True)
        DateRange(since=datetime.date(2017, 12, 29), until=datetime.date(2019, 12, 31))

        :param years: Number of years to go back as a positive integer.
        :param weekday: Indicates if we want the year end to be a weekday.
        :return: A new :py:class:`DateRange` instance.
        """
        ## Get the year end as requested:
        yearend = get_prev_year_end(self.since, years)

        ## Create the new date range and return:
        return DateRange(get_prev_weekday(yearend) if weekday and yearend.weekday() in {5, 6} else yearend, self.until)


#: Defines a custom financial periods container.
FinancialPeriods = Dict[str, DateRange]


def make_financial_periods(date: Date, lookback: PositiveInteger) -> FinancialPeriods:
    """
    Creates financial periods for the given date with ``lookback`` number of years.

    :param date: Date to create financial periods for.
    :param lookback: A positive integer describing the number of years to go back.
    :return: A dictionary of financial period label and date range for the financial period.

    >>> sorted(make_financial_periods(Date(2019, 1, 10), PositiveInteger(1)).keys())
    ['2018', 'DTD', 'MTD', 'YTD']
    >>> sorted(make_financial_periods(Date(2019, 1, 10), PositiveInteger(2)).keys())
    ['2017', '2018', 'DTD', 'MTD', 'YTD']
    >>> sorted(make_financial_periods(Date(2019, 1, 10), PositiveInteger(3)).keys())
    ['2016', '2017', '2018', 'DTD', 'MTD', 'YTD']
    >>> sorted(make_financial_periods(Date(2020, 2, 29), PositiveInteger(3)).keys())
    ['2017', '2018', '2019', 'DTD', 'MTD', 'YTD']
    >>> periods = make_financial_periods(Date(2020, 2, 29), PositiveInteger(3))
    >>> periods["DTD"]
    DateRange(since=datetime.date(2020, 2, 29), until=datetime.date(2020, 2, 29))
    >>> periods["MTD"]
    DateRange(since=datetime.date(2020, 2, 1), until=datetime.date(2020, 2, 29))
    >>> periods["YTD"]
    DateRange(since=datetime.date(2020, 1, 1), until=datetime.date(2020, 2, 29))
    >>> periods["2019"]
    DateRange(since=datetime.date(2019, 1, 1), until=datetime.date(2019, 12, 31))
    >>> periods["2018"]
    DateRange(since=datetime.date(2018, 1, 1), until=datetime.date(2018, 12, 31))
    >>> periods["2017"]
    DateRange(since=datetime.date(2017, 1, 1), until=datetime.date(2017, 12, 31))
    """
    ## Get years iterable:
    years = (date.year - i for i in range(1, lookback + 1) if i <= date.year)

    ## Build ranges and return:
    return OrderedDict(
        (
            ("DTD", DateRange.dtd(date)),
            ("MTD", DateRange.mtd(date)),
            ("YTD", DateRange.ytd(date)),
            *((f"{y}", DateRange.year(PositiveInteger(y))) for y in years),
        )
    )


def get_now(**kwargs: int) -> DateTime:
    """
    Returns the current date/time with replacements if provided.

    >>> get_now(year=1981, month=8, day=27, hour=18, minute=19, second=20, microsecond=1)
    datetime.datetime(1981, 8, 27, 18, 19, 20, 1)
    """
    return DateTime.now().replace(**kwargs)  # type: ignore


def get_today(**kwargs: int) -> Date:
    """
    Returns the current date with replacements if provided.

    >>> get_today(year=1981, month=8, day=27)
    datetime.date(1981, 8, 27)
    """
    return Date.today().replace(**kwargs)


def get_yesterday(x: Optional[Date] = None) -> Date:
    """
    Returns yesterday as of given (optional) date.

    >>> get_yesterday() == get_today() - TimeDelta(days=1)
    True
    >>> get_yesterday(Date(2019, 1, 1))
    datetime.date(2018, 12, 31)
    """
    return (x or get_today()) - TimeDelta(days=1)


def get_tomorrow(x: Optional[Date] = None) -> Date:
    """
    Returns tomorrow as of given (optional) date.

    >>> get_tomorrow() == get_today() + TimeDelta(days=1)
    True
    >>> get_tomorrow(Date(2018, 12, 31))
    datetime.date(2019, 1, 1)
    """
    return (x or get_today()) + TimeDelta(days=1)


def get_prev_weekday(x: Optional[Date] = None) -> Date:
    """
    Returns the previous week day as of given (optional) date.

    :param x: Optional date in time.
    :return: Previous business day.

    >>> get_prev_weekday(Date(2020, 1, 1))
    datetime.date(2019, 12, 31)
    >>> get_prev_weekday(Date(2020, 1, 2))
    datetime.date(2020, 1, 1)
    >>> get_prev_weekday(Date(2020, 1, 3))
    datetime.date(2020, 1, 2)
    >>> get_prev_weekday(Date(2020, 1, 4))
    datetime.date(2020, 1, 3)
    >>> get_prev_weekday(Date(2020, 1, 5))
    datetime.date(2020, 1, 3)
    >>> get_prev_weekday(Date(2020, 1, 6))
    datetime.date(2020, 1, 3)
    >>> get_prev_weekday(Date(2020, 1, 7))
    datetime.date(2020, 1, 6)
    """
    ## Get the day:
    x = x or get_today()

    ## Define the offset:
    offset = max(1, (x.weekday() + 6) % 7 - 3)

    ## Compute the day and return:
    return x - TimeDelta(days=offset)


def get_prev_year_end(x: Optional[Date] = None, years: PositiveInteger = _POS_INT_1) -> Date:
    """
    Returns the year end of the previous year as of given (optional) date.

    >>> get_prev_year_end() == Date(get_today().year - 1, 12, 31)
    True
    >>> get_prev_year_end(Date(2019, 1, 1))
    datetime.date(2018, 12, 31)
    >>> get_prev_year_end(Date(2018, 12, 31))
    datetime.date(2017, 12, 31)
    >>> get_prev_year_end(Date(2018, 12, 31), PositiveInteger(2))
    datetime.date(2016, 12, 31)
    """
    return Date((x or get_today()).year - years, 12, 31)


def get_year_start(x: Optional[Date] = None) -> Date:
    """
    Returns the start of the year as of the given date.

    >>> get_year_start(Date(2017, 1, 1))
    datetime.date(2017, 1, 1)
    >>> get_year_start(Date(2017, 7, 29))
    datetime.date(2017, 1, 1)
    >>> get_year_start(Date(2017, 12, 31))
    datetime.date(2017, 1, 1)
    """
    return (x or get_today()).replace(month=1, day=1)


def get_year_end(x: Optional[Date] = None) -> Date:
    """
    Returns the start of the year as of the given date.

    >>> get_year_end(Date(2017, 1, 1))
    datetime.date(2017, 12, 31)
    >>> get_year_end(Date(2017, 7, 29))
    datetime.date(2017, 12, 31)
    >>> get_year_end(Date(2017, 12, 31))
    datetime.date(2017, 12, 31)
    """
    return (x or get_today()).replace(month=12, day=31)


def get_year_half_start(x: Optional[Date] = None) -> Date:
    """
    Returns the half year start as of the given date.

    >>> get_year_half_start(Date(2017, 1, 1))
    datetime.date(2017, 1, 1)
    >>> get_year_half_start(Date(2017, 5, 31))
    datetime.date(2017, 1, 1)
    >>> get_year_half_start(Date(2017, 6, 30))
    datetime.date(2017, 1, 1)
    >>> get_year_half_start(Date(2017, 7, 1))
    datetime.date(2017, 7, 1)
    >>> get_year_half_start(Date(2017, 7, 29))
    datetime.date(2017, 7, 1)
    >>> get_year_half_start(Date(2017, 12, 31))
    datetime.date(2017, 7, 1)
    """
    asof = x or get_today()
    return asof.replace(month=((asof.month - 1) // 6) * 6 + 1, day=1)


def get_year_half_end(x: Optional[Date] = None) -> Date:
    """
    Returns the half year end as of the given date.

    >>> get_year_half_end(Date(2017, 1, 1))
    datetime.date(2017, 6, 30)
    >>> get_year_half_end(Date(2017, 5, 31))
    datetime.date(2017, 6, 30)
    >>> get_year_half_end(Date(2017, 6, 30))
    datetime.date(2017, 6, 30)
    >>> get_year_half_end(Date(2017, 7, 1))
    datetime.date(2017, 12, 31)
    >>> get_year_half_end(Date(2017, 7, 29))
    datetime.date(2017, 12, 31)
    >>> get_year_half_end(Date(2017, 12, 31))
    datetime.date(2017, 12, 31)
    """
    return get_year_half_start(x or get_today()) + relativedelta(months=+6, days=-1)


def get_quarter_start(x: Optional[Date] = None) -> Date:
    """
    Returns the quarter start as of the given date.

    >>> get_quarter_start(Date(2017, 1, 1))
    datetime.date(2017, 1, 1)
    >>> get_quarter_start(Date(2017, 5, 31))
    datetime.date(2017, 4, 1)
    >>> get_quarter_start(Date(2017, 6, 30))
    datetime.date(2017, 4, 1)
    >>> get_quarter_start(Date(2017, 7, 1))
    datetime.date(2017, 7, 1)
    >>> get_quarter_start(Date(2017, 7, 29))
    datetime.date(2017, 7, 1)
    >>> get_quarter_start(Date(2017, 12, 31))
    datetime.date(2017, 10, 1)
    """
    asof = x or get_today()
    return asof.replace(month=(asof.month - 1) // 3 * 3 + 1, day=1)


def get_quarter_end(x: Optional[Date] = None) -> Date:
    """
    Returns the quarter end as of the given date.

    >>> get_quarter_end(Date(2017, 1, 1))
    datetime.date(2017, 3, 31)
    >>> get_quarter_end(Date(2017, 5, 31))
    datetime.date(2017, 6, 30)
    >>> get_quarter_end(Date(2017, 6, 30))
    datetime.date(2017, 6, 30)
    >>> get_quarter_end(Date(2017, 7, 1))
    datetime.date(2017, 9, 30)
    >>> get_quarter_end(Date(2017, 7, 29))
    datetime.date(2017, 9, 30)
    >>> get_quarter_end(Date(2017, 9, 30))
    datetime.date(2017, 9, 30)
    >>> get_quarter_end(Date(2017, 10, 1))
    datetime.date(2017, 12, 31)
    >>> get_quarter_end(Date(2017, 12, 31))
    datetime.date(2017, 12, 31)
    """
    return get_quarter_start(x or get_today()) + relativedelta(months=+3, days=-1)


def get_month_start(x: Optional[Date] = None) -> Date:
    """
    Returns the start of the month as of the given date.

    >>> get_month_start(Date(2017, 2, 1))
    datetime.date(2017, 2, 1)
    >>> get_month_start(Date(2017, 2, 2))
    datetime.date(2017, 2, 1)
    >>> get_month_start(Date(2017, 3, 31))
    datetime.date(2017, 3, 1)
    """
    return (x or get_today()).replace(day=1)


def get_month_end(x: Optional[Date] = None) -> Date:
    """
    Returns the end of the month as of the given date.

    >>> get_month_end(Date(2017, 1, 1))
    datetime.date(2017, 1, 31)
    >>> get_month_end(Date(2017, 1, 2))
    datetime.date(2017, 1, 31)
    >>> get_month_end(Date(2017, 1, 31))
    datetime.date(2017, 1, 31)
    >>> get_month_end(Date(2017, 2, 1))
    datetime.date(2017, 2, 28)
    >>> get_month_end(Date(2017, 3, 1))
    datetime.date(2017, 3, 31)
    """
    return (x or get_today()).replace(day=1) + relativedelta(months=+1, days=-1)


def get_week_start(x: Optional[Date] = None) -> Date:
    """
    Returns the start of the week as of the given date.

    >>> get_week_start(Date(2017, 1, 15))
    datetime.date(2017, 1, 9)
    >>> get_week_start(Date(2017, 1, 16))
    datetime.date(2017, 1, 16)
    >>> get_week_start(Date(2017, 1, 18))
    datetime.date(2017, 1, 16)
    """
    asof = x or get_today()
    return asof - TimeDelta(days=(asof.isoweekday() - 1) % 7)


def get_week_end(x: Optional[Date] = None) -> Date:
    """
    Returns the end of the week as of the given date.

    >>> get_week_end(Date(2017, 1, 15))
    datetime.date(2017, 1, 15)
    >>> get_week_end(Date(2017, 1, 16))
    datetime.date(2017, 1, 22)
    >>> get_week_end(Date(2017, 1, 18))
    datetime.date(2017, 1, 22)
    >>> get_week_end(Date(2017, 1, 17))
    datetime.date(2017, 1, 22)
    >>> get_week_end(Date(2017, 1, 22))
    datetime.date(2017, 1, 22)
    """
    asof = x or get_today()
    return asof + TimeDelta(days=6 - (asof.isoweekday() - 1) % 7)


#: Type encoding for a lookup table of period starts.
PeriodStarts = Dict[
    Literal["year_start", "half_start", "quarter_start", "month_start", "week_start", "yesterday"], Date
]


def get_period_starts(x: Optional[Date] = None) -> PeriodStarts:
    """
    Returns important dates as of the given date.

    >>> get_period_starts(Date(2018, 8, 19))["year_start"]
    datetime.date(2018, 1, 1)
    >>> get_period_starts(Date(2018, 8, 19))["half_start"]
    datetime.date(2018, 7, 1)
    >>> get_period_starts(Date(2018, 8, 19))["quarter_start"]
    datetime.date(2018, 7, 1)
    >>> get_period_starts(Date(2018, 8, 19))["month_start"]
    datetime.date(2018, 8, 1)
    >>> get_period_starts(Date(2018, 8, 19))["week_start"]
    datetime.date(2018, 8, 13)
    >>> get_period_starts(Date(2018, 8, 19))["yesterday"]
    datetime.date(2018, 8, 18)
    """
    asof = x or get_today()
    return OrderedDict(
        [
            ("year_start", get_year_start(asof)),
            ("half_start", get_year_half_start(asof)),
            ("quarter_start", get_quarter_start(asof)),
            ("month_start", get_month_start(asof)),
            ("week_start", get_week_start(asof)),
            ("yesterday", asof - TimeDelta(days=1)),
        ]
    )


def get_quarter_end_stream(x: Optional[Date] = None) -> Iterator[Date]:
    """
    Returns a descending stream of quarter end dates.

    >>> from itertools import islice
    >>> list(islice(get_quarter_end_stream(Date(2018, 8, 12)), 3))
    [datetime.date(2018, 6, 30), datetime.date(2018, 3, 31), datetime.date(2017, 12, 31)]
    """
    ## Get asof date:
    asof = x or get_today()

    ## Get the last quarter end:
    e = get_quarter_start(asof) - TimeDelta(days=1)

    ## Yield this:
    yield e

    ## Forever:
    while True:
        e = get_month_end(e - relativedelta(months=3))
        yield e


def ensure_datetime(value: Union[Date, DateTime, str], **kwargs: int) -> DateTime:
    """
    Attempts to convert the value to a `datetime.datetime` instance
    with the date/time fields replaced by `kwargs` if given.

    >>> ensure_datetime(Date(2015, 10, 10))
    datetime.datetime(2015, 10, 10, 0, 0)
    >>> ensure_datetime(DateTime(2015, 10, 10))
    datetime.datetime(2015, 10, 10, 0, 0)
    >>> ensure_datetime("2015-10-10")
    datetime.datetime(2015, 10, 10, 0, 0)
    >>> ensure_datetime(DateTime(2015, 10, 10), hour=12)
    datetime.datetime(2015, 10, 10, 12, 0)
    >>> ensure_datetime(DateTime(2015, 10, 10), minute=59)
    datetime.datetime(2015, 10, 10, 0, 59)
    >>> ensure_datetime("2015-10-10", second=30)
    datetime.datetime(2015, 10, 10, 0, 0, 30)
    >>> ensure_datetime("2015-10-10", second=0)
    datetime.datetime(2015, 10, 10, 0, 0)
    >>> ensure_datetime("2015-10-10", microsecond=10)
    datetime.datetime(2015, 10, 10, 0, 0, 0, 10)
    >>> ensure_datetime("A")
    Traceback (most recent call last):
    ...
    ValueError: Can not parse value into a date/time object: A
    >>> ensure_datetime(1)
    Traceback (most recent call last):
    ...
    ValueError: Don't know how to convert value to date/time object: 1
    """
    ## Check the type of the value and act accordingly.
    if isinstance(value, DateTime):
        ## It is a datetime instance. Nothing to be done. Just return with replacement:
        return value.replace(**kwargs)  # type: ignore
    elif isinstance(value, Date):
        ## It is a date instance. Set to morning and return with replacement:
        return DateTime.combine(value, DateTime.min.time()).replace(**kwargs)  # type: ignore
    elif isinstance(value, str):
        ## We have a string. Attempt to parse and return with replacement:
        try:
            return parse(value).replace(**kwargs)  # type: ignore
        except ParserError:
            raise ValueError("Can not parse value into a date/time object: {}".format(value))

    ## We have a problem here: Don't know how to convert other
    ## object. Raise a value error:
    raise ValueError("Don't know how to convert value to date/time object: {}".format(value))


def ensure_date(value: Union[Date, DateTime, str], **kwargs: int) -> Date:
    """
    Attempts to convert the value to a `datetime.date` instance with the
    date fields replaced by `kwargs` if given.

    >>> ensure_date(DateTime(2015, 10, 10))
    datetime.date(2015, 10, 10)

    >>> ensure_date(DateTime(2015, 10, 10))
    datetime.date(2015, 10, 10)

    >>> ensure_date("2015-10-10")
    datetime.date(2015, 10, 10)

    >>> ensure_date(DateTime(2015, 10, 10), hour=12)
    datetime.date(2015, 10, 10)

    >>> ensure_date(DateTime(2015, 10, 10), minute=59)
    datetime.date(2015, 10, 10)

    >>> ensure_date("2015-10-10", second=30)
    datetime.date(2015, 10, 10)

    >>> ensure_date("2015-10-10", second=0)
    datetime.date(2015, 10, 10)

    >>> ensure_date("2015-10-10", microsecond=10)
    datetime.date(2015, 10, 10)
    """
    return ensure_datetime(value, **kwargs).date()
