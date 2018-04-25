"""View module.

References
----------
    Table can be displayed in a treeview:
    https://stackoverflow.com/questions/9348264/does-tkinter-have-a-table-widget

    General tkinter references:
    http://www.tkdocs.com/
    https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html

"""
import tkinter as tk
from tkinter import ttk


class View:
    """Representation of the widgets in the root window."""

    def __init__(self, master):
        """Construct the container window."""
        self.controller = master
        self.container = ttk.Frame(master, height=400, width=400, padding=5)
        self.table = TablePanel(self.container)
        self.menu_panel = MenuPanel(self.container, master)
        self.message_panel = MessagePanel(self.container)
        self.tabframe = ttk.Notebook(self.container)
        self.game_panel = GamePanel(self.tabframe)
        self.team_panel = TeamPanel(self.tabframe)
        self.tabframe.add(self.game_panel.frame, text="Game")
        self.tabframe.add(self.team_panel.frame, text="Team")
        self.configure_rc()
        self.place_widgets()

    def place_widgets(self):
        """Set up the layout of the view."""
        self.container.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.table.frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.menu_panel.frame.grid(row=1, column=0, sticky=tk.N+tk.S)
        self.tabframe.grid(row=3, column=0, sticky=tk.E+tk.W)
        self.message_panel.frame.grid(row=2, column=0, sticky=tk.E+tk.W,
                                      ipady=5, pady=5)

    def configure_rc(self):
        """Configure the size and weight rows/cols of the container."""
        self.container.columnconfigure(0, minsize=350, weight=1)
        self.container.rowconfigure(0, weight=1)


class TablePanel:
    """Table representation of the data."""

    def __init__(self, master):
        """Construct the widgets of the table panel."""
        self.frame = ttk.Treeview(master, columns=(
            'team', 'played', 'won', 'draw', 'lost', 'goals', 'points'))
        self.create_headings()
        self.set_up_columns()

    def create_headings(self):
        """Set up the labels of the panel data."""
        self.frame.heading('team', text='Team')
        self.frame.heading('played', text='P')
        self.frame.heading('won', text='W')
        self.frame.heading('draw', text='D')
        self.frame.heading('lost', text='L')
        self.frame.heading('goals', text='G')
        self.frame.heading('points', text='Pt')

    def set_up_columns(self):
        """Configure the columns of the table panel."""
        self.frame.column('#0', width=1)
        self.frame.column('team', minwidth=50, width=100, anchor=tk.CENTER)
        self.frame.column(
            'played', minwidth=30, width=50, anchor=tk.CENTER)
        self.frame.column('won', minwidth=30, width=50, anchor=tk.CENTER)
        self.frame.column('draw', minwidth=30, width=50, anchor=tk.CENTER)
        self.frame.column('lost', minwidth=30, width=50, anchor=tk.CENTER)
        self.frame.column('goals', minwidth=30, width=50, anchor=tk.CENTER)
        self.frame.column(
            'points', minwidth=30, width=50, anchor=tk.CENTER)

    def insert(self, values, iid=None):
        """Insert a team in the table panel using the name as iid."""
        self.frame.insert('', 'end', iid, values=values)

    def update_column(self, iid, column, value):
        """Update column value for the team matching 'iid'."""
        self.frame.set(iid, column, value)

    def get_lines(self):
        """Return a tuple with iid for every line in the table panel."""
        return self.frame.get_children()


class MessagePanel:
    """A panel for displaying messages to the user."""

    def __init__(self, master):
        """Construct the message panel."""
        self.frame = ttk.LabelFrame(
            master, height=100, width=400, padding=5, text='Messages')
        self.frame.grid_propagate(0)
        self.yscroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.message_box = tk.Listbox(
            self.frame, relief=tk.SUNKEN, state=tk.DISABLED,
            yscrollcommand=self.yscroll.set, width=45, height=5, bg='white',
            disabledforeground='black')
        self.yscroll['command'] = self.message_box.yview
        self.configure_rc()
        self.place_widgets()

    def place_widgets(self):
        """Set up the layout of the panel."""
        self.message_box.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.yscroll.grid(row=0, column=1, sticky=tk.N+tk.S)

    def configure_rc(self):
        """Configure size and weight for rows/cols of the panel."""
        self.frame.columnconfigure(0, minsize=400, weight=1)
        self.frame.rowconfigure(0, minsize=80)
        self.message_box.columnconfigure(0, minsize=400, weight=1)

    def insert(self, message):
        """Insert the message to the message box."""
        self.message_box.configure(state=tk.NORMAL)
        self.message_box.insert(tk.END, message)
        self.message_box.see(tk.END)
        self.message_box.configure(state=tk.DISABLED)


class GamePanel:
    """A panel for adding stats from a new game."""

    def __init__(self, master):
        """Construct the game panel."""
        self.home_team_text = tk.StringVar()
        self.away_team_text = tk.StringVar()
        self.home_goal_text = tk.StringVar()
        self.away_goal_text = tk.StringVar()
        self.frame = ttk.Frame(master, padding=10, width=400, height=200)
        self.home_team_label = ttk.Label(self.frame, text="Home team")
        self.home_team_entry = ttk.Entry(
            self.frame, textvariable=self.home_team_text, width=20)
        self.away_team_label = ttk.Label(self.frame, text="Away team")
        self.away_team_entry = ttk.Entry(
            self.frame, textvariable=self.away_team_text, width=20)
        self.goal_label = ttk.Label(self.frame, text="Goals")
        self.home_goal_entry = ttk.Entry(
            self.frame, textvariable=self.home_goal_text, width=3)
        self.away_goal_entry = ttk.Entry(
            self.frame, textvariable=self.away_goal_text, width=3)
        self.submit_button = ttk.Button(self.frame, text="Submit")
        self.configure_rc()
        self.place_widgets()

    def configure_rc(self):
        """Configure size and weight for rows/cols of the panel."""
        self.frame.columnconfigure(0, minsize=100, weight=0)
        self.frame.columnconfigure(1, minsize=100, weight=0)
        self.frame.columnconfigure(2, minsize=30, weight=1)

    def place_widgets(self):
        """Set up the layout of the panel."""
        self.home_team_label.grid(row=0, column=0)
        self.home_team_entry.grid(row=1, column=0)
        self.away_team_label.grid(row=2, column=0)
        self.away_team_entry.grid(row=3, column=0)
        self.goal_label.grid(row=0, column=1)
        self.home_goal_entry.grid(row=1, column=1)
        self.away_goal_entry.grid(row=3, column=1)
        self.submit_button.grid(row=3, column=2, sticky=tk.E, padx=15)


