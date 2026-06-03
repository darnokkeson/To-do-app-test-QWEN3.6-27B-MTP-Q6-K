#!/usr/bin/env python3
"""Main application — wires together GUI components."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime
from tkinter import Button, Frame, StringVar, messagebox

import ttkbootstrap as ttk

from gui.config import load_geometry, save_geometry
from gui.input_panel import InputPanel
from gui.styles import (
    ACCENT,
    BG,
    DANGER,
    FONT_BUTTON,
    FONT_CAPTION,
    FONT_TITLE,
    SEPARATOR,
    SURFACE,
    TEXT,
    TEXT_SECONDARY,
    THEME_NAME,
)
from gui.task_table import TaskTable
from todo.store import load_todos, next_id, save_todos


class TaskApp:
    def __init__(self, root):
        root.title("Tasks")
        root.minsize(860, 460)

        saved_geom = load_geometry()
        root.geometry(saved_geom or "1100x540")
        root.configure(bg=BG)

        def on_close():
            save_geometry(root.geometry())
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_close)

        # -- header --------------------------------------------------------
        header = Frame(root, bg=BG)
        header.pack(fill="x", padx=20, pady=(16, 4))

        ttk.Label(
            header,
            text="Tasks",
            font=FONT_TITLE,
            foreground=TEXT,
        ).pack(side="left")

        self._stats = StringVar(value="0 tasks · 0 done · 0 remaining")
        ttk.Label(
            header,
            textvariable=self._stats,
            font=FONT_CAPTION,
            foreground=TEXT_SECONDARY,
        ).pack(side="right")

        # -- separator line ------------------------------------------------
        Frame(root, height=1, bg=SEPARATOR).pack(fill="x", padx=12)

        # -- input ---------------------------------------------------------
        self._input = InputPanel(root, self._add_task)

        # -- task list -----------------------------------------------------
        self._table = TaskTable(root)
        self._table.set_toggle_callback(self._toggle_task)

        # -- action buttons ------------------------------------------------
        btn_frame = Frame(root, bg=BG)
        btn_frame.pack(fill="x", padx=20, pady=(0, 4))

        Button(
            btn_frame,
            text="Complete",
            command=self._toggle_btn,
            font=FONT_BUTTON,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=6,
            cursor="hand2",
        ).pack(side="right", padx=(8, 0))

        Button(
            btn_frame,
            text="Delete",
            command=self._delete_task,
            font=FONT_BUTTON,
            bg=DANGER,
            fg="white",
            activebackground=DANGER,
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=6,
            cursor="hand2",
        ).pack(side="right")

        # -- keyboard hints ------------------------------------------------
        hints = Frame(root, bg=BG)
        hints.pack(fill="x", pady=(0, 10))
        ttk.Label(
            hints,
            text="Double-click to toggle  ·  Delete key to remove",
            font=FONT_CAPTION,
            foreground=TEXT_SECONDARY,
        ).pack()

        # -- keyboard shortcuts --------------------------------------------
        root.bind("<Control-Return>", lambda _e: self._toggle_btn())
        root.bind("<Delete>", lambda _e: self._delete_task())

        self._refresh()

    # -- data actions ------------------------------------------------------

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
            self._table.clear_selection()
            self._refresh()

    # -- UI helpers --------------------------------------------------------

    def _toggle_btn(self):
        self._toggle_task(self._table.selected_id)

    def _refresh(self):
        todos = self._table.refresh()
        total = len(todos)
        done = sum(1 for t in todos if t["done"])
        self._stats.set(f"{total} tasks · {done} done · {total - done} remaining")


def main():
    root = ttk.Window(themename=THEME_NAME)
    TaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
