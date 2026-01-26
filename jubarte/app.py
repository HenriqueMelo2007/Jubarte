from typing import List, Tuple

from .core.scheduler import SimpleSpacedScheduler
from .export.ics_exporter import ICSExporter
from .models import ReviewEntry, StudyItem, new_item
from .storage.file_store import FileStore
from .ui.interactive import interactive_loop


class App:
    def __init__(self, store=None, scheduler=None, exporter=None):
        self.store = store or FileStore()
        self.scheduler = scheduler or SimpleSpacedScheduler()
        self.exporter = exporter or ICSExporter()

    def add_item(self, title: str, notes: str = "") -> StudyItem:
        item = new_item(title, notes)
        self.store.save_item(item)
        entry = self.scheduler.generate_initial(item)
        self.store.save_entry(entry)
        return item

    def list_items(self, due_only: bool = False) -> List[Tuple[StudyItem, ReviewEntry]]:
        items = {it.id: it for it in self.store.load_items()}
        entries = {e.item_id: e for e in self.store.load_entries()}
        res = []
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        for item_id, item in items.items():
            entry = entries.get(item_id)
            if not entry:
                continue
            if due_only and entry.next_review.date() != now.date():
                continue
            res.append((item, entry))
        return res

    def review_item(self, item_id: str, result: str) -> ReviewEntry:
        entry = self.store.load_entry_for_item(item_id)
        if not entry:
            raise ValueError("Item não encontrado")
        entry = self.scheduler.update(entry, result)
        self.store.save_entry(entry)
        return entry

    def export_ics(self, path: str) -> None:
        entries = self.store.load_entries()
        items = {it.id: it for it in self.store.load_items()}
        self.exporter.export(entries, items, path)

    def run_interactive(self) -> None:
        interactive_loop(self)
