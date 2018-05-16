import pytest
from fbseries.controller import Controller, sortf, empty, isposint

def test_import():
    controller = Controller()
    pass

values = [
    ('value', False),
    ('multiple words in string', False),
    (1, False),
    ("1 2 3 4", False),
    (0, False),
    ({'key': 'value'}, False),
    ([0, 0, 0], False),
    (["", ' '], False),
    (("", ' '), False),
    ("", True),
    (" ", True),
    (list(), True),
    (tuple(), True),
    (dict(), True),
]
@pytest.mark.parametrize("val, expected", values)
def test_empty(val, expected):
    """Test the empty function."""
    assert empty(val) == expected


def test_pos_int():
    """Test the positive integer function."""
    assert isposint(1, 22, '333', 444, 404)
    assert not isposint(1, -1)
    invalid = (
        -1, "", ' ', 'sss', [], (), [0, 0], "-1", (0, 0)
    )
    for value in invalid:
        assert not isposint(value)
