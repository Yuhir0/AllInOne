from typing import Any


class NoneSafe:
    """
    Use this to avoid None object has no attribute 'x' whithout using if comparsion
    >>> NoneSafe(MyObject).my_attribute.__safe__

    It works for methods to
    >>> NoneSafe(MyObject).my_method().__

    And it coul be stacked
    >>> ~NoneSafe(MyObject).my_attribute.my_method()
    """
    def __init__(self, obj: Any) -> None:
        self.__safe: Any = obj

    @property
    def __safe__(self) -> Any:
        return self.__safe

    @property
    def __(self) -> Any:
        return self.__safe__

    def __invert__(self) -> Any:
        return self.__safe__

    def __getattribute__(self, attr_name: str) -> 'NoneSafe':
        try:
            return super(NoneSafe, self).__getattribute__(attr_name)
        except AttributeError:
            obj = self.__safe
            if obj is not None:
                return NoneSafe(obj.__getattribute__(attr_name))
            return NoneSafe(None)

    def __call__(self, *args, **kwargs) -> 'NoneSafe':
        if self.__safe is not None:
            return NoneSafe(self.__safe(*args, **kwargs))
        return NoneSafe(None)
