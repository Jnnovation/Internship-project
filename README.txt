Task Manager CLI

A simple command-line task manager written in Python.

Features: - Create tasks with name and description - View full task
details - Update existing tasks - Delete tasks with confirmation -
Automatic timestamp tracking - JSON-based storage (database.json)

Requirements: - Python 3.x

How to Run: Open a terminal in the project folder and run:

python InternshipProject.py

Usage: [C]reate | [R]eload | [U]pdate | [D]elete | [V]iew | [E]rase Database | [Q]uit

-   Create →          Add a new task (guided input)
-   Reload →          Reload tasks from file
-   Update →          Edit task name or description
-   Delete →          Remove a task (with confirmation)
-   View →            See full details of a task
-   Erase database →  Erases the database after two confirmations and restarts the program.
                      (The restart will generate an empty database file.)
-   Quit →            Exit the program

Notes: - Tasks are stored in database.json - The file is created
automatically if it does not exist. Ensure the program remains in
a folder so you know where to find the database.

Some things have been considered to be added to the program, however i have elected to keep
it simple. i have considered the following:

- Outside commands being able to interact with the program.
    This would make UI integration incredibly easy, however as i will not be making one now,
    i find it generally unnecessary.
- Different filetypes for the database such as CSV.
    Due to Python's integration of Json, i found it easier to implement this way. Due to the
    simplicity of my program, it has no other effect.
- Designing a UI
    I felt that for the amount of time i had and relatively low expectations, a command line TUI would suffice.

Sources:
https://stackoverflow.com/questions/5721674/what-are-some-mainstream-lightweight-alternatives-to-storing-files-in-csv-for
https://realpython.com/cheatsheets/python/
https://www.w3schools.com/python/
