"""Model for a sport series like table.

References
----------
Lambda functions and expression lists (sort using multiple criteria)
https://docs.python.org/3.6/reference/expressions.html?highlight=lambda#expression-lists

"""

import os.path


class Team:
    """Represents a team in the series.

    A team has a name, and these stats:
    games_played
    games_won
    games_draw
    games_lost
    goals(scored, conceded)
    points
    """

    def __init__(self, name, won=0, draw=0, lost=0, goals=(0, 0)):
        """Create a team instance.

        params:
        name - team name
        won - games won
        draw - games ended in draw
        lost - games lost
        goals - (scored, conceded)
        """
        self.name = name
        self.set_values(won, draw, lost, goals)

    def __repr__(self):
        """Return representation of this instance."""
        return (
            "team({name}, {played}, {won}, {draw}, {lost}, {sc}-{cc},"
            "{points})".format(
                name=self.name, played=self.games_played, won=self.games_won,
                draw=self.games_draw, lost=self.games_lost, sc=self.goals[0],
                cc=self.goals[1], points=self.points
            )
        )

    def __str__(self):
        """Return the table line for this team as a string."""
        played = str(self.games_played)
        won = str(self.games_won)
        draw = str(self.games_draw)
        lost = str(self.games_lost)
        goals = self.goals_to_string().strip()
        points = str(self.points)
        string = (
            self.name.ljust(20)
            + played.center(6)
            + won.center(5)
            + draw.center(5)
            + lost.center(5)
            + goals.center(7)
            + points.center(5)
            )
        return string

    def set_values(self, *args):
        """Set the team stats to values."""
        self.games_won = int(args[0])
        self.games_draw = int(args[1])
        self.games_lost = int(args[2])
        self.goals = [int(args[3][0]), int(args[3][1])]
        self.games_played = sum([
            int(self.games_won),
            int(self.games_draw),
            int(self.games_lost)])
        self.points = sum([
            int(self.games_won)*3,
            int(self.games_draw)*1])

    def goals_to_string(self):
        """Return the teams goals as a string.

        The sting is in the format 'a-b' where a is scored goals and b
        is conceded goals.
        """
        return str(self.goals[0]) + "-" + str(self.goals[1]) + "\n"

    def add_scored_goals(self, goals):
        """Add 'goals' to scored goals."""
        self.goals[0] += goals

    def add_conceded_goals(self, goals):
        """Add 'goals' to conceded goals."""
        self.goals[1] += goals

    def goal_diff(self):
        """Return difference in scored vs succeded goals."""
        return self.goals[0] - self.goals[1]

    def won(self):
        """Insert game stats from a win."""
        self.games_won += 1
        self.games_played += 1
        self.points += 3

    def lost(self):
        """Insert game stats from a loss."""
        self.games_lost += 1
        self.games_played += 1

    def draw(self):
        """Insert game stats from a draw."""
        self.points += 1
        self.games_draw += 1
        self.games_played += 1


class Table:
    """Represents a table of the series statistics."""

    def __init__(self, fname=None):
        """Create a table from file.

        If a file named 'fname' exists it will be read into a new
        table. If it doesn't exist it will be created. If fname is
        not given 'table.csv' will be used as filename.

        Input:
        fname - filename to be used for storing the table.

        Output:
        team_list - a list of teams instances.
        """
        self.team_list = []
        default_fname = './table.csv'
        if fname is None:
            self.fname = default_fname
        else:
            self.fname = fname
            self.read_from_file(fname)

    def __str__(self):
        """Print the table."""
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
        for team in self.team_list:
            string += (str(team) + "\n")
        return string

    def __iter__(self):
        """Iterate the team_list."""
        return iter(self.team_list)

    def __len__(self):
        """Return length of team_list."""
        return len(self.team_list)

    def read_from_file(self, fname):
        """Create a new list of teams read from file."""
        self.team_list = []  # Empty list at each read
        with open(fname, 'r') as table_file:
            for line in table_file:
                data = line.split(',')
                name = data[0]
                won = int(data[1])
                draw = int(data[2])
                lost = int(data[3])
                goals = (data[4].replace('-', ' ')).split()
                new_team = Team(name, won, draw, lost, goals)
                self.team_list.append(new_team)

    def save(self, fname=None):
        """Store the table on disk.

        fname - name of the file to store the data.
        """
        if fname is None:
            fname = self.fname

        with open(fname, 'w') as table_file:
            for team in self:
                line = ([
                    team.name,
                    str(team.games_won),
                    str(team.games_draw),
                    str(team.games_lost),
                    team.goals_to_string()])
                table_file.writelines(",".join(line))

    def find_team(self, name):
        """Return a team instance with name matching 'name'.

        If no team is found a TeamNotFound exception is raised.
        """
        for team in self:
            if team.name == name:
                break
        else:
            raise LookupError
        return team

    def list_team_names(self):
        """Generate team names.

        Can be used for autocompletes etc.
        """
        for team in self.team_list:
            yield team.name

    def new_team(self, name, won=0, draw=0, lost=0, goals=(0, 0)):
        """Append a new team in the team list."""
        goals = list(goals)
        new_team = Team(name, won, draw, lost, goals)
        self.team_list.append(new_team)

    def sort(self):
        """Sorts the list of teams based on criteria.

        1. Points
        2. Goal difference
        3. Scored goals
        4. Alphabetically
        """
        self.team_list.sort(key=lambda x: (
            -x.points,
            -x.goal_diff(),
            -x.goals[0],
            x.name
        ), reverse=False)

    def insert_statistics(self, home_team, away_team, home_goals, away_goals):
        """Insert stats for a new played game.

        home_team (string) - Name of home team.
        away_teams (string) - Name of away team.
        home_goals (int) - Home team scored goals.
        away_goals (int) - Away team scored goals.
        """
        team_1 = self.find_team(home_team)
        team_2 = self.find_team(away_team)

        if home_goals == away_goals:
            team_1.draw()
            team_2.draw()
        elif home_goals > away_goals:
            team_1.won()
            team_2.lost()
        else:
            team_1.lost()
            team_2.won()

        team_1.add_scored_goals(home_goals)
        team_1.add_conceded_goals(away_goals)
        team_2.add_scored_goals(away_goals)
        team_2.add_conceded_goals(home_goals)
