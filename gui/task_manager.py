#!/usr/bin/env python3
"""Tkinter Desktop Task Manager — shares todo/todos.json with CLI app"""

import json
import os
from datetime import datetime
from tkinter import Button, Entry, Frame, Listbox, StringVar, Tk, messagebox, ttk

TODO_FILE = os.path.join(os.path.dirname(__file__), "..", "todo", "todos.json")


def load_todos():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
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


class TaskApp:
    def __init__(self, root):
        root.title("Task Manager")
        root.geometry("500x450")
        root.minsize(400, 350)

        input_frame = Frame(root)
        input_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.entry = Entry(input_frame, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", lambda e: self.add_task())

        Button(input_frame, text="Add", command=self.add_task, width=6).pack(
            side="right"
        )

        list_frame = Frame(root)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = Listbox(
            list_frame,
            font=("Segoe UI", 11),
            selectmode="single",
            yscrollcommand=scrollbar.set,
            height=12,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Double-Button-1>", self.toggle_task)

        btn_frame = Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        Button(btn_frame, text="Delete", command=self.delete_task, width=10).pack(
            side="right", padx=5
        )

        self.stats = StringVar(value="0 tasks | 0 completed | 0 remaining")
        ttk.Label(root, textvariable=self.stats).pack(pady=(0, 8))

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, "end")
        todos = load_todos()
        for t in todos:
            status = "x" if t["done"] else " "
            self.listbox.insert("end", f"[{status}] {t['text']}  ({t['created']})")

        total = len(todos)
        done = sum(1 for t in todos if t["done"])
        self.stats.set(f"{total} tasks | {done} completed | {total - done} remaining")

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            return

        todos = load_todos()
        todos.append(
            {
                "id": next_id(todos),
                "text": text,
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        save_todos(todos)
        self.entry.delete(0, "end")
        self.refresh()

    def toggle_task(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        todos = load_todos()
        if index < len(todos):
            todos[index]["done"] = not todos[index]["done"]
            save_todos(todos)
            self.refresh()
            self.listbox.selection_set(index)

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return

        index = selection[0]
        todos = load_todos()
        if index < len(todos):
            del todos[index]
            save_todos(todos)
            self.refresh()


def main():
    root = Tk()
    TaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
