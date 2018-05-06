"""Test the table class."""

# Ignore warnings for redefining fixtures
# pylama:ignore=W0621,W0612,F0002

import os
import tempfile
import pytest

from fbseries.model import Table, Team, game
from fbseries.controller import non_empty, isposint, sortf


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


class TestTeam:
    """Tests for the team class."""

    def test_import_team(self):
        """Test table can be imported and that we can create an instance."""
        team = Team('Name')
        assert isinstance(team, Team)

    def test_add_different_no_arguments(self, et):
        """Test possible arguments needed to create an item (Team)."""
        name = 'Name'

        et.add(name)
        assert et[0].name == name

    def test_all_args_given(self, et):
        """Test that all possible args can be given."""
        name = 'Name'
        stats = (1, 1, 2, 3, 4)
        points = stats[0] * 3 + stats[1]
        games = stats[0] + stats[1] + stats[2]

        et.add(name, *stats)

        expected = (name,) + (games,) + stats + (points,)
        result  = (
            et[0].name,
            et[0].games,
            et[0].wins,
            et[0].draws,
            et[0].losses,
            et[0].scored,
            et[0].conceded,
            et[0].points,
        )
        assert expected == result

    def test_wrong_no_args(self, et):
        """Test that wrong No. arguments raises TypeError."""
        name = 'Liverpool'
        faulty_args = (
        (name, 1),
        (name, 1, 1),
        (name, 1, 1, 1,),
        (name, 1, 1, 1, 1),
        (name, 1, 1, 1, 1, 1, 1),
        )
        for arg in faulty_args:
            with pytest.raises(
                TypeError,
                message="Expected TypeError if args != 1 or 6"
            ):
                et.add(*arg)

    def test_team_repr(self):
        """Test the teams repr function."""
        name = 'Liverpool'
        team = Team(name, 1, 2, 3, 4, 5)
        expected = f"Team({name}, 6, 1, 2, 3, 4-5, 5)"
        result = repr(team)
        assert result == expected


