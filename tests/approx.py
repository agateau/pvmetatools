from typing import Any, Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Comparable(Protocol[T_co]):
    def __lt__(self, value: Any, /) -> bool:
        ...

    def __le__(self, value: Any, /) -> bool:
        ...


class Approx:
    """
    A class to wrap a value to test for "A approximately equals B".


    >>> 14 == Approx(12, 15)
    True
    >>> 14 == Approx(12, 13)
    False
    >>> "b" == Approx("a", "c")
    True
    >>> "b" == Approx(1, 2)
    Traceback (most recent call last):
        ...
    NotImplementedError
    """

    def __init__(self, minv: Comparable[T_co], maxv: Comparable[T_co]) -> None:
        self.type = type(minv)
        self.minv = minv
        self.maxv = maxv

    def __eq__(self, value: Any, /) -> bool:
        if not isinstance(value, self.type):
            raise NotImplementedError

        return self.minv <= value < self.maxv
