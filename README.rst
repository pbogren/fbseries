=================================================
FBseries
=================================================
:Info: A simple GUI for managing a sports series table.
:Author: Patrik Bogren

Install:
========
Run it with ``python -m fbseries`` from the src/ directory or install it using
pip: ``pip install .`` from the toplevel directory.

Use:
=======
The program is very self explanatory.

Start the app and begin inserting new teams in the series from the ``Team``
panel or load a previously created table from file using the ``open`` button.

Now you can insert statistics from a new game in the ``Game`` panel. Enter the
names and the score for each team. Currently the app uses soccer values for the
points (win = 3 pts, draw = 1 pt).

A team can be edited in the ``Team`` panel by selecting the ``edit`` radio button.
Start typing the name of the team to edit in the ``name`` field. The autocomplete
functionality will assist you with this.

The table can be saved to a ``.csv`` file with the ``Save`` button.
The format for this file is::

    # table.csv
    <name>,<wins>,<draws>,<losses>,<scored goals>,<conceded goals>
