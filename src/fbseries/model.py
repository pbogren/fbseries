"""Model for a sport series like table.

References
----------
Lambda functions and expression lists (sort using multiple criteria)
https://docs.python.org/3.6/reference/expressions.html?highlight=lambda#expression-lists

"""
# pylama: ignore=W0511,F0002


class Team:
    """Represents a team in the series."""

    def __init__(self, name, wins=0, draws=0, losses=0, goals=(0, 0)):
        """Create a team instance.

        params:
        name - team name
        wins - games won
        draws - games ended in draw
        losses - games lost
        goals - (scored, conceded)
        """
        self.name = name
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals = [int(g) for g in goals]
        self.games = sum([
            int(self.wins),
            int(self.draws),
            int(self.losses)
        ])
        self.points = sum([
            int(self.wins)*3,
            int(self.draws)*1
        ])

    def __repr__(self):
        """Return representation of this instance."""
        return (
            "team({name}, {games}, {wins}, {draws}, {losses}, {goals},"
            "{points})".format(
                name=self.name,
                games=self.games,
                wins=self.wins,
                draws=self.draws,
                losses=self.losses,
                goals=self.goals_to_string(),
                points=self.points
            )
        )

    def __str__(self):
        """Return the table line for this team as a string."""
        goals = self.goals_to_string().strip()
        return " ".join([
            f"{self.name:<20}",
            f"{self.games:^6}",
            f"{self.wins:^3}",
            f"{self.draws:^5}",
            f"{self.losses:^5}",
            f"{goals:^5}",
            f"{self.points:^7}",
        ])

    def goals_to_string(self):
        """Return the teams goals as a string.

        The sting is in the format 'a-b' where a is scored goals and b
        is conceded goals.
        """
        return "-".join([str(g) for g in self.goals])

    def goal_diff(self):
        """Return difference in scored vs succeded goals."""
        return self.goals[0] - self.goals[1]

    def won(self):
        """Insert game stats from a win."""
        self.wins += 1
        self.games += 1
        self.points += 3

    def lost(self):
        """Insert game stats from a loss."""
        self.losses += 1
        self.games += 1

    def draw(self):
        """Insert game stats from a draw."""
        self.points += 1
        self.draws += 1
        self.games += 1


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
            self.read(fname)

    def __str__(self):
        """Print the table."""
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
        content = "\n".join([str(team) for team in self])
        return "".join([header, content])

    def __repr__(self):
        """Representation of the table class."""
        names = ", ".join([f"'{team.name}'" for team in self])
        return f"Table({names})"

    def __iter__(self):
        """Iterate the team_list."""
        for team in self.team_list:
            yield team

    def __getitem__(self, index):
        """Return item at index position of table."""
        if isinstance(index, slice):
            return Table(jjindex)
        if index >= len(self):
            raise IndexError
        return self.team_list[index]

    def __setitem__(self, index, item):
        self.team_list[index] = item

    def __contains__(self, name):
        """Return true if table contains team 'name', false otherwise."""
        try:
            self.find(name)
        except LookupError:
            return False
        else:
            return True

    def __len__(self):
        """Return length of team_list."""
        return len(self.team_list)

    def read(self, fname):
        """Create a new list of teams read from file."""
        self.team_list = []  # Empty list at each read
        with open(fname, 'r') as table_file:
            for line in table_file:
                data = line.split(',')
                name = data[0]
                wins = int(data[1])
                draws = int(data[2])
                losses = int(data[3])
                goals = [int(g) for g in data[4].split('-')]
                new_team = Team(name, wins, draws, losses, goals)
                self.team_list.append(new_team)

    def save(self, fname=None):
        """Store the table on disk.

        fname - name of the file to store the data.
        """
        if fname is None:
            fname = self.fname
        with open(fname, 'w') as table_file:
            for team in self:
                line = [
                    team.name,
                    str(team.wins),
                    str(team.draws),
                    str(team.losses),
                    team.goals_to_string(),
                ]
                table_file.writelines(",".join(line))

    def find(self, name):
        """Return a team instance with name matching 'name'.

        If no team is found a LookupError exception is raised.
        """
        for team in self:
            if team.name == name:
                break
        else:
            raise LookupError
        return team

    def index(self, name):
        """Return index, team_instance with name"""
        for i, team in enumerate(self):
            if team.name == name:
                break
        else:
            raise LookupError
        return i

    def names(self):
        """Generate team names.

        Can be used for autocompletes etc.
        """
        for team in self:
            yield team.name

    def add(self, name, wins=0, draws=0, losses=0, goals=(0, 0)):
        """Append a new team in the team list."""
        goals = list(goals)
        new_team = Team(
            name=name,
            wins=wins,
            draws=draws,
            losses=losses,
            goals=[int(g) for g in goals]
        )
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

    def game(self, hometeam, awayteam, homegoals, awaygoals):
        """Insert stats for a new played game.

        hometeam (string) - Name of home team.
        awayteams (string) - Name of away team.
        homegoals (int) - Home team scored goals.
        awaygoals (int) - Away team scored goals.
        """
        team_1 = self.find(hometeam)
        team_2 = self.find(awayteam)

        if homegoals == awaygoals:
            team_1.draw()
            team_2.draw()
        elif homegoals > awaygoals:
            team_1.won()
            team_2.lost()
        else:
            team_1.lost()
            team_2.won()

        team_1.goals[0] += homegoals
        team_1.goals[1] += awaygoals
        team_1.goals[0] += awaygoals
        team_1.goals[1] += homegoals
