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

    def export(
        self,
        reviews: Iterable["ReviewItem"],
        items: Mapping[str, "StudyItem"],
        path: Union[str, Path],
    ) -> None:
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

        if dt is None:
            raise ValueError("datetime is required for event")
        if dt.tzinfo is None:

            dt = dt.replace(tzinfo=timezone.utc)
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y%m%dT%H%M%SZ")

    def _escape(self, text: str) -> str:

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

        if len(line) <= limit:
            return line
        parts = [line[i : i + limit] for i in range(0, len(line), limit)]
        return "\r\n ".join(parts)
