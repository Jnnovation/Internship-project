import os
import json
import uuid
import time
from datetime import datetime
import sys

DB_FILE = "database.json"


# Database
# Handles reading, writing, and initializing the JSON file

# Create database if it doesn't exist, otherwise load it
def init_database():
    if not os.path.exists(DB_FILE):
        data = {"tasks": []}
        save_database(data)
        return data
    else:
        with open(DB_FILE, "r") as f:
            return json.load(f)

# Save current state to the JSON file
def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Reload data from disk (useful if file changed externally)
def reload_database():
    with open(DB_FILE, "r") as f:
        return json.load(f)


# Utility
# Small helper functions used across the program

# Clears the terminal screen
def clear():
    os.system("clear" if os.name == "posix" else "cls")

# Short pause to make things such as confirmations readable
def wait():
    time.sleep(1)

# Ask user for yes/no confirmation
def confirm(message="Continue? (y/n): "):
    while True:
        choice = input(f"\n{message}").lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        else:
            print("Please enter y or n.")


# Task logic
# CRUD functionality and the Update and Delete database i added

# Prompt user to enter task details
def create_task():
    print("=== Create Task ===")

    name = input("Name: ")
    description = input("Description: ")

    now = datetime.now().isoformat()

    # Return a new task dictionary
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "created_at": now,
        "updated_at": now
    }

# Show a numbered list of tasks (basic overview)
def list_tasks(data):
    if not data["tasks"]:
        print("No tasks found.")
        return

    for i, task in enumerate(data["tasks"], start=1):
        print(f"{i}. {task['name']} ({task['id']})")

# Display full details of a selected task
def view_task(data):
    print("=== View Task ===")
    list_tasks(data)

    if not data["tasks"]:
        return

    try:
        index = int(input("Select task number: ")) - 1
        task = data["tasks"][index]

        while True:
            clear()
            print("=== TASK DETAILS ===\n")
            print(f"ID: {task['id']}")
            print(f"Name: {task['name']}")
            print(f"Description: {task['description']}")
            print(f"Created at: {task['created_at']}")
            print(f"Last updated: {task['updated_at']}\n")

            print("1. Exit")
            choice = input("Select option: ").strip()
            if choice == "1":
                break
            else:
                print("Invalid option.")
                wait()

    except:
        print("Invalid selection.")
        wait()

# Remove a task after confirmation
def delete_task(data):
    print("=== Delete Task ===")
    list_tasks(data)

    if not data["tasks"]:
        return

    try:
        index = int(input("Select task number: ")) - 1
        task = data["tasks"][index]

        if confirm(f"Delete '{task['name']}'? (y/n): "):
            data["tasks"].pop(index)
            save_database(data)
            print("Deleted.")
        else:
            print("Cancelled.")

        wait()

    except:
        print("Invalid selection.")
        wait()

# Edit task fields (name or description)
def update_task(data):
    print("=== Update Task ===")
    list_tasks(data)

    if not data["tasks"]:
        return

    try:
        index = int(input("Select task number: ")) - 1
        task = data["tasks"][index]
    except:
        print("Invalid selection.")
        wait()
        return

# Field selection loop
    while True:
        clear()
        print(f"Editing: {task['name']}")
        print("""
1. Name
2. Description
3. Back
""")

        choice = input("Select field: ").strip()

        if choice == "1":
            if confirm(f"Change name of '{task['name']}'? (y/n): "):
                task["name"] = input("New name: ")
                task["updated_at"] = datetime.now().isoformat()
                save_database(data)
        elif choice == "2":
            if confirm(f"Change description of '{task['name']}'? (y/n): "):
                task["description"] = input("New description: ")
                task["updated_at"] = datetime.now().isoformat()
                save_database(data)
        elif choice == "3":
            break
        else:
            print("Invalid option.")
            wait()


# UI
# Responsible for drawing what the user sees

def draw_ui(data, last_reloaded):
    clear()

    print("=== TASK MANAGER ===\n")
    print(f"Last reload: {last_reloaded}\n")

    # Show all task names
    if data["tasks"]:
        for task in data["tasks"]:
            print(f"- {task['name']}")
    else:
        print("No tasks yet.")

    print("\n" + "=" * 40)
    print("[C]reate | [R]eload | [U]pdate | [D]elete | [V]iew | [E]rase Database | [Q]uit")


# Main loop
# Controls program flow and user interaction

def main():
    # Initialize data and track last reload time
    data = init_database()
    last_reloaded = datetime.now().isoformat()

    # Main program loop
    while True:
        draw_ui(data, last_reloaded)
        choice = input("Choose option: ").lower()

        if choice == "c":
            clear()
            task = create_task()
            data["tasks"].append(task)
            save_database(data)
            print("Task created.")
            wait()

        elif choice == "v":
            clear()
            view_task(data)
            wait()

        elif choice == "r":
            data = reload_database()
            last_reloaded = datetime.now().isoformat()

        elif choice == "u":
            clear()
            update_task(data)

        elif choice == "d":
            clear()
            delete_task(data)

        elif choice == "q":
            if confirm("Are you sure you want to quit? (y/n): "):
                break

        elif choice == "e":
            clear()
            # First confirmation
            if confirm("Are you sure you want to erase the database? (y/n): "):
                # U REALLY REALLY sure bout that bro?
                if confirm("Doing this means permanently removing the database.json file. Continue? (y/n): "):
                    try:
                        os.remove(DB_FILE)
                        print("Database erased. Restarting program in 1 second...")
                        time.sleep(1)
                        # Restart the program
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    except FileNotFoundError:
                        print("Database file not found, nothing to erase.")
                else:
                    print("Cancelled.")
            else:
                print("Cancelled.")
            wait()

        else:
            print("Invalid option.")
            wait()


# Entry point of the program
if __name__ == "__main__":
    main()
