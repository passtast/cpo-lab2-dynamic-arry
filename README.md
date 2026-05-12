# Lab 2: Immutable Dynamic Array

## Description

This laboratory work implements an immutable dynamic array in Python.

The main idea is that every operation returns a new `DynamicArray` object
instead of changing the existing one.

## Project structure

- `dynamic_array.py`: implementation of the immutable dynamic array.
- `dynamic_array_test.py`: unit tests and property-based tests.
- `README.md`: project documentation.

## Features

- Immutable `DynamicArray` object.
- `cons` operation.
- `remove` operation by index.
- `length` operation.
- `member` operation.
- `reverse` operation.
- `to_list` and `from_list` conversion.
- `find` operation.
- `filter` operation.
- `map` operation.
- `reduce` operation.
- `empty` operation.
- `concat` operation.
- Iterator support.
- Equality support with `__eq__`.
- String serialization with `__str__`.

## Design notes

The internal storage is implemented with a tuple.

A tuple is used because it is immutable in Python. This helps prevent accidental
in-place changes. Operations such as `cons`, `remove`, `reverse`, `map`,
`filter`, and `concat` construct and return new `DynamicArray` objects.

Some functions are implemented recursively to follow the laboratory work
requirements. One implementation limitation is Python's recursion depth limit,
which may affect very large arrays.

The `remove` operation removes an element by index because the dynamic array
API test uses index-based removal.

## Testing

The project includes:

- the API test from the laboratory work description;
- additional unit tests for immutability and edge cases;
- property-based tests with Hypothesis.

## Contribution

- Yu Xintong: implementation, tests, and documentation.

## Changelog

### Initial submission

- Implemented immutable `DynamicArray`.
- Added functional-style API.
- Added unit tests.
- Added property-based tests.
- Updated README documentation.