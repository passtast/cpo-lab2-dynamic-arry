import pytest
from hypothesis import given
from hypothesis import strategies as st

from dynamic_array import (
    DynamicArray,
    concat,
    cons,
    empty,
    filter as da_filter,
    find,
    from_list,
    length,
    map as da_map,
    member,
    reduce as da_reduce,
    remove,
    reverse,
    to_list,
)


def test_api() -> None:
    empty_array: DynamicArray[object] = DynamicArray()
    l1 = cons(None, cons(1, empty_array))
    l2 = cons(1, cons(None, empty_array))

    assert str(empty_array) == "[]"
    assert str(l1) == "[None, 1]"
    assert str(l2) == "[1, None]"

    assert empty_array != l1
    assert empty_array != l2
    assert l1 != l2
    assert l1 == cons(None, cons(1, empty_array))

    assert length(empty_array) == 0
    assert length(l1) == 2
    assert length(l2) == 2

    assert str(remove(l1, 0)) == "[1]"
    assert str(remove(l1, 1)) == "[None]"

    assert not member(None, empty_array)
    assert member(None, l1)
    assert member(1, l1)
    assert not member(2, l1)

    assert l1 == reverse(l2)

    assert to_list(l1) == [None, 1]
    assert l1 == from_list([None, 1])

    assert concat(l1, l2) == from_list([None, 1, 1, None])

    buf = []
    for e in l1:
        buf.append(e)
    assert buf == [None, 1]

    lst = to_list(l1) + to_list(l2)
    for e in l1:
        lst.remove(e)
    for e in l2:
        lst.remove(e)
    assert lst == []


def test_empty_function() -> None:
    assert empty() == DynamicArray()
    assert str(empty()) == "[]"


def test_cons_does_not_change_original_array() -> None:
    original = from_list([1, 2])
    updated = cons(0, original)

    assert to_list(original) == [1, 2]
    assert to_list(updated) == [0, 1, 2]


def test_remove_does_not_change_original_array() -> None:
    original = from_list([1, 2, 3])
    updated = remove(original, 1)

    assert to_list(original) == [1, 2, 3]
    assert to_list(updated) == [1, 3]


def test_reverse_does_not_change_original_array() -> None:
    original = from_list([1, 2, 3])
    updated = reverse(original)

    assert to_list(original) == [1, 2, 3]
    assert to_list(updated) == [3, 2, 1]


def test_remove_invalid_index() -> None:
    array = from_list([1, 2, 3])

    with pytest.raises(IndexError):
        remove(array, -1)

    with pytest.raises(IndexError):
        remove(array, 3)


def test_find_filter_map_reduce() -> None:
    array = from_list([1, 2, 3, 4])

    assert find(array, lambda x: x > 2) == 3
    assert find(array, lambda x: x > 10) is None

    assert to_list(da_filter(array, lambda x: x % 2 == 0)) == [2, 4]
    assert to_list(da_map(array, lambda x: x * 10)) == [10, 20, 30, 40]
    assert da_reduce(array, lambda acc, x: acc + x, 0) == 10


def test_reduce_without_initial_value() -> None:
    array = from_list([1, 2, 3])

    assert da_reduce(array, lambda acc, x: acc + x) == 6


def test_reduce_empty_without_initial_value() -> None:
    with pytest.raises(TypeError):
        da_reduce(empty(), lambda acc, x: acc + x)


@given(st.lists(st.integers()))
def test_from_list_to_list_identity(values: list[int]) -> None:
    assert to_list(from_list(values)) == values


@given(st.lists(st.integers()))
def test_length_is_equal_to_python_list_length(values: list[int]) -> None:
    assert length(from_list(values)) == len(values)


@given(st.lists(st.integers()))
def test_reverse_is_equal_to_python_reverse(values: list[int]) -> None:
    assert to_list(reverse(from_list(values))) == list(reversed(values))


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_concat_is_equal_to_python_list_concat(
    left: list[int],
    right: list[int],
) -> None:
    assert to_list(concat(from_list(left), from_list(right))) == left + right


@given(st.lists(st.integers()))
def test_concat_has_empty_identity(values: list[int]) -> None:
    array = from_list(values)
    empty_array: DynamicArray[int] = empty()

    assert concat(empty_array, array) == array
    assert concat(array, empty_array) == array


@given(
    st.lists(st.integers()),
    st.lists(st.integers()),
    st.lists(st.integers()),
)
def test_concat_is_associative(
    first_values: list[int],
    second_values: list[int],
    third_values: list[int],
) -> None:
    first = from_list(first_values)
    second = from_list(second_values)
    third = from_list(third_values)

    left_result = concat(concat(first, second), third)
    right_result = concat(first, concat(second, third))

    assert left_result == right_result


@given(st.integers(), st.lists(st.integers()))
def test_cons_adds_value_to_head(value: int, values: list[int]) -> None:
    array = from_list(values)
    updated = cons(value, array)

    assert to_list(updated) == [value] + values
    assert to_list(array) == values


@given(st.lists(st.integers(), min_size=1), st.integers())
def test_remove_by_index_is_equal_to_python_list(
    values: list[int],
    raw_index: int,
) -> None:
    index = raw_index % len(values)
    array = from_list(values)

    expected = values[:index] + values[index + 1:]
    actual = to_list(remove(array, index))

    assert actual == expected
    assert to_list(array) == values


@given(st.lists(st.integers()))
def test_map_is_equal_to_python_list_comprehension(
    values: list[int],
) -> None:
    array = from_list(values)

    actual = to_list(da_map(array, lambda x: x + 1))
    expected = [x + 1 for x in values]

    assert actual == expected


@given(st.lists(st.integers()))
def test_filter_is_equal_to_python_list_comprehension(
    values: list[int],
) -> None:
    array = from_list(values)

    actual = to_list(da_filter(array, lambda x: x % 2 == 0))
    expected = [x for x in values if x % 2 == 0]

    assert actual == expected


@given(st.lists(st.integers()))
def test_reduce_sum_is_equal_to_python_sum(values: list[int]) -> None:
    array = from_list(values)

    assert da_reduce(array, lambda acc, x: acc + x, 0) == sum(values)
