import json
from pathlib import Path
from typing import Dict, List

from jubarte.models import ReviewItem, StudyItem

from .memory_store import MemoryStore


class FileStore:
    def __init__(self, path: str | Path = "data.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"items": [], "reviews": []})

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

    def save_review(self, review: ReviewItem) -> None:
        d = self._read()
        reviews = d.get("reviews", [])
        reviews.append(review.to_dict())
        d["reviews"] = reviews
        self._write(d)

    def load_reviews(self) -> List[ReviewItem]:
        d = self._read()
        return [ReviewItem.from_dict(r) for r in d.get("reviews", [])]

    def load_review_for_item(self, item_id: str) -> ReviewItem | None:
        for r in self.load_reviews():
            if r.item_id == item_id:
                return r
        return None

    def clear(self) -> None:
        self._write({"items": [], "reviews": []})

    def remove_reviews_for_item(self, item_id: str) -> Dict[str, List[dict]]:
        d = self._read()
        reviews = [r for r in d.get("reviews", []) if r.get("item_id") != item_id]
        d["reviews"] = reviews
        self._write(d)
        print(d)
        return d

    def remove_item_by_title(self, title: str) -> None:
        d = self._read()
        item_id = ""
        for item in d["items"]:
            if item["title"] == title:
                item_id = item["id"]
                break
        d = self.remove_reviews_for_item(item_id=item_id)
        items = [it for it in d.get("items", []) if it.get("title") != title]
        d["items"] = items
        self._write(d)

    def as_memory(self) -> MemoryStore:
        ms = MemoryStore()
        for it in self.load_items():
            ms.save_item(it)
        for r in self.load_reviews():
            ms.save_review(r)
        return ms