class TeamPanel:
    """The panel for adding a team to the table or changing existing team."""

    def __init__(self, master):
        """Construct the panel."""
        self.frame = ttk.Frame(master, width=400, height=100, padding=5,)
        self.master = master
        self.insert_method = tk.StringVar()
        self.name_text = tk.StringVar()
        self.won_text = tk.StringVar()
        self.draw_text = tk.StringVar()
        self.lost_text = tk.StringVar()
        self.scored_text = tk.StringVar()
        self.conceded_text = tk.StringVar()
        self.radio_new = ttk.Radiobutton(self.frame, value='new', text='New',
                                         variable=self.insert_method)
        self.radio_edit = ttk.Radiobutton(self.frame, value='edit',
                                          text='Edit',
                                          variable=self.insert_method)
        self.radio_new.invoke()
        self.name = ttk.Entry(self.frame, textvariable=self.name_text,
                              width=20)
        self.won = ttk.Entry(self.frame, textvariable=self.won_text,
                             width=3)
        self.draw = ttk.Entry(self.frame, textvariable=self.draw_text,
                              width=3)
        self.lost = ttk.Entry(self.frame, textvariable=self.lost_text,
                              width=3)
        self.scored = ttk.Entry(self.frame, textvariable=self.scored_text,
                                width=3)
        self.conceded = ttk.Entry(self.frame, textvariable=self.conceded_text,
                                  width=3)
        self.name_label = ttk.Label(self.frame, text="Name")
        self.won_label = ttk.Label(self.frame, text="W")
        self.draw_label = ttk.Label(self.frame, text="D")
        self.lost_label = ttk.Label(self.frame, text="L")
        self.scored_label = ttk.Label(self.frame, text="Scd")
        self.goal_separator = ttk.Label(self.frame, text='-')
        self.conceded_label = ttk.Label(self.frame, text="Con")
        self.submit_button = ttk.Button(self.frame, text="Submit")
        self.configure_rc()
        self.place_widgets()

    def configure_rc(self):
        """Configure size and weight for rows/cols of the panel."""
        self.frame.columnconfigure(0, minsize=30, weight=0)
        self.frame.columnconfigure(1, minsize=70, weight=0)
        self.frame.columnconfigure(2, minsize=30, weight=0)
        self.frame.columnconfigure(3, minsize=30, weight=0)
        self.frame.columnconfigure(4, minsize=30, weight=0)
        self.frame.columnconfigure(5, minsize=30, weight=0)
        self.frame.columnconfigure(6, minsize=5, weight=0)
        self.frame.columnconfigure(7, minsize=30, weight=0)
        self.frame.columnconfigure(8, minsize=30, weight=1)

    def place_widgets(self):
        """Set up the layout of the panel."""
        self.radio_new.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.radio_edit.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.name_label.grid(row=1, column=0, columnspan=2, pady=2)
        self.won_label.grid(row=1, column=2, pady=2)
        self.draw_label.grid(row=1, column=3, pady=2)
        self.lost_label.grid(row=1, column=4, pady=2)
        self.scored_label.grid(row=1, column=5, pady=2)
        self.conceded_label.grid(row=1, column=7, pady=2)
        self.name.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
        self.won.grid(row=2, column=2, pady=2, padx=5)
        self.draw.grid(row=2, column=3, pady=2, padx=5)
        self.lost.grid(row=2, column=4, pady=2, padx=5)
        self.scored.grid(row=2, column=5, pady=2, padx=1)
        self.goal_separator.grid(row=2, column=6, pady=1)
        self.conceded.grid(row=2, column=7, pady=2, padx=1)
        self.submit_button.grid(row=2, column=8, sticky=tk.E, padx=15, pady=2)


class MenuPanel:
    """The panel for new/open/save table."""

    def __init__(self, master, controller):
        """Set up the menu panel."""
        self.frame = ttk.Frame(master, width=400, height=50, padding=5)
        self.master = master
        self.new_button = ttk.Button(self.frame, text='New',
                                     command=controller.new_button_handler)
        self.open_button = ttk.Button(self.frame, text='Open',
                                      command=controller.open_button_handler)
        self.save_button = ttk.Button(self.frame, text='Save',
                                      command=controller.save_button_handler)
        self.configure_rc()
        self.place_widgets()

    def configure_rc(self):
        """Configure size and weight for rows/cols of the panel."""
        self.frame.columnconfigure(0, minsize=130)
        self.frame.columnconfigure(1, minsize=130)
        self.frame.columnconfigure(2, minsize=130)

    def place_widgets(self):
        """Set up the layout of the panel."""
        self.new_button.grid(row=0, column=0, padx=15)
        self.open_button.grid(row=0, column=1, padx=15)
        self.save_button.grid(row=0, column=2, padx=15)
