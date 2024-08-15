from safenav import make_safenav


class Record:
    def __init__(self):
        self.name = "Mario"
        self.age = 28
        self.scores = [24, 28]


class A:
    def __init__(self):
        self.a = 1  # type: int
        self.b = Record()
        self.c = "ciao"  # type: str


a = make_safenav(A())
print(a.a)
print(a.e)
print(a.b.name)
print(type(a.b.name))
print(a.b.c.f or "ciao")
