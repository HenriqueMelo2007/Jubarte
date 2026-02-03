from typing import List, Tuple

from .core.scheduler import SimpleSpacedScheduler
from .export.ics_exporter import ICSExporter
from .models import ReviewItem, StudyItem, new_item
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
        review = self.scheduler.generate_initial(item)
        self.store.save_review(review)
        return item

    def list_items(self, due_only: bool = False) -> List[Tuple[StudyItem, ReviewItem]]:
        items = {it.id: it for it in self.store.load_items()}
        reviews = {r.item_id: r for r in self.store.load_reviews()}
        res = []
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        for item_id, item in items.items():
            review = reviews.get(item_id)
            if not review:
                continue
            if due_only and review.review_date.date() != now.date():
                continue
            res.append((item, review))
        return res

    def export_ics(self, path: str) -> None:
        reviews = self.store.load_reviews()
        items = {it.id: it for it in self.store.load_items()}
        self.exporter.export(reviews, items, path)

    def run_interactive(self) -> None:
        interactive_loop(self)
