from typing import List


def interactive_loop(app) -> None:
    print("Jubarte — modo interativo. Digite 'help' para comandos.")
    while True:
        try:
            line = input("jubarte> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo.")
            break
        if not line:
            continue
        parts: List[str] = line.split()
        cmd = parts[0]
        args = parts[1:]

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
