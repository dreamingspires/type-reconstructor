from typing import Callable, Dict, List, Tuple, Union, Type, Optional#, get_args, get_origin
from collections.abc import Callable as CollectionsCallable
from typing_extensions import get_args, get_origin

def _get_origin_advanced(tp: type):
    origin = get_origin(tp)
    if origin == list:
        return List
    elif origin == tuple:
        return Tuple
    elif origin == dict:
        return Dict
    elif origin == type:
        return Type
    elif origin == CollectionsCallable:
        return Callable
    else:
        return origin

ElementType = type
ReconstructorFunc = Callable[[ElementType], type]

def extract_element(start_type: type, condition_callback: Callable[[ElementType], bool]) -> Tuple[ElementType, ReconstructorFunc]:
    """
    Takes a type, and the condition to extract
    Returns tuple of:
    Extracted element
    Function that takes extracted element and wraps in outer types
    """
    EllipsisType = type(...)
    TypeReconstructor = Union[EllipsisType, type, Tuple[type, List['TypeReconstructor']]]
    def get_type_reconstructor(tp: type) -> Tuple[TypeReconstructor, Optional[ElementType]]:
        args = list(get_args(tp))
        origin = _get_origin_advanced(tp)
        if args == [] or origin is None:
            if condition_callback(tp):
                return ..., tp
            else:
                return tp, None
        else:
            possible_elements = []
            new_args = []
            for arg in args:
                # TODO Allow for case where arg is a list in callable
                type_reconstructor, element = get_type_reconstructor(arg)
                if element is not None:
                    possible_elements += [element]
                new_args += [type_reconstructor]
            if len(possible_elements)>1:
                if len(set(possible_elements))> 1:
                    raise ValueError('More than one extraction element found')
                else:
                    relevant_element = possible_elements[0]
            elif len(possible_elements) == 1:
                relevant_element = possible_elements[0]
            else:
                relevant_element = None
            return (origin, new_args), relevant_element

    def get_reconstruct_type(type_reconstructor: TypeReconstructor):
        def reconstruct_type(tp: ElementType):                
            def func_type_inner(current_type_reconstructor: TypeReconstructor) -> type:
                if isinstance(current_type_reconstructor, EllipsisType):
                    return tp
                elif isinstance(current_type_reconstructor, tuple):
                    origin = current_type_reconstructor[0]
                    args = current_type_reconstructor[1]
                    new_args = []
                    for arg in args:
                        new_arg = func_type_inner(arg)
                        new_args += [new_arg]
                    if hasattr(origin, '__getitem__'):
                        return origin[tuple(new_args)] #type:ignore
                    else:
                        raise ValueError('Origin invalid')
                else:
                    return current_type_reconstructor
            return func_type_inner(type_reconstructor)
        return reconstruct_type

    type_reconstructor, element = get_type_reconstructor(start_type)
    if element is None:
        raise ValueError('Element not found')
    reconstruct_type = get_reconstruct_type(type_reconstructor)
    return element, reconstruct_type