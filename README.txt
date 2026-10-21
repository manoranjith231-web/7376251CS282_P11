P11 - CREATURE INDEX (POKEDEX-STYLE)
=====================================

Name: MANORANJITH M
Register number: 7376251CS282
Project number: P11

Project overview
----------------
Creature Index is a Python terminal application that stores fictional creatures and their battle statistics. Users operate the program through a numbered text menu. The project uses core Python only: no third-party packages, frameworks, GUI, database, or random numbers.

Files
-----
main.py         Main program and menu.
creatures.txt   Pipe-separated creature records (15 sample records).
README.txt      Project description and instructions.
sample_run.txt  Example terminal session.
team.txt        Team save file; the program updates it when a team is saved.

Requirements
------------
- Python 3
- Keep all project files in the same folder.
- No pip installation is needed.

How to run
----------
1. Open a terminal in this folder.
2. Run: python main.py
   On Windows, you can also run: py main.py
3. Enter a menu number and follow the prompts.
4. Select 8 to exit.

Features
--------
1. View all creatures and their statistics.
2. Search by creature number or name.
3. Filter creatures by type: Fire, Water, Grass, Electric, or Rock.
4. Compare HP, Attack, Defence, and Speed, plus the combined total.
5. Display the full evolution chain from a selected creature.
6. Battle two different creatures. The faster creature attacks first; turns alternate. Damage is Attack - (Defence // 2), with a minimum of 1. Damage is doubled for the listed type advantages: Fire beats Grass, Water beats Fire, Grass beats Water, Electric beats Water, and Rock beats Fire. Battle ends when one creature's HP reaches zero.
7. Build a team of up to six different creatures, view it, and save it to team.txt. A saved team is loaded on the next run.

Data format
-----------
Each data record uses:
No|Name|Type|HP|Attack|Defence|Speed|EvolvesTo

The final field is left empty when a creature does not evolve further. The first line and comment lines are ignored by the program.

Notes
-----
- Creature statistics are fixed values; no random numbers are used.
- The program reads the data from creatures.txt, so do not rename or move it away from main.py.
- team.txt is created/updated when the Save team option is selected.
