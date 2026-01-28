"""
Domain models for study items and review scheduling.

This module defines the core data structures used by the Jubarte
application, including study items and their associated review
entries, as well as helper functions for time handling and object
serialization.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def _now_utc() -> datetime:
    """
    Return the current date and time in UTC.

    This function is intended to be used as a default factory for
    timestamp fields to ensure consistent, timezone-aware values.

    Returns:
        datetime: The current UTC date and time.
    """
    return datetime.now(timezone.utc)


@dataclass
class StudyItem:
    """
    Represent a study topic managed by the application.

    A StudyItem stores the user-defined content to be reviewed,
    including its title, optional notes, and creation timestamp.
    """

    id: str
    title: str
    notes: str = ""
    created_at: datetime = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the study item to a dictionary.

        The resulting dictionary is suitable for persistence
        (e.g., JSON storage).

        Returns:
            Dict[str, Any]: A dictionary representation of the study item.
        """
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StudyItem":
        """
        Create a StudyItem instance from a dictionary.

        Args:
            d (Dict[str, Any]): A dictionary containing the serialized
            study item data.

        Returns:
            StudyItem: A reconstructed StudyItem instance.
        """
        return StudyItem(
            id=d["id"],
            title=d["title"],
            notes=d.get("notes", ""),
            created_at=datetime.fromisoformat(d["created_at"]),
        )


@dataclass
class ReviewEntry:
    """
    Represent the review schedule and history for a study item.

    A ReviewEntry tracks when an item should be reviewed next,
    the current review interval, ease factor, repetition count,
    and a history of past review results.
    """

    item_id: str
    next_review: datetime
    interval_days: int
    ease: float
    repetitions: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the review entry to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the review entry.
        """
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
        """
        Create a ReviewEntry instance from a dictionary.

        Args:
            d (Dict[str, Any]): A dictionary containing the serialized
            review entry data.

        Returns:
            ReviewEntry: A reconstructed ReviewEntry instance.
        """
        return ReviewEntry(
            item_id=d["item_id"],
            next_review=datetime.fromisoformat(d["next_review"]),
            interval_days=int(d["interval_days"]),
            ease=float(d.get("ease", 2.5)),
            repetitions=int(d.get("repetitions", 0)),
            history=d.get("history", []),
        )


def new_item(title: str, notes: str = "") -> StudyItem:
    """
    Create a new study item with a generated unique identifier.

    Args:
        title (str): The title of the study item.
        notes (str, optional): Optional notes or description associated
        with the item. Defaults to an empty string.

    Returns:
        StudyItem: A newly created study item instance.
    """
    return StudyItem(id=str(uuid.uuid4()), title=title, notes=notes)
