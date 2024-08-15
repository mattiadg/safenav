# Safe Navigation

This is an example code, not an installable library, that shows how we can concatenate operations like 
getting an attribute or indexing, while not crashing the program if None or an Exception shows up somewhere.

## Code
The sample class that allows everything is defined in safenav.py:

```python
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
```

It is a mixin: when another class inherits from it, it obtains the functionalities enabled by this class.  
But fear not! You don't need to add this class as a parent to all your classes, you can just use the function 
`make_safenav` on any object to make a copy with this mixin!

## Usage
The use cases are shown in tests.py:

```python
from safenav import make_safenav, SafeNavigation, SafeNone


def test_chain_none_attr():
    assert make_safenav(None).x.y == SafeNone()


def test_chain_none_item():
    assert make_safenav(None)["item1"]["item2"] == SafeNone()


def test_good_values():
    elem = make_safenav([1, "two", {"three": 3}])
    assert elem.x == SafeNone()
    assert isinstance(elem[0], SafeNavigation)
    assert elem[0] == 1
    assert len(elem[1]) == 3
    assert elem[2]["three"] == 3
    assert isinstance(elem[2]["three"], SafeNavigation)
    assert elem[2]["one"] == SafeNone()
```

This can help to simplify coding situations like:
``` python
l = parse_external_data(data)
if l:
    names = [(x.name or "NONAME") if x else "NONAME" for x in l]
```
which becomes
``` python
x = make_safenav(parse_external_data(data))
names = [x.name or "NONAME" for x in l]
```
and the simplification is even more apparent if more attributes or indexes have to be concatenated.

## Why not a library?
This code is very simple and short and can be easily copied and adapted to your project without a need for
an additional dependency. It is also more flexible if you have the option to modify the class at your will.

## Comparison with Nullable
Some time ago I released [Nullable](https://github.com/mattiadg/nullable) with a similar goal, so why this now?
The answer is that Nullable presents two main drawbacks:  
1. any type information on fields is lost
2. an explicit call to get() is needed to obtain the actual object, and then it is not Nullable anymore

With SafeNavigation, you get the same power as Nullable while solving both drawbacks at once. The only change needed 
is to call make_safenav(obj) instead of Nullable(obj).