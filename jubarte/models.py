"""Data models for Jubarte.

This module defines lightweight data classes used by the Jubarte application:

- ``StudyItem``: represents a single study topic / item created by the user.
- ``ReviewItem``: represents a scheduled review for a study item (links an item
  id to a review date).

Helper utilities for creating new items and (de)serializing instances to/from
JSON-serializable dictionaries are also provided.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


def _now_utc() -> datetime:
    """Return the current date and time in UTC.

    The returned ``datetime`` is timezone-aware (``tzinfo=datetime.timezone.utc``).

    Returns:
        datetime: Current UTC date/time with UTC tzinfo.
    """
    return datetime.now(timezone.utc)


@dataclass
class StudyItem:
    """A study/topic entry stored by the application.

    Attributes:
        id: A unique identifier for the item (UUID string).
        title: Short title of the study item.
        notes: Optional free-text notes for the item.
        created_at: Timestamp when the item was created (UTC).
    """

    id: str
    title: str
    notes: str = ""
    created_at: datetime = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the StudyItem to a JSON-serializable dictionary.

        The ``created_at`` field is converted to an ISO 8601 string using
        ``datetime.isoformat()`` so the result can be stored in JSON files.

        Returns:
            Dict[str, Any]: Dictionary representation suitable for JSON.
        """
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StudyItem":
        """Create a StudyItem from a dictionary produced by :meth:`to_dict`.

        The function expects ``created_at`` to be an ISO 8601 string. Missing
        optional fields (e.g. ``notes``) use sensible defaults.

        Args:
            d: Dictionary with keys ``id``, ``title`` and ``created_at`` (ISO
                string). ``notes`` is optional.

        Returns:
            StudyItem: A new instance reconstructed from ``d``.
        """
        return StudyItem(
            id=d["id"],
            title=d["title"],
            notes=d.get("notes", ""),
            created_at=datetime.fromisoformat(d["created_at"]),
        )


@dataclass
class ReviewItem:
    """Represents a scheduled review for a study item.

    Attributes:
        item_id: The ``id`` of the associated :class:`StudyItem`.
        review_date: The date and time when the review should occur (UTC).
    """

    item_id: str
    review_date: datetime

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the ReviewItem to a JSON-serializable dictionary.

        The ``review_date`` is converted to an ISO 8601 string.

        Returns:
            Dict[str, Any]: Dictionary representation suitable for JSON.
        """
        return {
            "item_id": self.item_id,
            "review_date": self.review_date.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ReviewItem":
        """Create a ReviewItem from a dictionary produced by :meth:`to_dict`.

        Args:
            d: Dictionary with keys ``item_id`` and ``review_date`` (ISO
                string).

        Returns:
            ReviewItem: A new instance reconstructed from ``d``.
        """
        return ReviewItem(
            item_id=d["item_id"],
            review_date=datetime.fromisoformat(d["review_date"]),
        )


def new_item(title: str, notes: str = "") -> StudyItem:
    """Create a new StudyItem with a generated UUID and current creation time.

    The function generates a UUID4 string for the ``id`` and sets
    ``created_at`` to the current UTC datetime.

    Args:
        title: Title for the new study item.
        notes: Optional notes text. Defaults to an empty string.

    Returns:
        StudyItem: The newly created study item.
    """
    return StudyItem(id=str(uuid.uuid4()), title=title, notes=notes)
