from datetime import datetime
from typing import List

from jubarte.models import ReviewEntry, StudyItem


class ICSExporter:
    def export(
        self, entries: List[ReviewEntry], items: dict[str, StudyItem], path: str
    ) -> None:
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//jubarte//EN",
        ]

        for e in entries:
            item = items.get(e.item_id)
            uid = f"{e.item_id}-{int(e.next_review.timestamp())}@jubarte"
            dtstart = e.next_review.strftime("%Y%m%dT%H%M%SZ")
            summary = f"Revisão: {item.title if item else e.item_id}"
            description = item.notes if item else ""
            lines += [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART:{dtstart}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                "END:VEVENT",
            ]

        lines.append("END:VCALENDAR")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
