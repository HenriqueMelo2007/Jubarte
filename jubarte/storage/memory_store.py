from typing import Dict, List

from jubarte.models import ReviewEntry, StudyItem


class MemoryStore:
    def __init__(self) -> None:
        self._items: Dict[str, StudyItem] = {}
        self._entries: Dict[str, ReviewEntry] = {}

    def save_item(self, item: StudyItem) -> None:
        self._items[item.id] = item

    def load_items(self) -> List[StudyItem]:
        return list(self._items.values())

    def save_entry(self, entry: ReviewEntry) -> None:
        self._entries[entry.item_id] = entry

    def load_entries(self) -> List[ReviewEntry]:
        return list(self._entries.values())

    def load_entry_for_item(self, item_id: str) -> ReviewEntry | None:
        return self._entries.get(item_id)
