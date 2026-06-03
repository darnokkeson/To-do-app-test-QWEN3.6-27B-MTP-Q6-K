#!/usr/bin/env python3
"""Design tokens — colors, typography, and theme configuration."""

# -- Theme ------------------------------------------------------------------
THEME_NAME = "cosmo"

# -- Palette ----------------------------------------------------------------
BG = "#f5f5f7"
SURFACE = "#ffffff"
ACCENT = "#007aff"
TEXT = "#1d1d1f"
TEXT_SECONDARY = "#86868b"
SEPARATOR = "#e5e5ea"
DANGER = "#ff3b30"
SUCCESS = "#34c759"
OVERDUE = "#ff3b30"

# -- Priority ---------------------------------------------------------------
PRIORITY_COLORS = {
    "high": "#ff3b30",
    "medium": "#ff9500",
    "low": "#34c759",
}

PRIORITY_BADGE = {
    "high": {"bg": "#fff0f0", "fg": "#ff3b30"},
    "medium": {"bg": "#fff8f0", "fg": "#ff9500"},
    "low": {"bg": "#f0fff4", "fg": "#34c759"},
}

# -- Typography -------------------------------------------------------------
FONT_FAMILY = ("Inter", "Segoe UI", "system-ui", "sans-serif")
FONT_TITLE = (FONT_FAMILY, 16, "bold")
FONT_BODY = (FONT_FAMILY, 13)
FONT_BUTTON = (FONT_FAMILY, 12)
FONT_CAPTION = (FONT_FAMILY, 11)
FONT_SMALL = (FONT_FAMILY, 10)
