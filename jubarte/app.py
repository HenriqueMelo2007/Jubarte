"""
Application service layer for the study/review scheduling system.

This module defines the main `App` class, which coordinates storage,
review scheduling, calendar export, and the interactive UI. It provides
a high-level API for managing study items and their associated reviews.

Responsibilities:
    - Create and persist study items
    - Generate initial spaced-review schedules
    - List scheduled reviews (optionally only those due today)
    - Export review schedules to an ICS calendar file
    - Run an interactive command-line interface
    - Manage stored data (clear or remove items)

Typical Usage:
    app = App()
    app.add_item("Neuroscience basics", "Read chapter 1")
    due_reviews = app.list_items(due_only=True)
    app.export_ics("schedule.ics")
    app.run_interactive()
"""

from typing import List, Tuple

from .core.scheduler import SimpleSpacedScheduler
from .export.ics_exporter import ICSExporter
from .models import ReviewItem, StudyItem, new_item
from .storage.file_store import FileStore
from .ui.interactive import interactive_loop


class App:
    """High-level application interface for managing study items and reviews.

    The App class orchestrates the system components:
        - Storage backend for persistence
        - Spaced-review scheduler for generating reviews
        - Calendar exporter for ICS output
        - Interactive CLI loop

    Custom implementations of storage, scheduling, or exporting
    can be injected via the constructor.
    """

    def __init__(self, store=None, scheduler=None, exporter=None):
        """Initialize the application with optional dependency injection.

        Args:
            store: Storage backend responsible for persisting items and reviews.
                Defaults to FileStore.
            scheduler: Scheduling strategy used to generate review sessions.
                Defaults to SimpleSpacedScheduler.
            exporter: Calendar exporter used to generate ICS files.
                Defaults to ICSExporter.
        """
        self.store = store or FileStore()
        self.scheduler = scheduler or SimpleSpacedScheduler()
        self.exporter = exporter or ICSExporter()

    def add_item(self, title: str, notes: str = "") -> StudyItem:
        """Create a new study item and generate its initial review schedule.

        Args:
            title: Title or main subject of the study item.
            notes: Optional supplementary notes or description.

        Returns:
            The newly created StudyItem instance.
        """
        item = new_item(title, notes)
        items = {it.id: it for it in self.store.load_items()}
        for it in items.values():
            if it.title == title:
                raise ValueError(f"An item with title '{title}' already exists.")
        self.store.save_item(item)
        reviews = self.scheduler.generate_initial(item)
        for review in reviews:
            self.store.save_review(review)
        return item

    def list_items(self, due_only: bool = False) -> List[Tuple[StudyItem, ReviewItem]]:
        """List study items paired with their scheduled reviews.

        Args:
            due_only: If True, returns only reviews scheduled for today.

        Returns:
            A list of tuples containing (StudyItem, ReviewItem).
        """
        items = {it.id: it for it in self.store.load_items()}
        reviews = self.store.load_reviews()
        res = []
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        for review in reviews:
            item_id, item = next(
                (k, v) for k, v in items.items() if k == review.item_id
            )
            if due_only and review.review_date.date() != now.date():
                continue
            res.append((item, review))

        return res

    def export_ics(self, path: str) -> None:
        """Export all scheduled reviews to an ICS calendar file.

        Args:
            path: Destination file path for the generated ICS file.
        """
        reviews = self.store.load_reviews()
        if reviews:
            items = {it.id: it for it in self.store.load_items()}
            self.exporter.export(reviews, items, path)
            print(f"Exported: {path}")
        else:
            print("No reviews to export.")

    def run_interactive(self) -> None:
        """Start the interactive command-line interface."""
        interactive_loop(self)

    def clear(self) -> None:
        """Remove all stored study items and reviews."""
        self.store.clear()

    def remove_item(self, title: str) -> None:
        """Remove a study item and its associated reviews by title.

        Args:
            title: Title of the study item to remove.
        """
        self.store.remove_item_by_title(title)
