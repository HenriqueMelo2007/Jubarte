"""jubarte CLI

This module provides a command-line interface for the Jubarte application.
It exposes two helpers:

- ``build_parser()`` — constructs and returns an ``argparse.ArgumentParser``
  configured with the supported subcommands (add, interactive, export, list, clear, remove, and
  version).
- ``main(argv=None)`` — program entry point that parses the provided
  arguments, instantiates :class:`~.app.App` and dispatches the chosen
  subcommand.

The CLI is intentionally small: the heavy lifting belongs to :class:`.app.App`.
"""

import argparse

from .app import App


def build_parser():
    """Build and return the top-level argument parser for the Jubarte CLI.

    The parser is configured with the following subcommands and arguments:

    - ``add <title> [--notes|-n NOTES]``: add a new study/topic with an optional
      notes field.
    - ``interactive``: start the interactive REPL mode.
    - ``export <output>``: export items to an iCalendar (``.ics``) file.
    - ``clear``: clear all stored items and reviews.
    - ``remove <title>``: remove an item by its title.
    - ``list [--due-today]``: list stored items; ``--due-today`` limits results
      to items due today.
    - ``version``: print the package version and exit.

    Returns:
        argparse.ArgumentParser: a ready-to-use parser instance.
    """

    jubarte_parser = argparse.ArgumentParser(prog="jubarte")
    sub_parsers = jubarte_parser.add_subparsers(dest="cmd")

    add = sub_parsers.add_parser("add", help="Add a new topic")
    add.add_argument("title", help="Title of the topic to add")
    add.add_argument("--notes", "-n", default="", help="Optional notes for the topic")

    sub_parsers.add_parser("interactive", help="Interactive mode (REPL)")

    exp = sub_parsers.add_parser("export", help="Export to .ics file")
    exp.add_argument("output", help="output .ics file")

    list_p = sub_parsers.add_parser("list", help="List items")
    list_p.add_argument("--due-today", action="store_true", help="Only items due today")

    sub_parsers.add_parser("clear", help="Clear all items and reviews")

    remove = sub_parsers.add_parser("remove", help="Remove an item by title")
    remove.add_argument("title", help="Title of the item to remove")

    sub_parsers.add_parser("version", help="Show version")

    return jubarte_parser


def main(argv=None):
    """CLI entry point: parse arguments and dispatch to :class:`App`.

    This function builds the argument parser with :func:`build_parser`, parses
    the provided ``argv`` (a list of strings or ``None`` to read from
    ``sys.argv``), creates an :class:`App` instance and executes the selected
    command. Side effects include printing messages to stdout and writing an
    output file when the ``export`` command is used.

    Args:
        argv (list[str] | None, optional): List of command-line arguments to
            parse (excluding the program name). If ``None`` the real command
            line is used. Defaults to ``None``.

    Returns:
        None: this function does not return a value; it performs actions based
        on the parsed subcommand.

    Raises:
        SystemExit: if argument parsing fails or if ``--help`` is requested
            (raised by ``argparse``). Other exceptions raised by underlying
            :class:`App` methods may propagate to the caller.
    """

    jubarte_parser = build_parser()
    parsed_user_args = jubarte_parser.parse_args(argv)
    app = App()

    if parsed_user_args.cmd == "add":
        item = app.add_item(parsed_user_args.title, parsed_user_args.notes)
        print(f"Added: {item.title}")
    elif parsed_user_args.cmd == "interactive":
        app.run_interactive()
    elif parsed_user_args.cmd == "export":
        app.export_ics(parsed_user_args.output)
        print(f"Exported: {parsed_user_args.output}")
    elif parsed_user_args.cmd == "list":
        items = app.list_items(due_only=parsed_user_args.due_today)
        for it, review in items:
            print(f"{it.title} | Review date: {review.review_date.isoformat()[:10]}")
    elif parsed_user_args.cmd == "version":
        from . import __version__

        print(__version__)
    elif parsed_user_args.cmd == "clear":
        app.clear()
    elif parsed_user_args.cmd == "remove":
        items = app.list_items()
        to_remove = [it for it, _ in items if it.title == parsed_user_args.title]
        if not to_remove:
            print(f"No item found with title: {parsed_user_args.title}")
        else:
            for it in to_remove:
                app.remove_item(it.title)

    else:
        jubarte_parser.print_help()
