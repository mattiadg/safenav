from types import NoneType
from typing import TypeVar


class SafeNavigation:
    def __getattribute__(self, item):
        obj = super().__getattribute__(item)
        return make_safenav(obj)

    def __getattr__(self, item):
        return SafeNone()

    def __getitem__(self, item):
        try:
            obj = super().__getitem__(item)
            return make_safenav(obj)
        except (AttributeError, KeyError):
            return SafeNone()


T = TypeVar("T")


def make_safenav(obj: T) -> T:
    if obj is None:
        return SafeNone()
    orig_cls = type(obj)
    try:
        cls_dict = {"__new__": normal_new, "__init__": normal_init}
        __dict = obj.__dict__
    except AttributeError:
        cls_dict = {"__new__": builtin_new}

    safe_cls = type(orig_cls.__name__ + "_safe", (SafeNavigation, orig_cls), cls_dict)
    obj1 = safe_cls(obj)
    return obj1


class SafeNone(SafeNavigation):
    def __str__(self):
        return "None"

    def __repr__(self):
        return "None"

    def __bool__(self):
        return False

    def __eq__(self, other):
        if isinstance(other, (SafeNone, NoneType)):
            return True
        return False


def builtin_new(cls, value):
    return super(cls, cls).__new__(cls, value)


def normal_new(cls, obj):
    new_obj = super(cls, cls).__new__(cls)
    new_obj.__dict__ = obj.__dict__
    return new_obj


def normal_init(self, other):
    self.__dict__ = other.__dict__
