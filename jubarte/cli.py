import argparse

from .app import App


def build_parser():
    p = argparse.ArgumentParser(prog="jubarte")
    sub = p.add_subparsers(dest="cmd")

    add = sub.add_parser("add", help="Adicionar novo tópico")
    add.add_argument("title")
    add.add_argument("--notes", "-n", default="")

    sub.add_parser("interactive", help="Modo interativo (REPL)")

    exp = sub.add_parser("export", help="Exportar .ics")
    exp.add_argument("output", help="arquivo.ics")

    list_p = sub.add_parser("list", help="Listar itens")
    list_p.add_argument(
        "--due-today", action="store_true", help="Apenas itens para hoje"
    )

    review = sub.add_parser("review", help="Marcar resultado de revisão")
    review.add_argument("item_id")
    review.add_argument(
        "--result", choices=["again", "hard", "good", "easy"], required=True
    )

    sub.add_parser("version", help="Mostrar versão")

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    app = App()

    if args.cmd == "add":
        item = app.add_item(args.title, args.notes)
        print(f"Adicionado: {item.id} - {item.title}")
    elif args.cmd == "interactive":
        app.run_interactive()
    elif args.cmd == "export":
        app.export_ics(args.output)
        print(f"Exportado: {args.output}")
    elif args.cmd == "list":
        items = app.list_items(due_only=args.due_today)
        for it, entry in items:
            print(f"{it.id} | {it.title} | Próx: {entry.next_review.isoformat()}")
    elif args.cmd == "review":
        entry = app.review_item(args.item_id, args.result)
        print(f"Revisado: {args.item_id} → próxima: {entry.next_review.isoformat()}")
    elif args.cmd == "version":
        from . import __version__

        print(__version__)
    else:
        parser.print_help()
