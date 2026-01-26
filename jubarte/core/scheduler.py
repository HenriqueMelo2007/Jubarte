from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jubarte.models import ReviewEntry, StudyItem


class Scheduler(ABC):
    @abstractmethod
    def generate_initial(self, item: "StudyItem") -> "ReviewEntry":
        pass

    @abstractmethod
    def update(self, entry: "ReviewEntry", result: str) -> "ReviewEntry":
        pass


class SimpleSpacedScheduler(Scheduler):
    BASE_INTERVALS = [1, 3, 7, 14]

    def generate_initial(self, item: "StudyItem") -> "ReviewEntry":
        now = datetime.now(timezone.utc)
        next_r = now + timedelta(days=self.BASE_INTERVALS[0])
        from jubarte.models import ReviewEntry

        return ReviewEntry(
            item_id=item.id,
            next_review=next_r,
            interval_days=self.BASE_INTERVALS[0],
            ease=2.5,
            repetitions=0,
        )

    def update(self, entry: "ReviewEntry", result: str) -> "ReviewEntry":
        factor = {
            "again": 1,
            "hard": 1.2,
            "good": 2,
            "easy": 3,
        }[result]

        new_interval = max(1, int(round(entry.interval_days * factor)))
        entry.repetitions += 1
        entry.interval_days = new_interval
        entry.next_review = datetime.now(timezone.utc) + timedelta(days=new_interval)
        if result == "easy":
            entry.ease = min(4.5, entry.ease + 0.15)
        elif result == "again":
            entry.ease = max(1.3, entry.ease - 0.2)

        entry.history.append(
            {"when": datetime.now(timezone.utc).isoformat(), "result": result}
        )
        return entry
