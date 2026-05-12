from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")

_MISSING = object()


class DynamicArray(Generic[T]):
    """Immutable dynamic array based on tuple storage."""

    __slots__ = ("_items",)

    _items: tuple[T, ...]

    def __init__(self, items: Iterable[T] = ()) -> None:
        object.__setattr__(self, "_items", tuple(items))

    def __setattr__(self, name: str, value: object) -> None:
        if hasattr(self, name):
            raise AttributeError("DynamicArray is immutable")
        object.__setattr__(self, name, value)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DynamicArray):
            return False
        return self._items == other._items

    def __str__(self) -> str:
        return str(list(self._items))

    def __repr__(self) -> str:
        return f"DynamicArray({list(self._items)!r})"


def empty() -> DynamicArray[T]:
    return DynamicArray()


def cons(value: T, array: DynamicArray[T]) -> DynamicArray[T]:
    return DynamicArray((value,) + array._items)


def remove(array: DynamicArray[T], index: int) -> DynamicArray[T]:
    if index < 0 or index >= len(array):
        raise IndexError("index out of range")

    return DynamicArray(array._items[:index] + array._items[index + 1 :])


def length(array: DynamicArray[T]) -> int:
    return len(array)


def member(value: T, array: DynamicArray[T]) -> bool:
    def helper(index: int) -> bool:
        if index == len(array):
            return False
        if array._items[index] == value:
            return True
        return helper(index + 1)

    return helper(0)


def reverse(array: DynamicArray[T]) -> DynamicArray[T]:
    def helper(index: int) -> tuple[T, ...]:
        if index < 0:
            return ()
        return (array._items[index],) + helper(index - 1)

    return DynamicArray(helper(len(array) - 1))


def to_list(array: DynamicArray[T]) -> list[T]:
    return list(array._items)


def from_list(values: list[T]) -> DynamicArray[T]:
    return DynamicArray(values)


def find(array: DynamicArray[T], predicate: Callable[[T], bool]) -> Optional[T]:
    def helper(index: int) -> Optional[T]:
        if index == len(array):
            return None

        current = array._items[index]
        if predicate(current):
            return current

        return helper(index + 1)

    return helper(0)


def filter(
    array: DynamicArray[T],
    predicate: Callable[[T], bool],
) -> DynamicArray[T]:
    def helper(index: int) -> tuple[T, ...]:
        if index == len(array):
            return ()

        current = array._items[index]
        rest = helper(index + 1)

        if predicate(current):
            return (current,) + rest

        return rest

    return DynamicArray(helper(0))


def map(
    array: DynamicArray[T],
    function: Callable[[T], U],
) -> DynamicArray[U]:
    def helper(index: int) -> tuple[U, ...]:
        if index == len(array):
            return ()

        return (function(array._items[index]),) + helper(index + 1)

    return DynamicArray(helper(0))


def reduce(
    array: DynamicArray[T],
    function: Callable[[Any, T], Any],
    initial: Any = _MISSING,
) -> Any:
    if len(array) == 0 and initial is _MISSING:
        raise TypeError("reduce() of empty DynamicArray with no initial value")

    def helper(index: int, accumulator: Any) -> Any:
        if index == len(array):
            return accumulator

        return helper(index + 1, function(accumulator, array._items[index]))

    if initial is _MISSING:
        return helper(1, array._items[0])

    return helper(0, initial)


def concat(
    left: DynamicArray[T],
    right: DynamicArray[T],
) -> DynamicArray[T]:
    return DynamicArray(left._items + right._items)
