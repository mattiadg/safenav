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
