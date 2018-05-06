"""Model for a sport series like table.

References
----------
lambda functions and expression lists (sort using multiple criteria)
https://docs.python.org/3.6/reference/expressions.html?highlight=lambda#expression-lists

"""
# pylama: ignore=w0511
HEADER = " ".join([
    f"{'Team':^20}",
    f"{'Played':^6}",
    f"{'Wins':^3}",
    f"{'Draws':^5}",
    f"{'Losses':^5}",
    f"{'Goals':^5}",
    f"{'Pts':^7}",
    "\n",
])


class Team:
    """Represents a team in the series."""

    def __init__(self, name, *args):
        """Create a team instance.

        params:
        name - team name
        wins - games won
        draws - games ended in draw
        losses - games lost
        scored - scored goals
        conceded - conceded goals
        """
        self.name = name
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.scored = 0
        self.conceded = 0

        if len(args) == 5:
            wins, draws, losses, scored, conceded = args
            self.wins = int(wins)
            self.draws = int(draws)
            self.losses = int(losses)
            self.scored = int(scored)
            self.conceded = int(conceded)
        elif len(args) != 0:
            raise TypeError("Wrong number of arguments. Expected 1 or 6")

    def __repr__(self):
        """Return representation of this instance."""
        return (
            "Team({name}, {games}, {wins}, {draws}, {losses}, {goals}, {pts})"
            .format(
                name=self.name,
                games=self.games,
                wins=self.wins,
                draws=self.draws,
                losses=self.losses,
                goals=self.goals_as_string(),
                pts=self.points
            )
        )

    def __str__(self):
        """Return the table line for this team as a string."""
        goals = self.goals_as_string()
        return " ".join([
            f"{self.name:<20}",
            f"{self.games:^6}",
            f"{self.wins:^3}",
            f"{self.draws:^5}",
            f"{self.losses:^5}",
            f"{goals:^5}",
            f"{self.points:^7}",
        ])

    def goals_as_string(self):
        """Return the teams goals as a string.

        The sting is in the format 'a-b' where a is scored goals and b
        is conceded goals.
        """
        return f"{self.scored}-{self.conceded}"

    @property
    def games(self):
        """Return calculated number of games."""
        return sum([self.wins, self.draws, self.losses])

    @property
    def points(self):
        """Return calculated points."""
        return sum([self.wins * 3, self.draws])

    @property
    def goal_diff(self):
        """Return difference in scored vs succeded goals."""
        return self.scored - self.conceded


class Table:
    """A container of items that can be represented in a table.

    A table is a basic container for items. Each item must have a 'name'
    attribute and must be able to be instantiated with a string as the only
    argument.

    A new table can be created without any arguments. To create a table from a
    previously saved file the name of that file can be given as argument::
        >>> table = Table()  # Or table = Table('table.csv')
        >>> table

    New items can be created with just the name as argument, any following
    arguments will simply be passed on to the __init__ method for the item
    class.
        >>> table.add('Name')

    The items in the table can be accessed either by index or by 'name'::
        >>> table[0].name
        'Name'
        >>> table['Name'].name
        'Name'

    The items can be saved to a .csv file with the data of each item on a
    separate row with the following format::
        <name>,<attr1>,<attr2>,...,<attrN>
    where each attr field is the string represantation of the value of each
    attribute of the item.


    """

    def __init__(self, fname=None, header=HEADER, cls=Team):
        """Create an empty table or read one from file.

        Input:
        fname - filename to be used for storing the table.
        header - A header for the string representation of the table.
        cls - The class for the items. When read from file each new item
                will be an instance of this class

        Output:
        rows - a list of cls instances.
        """
        if not hasattr(cls(''), 'name'):
            raise AttributeError("Must have attribute 'name'")
        self.cls = cls
        self.rows = list()
        self.header = header
        default_fname = './table.csv'
        if fname is None:
            self.fname = default_fname
        else:
            self.fname = fname
            self.read(fname)

    def __str__(self):
        """Print the table."""
        content = "\n".join([str(item) for item in self])
        return "".join([self.header, content])

    def __repr__(self):
        """Representation of the table class."""
        names = ", ".join([f"'{item.name}'" for item in self])
        return f"Table({names})"

    def __iter__(self):
        """Iterate the rows."""
        for item in self.rows:
            yield item

    def __getitem__(self, index):
        """Return item at index position of table."""
        if isinstance(index, str):
            rv = self.find(index)
        elif isinstance(index, int):
            rv = self.rows[index]
        else:
            raise clsError("Index must be string or integer")

        return rv

    def __setitem__(self, index, item):
        """Set new item at index."""
        if index == len(self):
            self.rows.append(item)
        else:
            self.rows[index] = item

    def __contains__(self, name):
        """Check existance of item with name=name in table."""
        try:
            self.find(name)
        except LookupError:
            return False
        else:
            return True

    def __len__(self):
        """Return length of rows."""
        return len(self.rows)

    def __bool__(self):
        """Return true if table is not empty."""
        return bool(self.rows)

    def read(self, fname):
        """Create a new list of teams read from file."""
        self.rows = []  # Empty list at each read
        with open(fname, 'r') as table_file:
            for line in table_file:
                data = line.split(',')
                new_item = self.cls(*data)
                self.rows.append(new_item)

    def save(self, fname=None):
        """Store the table on disk.

        fname - name of the file to store the data.
        """
        if fname is None:
            fname = self.fname
        with open(fname, 'w') as table_file:
            for item in self:
                keys = [k for k in item.__dict__.keys()]
                attrs = [str(getattr(item, k)) for k in keys]
                table_file.writelines(",".join(attrs) + "\n")

    def find(self, name):
        """Return a team instance with name matching 'name'.

        If no team is found a LookupError exception is raised.
        """
        for item in self:
            if item.name == name:
                break
        else:
            raise LookupError
        return item

    def _index(self, name):
        """Return position for item with name."""
        for i, item in enumerate(self):
            if item.name == name:
                break
        else:
            raise LookupError
        return i

    def add(self, *args):
        """Append a new team in the team list."""
        if len(args) == 1 and type(args[0]) is self.cls:
            self.rows.append(args[0])
        else:
            new_item = self.cls(*args)
            self.rows.append(new_item)

    def sort(self, key):
        """Sorts the list of teams based on criteria.

        1. Points
        2. Goal difference
        3. Scored goals
        4. Alphabetically
        """
        self.rows.sort(key=key)


def game(table, hometeam, awayteam, homegoals, awaygoals):
    """Insert stats for a new played game.

    table - table instance where teams are located
    hometeam (string) - Name of home team.
    awayteams (string) - Name of away team.
    homegoals (int) - Home team scored goals.
    awaygoals (int) - Away team scored goals.
    """
    team_1 = table.find(hometeam)
    team_2 = table.find(awayteam)

    if homegoals == awaygoals:
        team_1.draws += 1
        team_2.draws += 1
    elif homegoals > awaygoals:
        team_1.wins += 1
        team_2.losses += 1
    else:
        team_1.losses += 1
        team_2.wins += 1

    team_1.scored += homegoals
    team_1.conceded += awaygoals
    team_2.scored += awaygoals
    team_2.conceded += homegoals
