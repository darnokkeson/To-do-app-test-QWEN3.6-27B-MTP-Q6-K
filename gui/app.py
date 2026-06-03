#!/usr/bin/env python3
"""Main application — wires together GUI components."""

import sys
from pathlib import Path

# Ensure project root is on sys.path so `gui.*` and `todo.*` resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime
from tkinter import Button, Frame, StringVar, Tk, messagebox
from tkinter.ttk import Label as TLabel

from gui.config import load_geometry, save_geometry
from gui.input_panel import InputPanel
from gui.task_table import TaskTable
from todo.store import load_todos, next_id, save_todos


class TaskApp:
    def __init__(self, root):
        root.title("Task Manager")
        root.minsize(800, 400)

        saved_geom = load_geometry()
        root.geometry(saved_geom or "1050x500")

        def on_close():
            save_geometry(root.geometry())
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_close)

        # Build UI
        self._input = InputPanel(root, self._add_task)

        self._table = TaskTable(root, self._toggle_task)

        btn_frame = Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        Button(btn_frame, text="Toggle Done", command=self._toggle_btn, width=12).pack(
            side="right", padx=5
        )
        Button(btn_frame, text="Delete", command=self._delete_task, width=10).pack(
            side="right", padx=5
        )

        self._stats = StringVar(value="0 tasks | 0 completed | 0 remaining")
        TLabel(root, textvariable=self._stats).pack(pady=(0, 8))

        self._refresh()

    # -- data actions ----------------------------------------------------------

    def _add_task(self, text, priority, due_date):
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
        self._refresh()

    def _toggle_task(self, todo_id):
        if todo_id is None:
            return
        todos = load_todos()
        for t in todos:
            if t["id"] == todo_id:
                t["done"] = not t["done"]
                save_todos(todos)
                self._refresh()
                self._table.selection_set(todo_id)
                return

    def _delete_task(self):
        todo_id = self._table.selected_id
        if todo_id is None:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return
        todos = load_todos()
        new_todos = [t for t in todos if t["id"] != todo_id]
        if len(new_todos) < len(todos):
            save_todos(new_todos)
            self._refresh()

    # -- UI helpers ------------------------------------------------------------

    def _toggle_btn(self):
        self._toggle_task(self._table.selected_id)

    def _refresh(self):
        todos = self._table.refresh()
        total = len(todos)
        done = sum(1 for t in todos if t["done"])
        self._stats.set(f"{total} tasks | {done} completed | {total - done} remaining")


def main():
    root = Tk()
    TaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
