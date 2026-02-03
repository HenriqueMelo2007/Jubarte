from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jubarte.models import ReviewItem, StudyItem


class Scheduler(ABC):
    @abstractmethod
    def generate_initial(self, item: "StudyItem") -> "ReviewItem":
        pass


class SimpleSpacedScheduler(Scheduler):
    BASE_INTERVALS = [1, 3, 7, 14]

    def generate_initial(self, item: "StudyItem") -> "ReviewItem":
        now = datetime.now(timezone.utc)
        r_date = now + timedelta(days=self.BASE_INTERVALS[0])
        from jubarte.models import ReviewItem

        return ReviewItem(
            item_id=item.id,
            review_date=r_date,
        )
