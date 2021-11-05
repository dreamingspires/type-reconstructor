# Welcome to Type Reconstructor!

This library was made to allow users to replace elements of type hints, in a find and replace style.

# Installation

`pip install type-reconstructor`

or

`poetry add type-reconstructor`

# Usage

Suppose I want to replace all instance of `str` with `bool` in the type hint: `Union[List[str], str]`

With type reconstructor this is easy, and requires no knowledge of the type hint structure.

```py
from type_reconstructor import extract_element

test_type = Union[List[str], str]

def condition(test: type) -> bool:
    return test == str

string, reconstruct_type = extract_element(test_type, condition)
print(string)
# <class 'str'>
print(reconstruct_type(bool))
# Union[List[bool], bool]
```