#!/usr/bin/env python3
"""Shared data store for todos (JSON file)."""

import json
import os

_BASE = os.path.dirname(__file__)
TODO_FILE = os.path.join(_BASE, "todos.json")
CONFIG_FILE = os.path.join(_BASE, "gui_config.json")


def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            todos = json.load(f)
        for t in todos:
            t.setdefault("priority", "medium")
            t.setdefault("due_date", None)
        return todos
    except (json.JSONDecodeError, OSError):
        return []


def save_todos(todos):
    os.makedirs(os.path.dirname(TODO_FILE), exist_ok=True)
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)


def next_id(todos):
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1
