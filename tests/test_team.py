from fbseries.model import Team


def test_can_be_created_with_just_a_name():
    team = Team('new name')
    assert team.name == 'new name', 'Team cannot be created with a just a name'
    assert team.name != 'not new name', 'Team name is not new'


def test_can_convert_goals_to_string():
    team = Team('name', 1, 2, 3, (1, 1))
    assert team.goals_to_string() == '1-1\n',  'Goals to string'
