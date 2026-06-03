#!/usr/bin/env python3
"""Task table with Treeview, scrollbars, and refresh logic."""

from tkinter import Frame
from tkinter.ttk import Scrollbar, Style, Treeview

from gui.styles import PRIORITY_COLORS, PRIORITY_EMOJI
from todo.store import load_todos
from todo.utils import is_overdue


class TaskTable:
    COLUMNS = ("status", "task", "priority", "due_date", "created")

    def __init__(self, parent, on_toggle):
        self._on_toggle = on_toggle
        self._frame = Frame(parent)
        self._frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = Style()
        style.configure("Treeview", rowheight=40)

        self._tree = Treeview(
            self._frame, columns=self.COLUMNS, show="headings", selectmode="extended"
        )

        self._tree.heading("status", text="✓")
        self._tree.heading("task", text="Task")
        self._tree.heading("priority", text="Priority")
        self._tree.heading("due_date", text="Due Date")
        self._tree.heading("created", text="Created")

        self._tree.column("status", width=50, anchor="center")
        self._tree.column("task", width=500, anchor="w")
        self._tree.column("priority", width=130, anchor="center")
        self._tree.column("due_date", width=150, anchor="center")
        self._tree.column("created", width=140, anchor="center")

        v_scroll = Scrollbar(self._frame, orient="vertical", command=self._tree.yview)
        h_scroll = Scrollbar(self._frame, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self._tree.pack(side="left", fill="both", expand=True)

        for level, color in PRIORITY_COLORS.items():
            self._tree.tag_configure(level, foreground=color)
        self._tree.tag_configure("overdue", foreground=PRIORITY_COLORS["high"])

        self._tree.bind(
            "<Double-Button-1>", lambda _e: self._on_toggle(self.selected_id)
        )

    @property
    def selected_id(self):
        selected = self._tree.selection()
        if not selected:
            return None
        try:
            return int(selected[0])
        except ValueError:
            return None

    def refresh(self):
        for item in self._tree.get_children():
            self._tree.delete(item)

        todos = load_todos()
        for t in todos:
            status = "✓" if t["done"] else " "
            priority = t.get("priority", "medium")
            due = t.get("due_date")
            created = t.get("created", "")

            priority_display = (
                f"{PRIORITY_EMOJI.get(priority, '')} {priority.capitalize()}"
            )

            if due:
                overdue_str = " ⚠️ OVERDUE" if not t["done"] and is_overdue(due) else ""
                due_display = f"{due}{overdue_str}"
            else:
                due_display = "-"

            tag = "overdue" if (not t["done"] and is_overdue(due)) else priority

            self._tree.insert(
                "",
                "end",
                iid=str(t["id"]),
                values=(status, t["text"], priority_display, due_display, created),
                tags=(tag,),
            )

        return todos

    def selection_set(self, iid):
        self._tree.selection_set(str(iid))
