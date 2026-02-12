"""
Persistent file-based storage module for study and review data.

This module defines the FileStore class, a storage backend responsible for
reading and writing StudyItem and ReviewItem objects to a JSON file on disk.
It manages serialization and deserialization of data, ensures the storage
file exists, and provides methods for saving, loading, removing, and clearing
stored records.

The class supports conversion of file-based data into an in-memory
MemoryStore instance for runtime operations.

Returns:
    None
"""

import json
from pathlib import Path
from typing import Dict, List

from jubarte.models import ReviewItem, StudyItem

from .memory_store import MemoryStore


class FileStore:
    """
    JSON file–based persistence layer for StudyItem and ReviewItem objects.

    The FileStore manages structured storage in a single JSON file, maintaining
    two collections:
    - "items": serialized StudyItem objects.
    - "reviews": serialized ReviewItem objects.

    It provides operations for saving, retrieving, deleting, and converting
    stored data while ensuring safe file writing through temporary file
    replacement.
    """

    def __init__(self, path: str | Path = "data.json") -> None:
        """
        Initialize the FileStore with a target file path.

        The directory is created if it does not exist. If the file is missing,
        an initial JSON structure with empty item and review lists is written.

        Args:
            path (str | Path, optional): Location of the JSON storage file.
                                         Defaults to "data.json".
        """
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"items": [], "reviews": []})

    def _read(self) -> Dict:
        """
        Load and parse the JSON data from disk.

        Returns:
            Dict: The full JSON content containing stored items and reviews.
        """
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict) -> None:
        """
        Write structured data safely to the JSON file.

        Data is first written to a temporary file and then atomically
        replaces the original file to reduce the risk of corruption.

        Args:
            data (Dict): The complete data structure to be written.
        """
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    def save_item(self, item: StudyItem) -> None:
        """
        Insert or update a StudyItem in the storage file.

        If an item with the same identifier already exists, it is replaced.

        Args:
            item (StudyItem): The study item to be stored.
        """
        d = self._read()
        items = [it for it in d.get("items", []) if it.get("id") != item.id]
        items.append(item.to_dict())
        d["items"] = items
        self._write(d)

    def load_items(self) -> List[StudyItem]:
        """
        Retrieve all StudyItem objects from storage.

        Returns:
            List[StudyItem]: A list of StudyItem instances reconstructed
                             from serialized data.
        """
        d = self._read()
        return [StudyItem.from_dict(it) for it in d.get("items", [])]

    def save_review(self, review: ReviewItem) -> None:
        """
        Append a ReviewItem record to storage.

        Args:
            review (ReviewItem): The review entry to be serialized and stored.
        """
        d = self._read()
        reviews = d.get("reviews", [])
        reviews.append(review.to_dict())
        d["reviews"] = reviews
        self._write(d)

    def load_reviews(self) -> List[ReviewItem]:
        """
        Retrieve all ReviewItem objects from storage.

        Returns:
            List[ReviewItem]: A list of ReviewItem instances reconstructed
                              from serialized data.
        """
        d = self._read()
        return [ReviewItem.from_dict(r) for r in d.get("reviews", [])]

    def load_review_for_item(self, item_id: str) -> ReviewItem | None:
        """
        Retrieve the first review associated with a specific study item.

        Args:
            item_id (str): Identifier of the study item.

        Returns:
            ReviewItem | None: The matching ReviewItem if found;
                               otherwise None.
        """
        for r in self.load_reviews():
            if r.item_id == item_id:
                return r
        return None

    def clear(self) -> None:
        """
        Remove all stored items and reviews.

        The JSON file is reset to its initial empty structure.
        """
        self._write({"items": [], "reviews": []})

    def remove_reviews_for_item(self, item_id: str) -> Dict[str, List[dict]]:
        """
        Delete all review records associated with a given study item.

        Args:
            item_id (str): Identifier of the study item whose reviews
                           should be removed.

        Returns:
            Dict[str, List[dict]]: The updated data structure after
                                   removal of the reviews.
        """
        d = self._read()
        reviews = [r for r in d.get("reviews", []) if r.get("item_id") != item_id]
        d["reviews"] = reviews
        self._write(d)
        print(d)
        return d

    def remove_item_by_title(self, title: str) -> None:
        """
        Remove a study item by its title and delete associated reviews.

        Args:
            title (str): Title of the study item to be removed.
        """
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
        """
        Convert file-based data into an in-memory MemoryStore instance.

        All stored StudyItem and ReviewItem objects are loaded from disk
        and inserted into a new MemoryStore object.

        Returns:
            MemoryStore: A populated in-memory representation of the data.
        """
        ms = MemoryStore()
        for it in self.load_items():
            ms.save_item(it)
        for r in self.load_reviews():
            ms.save_review(r)
        return ms
