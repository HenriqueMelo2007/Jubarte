"""Interactive REPL for the Jubarte CLI.

This module exposes a single function, ``interactive_loop(app)`` which runs a
small read–eval–print loop allowing users to interact with a running ``App``
instance. The function performs input parsing and delegates actions to the
provided ``app`` object. The ``app`` is expected to implement the following
methods used by the loop:

- ``add_item(title: str) -> StudyItem``
- ``list_items() -> Iterable[Tuple[StudyItem, ReviewItem]]``
- ``review_item(item_id: str, result: str) -> ReviewItem``
- ``export_ics(path: str) -> None``]
- ``clear() -> None``
- ``remove_item(title: str) -> None``

All messages and prompts are written to stdout; this function is intended for
use in a terminal and has side effects (printing, reading stdin, and calling
``app`` methods).
"""

from typing import Any, List


def interactive_loop(app: Any) -> None:
    """Start a simple interactive loop that accepts user commands.

    The loop reads lines from standard input, splits them into a command and
    arguments, and executes one of the supported commands by calling the
    corresponding method on ``app``. When the user sends EOF (Ctrl+D) or
    interrupts (Ctrl+C) the loop exits gracefully.

    Supported commands:
      - ``help``: show available commands.
      - ``add <title>``: create a new study item with the given title.
      - ``list``: list all items and their next review date.
      - ``export <file.ics>``: export items to an iCalendar file.
      - ``exit``: exit the interactive loop.
      - ``clear``: clear all items and reviews.
      - ``remove <title>``: remove an item by its title.

    Args:
        app: An application object implementing the methods described in the
            module docstring. The function does not validate the object's
            type at runtime; it will raise AttributeError if required methods
            are missing.

    Returns:
        None: The function runs until the user exits and does not return a
        value.
    """
    print("Jubarte — interactive mode. Type 'help' for commands.")
    while True:
        try:
            line = input("jubarte> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not line:
            continue
        user_input: List[str] = line.split()
        cmd = user_input[0]
        args = user_input[1:]

        if cmd == "help":
            print(
                "commands: add <title>, list, export <file>, clear, remove <title>, exit"
            )
        elif cmd == "exit":
            break
        elif cmd == "add":
            title = " ".join(args)
            if not title:
                print("Title is required")
                continue
            item = app.add_item(title)
            print(f"Added: {item.title}")
        elif cmd == "list":
            for it, review in app.list_items():
                print(
                    f"{it.title} | Review date: {review.review_date.isoformat()[:10]}"
                )
        elif cmd == "export":
            if len(args) < 1:
                print("Usage: export <file.ics>")
                continue
            app.export_ics(args[0])
            print("Exported.")
        elif cmd == "clear":
            app.clear()
            print("Cleared all items and reviews.")
        elif cmd == "remove":
            if len(args) < 1:
                print("Usage: remove <title>")
                continue
            title = " ".join(args)
            app.remove_item(title)
            print(f"Removed item with title: {title}")
        else:
            print("Unknown command. Type 'help'.")
