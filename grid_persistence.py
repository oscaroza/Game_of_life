import atexit
import json
import signal
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "live_cells_state.json"
_signals_registered = False


def _collect_live_cells(grid, num_rows, num_cols):
    live_cells = []
    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == 1:
                live_cells.append([row, col])
    return live_cells


def save_live_cells(grid, num_rows, num_cols, state_file=STATE_FILE):
    payload = {
        "rows": num_rows,
        "cols": num_cols,
        "live_cells": _collect_live_cells(grid, num_rows, num_cols),
    }
    try:
        state_file.write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        return 0
    return len(payload["live_cells"])


def load_live_cells(grid, num_rows, num_cols, state_file=STATE_FILE):
    if not state_file.exists():
        return 0

    try:
        payload = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return 0

    live_cells = payload.get("live_cells", [])
    if not isinstance(live_cells, list):
        return 0

    for row in range(num_rows):
        for col in range(num_cols):
            grid[row][col] = 0

    restored = 0
    for cell in live_cells:
        if not isinstance(cell, (list, tuple)) or len(cell) != 2:
            continue

        row, col = cell
        if not isinstance(row, int) or not isinstance(col, int):
            continue
        if 0 <= row < num_rows and 0 <= col < num_cols:
            grid[row][col] = 1
            restored = restored + 1

    return restored


def _safe_run(callback):
    try:
        callback()
    except Exception:
        return


def register_auto_save(save_callback):
    global _signals_registered

    atexit.register(lambda: _safe_run(save_callback))

    if _signals_registered:
        return

    def _signal_handler(signum, frame):
        _safe_run(save_callback)
        raise SystemExit(0)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _signal_handler)
        except (ValueError, OSError, RuntimeError):
            continue

    _signals_registered = True
