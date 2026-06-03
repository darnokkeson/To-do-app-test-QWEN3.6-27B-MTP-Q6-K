# 📋 To-Do App

A lightweight task manager with both CLI and Tkinter desktop interfaces, sharing the same JSON data store.

## ✨ What's Done

- **CLI task manager** (`todo/todo.py`) — add, list, complete, and remove tasks from the terminal
- **Tkinter desktop app** (`gui/app.py`) — native GUI with task list, double-click to toggle, delete, and live stats
- **Shared data store** (`todo/todos.json`) — both interfaces read/write the same file
- **Shared data layer** (`todo/store.py`, `todo/utils.py`) — no code duplication between CLI and GUI
- **Modular GUI** — input panel, task table, styles, and config each in their own file
- **Safe ID generation** — IDs are unique and never collide after deletions
- **Error handling** — graceful recovery from corrupt JSON or bad input

## 📁 Project Structure

```
todo/
├── __init__.py
├── store.py        # load/save/next_id (shared by CLI + GUI)
├── utils.py        # is_overdue, validate_date (shared by CLI + GUI)
└── todo.py         # CLI entry point
gui/
├── __init__.py
├── app.py          # main TaskApp + main() entry point
├── input_panel.py  # task input row
├── task_table.py   # Treeview table + refresh
├── config.py       # window geometry persistence
└── styles.py       # priority emojis and colors
```

## 🚀 Next Features

- [x] **Priority levels** — High / Medium / Low with color coding
- [x] **Due dates** — Set deadlines and highlight overdue tasks
- [ ] **Categories / Tags** — Group tasks (work, personal, etc.)
- [ ] **Search & Filter** — Find tasks fast, filter by status or priority
- [ ] **Task editing** — Rename a task without deleting and re-adding it
- [ ] **Dark mode** — Toggle between light and dark themes
- [x] **Persistent layout** — Remember window size and position
- [ ] **Drag & drop reorder** — Manually sort task priority

## Usage

```bash
# CLI
python todo/todo.py list
python todo/todo.py add "Buy groceries"
python todo/todo.py done 1
python todo/todo.py rm 1

# Tkinter GUI
python gui/app.py
```
