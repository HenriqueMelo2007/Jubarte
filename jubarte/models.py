import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class StudyItem:
    id: str
    title: str
    notes: str = ""
    created_at: datetime = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StudyItem":
        return StudyItem(
            id=d["id"],
            title=d["title"],
            notes=d.get("notes", ""),
            created_at=datetime.fromisoformat(d["created_at"]),
        )


@dataclass
class ReviewEntry:
    item_id: str
    next_review: datetime
    interval_days: int
    ease: float
    repetitions: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "next_review": self.next_review.isoformat(),
            "interval_days": self.interval_days,
            "ease": self.ease,
            "repetitions": self.repetitions,
            "history": self.history,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ReviewEntry":
        return ReviewEntry(
            item_id=d["item_id"],
            next_review=datetime.fromisoformat(d["next_review"]),
            interval_days=int(d["interval_days"]),
            ease=float(d.get("ease", 2.5)),
            repetitions=int(d.get("repetitions", 0)),
            history=d.get("history", []),
        )


def new_item(title: str, notes: str = "") -> StudyItem:
    return StudyItem(id=str(uuid.uuid4()), title=title, notes=notes)
