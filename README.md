# 📋 To-Do App

A lightweight task manager with both CLI and Tkinter desktop interfaces, sharing the same JSON data store.

## ✨ What's Done

- **CLI task manager** (`todo/todo.py`) — add, list, complete, and remove tasks from the terminal
- **Tkinter desktop app** (`gui/task_manager.py`) — native GUI with task list, double-click to toggle, delete, and live stats
- **Shared data store** (`todo/todos.json`) — both interfaces read/write the same file
- **Safe ID generation** — IDs are unique and never collide after deletions
- **Error handling** — graceful recovery from corrupt JSON or bad input

## 🚀 Next Features

- [ ] **Priority levels** — High / Medium / Low with color coding
- [ ] **Due dates** — Set deadlines and highlight overdue tasks
- [ ] **Categories / Tags** — Group tasks (work, personal, etc.)
- [ ] **Search & Filter** — Find tasks fast, filter by status or priority
- [ ] **Task editing** — Rename a task without deleting and re-adding it
- [ ] **Dark mode** — Toggle between light and dark themes
- [ ] **Persistent layout** — Remember window size and position
- [ ] **Drag & drop reorder** — Manually sort task priority

## Usage

```bash
# CLI
python todo/todo.py list
python todo/todo.py add "Buy groceries"
python todo/todo.py done 1
python todo/todo.py rm 1

# Tkinter GUI
python gui/task_manager.py
```
