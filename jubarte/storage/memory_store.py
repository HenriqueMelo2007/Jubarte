"""
In-memory storage component for study and review data.

This module defines the MemoryStore class, a lightweight repository that
manages StudyItem and ReviewItem objects during application runtime.
It provides methods to save and retrieve study items and their associated
review records using dictionary-based indexing.

Returns:
    None
"""

from typing import Dict, List

from jubarte.models import ReviewItem, StudyItem


class MemoryStore:
    """
    Runtime storage manager for StudyItem and ReviewItem objects.

    The MemoryStore maintains two internal collections:
    - Study items indexed by their unique identifier.
    - Review records indexed by the identifier of the related study item.

    It provides methods to add, retrieve, and query stored entities,
    enabling application components to manage learning content and
    associated review metadata during execution.
    """

    def __init__(self) -> None:
        """
        Initialize the in-memory storage structures.

        Two dictionaries are created:
        - _items: maps study item IDs to StudyItem instances.
        - _reviews: maps study item IDs to ReviewItem instances.
        """
        self._items: Dict[str, StudyItem] = {}
        self._reviews: Dict[str, ReviewItem] = {}

    def save_item(self, item: StudyItem) -> None:
        """
        Store or update a StudyItem in memory.

        Args:
            item (StudyItem): The study item instance to be stored.
                              Its unique identifier is used as the key.
        """
        self._items[item.id] = item

    def load_items(self) -> List[StudyItem]:
        """
        Retrieve all stored study items.

        Returns:
            List[StudyItem]: A list containing every StudyItem currently
                             stored in memory.
        """
        return list(self._items.values())

    def save_review(self, review: ReviewItem) -> None:
        """
        Store or update a ReviewItem associated with a study item.

        Args:
            review (ReviewItem): The review data linked to a specific
                                 study item via review.item_id.
        """
        self._reviews[review.item_id] = review

    def load_reviews(self) -> List[ReviewItem]:
        """
        Retrieve all stored review records.

        Returns:
            List[ReviewItem]: A list containing every ReviewItem currently
                              stored in memory.
        """
        return list(self._reviews.values())

    def load_review_for_item(self, item_id: str) -> ReviewItem | None:
        """
        Retrieve the review associated with a specific study item.

        Args:
            item_id (str): The unique identifier of the study item.

        Returns:
            ReviewItem | None: The corresponding ReviewItem if present;
                               otherwise None when no review is stored
                               for the given item.
        """
        return self._reviews.get(item_id)
