#!/usr/bin/env python3
"""Tkinter Desktop Task Manager with Priority and Due Dates"""

import json
import os
from datetime import datetime
from tkinter import Button, Entry, Frame, StringVar, Tk, messagebox
from tkinter import ttk

TODO_FILE = os.path.join(os.path.dirname(__file__), "..", "todo", "todos.json")

PRIORITY_EMOJI = {"high": "🔴", "medium": "🟠", "low": "🟢"}
PRIORITY_COLORS = {"high": "#f38ba8", "medium": "#fab387", "low": "#a6e3a1"}


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
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class TaskApp:
    def __init__(self, root):
        root.title("Task Manager")
        root.geometry("1050x500")
        root.minsize(800, 400)

        # Input row
        input_frame = Frame(root)
        input_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.entry = Entry(input_frame, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = StringVar(value="Medium")
        self.priority_cb = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=8,
        )
        self.priority_cb.pack(side="left", padx=5)

        ttk.Label(input_frame, text="Due:").pack(side="left", padx=(5, 2))
        self.due_entry = Entry(input_frame, width=12, font=("Segoe UI", 12))
        self.due_entry.pack(side="left", padx=2)

        Button(input_frame, text="Add", command=self.add_task, width=5).pack(
            side="left", padx=5
        )

        # Table frame
        table_frame = Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("status", "task", "priority", "due_date", "created")
        self.treeview = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="extended"
        )

        # Column headers and widths
        self.treeview.heading("status", text="✓")
        self.treeview.heading("task", text="Task")
        self.treeview.heading("priority", text="Priority")
        self.treeview.heading("due_date", text="Due Date")
        self.treeview.heading("created", text="Created")

        self.treeview.column("status", width=50, anchor="center")
        self.treeview.column("task", width=400, anchor="w")
        self.treeview.column("priority", width=120, anchor="center")
        self.treeview.column("due_date", width=130, anchor="center")
        self.treeview.column("created", width=130, anchor="center")

        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.treeview.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.treeview.pack(side="left", fill="both", expand=True)

        # Color tags
        for level, color in PRIORITY_COLORS.items():
            self.treeview.tag_configure(level, foreground=color)
        self.treeview.tag_configure("overdue", foreground="#f38ba8")

        # Double-click to toggle
        self.treeview.bind("<Double-Button-1>", self.toggle_task)

        # Bottom buttons
        btn_frame = Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        Button(btn_frame, text="Toggle Done", command=self.toggle_task, width=12).pack(
            side="right", padx=5
        )
        Button(btn_frame, text="Delete", command=self.delete_task, width=10).pack(
            side="right", padx=5
        )

        self.stats = StringVar(value="0 tasks | 0 completed | 0 remaining")
        ttk.Label(root, textvariable=self.stats).pack(pady=(0, 8))

        self.refresh()

    def refresh(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        todos = load_todos()
        for t in todos:
            status = "✓" if t["done"] else " "
            priority = t.get("priority", "medium")
            due = t.get("due_date")
            created = t.get("created", "")

            priority_display = f"{PRIORITY_EMOJI.get(priority, '')} {priority.capitalize()}"

            if due:
                overdue_str = " ⚠️ OVERDUE" if not t["done"] and is_overdue(due) else ""
                due_display = f"{due}{overdue_str}"
            else:
                due_display = "-"

            if not t["done"] and is_overdue(due):
                tag = "overdue"
            else:
                tag = priority

            self.treeview.insert(
                "", "end",
                iid=str(t["id"]),
                values=(status, t["text"], priority_display, due_display, created),
                tags=(tag,),
            )

        total = len(todos)
        done = sum(1 for t in todos if t["done"])
        self.stats.set(f"{total} tasks | {done} completed | {total - done} remaining")

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            return

        priority = self.priority_var.get().lower()
        due_date = self.due_entry.get().strip() or None

        if due_date and not validate_date(due_date):
            messagebox.showwarning("Invalid Date", "Please use YYYY-MM-DD format.")
            return

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

        self.entry.delete(0, "end")
        self.due_entry.delete(0, "end")
        self.refresh()

    def get_selected_todo_id(self):
        selected = self.treeview.selection()
        if not selected:
            return None
        try:
            return int(selected[0])
        except ValueError:
            return None

    def toggle_task(self, event=None):
        todo_id = self.get_selected_todo_id()
        if todo_id is None:
            return
        todos = load_todos()
        for t in todos:
            if t["id"] == todo_id:
                t["done"] = not t["done"]
                save_todos(todos)
                self.refresh()
                self.treeview.selection_set(str(todo_id))
                return

    def delete_task(self):
        todo_id = self.get_selected_todo_id()
        if todo_id is None:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return
        todos = load_todos()
        new_todos = [t for t in todos if t["id"] != todo_id]
        if len(new_todos) < len(todos):
            save_todos(new_todos)
            self.refresh()


def main():
    root = Tk()
    TaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
