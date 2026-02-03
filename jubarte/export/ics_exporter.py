from datetime import datetime
from typing import List

from jubarte.models import ReviewItem, StudyItem


class ICSExporter:
    def export(
        self, reviews: List[ReviewItem], items: dict[str, StudyItem], path: str
    ) -> None:
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//jubarte//EN",
        ]

        for r in reviews:
            item = items.get(r.item_id)
            uid = f"{r.item_id}-{int(r.review_date.timestamp())}@jubarte"
            dtstart = r.review_date.strftime("%Y%m%dT%H%M%SZ")
            summary = f"Revisão: {item.title if item else r.item_id}"
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
