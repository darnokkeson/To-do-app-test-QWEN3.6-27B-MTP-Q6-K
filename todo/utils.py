#!/usr/bin/env python3
"""Shared utility helpers."""

from datetime import datetime


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