class TestTable:
    """Tests for the Table class."""

    def test_index_int(self, et):
        """Test the table can return index it items."""
        oknames = "Liverpool Blackpool Southhampton".split()
        for i, name in enumerate(oknames):
            et.add(name)
            expected = i
            value = et._index(name)
            assert value == expected

        faulty_names = "Some other names".split()
        for name in faulty_names:
            with pytest.raises(LookupError, message="Expected LookupError"):
                et._index(name)

    def test_index_str(self, et):
        """Test the table can return index it items."""
        oknames = "Liverpool Blackpool Southhampton".split()
        for name in oknames:
            et.add(name)
            expected = name
            value = et[name].name
            assert value == expected

        faulty_names = "Some other names".split()
        for name in faulty_names:
            with pytest.raises(LookupError, message="Expected LookupError"):
                et._index(name)

    def test_imported(self, et):
        """Test table can be imported and that we can create an instance."""
        assert isinstance(et, Table)

    def test_open_empty_file(self, tf):
        """Test an empty file can be opened."""
        table = Table(tf.name)
        assert table.rows == []

    def test_save_file(self, tf):
        """Test saved file."""
        table = Table(tf.name)
        table.add('Arsenal')
        table.save()
        with open(tf.name) as f:
            result = next(f)
        expected = "Arsenal,0,0,0,0,0\n"
        assert result ==  expected

    def test_save_as_new(self):
        """Test save with new filename."""
        old = tempfile.NamedTemporaryFile()
        new = tempfile.NamedTemporaryFile()
        table = Table(old.name)
        table.add('Arsenal')
        table.save(new.name)
        with open(new.name) as f:
            result = next(f)
        expected = "Arsenal,0,0,0,0,0\n"
        assert result == expected

    def test_print_table(self, et):
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
        result = str(et)
        assert result == expected

    def test_repr(self, et):
        """Test the dunder repr."""
        et.add('Arsenal')
        et.add('Liverpool')
        expected = "Table('Arsenal', 'Liverpool')"
        result = repr(et)
        assert result == expected

    def test_create_new_csv(self):
        """Test that a new table.csv file is created when no arg given."""
        try:
            table = Table()
            table.save()
            fname = "./table.csv"
            assert os.path.isfile(fname), "Default fname not created"
        finally:
            os.remove(fname)

    def test_add_instance(self, et):
        """Test the add method can take an instance as argument."""
        new_team = Team('Arsenal')
        et.add(new_team)
        assert et[0] is new_team

    def test_find_team(self, et):
        """Test that teams can be found."""
        team_names = ['Arsenal', 'Blackburn', 'Liverpool']
        for name in team_names:
            et.add(name)
        found_teams = [
            team for team in
            [et.find(name) for name in team_names]
        ]
        assert len(found_teams) == 3

    def test_find_team_throws_exception(self, et):
        """Test that an excepton is found if team is not found."""
        et.add('Arsenal')
        with pytest.raises(LookupError, message='Expected LookupError'):
            et.find('wrong name')

    def test_names(self, table):
        """Test the names generator."""
        names = ", ".join([team.name for team in table])
        expected = "Southhampton, Blackpool, Blackburn, Arsenal"
        assert names == expected

    def test_sort_points(self, tf):
        """Test points have highest sort priority."""
        table = Table(fname=tf.name)
        table.add('Arsenal', 1, 0, 1, 2, 1)
        table.add('Arsenal2', 1, 1, 1, 0, 0)
        table.sort(sortf)
        expected = "Arsenal2 Arsenal".split()
        result = [team.name for team in table]
        assert result == expected

    def test_add_one_args(self, et):
        """Test that the add method can take one arg."""
        et.add('Arsenal')
        expected = 'Arsenal'
        result = et[0].name
        assert result == expected

    def test_add_mult_pos_args(self, et):
        """Test that the add method can take multiple args."""
        name = 'Liverpool'
        stats = 1, 2, 3, 4, 5
        et.add(name, *stats)
        expected = (name, *stats)
        team = et[0]
        result = (
            team.name,
            team.wins,
            team.draws,
            team.losses,
            team.scored,
            team.conceded
        )
        assert result == expected

    @pytest.mark.parametrize("sink,rise", [
        (
            ('Blackpool', 1, 1, 1, 5, 4),  # sinking team
            ('Blackpool2', 1, 1, 1, 4, 2),  # rising team
        ),
    ])
    def test_sort_goal_diff(self, et, sink, rise):
        """Test same points sorts on goal-diff."""
        topteam = Team(*rise)
        bottomteam = Team(*sink)
        et.add(bottomteam)
        et.add(topteam)
        et.sort(sortf)
        assert et[0].name == topteam.name

    def test_sort_goals(self, tf):
        """Test same points and goal-diff sorts on goals."""
        table = Table(fname=tf.name)
        table.add('Chelsea', 2, 2, 2, 3, 1)
        table.add('Chelsea2', 2, 2, 2, 4, 2)
        table.sort(sortf)
        assert table.rows[0].name == 'Chelsea2'

    def test_sort_name(self, tf):
        """Test same stats sorts on name."""
        table = Table(fname=tf.name)
        table.add('Liverpool2', 2, 2, 2, 3, 2)
        table.add('Liverpool', 2, 2, 2, 3, 2)
        table.sort(sortf)
        assert table.rows[0].name == 'Liverpool'

    def test_lose_win(self, et):
        """Test correct points and goals are inserted in a lose-win game."""
        loser = Team('loser')
        winner = Team('winner')
        et.add(loser)
        et.add(winner)
        game(et, 'loser', 'winner', 0, 1)
        result = [
            {
                'games': t.games,
                'wins': t.wins,
                'draws': t.draws,
                'losses': t.losses,
                'points': t.points
            }
                for t in (et.find('loser'), et.find('winner'))
        ]
        expected = [
            {'games': 1, 'wins': 0, 'draws': 0, 'losses': 1, 'points': 0},
            {'games': 1, 'wins': 1, 'draws': 0, 'losses': 0, 'points': 3},
        ]
        assert result == expected

    def test_win_lose(self, et):
        """Test correct points and goals are inserted in a win-lose game."""
        loser = Team('loser')
        winner = Team('winner')
        et.add(loser)
        et.add(winner)
        game(et, 'winner', 'loser', 1, 0)
        result = [
            {
                'games': t.games,
                'wins': t.wins,
                'draws': t.draws,
                'losses': t.losses,
                'points': t.points
            }
                for t in (et.find('winner'), et.find('loser'))
        ]
        expected = [
            {'games': 1, 'wins': 1, 'draws': 0, 'losses': 0, 'points': 3},
            {'games': 1, 'wins': 0, 'draws': 0, 'losses': 1, 'points': 0},
        ]
        assert result == expected

    def test_draw(self, et):
        """Test correct points and goals are inserted in a draw game."""
        team1 = Team('team1')
        team2 = Team('team2')
        et.add(team1)
        et.add(team2)
        game(et, 'team1', 'team2', 1, 1)
        result = [
            {
                'games': t.games,
                'wins': t.wins,
                'draws': t.draws,
                'losses': t.losses,
                'points': t.points
            }
                for t in (et.find('team1'), et.find('team2'))
        ]
        expected = [
            {'games': 1, 'wins': 0, 'draws': 1, 'losses': 0, 'points': 1},
            {'games': 1, 'wins': 0, 'draws': 1, 'losses': 0, 'points': 1},
        ]
        assert result == expected

    def test_getitem(self, et):
        """Test table can be indexed."""
        et.add('Arsenal')
        assert et[0].name == 'Arsenal'
        with pytest.raises(IndexError, message='Expected IndexError'):
            team = et[1]

    def test_contains_oknames(self, et):
        """Test that the table 'contains' function."""
        oknames = "Liverpool Blackpool Southhampton".split()
        for name in oknames:
            et.add(name)
            assert name in et

        faulty_names = "Other teams"
        for name in faulty_names:
            assert name not in et

    def test_setitem(self, et):
        """Test the setitem function."""
        team1 = Team('Name')
        et[0] = team1
        team2 = Team('Other')
        et[0] = team2

        assert et[0] is team2

    def test_bool(self, et):
        assert not et
        et.add('New team')
        assert et

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


