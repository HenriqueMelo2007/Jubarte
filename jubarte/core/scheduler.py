from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from jubarte.models import ReviewItem, StudyItem


class Scheduler(ABC):
    @abstractmethod
    def generate_initial(self, item: "StudyItem") -> List["ReviewItem"]:
        pass


class SimpleSpacedScheduler(Scheduler):
    BASE_INTERVALS = [1, 3, 7, 14, 30, 60, 120, 240, 360, 720]

    def generate_initial(self, item: "StudyItem") -> List["ReviewItem"]:
        from jubarte.models import ReviewItem

        now = datetime.now(timezone.utc)

        reviews: list[ReviewItem] = []

        for days in self.BASE_INTERVALS:
            review_date = now + timedelta(days=days)
            reviews.append(
                ReviewItem(
                    item_id=item.id,
                    review_date=review_date,
                )
            )

        return reviews
