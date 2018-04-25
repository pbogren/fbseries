"""Test the table class."""

# Ignore warnings for redefining fixtures
# pylama:ignore=W0621,W0612

import os
import tempfile
import pytest

from fbseries.model import Table, TeamNotFound, filled, is_positive_integer


@pytest.fixture
def tf():
    """Run tests with a temp file."""
    return tempfile.NamedTemporaryFile()


@pytest.fixture
def et():
    """Run tests with a empty table."""
    return Table()


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
    table.new_team('Arsenal')
    table.save(tf.name)
    with open(tf.name) as f:
        string = next(f)
    assert string == "Arsenal,0,0,0,0-0\n" and len(table) == 1


def test_print_table(et):
    """Test print out."""
    et.new_team('Arsenal')
    string = (
        "Team".center(20)
        + "Played".center(6)
        + "Won".center(5)
        + "Draw".center(5)
        + "Lost".center(5)
        + "Goals".center(7)
        + "Pts".center(5)
        + "\n"
    )
    string += (
        "Arsenal".ljust(20)
        + "0".center(6)
        + "0".center(5)
        + "0".center(5)
        + "0".center(5)
        + "0-0".center(7)
        + "0".center(5)
        + "\n"
    )
    assert et.__str__() == string


def test_create_new_csv():
    """Test that a new table.csv file is created."""
    table = Table()
    fname = "./table.csv"
    assert os.path.isfile(fname)
    os.remove(fname)


def test_find_team(et):
    """Test that teams can be found."""
    team_names = ['Arsenal', 'Blackburn', 'Liverpool']
    for name in team_names:
        et.new_team(name)
    found_teams = [team for team in
                   [et.find_team(name) for name in team_names]]
    assert len(found_teams) == 3


def test_find_team_throws_exception(et):
    """Test that an excepton is found if team is not found."""
    et.new_team('Arsenal')
    with pytest.raises(TeamNotFound, message="Expected TeamNotFoundException"):
        et.find_team('wrong name')


def test_filled():
    """Test the filled function."""
    assert not filled("")
    assert not filled(" ")
    assert filled("value")
    assert filled("multiple values 1 2 3    ")
    assert filled(1)
    assert filled([1, -2, 3, "", "  ", (1, 2, 3)])


def test_pos_int():
    """Test the positive integer function."""
    assert is_positive_integer(1, 22, "333", 444, 404)
    assert not is_positive_integer(1, -1)
    invalid = (
        -1, "", " ", "sss", [], (), [0, 0], "-1", (0, 0)
    )
    for value in invalid:
        assert not is_positive_integer(value)


def test_sort_goals(tf):
    """Test points have highest sort priority"""
    table = Table(tf.name)
    table.new_team('Arsenal', 1, 0, 1, (2, 1))
    table.new_team('Arsenal2', 1, 1, 1, (0, 0))
    table.sort()
    assert table.team_list[0].name == "Arsenal2"
    assert table.team_list[1].name == "Arsenal"


def test_sort_goal_diff(tf):
    """Test same points sorts on goal-diff"""
    table = Table(tf.name)
    table.new_team('Blackpool', 1, 1, 1, (5, 4))
    table.new_team('Blackpool2', 1, 1, 1, (4, 2))
    table.sort()
    assert table.team_list[0].name == "Blackpool2"
    assert table.team_list[1].name == "Blackpool"


def test_sort_goals(tf):
    """Test same points and goal-diff sorts on goals"""
    table = Table(tf.name)
    table.new_team('Chelsea', 2, 2, 2, (3, 1))
    table.new_team('Chelsea2', 2, 2, 2, (4, 2))
    table.sort()
    assert table.team_list[0].name == "Chelsea2"
    assert table.team_list[1].name == "Chelsea"


def test_sort_name(tf):
    """Test same stats sorts on name."""
    table = Table(tf.name)
    table.new_team('Liverpool2', 2, 2, 2, (3, 2))
    table.new_team('Liverpool', 2, 2, 2, (3, 2))
    table.sort()
    assert table.team_list[0].name == "Liverpool"
    assert table.team_list[1].name == "Liverpool2"


def test_win_lose(tf):
    """Test correct points and goals are inserted in a win-lose game."""
    table = Table(tf.name)
    table.new_team('Liverpool')
    table.new_team('Chelsea')
    table.insert_statistics('Liverpool', 'Chelsea', 1, 0)
    chelsea = table.find_team('Chelsea')
    liverpool = table.find_team('Liverpool')
    assert chelsea.games_played == 1
    assert chelsea.games_won == 0
    assert chelsea.games_draw == 0
    assert chelsea.games_lost == 1
    assert chelsea.points == 0
    assert liverpool.games_played == 1
    assert liverpool.games_won == 1
    assert liverpool.games_draw == 0
    assert liverpool.games_lost == 0
    assert liverpool.points == 3


def test_lose_win(tf):
    """Test correct points and goals are inserted in a lose-win game."""
    table = Table(tf.name)
    table.new_team('Liverpool')
    table.new_team('Chelsea')
    table.insert_statistics('Chelsea', 'Liverpool', 0, 1)
    chelsea = table.find_team('Chelsea')
    liverpool = table.find_team('Liverpool')
    assert liverpool.games_played == 1
    assert liverpool.games_won == 1
    assert liverpool.games_draw == 0
    assert liverpool.games_lost == 0
    assert liverpool.points == 3
    assert chelsea.games_played == 1
    assert chelsea.games_won == 0
    assert chelsea.games_draw == 0
    assert chelsea.games_lost == 1
    assert chelsea.points == 0


def test_draw(tf):
    """Test correct points and goals are inserted in a draw game."""
    table = Table(tf.name)
    table.new_team('Liverpool')
    table.new_team('Chelsea')
    table.insert_statistics('Liverpool', 'Chelsea', 1, 1)
    chelsea = table.find_team('Chelsea')
    liverpool = table.find_team('Liverpool')
    assert chelsea.games_played == 1
    assert chelsea.games_won == 0
    assert chelsea.games_draw == 1
    assert chelsea.games_lost == 0
    assert chelsea.points == 1
    assert liverpool.games_played == 1
    assert liverpool.games_won == 0
    assert liverpool.games_draw == 1
    assert liverpool.games_lost == 0
    assert liverpool.points == 1
