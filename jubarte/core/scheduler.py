"""
Scheduling abstractions and implementations for generating review plans.

This module defines an abstract Scheduler interface used to produce
ReviewItem sequences from a StudyItem. It also provides a concrete
implementation, SimpleSpacedScheduler, which generates a predefined
series of review events based on fixed spaced-repetition intervals.

The scheduler is responsible for determining when review sessions
should occur, allowing different strategies to be implemented by
subclassing the base Scheduler.

Returns:
    None
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from jubarte.models import ReviewItem, StudyItem


class Scheduler(ABC):
    """
    Abstract base class defining the interface for review scheduling.

    Subclasses must implement the generate_initial method to create
    a list of ReviewItem objects derived from a given StudyItem.
    """

    @abstractmethod
    def generate_initial(self, item: "StudyItem") -> List["ReviewItem"]:
        """
        Produce an initial sequence of review events for a study item.

        Args:
            item (StudyItem): The study item used to generate review entries.

        Returns:
            List[ReviewItem]: A list of scheduled review events.
        """
        pass


class SimpleSpacedScheduler(Scheduler):
    """
    Fixed-interval spaced repetition scheduler.

    This implementation generates review events using a predefined set
    of intervals measured in days. Each interval is added to the current
    UTC timestamp to determine future review dates.
    """

    BASE_INTERVALS = [1, 3, 7, 14, 30, 60, 120, 240, 360, 720]

    def generate_initial(self, item: "StudyItem") -> List["ReviewItem"]:
        """
        Create a list of ReviewItem objects based on fixed spaced intervals.

        The method calculates future review dates starting from the current
        UTC time and generates a ReviewItem for each interval defined in
        BASE_INTERVALS.

        Args:
            item (StudyItem): The study item for which reviews will be scheduled.

        Returns:
            List[ReviewItem]: A list of ReviewItem instances representing
                              scheduled future reviews.
        """
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
