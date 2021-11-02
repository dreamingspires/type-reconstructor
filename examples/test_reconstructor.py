from type_reconstructor import extract_element
from typing import Callable, TypeVar, Union, List, Tuple, Optional, Literal, Type, Dict
test = TypeVar('test')

test_type = Union[Optional[List[str]], Tuple[int,str], Literal['test'], Dict[str, int], Type[int], Callable[[str, int], str], test]
print(test_type)
def condition(test: type) -> bool:
    return test == str

string, reconstruct_type = extract_element(test_type, condition)

print(reconstruct_type(bool))
