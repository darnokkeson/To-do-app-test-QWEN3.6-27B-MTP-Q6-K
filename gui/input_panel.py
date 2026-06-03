#!/usr/bin/env python3
"""Input panel for adding new tasks."""

from tkinter import Button, Entry, Frame, messagebox
from tkinter.ttk import Label

import ttkbootstrap as ttk

from gui.styles import (
    ACCENT,
    BG,
    FONT_BODY,
    FONT_BUTTON,
    FONT_CAPTION,
    SEPARATOR,
    SURFACE,
    TEXT,
    TEXT_SECONDARY,
)
from todo.utils import validate_date


class InputPanel:
    def __init__(self, parent, on_add):
        self._on_add = on_add

        self._frame = Frame(parent, bg=SURFACE, padx=16, pady=12)
        self._frame.pack(fill="x", padx=12, pady=(0, 8))

        # --- task entry ---
        self._entry = Entry(
            self._frame,
            font=FONT_BODY,
            bg=BG,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=SEPARATOR,
        )
        self._entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._entry.insert(0, "What needs to be done?")
        self._entry.bind("<FocusIn>", lambda _e: self._clear_hint())
        self._entry.bind("<Return>", lambda _e: self._try_add())

        # --- priority selector ---
        self._priority_var = ttk.StringVar(value="Medium")
        self._priority_cb = ttk.Combobox(
            self._frame,
            textvariable=self._priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=8,
        )
        self._priority_cb.pack(side="left", padx=(0, 12))

        # --- due date ---
        Label(
            self._frame,
            text="Due",
            font=FONT_CAPTION,
            foreground=TEXT_SECONDARY,
        ).pack(side="left", padx=(0, 4))

        self._due_entry = Entry(
            self._frame,
            width=12,
            font=FONT_BODY,
            bg=BG,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=SEPARATOR,
        )
        self._due_entry.pack(side="left", padx=(0, 12))

        # --- add button ---
        self._add_btn = Button(
            self._frame,
            text="Add",
            command=self._try_add,
            font=FONT_BUTTON,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=6,
            cursor="hand2",
        )
        self._add_btn.pack(side="left")

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

    def _clear_hint(self):
        if self._entry.get() == "What needs to be done?":
            self._entry.delete(0, "end")
        self._entry.config(fg=TEXT)

    def _try_add(self):
        if not self.text:
            return
        if self.due_date and not validate_date(self.due_date):
            messagebox.showwarning("Invalid Date", "Please use YYYY-MM-DD format.")
            return
        self._on_add(self.text, self.priority, self.due_date)
        self.clear()
