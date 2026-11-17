import re
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional


class ExperienceMatcher:
    """Calculates non-overlapping chronological employment tenure and tenure alignment."""

    MONTHS_MAP = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12
    }

    @classmethod
    def _parse_date(cls, date_str: Optional[str], is_end: bool = False) -> Optional[datetime]:
        if not date_str:
            return None

        cleaned = date_str.strip().lower()
        if is_end and any(w in cleaned for w in ["present", "current", "now", "ongoing"]):
            return datetime.now()

        match_my = re.search(r"([a-z]+)\.?\s+(\d{4})", cleaned)
        if match_my:
            m_name = match_my.group(1)
            year = int(match_my.group(2))
            month = cls.MONTHS_MAP.get(m_name, 1)
            return datetime(year, month, 1)

        match_slash = re.search(r"(\d{1,2})\/(\d{4})", cleaned)
        if match_slash:
            month = int(match_slash.group(1))
            year = int(match_slash.group(2))
            return datetime(year, max(1, min(12, month)), 1)

        match_y = re.search(r"\b(19\d{2}|20\d{2})\b", cleaned)
        if match_y:
            year = int(match_y.group(1))
            return datetime(year, 12 if is_end else 1, 1)

        return None

    @classmethod
    def calculate_tenure(cls, work_experience: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates total non-overlapping months of employment across all jobs."""
        intervals: List[Tuple[datetime, datetime]] = []

        for job in work_experience:
            start_dt = cls._parse_date(job.get("start_date"), is_end=False)
            end_dt = cls._parse_date(job.get("end_date"), is_end=True)

            if start_dt and end_dt and start_dt <= end_dt:
                intervals.append((start_dt, end_dt))
            elif start_dt and not end_dt:
                intervals.append((start_dt, datetime.now()))

        if not intervals:
            num_roles = len(work_experience)
            return {
                "total_months": num_roles * 24,
                "total_years": round(num_roles * 2.0, 1),
                "has_overlaps": False,
                "overlap_months_deducted": 0,
                "confidence": "heuristic_fallback"
            }

        intervals.sort(key=lambda x: x[0])

        merged: List[Tuple[datetime, datetime]] = []
        raw_total_months = 0

        for start, end in intervals:
            # Inclusive month calculation (+ 1)
            months = (end.year - start.year) * 12 + (end.month - start.month) + 1
            raw_total_months += max(1, months)

            if not merged:
                merged.append((start, end))
            else:
                last_start, last_end = merged[-1]
                if start <= last_end:
                    merged[-1] = (last_start, max(last_end, end))
                else:
                    merged.append((start, end))

        deduplicated_months = 0
        for start, end in merged:
            m = (end.year - start.year) * 12 + (end.month - start.month) + 1
            deduplicated_months += max(1, m)

        overlap_deducted = max(0, raw_total_months - deduplicated_months)

        return {
            "total_months": deduplicated_months,
            "total_years": round(deduplicated_months / 12.0, 1),
            "has_overlaps": overlap_deducted > 0,
            "overlap_months_deducted": overlap_deducted,
            "confidence": "high"
        }

    @classmethod
    def match(
        cls,
        work_experience: List[Dict[str, Any]],
        experience_years_required: float
    ) -> Dict[str, Any]:
        tenure_info = cls.calculate_tenure(work_experience)
        candidate_years = tenure_info["total_years"]

        if experience_years_required <= 0:
            score = 100.0
            meets_requirement = True
        else:
            ratio = candidate_years / experience_years_required
            if ratio >= 1.0:
                score = 100.0
                meets_requirement = True
            elif ratio >= 0.75:
                score = 80.0 + (ratio - 0.75) * 60.0
                meets_requirement = True
            else:
                score = ratio * 80.0
                meets_requirement = False

        return {
            "score": round(min(100.0, max(0.0, score)), 1),
            "candidate_years": candidate_years,
            "required_years": experience_years_required,
            "meets_requirement": meets_requirement,
            "tenure_details": tenure_info
        }
