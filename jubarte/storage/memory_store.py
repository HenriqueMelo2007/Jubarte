from typing import Dict, List

from jubarte.models import ReviewItem, StudyItem


class MemoryStore:
    def __init__(self) -> None:
        self._items: Dict[str, StudyItem] = {}
        self._reviews: Dict[str, ReviewItem] = {}

    def save_item(self, item: StudyItem) -> None:
        self._items[item.id] = item

    def load_items(self) -> List[StudyItem]:
        return list(self._items.values())

    def save_review(self, review: ReviewItem) -> None:
        self._reviews[review.item_id] = review

    def load_reviews(self) -> List[ReviewItem]:
        return list(self._reviews.values())

    def load_review_for_item(self, item_id: str) -> ReviewItem | None:
        return self._reviews.get(item_id)
