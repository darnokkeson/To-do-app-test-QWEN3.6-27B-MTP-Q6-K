#!/usr/bin/env python3
"""Input panel for adding new tasks."""

from tkinter import Button, Entry, Frame, StringVar, messagebox
from tkinter.ttk import Combobox, Label

from todo.utils import validate_date


class InputPanel:
    def __init__(self, parent, on_add):
        self._on_add = on_add
        self._frame = Frame(parent)
        self._frame.pack(fill="x", padx=10, pady=(10, 0))

        self._entry = Entry(self._frame, font=("Segoe UI", 12))
        self._entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self._entry.bind("<Return>", lambda _e: self._try_add())

        self._priority_var = StringVar(value="Medium")
        self._priority_cb = Combobox(
            self._frame,
            textvariable=self._priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=8,
        )
        self._priority_cb.pack(side="left", padx=5)

        Label(self._frame, text="Due:").pack(side="left", padx=(5, 2))
        self._due_entry = Entry(self._frame, width=12, font=("Segoe UI", 12))
        self._due_entry.pack(side="left", padx=2)

        Button(self._frame, text="Add", command=self._try_add, width=5).pack(
            side="left", padx=5
        )

    @property
    def text(self):
        return self._entry.get().strip()

    @property
    def priority(self):
        return self._priority_var.get().lower()

    @property
    def due_date(self):
        return self._due_entry.get().strip() or None

    def clear(self):
        self._entry.delete(0, "end")
        self._due_entry.delete(0, "end")

    def _try_add(self):
        if not self.text:
            return
        if self.due_date and not validate_date(self.due_date):
            messagebox.showwarning("Invalid Date", "Please use YYYY-MM-DD format.")
            return
        self._on_add(self.text, self.priority, self.due_date)
        self.clear()
