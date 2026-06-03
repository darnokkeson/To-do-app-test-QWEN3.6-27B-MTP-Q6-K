#!/usr/bin/env python3
"""Window geometry persistence."""

import json
import os

from todo.store import CONFIG_FILE


def load_geometry():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        geom = config.get("geometry", "")
        parts = geom.split("+")
        size = parts[0].split("x")
        w, h = int(size[0]), int(size[1])
        if w >= 800 and h >= 400:
            return geom
    except (json.JSONDecodeError, OSError, ValueError, IndexError):
        pass
    return None


def save_geometry(geometry):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"geometry": geometry}, f, indent=2)
