"""Controller module."""
# pylama: ignore=w0511

import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from fbseries.model import Table, Team, game
from fbseries.view import View, TeamPanel
from fbseries.autocomplete import autocomplete


def sortf(x):
    """Sort function key."""
    return (-x.points, -x.goal_diff, -x.scored, x.name)


class Controller(tk.Tk):
    """App controller, intermediary between model and the view."""

    def __init__(self):
        """Construct a tk instance from super."""
        tk.Tk.__init__(self)
        self.fname = 'example-table.csv'
        self.model = Table(self.fname)
        self.filetypes = [("csv", "*.csv")]
        self.view = View(self)
        self.create_bindings()
        self.init_window()
        self.new_table_view()
        self.add_message("""\
            Welcome!
            table.csv has been created/loaded by default.  You can use
            the menu above to create a new, open or save the table.
            Use the panel below to insert statistics from a new game.
            Or create or edit a team manually.""")

    def init_window(self):
        """Set up the root window."""
        self.minsize(width='450', height='400')
        self.columnconfigure(0, minsize=400, weight=1)
        self.rowconfigure(0, minsize=400, weight=1)

    def create_bindings(self):
        """Create all the bindings for the widgets."""
        self.view.game_panel.submit_button.bind(
            '<Button-1>',
            self.submit_game_handler
        )
        self.view.game_panel.hometeam_entry.bind(
            '<KeyRelease>',
            self.autocomplete_handler
        )
        self.view.game_panel.awayteam_entry.bind(
            '<KeyRelease>',
            self.autocomplete_handler
        )
        self.view.team_panel.submit_button.bind(
            '<Button-1>',
            self.team_panel_handler
        )
        self.view.team_panel.name.bind(
            '<KeyRelease>',
            self.team_name_entry_handler
        )

    def run(self):
        """Start the main loop."""
        self.title("Premier League")
        self.mainloop()

    def read_model_from_file(self, fname):
        """Read and insert a new table in the table panel.

        fname (str) - filename containing the table.
        """
        self.model = Table(fname)
        self.model.sort(key=sortf)
        self.new_table_view()

    # ---------------------------- Handlers ---------------------------------
    def autocomplete_handler(self, event):
        """Handle entries with autocomplete.

        Makes sure the input was a character before passing the
        query along to the autocomplete function.
        """
        if not event.char.isprintable():
            return
        query = event.widget.get()
        name_list = self.model.names()
        substring = autocomplete(query, name_list)
        if substring:
            event.widget.delete(0, tk.END)
            event.widget.insert(tk.END, substring)

            if substring in self.model:
                # Found a match
                name = substring
                teampanel = event.widget.master._name == "teampanel"
                edit = self.view.team_panel.insert_method.get() == "edit"
                if teampanel and edit:
                    team = self.model.find(name)
                    self.view.team_panel.won_text.set(team.wins)
                    self.view.team_panel.draw_text.set(team.draws)
                    self.view.team_panel.lost_text.set(team.losses)
                    self.view.team_panel.scored_text.set(team.scored)
                    self.view.team_panel.conceded_text.set(team.conceded)

    def new_button_handler(self):
        """Handle 'new' button in the menupanel."""
        # fname = asksaveasfilename(
        #     title='New',
        #     defaultextension='.csv',
        #     filetypes=self.filetypes,
        #     initialfile=self.fname
        # )
        # # if fname:
        #     self.fname = fname  # Remember filename
        #     open(fname, 'w').close()  # create/overwrite
        result = messagebox.askokcancel(
            "Delete",
            "Are You Sure? \nUnsaved data will be lost!",
            icon='warning')
        if result:
            self.model = Table()
            self.new_table_view()
            self.add_message("Created a new table.")

    def open_button_handler(self):
        """Handle 'open' button in the menupanel."""
        fname = askopenfilename(
            title='Open',
            defaultextension='.csv',
            filetypes=self.filetypes,
            initialfile=self.fname
        )
        if fname:
            self.fname = fname  # Remember filename
            self.read_model_from_file(fname)
            self.add_message("Opened " + fname)

    def save_button_handler(self):
        """Handle 'save' button in the menupanel."""
        fname = asksaveasfilename(
            title='Save',
            defaultextension='.csv',
            filetypes=self.filetypes,
            initialfile=self.fname
        )
        if fname:
            self.fname = fname  # Remember filename
            self.model.save(fname)
            self.add_message("Saved as " + fname)

    def submit_game_handler(self, event):
        """Insert stats from a new game into the table."""
        hometeam = self.view.game_panel.hometeam_text.get()
        awayteam = self.view.game_panel.awayteam_text.get()
        homegoals_str = self.view.game_panel.homegoal_text.get()
        awaygoals_str = self.view.game_panel.awaygoal_text.get()

        all_filled = non_empty(
            hometeam,
            awayteam,
            homegoals_str,
            awaygoals_str
        )
        if not all_filled:
            self.add_message("All entries must be filled!")
            return
        exists = self.exists(hometeam, awayteam)
        pos_int = isposint(homegoals_str, awaygoals_str)
        if not exists:
            return
        if hometeam == awayteam:
            self.add_message("A team can't play against itself!")
            return
        if not pos_int:
            self.add_message("Data fields must be positive integers!")
            return
        self.insert_new_game(
            hometeam,
            awayteam,
            int(homegoals_str),
            int(awaygoals_str)
        )
        # Empty entry widgets
        self.view.game_panel.homegoal_text.set('')
        self.view.game_panel.awaygoal_text.set('')
        self.view.game_panel.awayteam_text.set('')
        self.view.game_panel.hometeam_text.set('')

    def team_name_entry_handler(self, event):
        """Perform autocomplete for team names in 'edit' mode."""
        method = self.view.team_panel.insert_method.get()
        if method == 'edit':
            self.autocomplete_handler(event)

    def team_panel_handler(self, event):
        """Handle team panel submit button.

        Edits or creates a new team in the table.
        """
        method = self.view.team_panel.insert_method.get()
        name = self.view.team_panel.name_text.get().strip()
        won = self.view.team_panel.won_text.get()
        draw = self.view.team_panel.draw_text.get()
        lost = self.view.team_panel.lost_text.get()
        scored = self.view.team_panel.scored_text.get()
        conceded = self.view.team_panel.conceded_text.get()
        data = (won, draw, lost, scored, conceded)

        inserted = False

        all_filled = non_empty(name, won, draw, lost, scored, conceded)
        if not all_filled:
            self.add_message("All entries must be filled!")
            return
        pos_int = isposint(won, draw, lost, scored, conceded)
        if not pos_int:
            self.add_message("Data fields must be positive integers!")
            return
        if method == 'new':
            inserted = self.new_team(name, *data)
        elif method == 'edit':
            inserted = self.edit_team(name, *data)
        else:
            self.add_message("Choose 'New' or 'Edit'")  # Just in case.
        if inserted:
            # Empty all entry widgets
            self.view.team_panel.name_text.set('')
            self.view.team_panel.won_text.set('')
            self.view.team_panel.draw_text.set('')
            self.view.team_panel.lost_text.set('')
            self.view.team_panel.scored_text.set('')
            self.view.team_panel.conceded_text.set('')
        else:
            self.add_message("Something went wrong....")

    def new_team(self, name, *stats):
        """Insert a new team into the view. Returns true if successful.

        name - A name for the new team.
        data - a tuple of statistics in the form (w,d,l,sc,cc)
        """
        if name is None:
            self.add_message("Error: Name is None!")
            return -1
        try:
            self.model.find(name)
        except LookupError:
            self.model.add(name, *stats)
            # Get the newly created team
            team = self.model.find(name)
            self.insert_team_in_view(team)
            self.sort_table_view()
            self.add_message(f"Created team {name}")
            return True
        else:
            # Duplicate
            self.add_message(f"{name} already exists!")
            return False

    def edit_team(self, name, *stats):
        """Edit the data of  a team in the view. Returns true if successful.

        name - A name for the new team.
        data - A tuple of statistics in the form (w,d,l,sc,cc)
        """
        try:
            i = self.model.index(name)
        except LookupError:
            self.add_message(f"No team named {name}")
            return False
        else:
            # Update existing team in model
            team = Team(name, *stats)
            self.model[i] = team
            # Update existing view
            self.update_table_line(team)
            self.sort_table_view()
            self.add_message("Edited team" + name)
            return True

    def insert_new_game(self, hometeam, awayteam, homegoals, awaygoals):
        """Insert statistics into the table model and update the view.

        Also prints a message to the user confirming successful update.

        hometeam - The name of the home team (str)
        awayteam - The name of the home team (str)
        homegoals - Number of goals for the home team (int)
        awaygoals - Number of goals for the away team (int)
        """
        game(
            self.model,
            hometeam,
            awayteam,
            homegoals,
            awaygoals
        )
        for team_name in [hometeam, awayteam]:
            team_instance = self.model.find(team_name)
            self.update_table_line(team_instance)
        self.sort_table_view()

        # Alert user of successfull insertion
        homegoals = str(homegoals)
        awaygoals = str(awaygoals)
        message = ' '.join([
            "Added game:",
            hometeam, homegoals,
            " - ",
            awaygoals, awayteam
        ])
        self.add_message(message)

    # ---------------------- Field evaluations ------------------------------
    def exists(self, *team_names):
        """Return true if every team name in the list exists in table model.

        If team is not found a message with the missing team name will be added
        and return False.
        """
        errors = False  # Since we want to capture all teams not found...
        for name in team_names:
            try:
                self.model.find(name)
            except LookupError:
                self.add_message("".join(["Could not find ", name, "!"]))
                errors = True
        return not errors

    # ------------------------ View manipulions -----------------------------
    def add_message(self, message):
        """Display 'message' to the user."""
        messages = message.splitlines()
        for m in messages:
            self.view.message_panel.insert(m.lstrip())

    def update_table_line(self, team):
        """Update the table line containing the team.

        team - A team instance.
        """
        self.view.table.update_column(
            team.name, 'played', team.games)
        self.view.table.update_column(
            team.name, 'won', team.wins)
        self.view.table.update_column(
            team.name, 'draw', team.draws)
        self.view.table.update_column(
            team.name, 'lost', team.losses)
        self.view.table.update_column(
            team.name, 'goals', team.goals_to_string())
        self.view.table.update_column(
            team.name, 'points', team.points)

    def sort_table_view(self):
        """Sorts the table model and updates the view."""
        self.model.sort(sortf)
        # move the team line in view to corresponding index in team_list
        team_names = self.model.names()
        for i, name in enumerate(team_names):
            self.view.table.frame.move(name, '', i)

    def new_table_view(self):
        """Create a new table in the table view."""
        table = self.model
        if self.view.table.get_lines():
            self.empty_table_view()
        for team in table:
            self.insert_team_in_view(team)

    def insert_team_in_view(self, team):
        """Insert a new line in the table view.

        team - team instance.
        """
        values = (
            team.name,
            str(team.games),
            str(team.wins),
            str(team.draws),
            str(team.losses),
            team.goals_to_string(),
            str(team.points),
        )
        self.view.table.insert(values, team.name)

    def empty_table_view(self):
        """Clear table in view."""
        lines = self.view.table.get_lines()
        for line in lines:
            self.view.table.frame.delete(line)


def non_empty(*args):
    """Return True if every item in the list is non-empty."""
    for item in args:
        if not str(item).strip():
            return False
    return True


def isposint(*values):
    """Return true if every argument given is int-castable and >= 0."""
    for value in values:
        try:
            value = int(value)
        except ValueError:
            # For string literals
            return False
        except TypeError:
            # For lists or other types
            return False
        if value < 0:
            return False
    return True
