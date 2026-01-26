import json
from pathlib import Path
from typing import Dict, List

from jubarte.models import ReviewEntry, StudyItem

from .memory_store import MemoryStore


class FileStore:
    def __init__(self, path: str | Path = "data.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"items": [], "entries": []})

    def _read(self) -> Dict:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict) -> None:
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    def save_item(self, item: StudyItem) -> None:
        d = self._read()
        items = [it for it in d.get("items", []) if it.get("id") != item.id]
        items.append(item.to_dict())
        d["items"] = items
        self._write(d)

    def load_items(self) -> List[StudyItem]:
        d = self._read()
        return [StudyItem.from_dict(it) for it in d.get("items", [])]

    def save_entry(self, entry: ReviewEntry) -> None:
        d = self._read()
        entries = [e for e in d.get("entries", []) if e.get("item_id") != entry.item_id]
        entries.append(entry.to_dict())
        d["entries"] = entries
        self._write(d)

    def load_entries(self) -> List[ReviewEntry]:
        d = self._read()
        return [ReviewEntry.from_dict(e) for e in d.get("entries", [])]

    def load_entry_for_item(self, item_id: str) -> ReviewEntry | None:
        for e in self.load_entries():
            if e.item_id == item_id:
                return e
        return None

    def as_memory(self) -> MemoryStore:
        ms = MemoryStore()
        for it in self.load_items():
            ms.save_item(it)
        for e in self.load_entries():
            ms.save_entry(e)
        return ms
