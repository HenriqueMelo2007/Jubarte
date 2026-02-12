"""
iCalendar (.ics) export utility for review scheduling data.

This module defines the ICSExporter class, responsible for transforming
ReviewItem records and their associated StudyItem metadata into a valid
VCALENDAR file. Each review is exported as a VEVENT entry containing
date, summary, and descriptive information derived from the related
study item.

The exporter ensures:
- Proper UTC datetime formatting compliant with the iCalendar standard.
- Escaping of reserved characters within text fields.
- Line folding according to RFC 5545 length requirements.
- Atomic file writing through temporary file replacement.

Raises:
    ValueError: If a review event does not contain a valid datetime.

Returns:
    None
"""

from __future__ import annotations

import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Mapping, Union

if TYPE_CHECKING:
    from jubarte.models import ReviewItem, StudyItem


class ICSExporter:
    """
    iCalendar exporter for review events.

    The ICSExporter generates a standards-compliant VCALENDAR file
    representing scheduled review events. Each ReviewItem is converted
    into a VEVENT structure that includes a unique identifier, timestamp,
    start datetime, summary derived from the study item title, and
    optional descriptive notes.

    The resulting file can be imported into calendar applications that
    support the iCalendar format.
    """

    def export(
        self,
        reviews: Iterable["ReviewItem"],
        items: Mapping[str, "StudyItem"],
        path: Union[str, Path],
    ) -> None:
        """
        Generate an iCalendar file containing review events.

        Reviews are sorted by their review_date attribute. Each review is
        converted into a VEVENT entry with metadata extracted from the
        associated StudyItem when available.

        Args:
            reviews (Iterable["ReviewItem"]): Collection of review entries
                to be exported as calendar events.
            items (Mapping[str, "StudyItem"]): Mapping of study item IDs
                to StudyItem objects used to enrich event information.
            path (Union[str, Path]): Destination file path for the
                generated .ics calendar file.
        """
        path = Path(path)
        export_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        lines: list[str] = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//jubarte//EN",
        ]

        for r in sorted(reviews, key=lambda x: getattr(x, "review_date", datetime.min)):
            item = items.get(r.item_id)
            uid = f"{r.item_id}-{uuid.uuid4()}@jubarte"
            dtstart = self._format_dt(r.review_date)
            summary = f"Review: {item.title if item else r.item_id}"
            description = item.notes if item else ""

            vevent = [
                "BEGIN:VEVENT",
                self._fold(f"UID:{self._escape(uid)}"),
                self._fold(f"DTSTAMP:{self._format_dt(export_time)}"),
                self._fold(f"DTSTART:{dtstart}"),
                self._fold(f"SUMMARY:{self._escape(summary)}"),
                self._fold(f"DESCRIPTION:{self._escape(description)}"),
                "END:VEVENT",
            ]
            lines.extend(vevent)

        lines.append("END:VCALENDAR")

        content = "\r\n".join(lines) + "\r\n"

        dirpath = path.parent
        dirpath.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=str(dirpath), prefix=f".{path.name}.", text=True
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as tf:
                tf.write(content)
            os.replace(tmp_path, str(path))
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    def _format_dt(self, dt: datetime) -> str:
        """
        Convert a datetime object into UTC iCalendar timestamp format.

        Args:
            dt (datetime): Datetime value representing the event start time.

        Raises:
            ValueError: If the datetime value is missing.

        Returns:
            str: Formatted timestamp string in YYYYMMDDTHHMMSSZ format.
        """
        if dt is None:
            raise ValueError("datetime is required for event")
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y%m%dT%H%M%SZ")

    def _escape(self, text: str) -> str:
        """
        Escape reserved characters according to iCalendar text rules.

        Args:
            text (str): Raw text to be escaped.

        Returns:
            str: Escaped text safe for inclusion in calendar fields.
        """
        if text is None:
            return ""
        s = str(text)
        s = s.replace("\\", "\\\\")
        s = s.replace("\r\n", "\n").replace("\r", "\n")
        s = s.replace("\n", r"\n")
        s = s.replace(",", r"\,")
        s = s.replace(";", r"\;")
        return s

    def _fold(self, line: str, limit: int = 75) -> str:
        """
        Apply line folding to comply with iCalendar line length limits.

        Args:
            line (str): A single calendar line.
            limit (int, optional): Maximum allowed line length before
                                   folding occurs. Defaults to 75.

        Returns:
            str: Line formatted with continuation prefixes when necessary.
        """
        if len(line) <= limit:
            return line
        parts = [line[i : i + limit] for i in range(0, len(line), limit)]
        return "\r\n ".join(parts)
