"""
Interactive command-line loop for the Jubarte application.

This module provides a simple REPL (Read–Eval–Print Loop) that allows
users to interact with the application without restarting the program.
Supported commands include adding items, listing reviews, recording
review results, exporting calendars, and exiting the session.
"""

from typing import List


def interactive_loop(app) -> None:
    """
    Run the interactive (REPL) mode of the Jubarte application.

    This function continuously reads user input from the terminal,
    parses commands, and delegates actions to the provided application
    instance. The loop exits when the user types `exit` or triggers
    an interrupt signal (Ctrl+C / Ctrl+D).

    Args:
        app: An application instance that implements the core Jubarte
        operations such as adding items, listing reviews, exporting
        calendar files, and recording review results.
    """
    print("Jubarte — modo interativo. Digite 'help' para comandos.")
    while True:
        try:
            line = input("jubarte> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo.")
            break
        if not line:
            continue
        user_input: List[str] = line.split()
        cmd = user_input[0]
        args = user_input[1:]

        if cmd == "help":
            print(
                "comandos: add <title>, list, review <id> <result>, export <file>, exit"
            )
        elif cmd == "exit":
            break
        elif cmd == "add":
            title = " ".join(args)
            if not title:
                print("Título obrigatório")
                continue
            item = app.add_item(title)
            print(f"Adicionado: {item.id}")
        elif cmd == "list":
            for it, entry in app.list_items():
                print(f"{it.id} | {it.title} | Próx: {entry.next_review.isoformat()}")
        elif cmd == "review":
            if len(args) < 2:
                print("Uso: review <id> <again|hard|good|easy>")
                continue
            item_id, result = args[0], args[1]
            try:
                entry = app.review_item(item_id, result)
                print(f"Próxima: {entry.next_review.isoformat()}")
            except Exception as e:
                print("Erro:", e)
        elif cmd == "export":
            if len(args) < 1:
                print("Uso: export <arquivo.ics>")
                continue
            app.export_ics(args[0])
            print("Exportado.")
        else:
            print("Comando desconhecido. Digite 'help'.")
