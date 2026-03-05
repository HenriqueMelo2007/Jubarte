# 🐋JUBARTE

```python
Python CLI tool for scheduling spaced reviews and exporting a calendar `.ics` file with review dates.
```

![Banner](/assets/wallpaper.png)

## Description

**Jubarte** is a command-line utility that allows users to register study topics and generate an initial review plan based on spaced-repetition intervals. The calculated dates can be exported as an iCalendar (`.ics`) file for import into calendar applications.  

The business logic (item creation, scheduling, persistence, and export) is organized in an application layer (`App`) and modular components (store, scheduler, exporter) that can be replaced or extended.

## Features

- Add a new study topic (title + optional notes).
- Automatically generate a set of initial reviews using predefined spaced intervals.
- List items and their upcoming reviews (optionally only those due today).
- Interactive terminal mode (REPL).
- Remove item(s) by title.
- Clear all stored data (items and reviews).
- Export all scheduled reviews to an iCalendar (`.ics`) file.

## Installation

### Pip

```bash
pip install jubarte
```

### Git Clone

> Requirements: Python `>=3.14,<3.15` (as defined in `pyproject.toml`)

Using **Poetry** (recommended for development):

```bash
git clone https://github.com/HenriqueMelo2007/Jubarte.git
cd Jubarte
poetry install
```

## Usage

> The main CLI command is exposed via the entry point jubarte.

- Add a study topic

```bash
jubarte add "Calculus - Derivatives" --notes "Review exercises from chapter 1"

# Expected output:
# Added: Calculus - Derivatives
```

- Interactive mode

```bash
jubarte interactive

# Starts the interactive command loop defined in jubarte.ui.interactive.
```

- List all items

```bash
jubarte list

# Example output:
# Calculus - Derivatives | Review date: 2026-03-06
```

- List items due today

```bash
jubarte list --due-today
```

- Export review schedule to .ics

```bash
jubarte export review_schedule.ics

# Example output:
#Exported: review_schedule.ics

# If no reviews exist:
# No reviews to export.
```

- Remove item(s) by title

```bash
jubarte remove "Calculus - Derivatives"

# Example output:
# Removed item(s) with title: Calculus - Derivatives
```

- Clear all stored data

```bash
jubarte clear

# Output:
# Cleared all items and reviews.
```

- Show version

```bash
jubarte version
```

## CLI interface

The CLI is built with `argparse` and supports the following subcommands:

- `add <title> [--notes|-n NOTES]` — add a new study topic.

- `interactive` — start interactive REPL mode.

- `export <output>` — export all scheduled reviews to an .ics file.

- `list [--due-today]` — list items and review dates; --due-today filters only reviews scheduled for the current day (UTC).

- `clear` — remove all stored items and reviews.

- `remove <title>` — remove items that match the provided title.

- `version` — print the package version.

Observed behavior from the implementation:

`add_item raises ValueError` if an item with the same title already exists.

`list_items(due_only=True)` compares review dates against the current UTC date.

`export_ics(path)` writes an .ics file using the exporter and prints the result.

## Scheduler

SimpleSpacedScheduler generates an initial sequence of reviews using fixed intervals (in days):

```python
[1, 3, 7, 14, 30, 60, 120, 240, 360, 720]
```

Each interval is added to the current UTC timestamp to determine future review dates.

## ICS Exporter

ICSExporter generates a standards-compliant iCalendar file:

- Datetimes formatted as YYYYMMDDTHHMMSSZ (UTC)
- Escapes reserved characters in text fields
- Applies line folding according to RFC 5545
- Writes files atomically using a temporary file and os.replace

## License

MIT

## Author

HenriqueMelo2007
