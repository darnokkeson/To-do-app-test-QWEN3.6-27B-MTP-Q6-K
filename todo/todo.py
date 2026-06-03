#!/usr/bin/env python3
"""Simple CLI To-Do List Manager with Priority and Due Dates"""

import json
import os
import sys
from datetime import datetime

TODO_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


def load_todos():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                todos = json.load(f)
            for t in todos:
                t.setdefault("priority", "medium")
                t.setdefault("due_date", None)
            return todos
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_todos(todos):
    os.makedirs(os.path.dirname(TODO_FILE), exist_ok=True)
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)


def next_id(todos):
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1


def is_overdue(due_date):
    if not due_date:
        return False
    try:
        due_dt = datetime.strptime(due_date, "%Y-%m-%d")
        return due_dt.date() < datetime.now().date()
    except ValueError:
        return False


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_todo(text, priority="medium", due_date=None):
    todos = load_todos()
    todos.append(
        {
            "id": next_id(todos),
            "text": text,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "priority": priority,
            "due_date": due_date,
        }
    )
    save_todos(todos)
    return todos[-1]


def complete_todo(todo_id):
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            save_todos(todos)
            print(f'✓ Toggled: "{t["text"]}"')
            return
    print(f"Todo #{todo_id} not found")


def remove_todo(todo_id):
    todos = load_todos()
    new_todos = [t for t in todos if t["id"] != todo_id]
    if len(new_todos) == len(todos):
        return False
    save_todos(new_todos)
    return True


def list_todos():
    todos = load_todos()
    if not todos:
        print("No todos yet.")
        return

    print(f"\n{'ID':<4} {'Status':<8} {'Priority':<10} {'Due Date':<14} {'Task'}")
    print("-" * 75)
    for t in todos:
        status = "[x]" if t["done"] else "[ ]"
        priority = t.get("priority", "medium").capitalize()
        due = t.get("due_date") or "-"

        overdue_tag = ""
        if not t["done"] and is_overdue(due):
            overdue_tag = " ⚠️ OVERDUE"

        print(f"{t['id']:<4} {status:<8} {priority:<10} {due:<14}{overdue_tag} {t['text']}")
    print()


def parse_add_args(args):
    text_parts = []
    priority = "medium"
    due_date = None

    i = 0
    while i < len(args):
        if args[i] in ("--priority", "-p") and i + 1 < len(args):
            priority = args[i + 1]
            i += 2
        elif args[i] in ("--due", "-d") and i + 1 < len(args):
            due_date = args[i + 1]
            i += 2
        else:
            text_parts.append(args[i])
            i += 1

    return " ".join(text_parts), priority, due_date


def show_help():
    print("""
Usage: python todo.py <command> [args]

Commands:
  list                        Show all todos
  add <text>                  Add a new todo
                              --priority | -p  high | medium | low  (default: medium)
                              --due | -d       YYYY-MM-DD            (optional)
  done <id>                   Toggle todo as complete/incomplete
  rm <id>                     Remove a todo
  help                        Show this help message

Examples:
  python todo.py add "Buy groceries" -p high -d 2026-06-10
  python todo.py add "Read a book" --priority low
  python todo.py list
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
                print("Usage: python todo.py add <text> [--priority high|medium|low] [--due YYYY-MM-DD]")
            else:
                text, priority, due_date = parse_add_args(sys.argv[2:])
                if not text:
                    print("Error: Task text is required.")
                elif priority not in ("high", "medium", "low"):
                    print(f"Error: Invalid priority '{priority}'. Use high, medium, or low.")
                elif due_date and not validate_date(due_date):
                    print("Error: Invalid date format. Use YYYY-MM-DD.")
                else:
                    todo = add_todo(text, priority, due_date)
                    due_str = f", Due: {due_date}" if due_date else ""
                    print(f'✓ Added: "{todo["text"]}" (Priority: {priority.capitalize()}{due_str})')
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
