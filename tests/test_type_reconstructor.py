import pytest
from type_reconstructor import extract_element
from typing import Callable, TypeVar, Union, List, Tuple, Optional, Literal, Type, Dict, Generic

@pytest.mark.asyncio
class TestTypeReconstructor:
    async def test_full(self):
        test_type = Union[Optional[List[str]], Tuple[int,str], Literal['test'], Dict[str, int], Type[int], Callable[[str, str, int], str]]
        def condition(test: type) -> bool:
            return test == str
        string, reconstruct_type = extract_element(test_type, condition)
        assert reconstruct_type(bool) == Union[Optional[List[bool]], Tuple[int,bool], Literal['test'], Dict[bool, int], Type[int], Callable[[bool, bool, int], bool]]
        assert string == str

    async def test_more_than_one_result(self):
        class Base:
            pass
        class SubType1(Base):
            pass
        class SubType2(Base):
            pass
        test_type = Union[Optional[List[SubType1]], Tuple[int,SubType2]]
        def condition(test: type) -> bool:
            try:
                return issubclass(test, Base)
            except TypeError:
                return False
        try:
            string, reconstruct_type = extract_element(test_type, condition)
        except ValueError as e:
            assert str(e) == 'More than one extraction element found'

    async def test_more_than_one_sub_result(self):
        class Base:
            pass
        class SubType1(Base):
            pass
        class SubType2(Base):
            pass
        test_type = Callable[[SubType1, SubType2], bool]
        def condition(test: type) -> bool:
            try:
                return issubclass(test, Base)
            except TypeError:
                return False
        try:
            string, reconstruct_type = extract_element(test_type, condition)
        except ValueError as e:
            assert str(e) == 'More than one extraction sub element found'

    async def test_element_not_found(self):
        class Base:
            pass
        test_type = Callable[[str, str], bool]
        def condition(test: type) -> bool:
            try:
                return issubclass(test, Base)
            except TypeError:
                return False
        try:
            string, reconstruct_type = extract_element(test_type, condition)
        except ValueError as e:
            assert str(e) == 'Element not found'

    async def test_single_sub_result(self):
        class Base:
            pass
        class SubType1(Base):
            pass
        test_type = Callable[[SubType1], bool]
        def condition(test: type) -> bool:
            try:
                return issubclass(test, Base)
            except TypeError:
                return False

        string, reconstruct_type = extract_element(test_type, condition)

    async def test_generic_origin(self):
        string = TypeVar('string')
        class Base(Generic[string]):
            pass
        test_type = Base[Base[bool]]
        def condition(test: type) -> bool:
            return test == bool
        string, reconstruct_type = extract_element(test_type, condition)
        assert reconstruct_type(str) == Base[Base[str]]
        print(reconstruct_type(str))

    async def test_generic_in_type(self):
        string = TypeVar('string')
        class Base(Generic[string]):
            pass
        test_type = List[Base]
        def condition(test: type) -> bool:
            return issubclass(test,Base)

        string, reconstruct_type = extract_element(test_type, condition)
        assert reconstruct_type(str) == List[str]
