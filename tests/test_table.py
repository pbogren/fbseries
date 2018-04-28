"""Test the table class."""

# Ignore warnings for redefining fixtures
# pylama:ignore=W0621,W0612,F0002

import os
import tempfile
import pytest

from fbseries.model import Table
from fbseries.controller import non_empty, isposint


@pytest.fixture
def tf():
    """Run tests with a temp file."""
    return tempfile.NamedTemporaryFile()


@pytest.fixture
def et():
    """Run tests with a empty table."""
    return Table()


@pytest.fixture
def table():
    """Run tests with table from example.csv."""
    fname = os.path.realpath('example-table.csv')
    return Table(fname)


def test_imported(et):
    """Test table can be imported and that we can create an instance."""
    assert isinstance(et, Table)


def test_open_empty_file(tf):
    """Test an empty file can be opened."""
    table = Table(tf.name)
    assert not table.team_list


def test_save_file(tf):
    """Test saved file."""
    table = Table(tf.name)
    table.add('Arsenal')
    table.save()
    with open(tf.name) as f:
        string = next(f)
    assert string == "Arsenal,0,0,0,0-0\n" and len(table) == 1


def test_save_as_new():
    """Test save with new filename."""
    old = tempfile.NamedTemporaryFile()
    new = tempfile.NamedTemporaryFile()
    assert old is not new
    table = Table(old.name)
    table.add('Arsenal')
    table.save(new.name)
    with open(new.name) as f:
        string = next(f)
    assert string == "Arsenal,0,0,0,0-0\n" and len(table) == 1


def test_print_table(et):
    """Test print out."""
    et.add('Arsenal')
    header = " ".join([
        f"{'Team':^20}",
        f"{'Played':^6}",
        f"{'Wins':^3}",
        f"{'Draws':^5}",
        f"{'Losses':^5}",
        f"{'Goals':^5}",
        f"{'Pts':^7}",
        "\n",
    ])
    content = "\n".join([str(team) for team in et])
    expected = "".join([header, content])
    assert et.__str__() == expected


def test_repr(et):
    """Test the dunder repr."""
    et.add('Arsenal')
    et.add('Liverpool')
    expected = "Table('Arsenal', 'Liverpool')"
    assert et.__repr__() == expected


def test_create_new_csv():
    """Test that a new table.csv file is created."""
    table = Table()
    table.save()
    fname = "./table.csv"
    assert os.path.isfile(fname)
    os.remove(fname)


def test_find_team(et):
    """Test that teams can be found."""
    team_names = ['Arsenal', 'Blackburn', 'Liverpool']
    for name in team_names:
        et.add(name)
    found_teams = [team for team in
                   [et.find(name) for name in team_names]]
    assert len(found_teams) == 3


def test_find_team_throws_exception(et):
    """Test that an excepton is found if team is not found."""
    et.add('Arsenal')
    with pytest.raises(LookupError, message='Expected LookupError'):
        et.find('wrong name')


def test_names(table):
    """Test the names generator."""
    names = ", ".join([name for name in table.names()])
    expected = "Southhampton, Blackpool, Blackburn, Arsenal"
    assert names == expected


def test_non_empty():
    """Test the non_empty function."""
    assert not non_empty("")
    assert not non_empty(' ')
    assert non_empty('value')
    assert non_empty('multiple values 1 2 3    ')
    assert non_empty(1)
    assert non_empty([1, -2, 3, "", '  ', (1, 2, 3)])


def test_pos_int():
    """Test the positive integer function."""
    assert isposint(1, 22, '333', 444, 404)
    assert not isposint(1, -1)
    invalid = (
        -1, "", ' ', 'sss', [], (), [0, 0], "-1", (0, 0)
    )
    for value in invalid:
        assert not isposint(value)


def test_sort_points(tf):
    """Test points have highest sort priority."""
    table = Table(fname=tf.name)
    table.add('Arsenal', 1, 0, 1, (2, 1))
    table.add('Arsenal2', 1, 1, 1, (0, 0))
    table.sort()
    assert table.team_list[0].name == 'Arsenal2'
    assert table.team_list[1].name == 'Arsenal'


def test_sort_goal_diff(tf):
    """Test same points sorts on goal-diff."""
    table = Table(fname=tf.name)
    table.add('Blackpool', 1, 1, 1, (5, 4))
    table.add('Blackpool2', 1, 1, 1, (4, 2))
    table.sort()
    assert table.team_list[0].name == 'Blackpool2'
    assert table.team_list[1].name == 'Blackpool'


def test_sort_goals(tf):
    """Test same points and goal-diff sorts on goals."""
    table = Table(fname=tf.name)
    table.add('Chelsea', 2, 2, 2, (3, 1))
    table.add('Chelsea2', 2, 2, 2, (4, 2))
    table.sort()
    assert table.team_list[0].name == 'Chelsea2'
    assert table.team_list[1].name == 'Chelsea'


def test_sort_name(tf):
    """Test same stats sorts on name."""
    table = Table(fname=tf.name)
    table.add('Liverpool2', 2, 2, 2, (3, 2))
    table.add('Liverpool', 2, 2, 2, (3, 2))
    table.sort()
    assert table.team_list[0].name == 'Liverpool'
    assert table.team_list[1].name == 'Liverpool2'


def test_win_lose(tf):
    """Test correct points and goals are inserted in a win-lose game."""
    table = Table(fname=tf.name)
    table.add('Liverpool')
    table.add('Chelsea')
    table.game('Liverpool', 'Chelsea', 1, 0)
    chelsea = table.find('Chelsea')
    liverpool = table.find('Liverpool')
    assert chelsea.games == 1
    assert chelsea.wins == 0
    assert chelsea.draws == 0
    assert chelsea.losses == 1
    assert chelsea.points == 0
    assert liverpool.games == 1
    assert liverpool.wins == 1
    assert liverpool.draws == 0
    assert liverpool.losses == 0
    assert liverpool.points == 3


def test_lose_win(tf):
    """Test correct points and goals are inserted in a lose-win game."""
    table = Table(fname=tf.name)
    table.add('Liverpool')
    table.add('Chelsea')
    table.game('Chelsea', 'Liverpool', 0, 1)
    chelsea = table.find('Chelsea')
    liverpool = table.find('Liverpool')
    assert liverpool.games == 1
    assert liverpool.wins == 1
    assert liverpool.draws == 0
    assert liverpool.losses == 0
    assert liverpool.points == 3
    assert chelsea.games == 1
    assert chelsea.wins == 0
    assert chelsea.draws == 0
    assert chelsea.losses == 1
    assert chelsea.points == 0


def test_draw(tf):
    """Test correct points and goals are inserted in a draw game."""
    table = Table(fname=tf.name)
    table.add('Liverpool')
    table.add('Chelsea')
    table.game('Liverpool', 'Chelsea', 1, 1)
    chelsea = table.find('Chelsea')
    liverpool = table.find('Liverpool')
    assert chelsea.games == 1
    assert chelsea.wins == 0
    assert chelsea.draws == 1
    assert chelsea.losses == 0
    assert chelsea.points == 1
    assert liverpool.games == 1
    assert liverpool.wins == 0
    assert liverpool.draws == 1
    assert liverpool.losses == 0
    assert liverpool.points == 1


def test_getitem(et):
    """Test table can be indexed."""
    et.add('Arsenal')
    assert et[0].name == 'Arsenal'
    with pytest.raises(IndexError, message='Expected IndexError'):
        team = et[1]
