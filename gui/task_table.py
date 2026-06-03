#!/usr/bin/env python3
"""Card-style task list with smooth scrolling."""

from tkinter import Canvas, Frame, Label, Scrollbar

import ttkbootstrap as ttk

from gui.styles import (
    BG,
    FONT_BODY,
    FONT_CAPTION,
    FONT_FAMILY,
    FONT_SMALL,
    OVERDUE,
    PRIORITY_BADGE,
    SEPARATOR,
    SUCCESS,
    SURFACE,
    TEXT,
    TEXT_SECONDARY,
)
from todo.store import load_todos
from todo.utils import is_overdue


class TaskTable:
    def __init__(self, parent):
        self._on_toggle = None
        self._selected_id = None
        self._frames = {}

        # container
        self._container = Frame(parent, bg=BG)
        self._container.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        # card surface
        self._card = Frame(self._container, bg=SURFACE)
        self._card.pack(fill="both", expand=True)

        # canvas + scrollbar
        self._canvas = Canvas(
            self._card,
            bg=SURFACE,
            highlightthickness=0,
            relief="flat",
        )
        self._scrollbar = ttk.Scrollbar(
            self._card, orient="vertical", command=self._canvas.yview
        )
        self._inner = Frame(self._canvas, bg=SURFACE)

        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.create_window((0, 0), window=self._inner, anchor="nw")

        self._scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # scrolling
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self._canvas.bind_all("<Button-4>", self._on_mousewheel)
        self._canvas.bind_all("<Button-5>", self._on_mousewheel)
        self._inner.bind("<Configure>", lambda _e: self._update_scroll_region())

    def set_toggle_callback(self, callback):
        self._on_toggle = callback

    # -- rendering ----------------------------------------------------------

    def refresh(self):
        # clear previous
        for widget in self._inner.winfo_children():
            widget.destroy()
        self._frames.clear()
        self._selected_id = None

        todos = load_todos()

        if not todos:
            self._render_empty()
            return todos

        for idx, t in enumerate(todos):
            self._render_task(t, idx)

        self._update_scroll_region()
        return todos

    def _render_empty(self):
        Label(
            self._inner,
            text="+",
            font=(FONT_FAMILY, 48),
            foreground=SEPARATOR,
            bg=SURFACE,
        ).pack(pady=(80, 16))
        Label(
            self._inner,
            text="No tasks yet",
            font=FONT_BODY,
            foreground=TEXT_SECONDARY,
            bg=SURFACE,
        ).pack(pady=(0, 8))
        Label(
            self._inner,
            text="Add a task above to get started",
            font=FONT_CAPTION,
            foreground=TEXT_SECONDARY,
            bg=SURFACE,
        ).pack(pady=(0, 60))

    def _render_task(self, t, idx):
        done = t["done"]
        priority = t.get("priority", "medium")
        due = t.get("due_date")
        created = t.get("created", "")

        badge = PRIORITY_BADGE.get(priority, PRIORITY_BADGE["medium"])

        row = Frame(self._inner, bg=SURFACE, padx=16, pady=12)
        row.pack(fill="x")

        # separator (not on first row)
        if idx > 0:
            sep = Frame(self._inner, height=1, bg=SEPARATOR)
            sep.pack(fill="x", padx=16)

        # checkbox circle
        check_color = SUCCESS if done else SEPARATOR
        check_text = "✓" if done else ""
        check = Label(
            row,
            text=check_text,
            font=(FONT_FAMILY, 14),
            foreground=check_color,
            bg=SURFACE,
            width=2,
        )
        check.pack(side="left", padx=(0, 12))

        # task name + done strike-through
        task_label = Label(
            row,
            text=t["text"],
            font=(FONT_FAMILY, 13, "italic" if done else "normal"),
            foreground=TEXT_SECONDARY if done else TEXT,
            bg=SURFACE,
            anchor="w",
        )
        task_label.pack(side="left", fill="x", expand=True, padx=(0, 12))

        # priority badge
        priority_label = Label(
            row,
            text=priority.capitalize(),
            font=FONT_SMALL,
            foreground=badge["fg"],
            background=badge["bg"],
            padx=8,
            pady=2,
        )
        priority_label.pack(side="left", padx=(0, 8))

        # due date
        if due:
            overdue = not done and is_overdue(due)
            due_display = due
            due_color = OVERDUE if overdue else TEXT_SECONDARY
            if overdue:
                due_display += "  ⚠"
        else:
            due_display = None
            due_color = TEXT_SECONDARY

        if due_display:
            due_label = Label(
                row,
                text=due_display,
                font=FONT_CAPTION,
                foreground=due_color,
                bg=SURFACE,
            )
            due_label.pack(side="left", padx=(0, 8))

        # created
        if created:
            created_label = Label(
                row,
                text=created,
                font=FONT_SMALL,
                foreground=TEXT_SECONDARY,
                bg=SURFACE,
            )
            created_label.pack(side="left")

        # interactions
        self._frames[t["id"]] = row
        row.bind("<Enter>", lambda _e, r=row: self._on_hover(r, True))
        row.bind("<Leave>", lambda _e, r=row: self._on_hover(r, False))
        row.bind(
            "<Double-Button-1>",
            lambda _e, tid=t["id"]: self._on_toggle(tid) if self._on_toggle else None,
        )
        row.bind(
            "<Button-1>",
            lambda _e, tid=t["id"]: self._select_task(tid, row),
        )

    # -- selection ----------------------------------------------------------

    def _select_task(self, task_id, row):
        if self._selected_id and self._selected_id in self._frames:
            old = self._frames[self._selected_id]
            old.config(bg=SURFACE)
        self._selected_id = task_id
        row.config(bg="#f0f4ff")

    @property
    def selected_id(self):
        return self._selected_id

    def clear_selection(self):
        if self._selected_id and self._selected_id in self._frames:
            self._frames[self._selected_id].config(bg=SURFACE)
        self._selected_id = None

    # -- hover --------------------------------------------------------------

    def _on_hover(self, row, entering):
        if row == self._frames.get(self._selected_id):
            return
        row.config(bg="#fafafa" if entering else SURFACE)

    # -- scroll -------------------------------------------------------------

    def _on_mousewheel(self, event):
        if event.num == 4:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self._canvas.yview_scroll(1, "units")
        elif event.num == 120:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 200:
            self._canvas.yview_scroll(1, "units")

    def _update_scroll_region(self):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
