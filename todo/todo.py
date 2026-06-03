#!/usr/bin/env python3
"""Simple CLI To-Do List Manager"""

import os
import sys

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.models.todo_store import add_todo, load_todos, remove_todo, toggle_todo


def complete_todo(todo_id):
    """Mark a todo as complete (toggle)."""
    if toggle_todo(todo_id):
        todos = load_todos()
        todo = next((t for t in todos if t["id"] == todo_id), None)
        if todo:
            print(f'✓ Completed: "{todo["text"]}"')
    else:
        print(f"Todo #{todo_id} not found")


def list_todos():
    """Display all todos in a formatted table."""
    todos = load_todos()
    if not todos:
        print("No todos yet.")
        return
    print(f"\n{'ID':<4} {'Status':<6} {'Created':<18} {'Task'}")
    print("-" * 60)
    for t in todos:
        status = "✓" if t["done"] else " "
        print(f"{t['id']:<4} {status:<6} {t['created']:<18} {t['text']}")
    print()


def show_help():
    """Display usage instructions."""
    print("""
Usage: python todo.py <command> [args]

Commands:
  list        Show all todos
  add <text>  Add a new todo
  done <id>   Mark a todo as complete
  rm <id>     Remove a todo
  help        Show this help message
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    else:
        cmd = sys.argv[1].lower()
        if cmd == "list":
            list_todos()
        elif cmd == "add":
            if len(sys.argv) < 3:
                print("Usage: python todo.py add <text>")
            else:
                todo = add_todo(" ".join(sys.argv[2:]))
                print(f'✓ Added: "{todo["text"]}"')
        elif cmd in ("done", "complete"):
            if len(sys.argv) < 3:
                print("Usage: python todo.py done <id>")
            else:
                try:
                    complete_todo(int(sys.argv[2]))
                except ValueError:
                    print("Error: ID must be a number")
        elif cmd in ("rm", "remove", "delete"):
            if len(sys.argv) < 3:
                print("Usage: python todo.py rm <id>")
            else:
                try:
                    if remove_todo(int(sys.argv[2])):
                        print(f"Removed todo #{sys.argv[2]}")
                    else:
                        print(f"Todo #{sys.argv[2]} not found")
                except ValueError:
                    print("Error: ID must be a number")
        elif cmd == "help":
            show_help()
        else:
            print(f"Unknown command: {cmd}")
            show_help()
