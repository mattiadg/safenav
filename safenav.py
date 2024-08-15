from typing import TypeVar


class SafeNavigation:
    def __getattribute__(self, item):
        try:
            obj = super().__getattribute__(item)
            return make_safenav(obj)
        except AttributeError:
            return super().__getattribute__(item)

    def __getattr__(self, item):
        return SafeNone()


T = TypeVar("T")


def make_safenav(obj: T) -> T:
    orig_cls = type(obj)
    try:
        cls_dict = {"__new__": normal_new, "__init__": normal_init}
        __dict = obj.__dict__
    except AttributeError:
        cls_dict = {"__new__": builtin_new}

    safe_cls = type(orig_cls.__name__ + "_safe", (orig_cls, SafeNavigation), cls_dict)
    obj1 = safe_cls(obj)
    return obj1


class SafeNone(SafeNavigation):
    def __str__(self):
        return "None"

    def __repr__(self):
        return "None"

    def __bool__(self):
        return False


def builtin_new(cls, value):
    return super(cls, cls).__new__(cls, value)


def normal_new(cls, obj):
    new_obj = super(cls, cls).__new__(cls)
    new_obj.__dict__ = obj.__dict__
    return new_obj


def normal_init(self, other):
    self.__dict__ = other.__dict__
