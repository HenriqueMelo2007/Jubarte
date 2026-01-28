"""
Command-line interface (CLI) entry point for the Jubarte application.

This module defines the argument jubarte_parser and the main command dispatcher,
mapping CLI commands to application behaviors such as adding study topics,
listing items, exporting calendars, and reviewing content.
"""

import argparse

from .app import App


def build_parser():
    """
    Build and configure the argument jubarte_parser for the Jubarte CLI.

    This function defines all supported subcommands and their arguments,
    including commands for adding items, listing pending reviews,
    exporting calendar files, and recording review results.

    Returns:
        argparse.ArgumentParser: A fully configured argument jubarte_parser
        for the Jubarte command-line interface.
    """
    jubarte_parser = argparse.ArgumentParser(prog="jubarte")
    sub_parsers = jubarte_parser.add_subparsers(dest="cmd")

    add = sub_parsers.add_parser("add", help="Adicionar novo tópico")
    add.add_argument("title")
    add.add_argument("--notes", "-n", default="")

    sub_parsers.add_parser("interactive", help="Modo interativo (REPL)")

    exp = sub_parsers.add_parser("export", help="Exportar .ics")
    exp.add_argument("output", help="arquivo.ics")

    list_p = sub_parsers.add_parser("list", help="Listar itens")
    list_p.add_argument(
        "--due-today", action="store_true", help="Apenas itens para hoje"
    )

    review = sub_parsers.add_parser("review", help="Marcar resultado de revisão")
    review.add_argument("item_id")
    review.add_argument(
        "--result", choices=["again", "hard", "good", "easy"], required=True
    )

    sub_parsers.add_parser("version", help="Mostrar versão")

    return jubarte_parser


def main(argv=None):
    """
    Execute the Jubarte CLI application.

    This function parses command-line arguments, initializes the application,
    and dispatches execution to the appropriate command handler based on
    the selected subcommand.

    Args:
        argv (list[str] | None, optional): A list of command-line arguments.
        If None, arguments are read directly from sys.argv.
    """
    jubarte_parser = build_parser()
    parsed_user_args = jubarte_parser.parse_args(argv)
    app = App()

    if parsed_user_args.cmd == "add":
        item = app.add_item(parsed_user_args.title, parsed_user_args.notes)
        print(f"Adicionado: {item.id} - {item.title}")
    elif parsed_user_args.cmd == "interactive":
        app.run_interactive()
    elif parsed_user_args.cmd == "export":
        app.export_ics(parsed_user_args.output)
        print(f"Exportado: {parsed_user_args.output}")
    elif parsed_user_args.cmd == "list":
        items = app.list_items(due_only=parsed_user_args.due_today)
        for it, entry in items:
            print(f"{it.id} | {it.title} | Próx: {entry.next_review.isoformat()}")
    elif parsed_user_args.cmd == "review":
        entry = app.review_item(parsed_user_args.item_id, parsed_user_args.result)
        print(
            f"Revisado: {parsed_user_args.item_id} → próxima: {entry.next_review.isoformat()}"
        )
    elif parsed_user_args.cmd == "version":
        from . import __version__

        print(__version__)
    else:
        jubarte_parser.print_help()
