#!/usr/bin/env python3
"""Normalize Meta/Facebook Ads Library results with deduplication and evidence signals.

v3.8 hardening changes:
- deduplicates repeated ad/library IDs across multiple retrieval calls
- merges complementary evidence instead of double-counting the same ad
- keeps the largest observed estimated_total_count so narrow follow-up searches do not
  overwrite a broader portfolio estimate
"""

from __future__ import annotations
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _unix_to_iso(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None
    try:
        if isinstance(value, str) and not value.isdigit():
            return value
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat()
    except (ValueError, TypeError, OSError):
        return None


def _normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def coverage_label(ratio: Optional[float]) -> str:
    if ratio is None:
        return "Unknown"
    if ratio >= 0.80:
        return "High"
    if ratio >= 0.40:
        return "Medium"
    return "Low"


def observability_label(score: float) -> str:
    if score >= 75:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


@dataclass
class ObservedAd:
    ad_id: str
    page_id: Optional[str] = None
    page_name: Optional[str] = None
    creative_body: str = ""
    headline: str = ""
    creation_time: Optional[str] = None
    delivery_start_time: Optional[str] = None
    snapshot_url: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    country_scope: List[str] = field(default_factory=list)
    days_running: Optional[int] = None
    source_fields_present: List[str] = field(default_factory=list)

    visual_inspected: bool = False
    creative_format_observed: bool = False
    observability_score: float = 0.0
    observability: str = "Low"

    hook: Optional[str] = None
    creative_angle: Optional[str] = None
    pain_point: Optional[str] = None
    desire: Optional[str] = None
    mechanism: Optional[str] = None
    value_proposition: Optional[str] = None
    offer: Optional[str] = None
    proof_type: Optional[str] = None
    cta: Optional[str] = None
    funnel_stage: Optional[str] = None
    content_theme: Optional[str] = None
    audience_message: Optional[str] = None
    timing_type: Optional[str] = None
    cluster_id: Optional[str] = None

    def calculate_observability(self) -> float:
        score = 0.0
        score += 25 if self.headline else 0
        score += 30 if self.creative_body else 0
        score += 30 if self.visual_inspected else 0
        score += 10 if self.delivery_start_time else 0
        score += 5 if self.snapshot_url else 0
        self.observability_score = float(score)
        self.observability = observability_label(score)
        return self.observability_score

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AdLibraryParser:
    """Normalize MCP/API-like Ads Library payloads without fabricating missing fields."""

    def __init__(self, analysis_date: Optional[datetime] = None):
        self.analysis_date = analysis_date or datetime.now(timezone.utc)
        if self.analysis_date.tzinfo is None:
            self.analysis_date = self.analysis_date.replace(tzinfo=timezone.utc)
        self.ads: List[ObservedAd] = []
        self._ad_index: Dict[str, int] = {}
        self.estimated_total_count: Optional[int] = None
        self.duplicate_records_merged: int = 0

    def add_from_mcp_results(self, payload: Any, countries: Optional[List[str]] = None,
                             status: Optional[str] = None) -> List[ObservedAd]:
        """Accept raw MCP result dict/string containing {estimated_total_count, ads}.

        Repeated ad IDs are merged in-place rather than appended. This is important when
        a workflow combines a broad Ads Library pull with targeted follow-up searches.
        """
        if isinstance(payload, str):
            payload = json.loads(payload)
        if isinstance(payload, dict) and isinstance(payload.get("results"), str):
            payload = json.loads(payload["results"])

        if isinstance(payload, dict) and payload.get("estimated_total_count") is not None:
            try:
                observed_total = int(payload["estimated_total_count"])
                if self.estimated_total_count is None:
                    self.estimated_total_count = observed_total
                else:
                    self.estimated_total_count = max(self.estimated_total_count, observed_total)
            except (TypeError, ValueError):
                pass

        ads = payload.get("ads", []) if isinstance(payload, dict) else []
        touched: List[ObservedAd] = []
        for raw in ads:
            incoming = self._normalize_one(raw, countries or [], status)
            ad_id = incoming.ad_id
            if ad_id and ad_id in self._ad_index:
                idx = self._ad_index[ad_id]
                self._merge_ads(self.ads[idx], incoming)
                self.duplicate_records_merged += 1
                touched.append(self.ads[idx])
            else:
                if ad_id:
                    self._ad_index[ad_id] = len(self.ads)
                self.ads.append(incoming)
                touched.append(incoming)
        return touched

    def _normalize_one(self, raw: Dict[str, Any], countries: List[str],
                       status: Optional[str]) -> ObservedAd:
        start_iso = _unix_to_iso(raw.get("ad_delivery_start_time") or raw.get("delivery_start_time"))
        creation_iso = _unix_to_iso(raw.get("ad_creation_time") or raw.get("creation_time"))
        days_running = None
        if start_iso:
            try:
                start = datetime.fromisoformat(start_iso)
                days_running = max(0, (self.analysis_date - start).days)
            except ValueError:
                pass

        field_map = {
            "page_id": raw.get("page_id"),
            "page_name": raw.get("page_name"),
            "ad_creative_body": raw.get("ad_creative_body") or raw.get("creative_body"),
            "ad_creative_link_title": raw.get("ad_creative_link_title") or raw.get("headline"),
            "ad_creation_time": raw.get("ad_creation_time") or raw.get("creation_time"),
            "ad_delivery_start_time": raw.get("ad_delivery_start_time") or raw.get("delivery_start_time"),
            "ad_snapshot_url": raw.get("ad_snapshot_url") or raw.get("snapshot_url"),
            "currency": raw.get("currency"),
        }
        present = [k for k, v in field_map.items() if v not in (None, "")]

        ad = ObservedAd(
            ad_id=str(raw.get("id") or raw.get("ad_id") or raw.get("library_id") or ""),
            page_id=str(raw["page_id"]) if raw.get("page_id") is not None else None,
            page_name=raw.get("page_name"),
            creative_body=_normalize_text(raw.get("ad_creative_body") or raw.get("creative_body")),
            headline=_normalize_text(raw.get("ad_creative_link_title") or raw.get("headline")),
            creation_time=creation_iso,
            delivery_start_time=start_iso,
            snapshot_url=raw.get("ad_snapshot_url") or raw.get("snapshot_url"),
            currency=raw.get("currency"),
            status=status or raw.get("status"),
            country_scope=list(countries or raw.get("country_scope") or []),
            days_running=days_running if days_running is not None else raw.get("days_running"),
            source_fields_present=present,
            visual_inspected=bool(raw.get("visual_inspected", False)),
            creative_format_observed=bool(raw.get("creative_format_observed", False)),
        )
        for attr in (
            "hook", "creative_angle", "pain_point", "desire", "mechanism",
            "value_proposition", "offer", "proof_type", "cta", "funnel_stage",
            "content_theme", "audience_message", "timing_type", "cluster_id",
        ):
            value = raw.get(attr)
            if value not in (None, ""):
                setattr(ad, attr, value)
        ad.calculate_observability()
        return ad

    @staticmethod
    def _prefer(existing: Any, incoming: Any) -> Any:
        if existing in (None, "", []):
            return incoming
        return existing

    def _merge_ads(self, existing: ObservedAd, incoming: ObservedAd) -> None:
        # Prefer already-known values, but enrich gaps with later retrieval evidence.
        scalar_fields = (
            "page_id", "page_name", "creative_body", "headline", "creation_time",
            "delivery_start_time", "snapshot_url", "currency", "status",
            "hook", "creative_angle", "pain_point", "desire", "mechanism",
            "value_proposition", "offer", "proof_type", "cta", "funnel_stage",
            "content_theme", "audience_message", "timing_type", "cluster_id",
        )
        for name in scalar_fields:
            setattr(existing, name, self._prefer(getattr(existing, name), getattr(incoming, name)))

        existing.country_scope = sorted(set(existing.country_scope) | set(incoming.country_scope))
        existing.source_fields_present = sorted(set(existing.source_fields_present) | set(incoming.source_fields_present))
        existing.visual_inspected = existing.visual_inspected or incoming.visual_inspected
        existing.creative_format_observed = existing.creative_format_observed or incoming.creative_format_observed

        known_days = [x for x in (existing.days_running, incoming.days_running) if x is not None]
        existing.days_running = max(known_days) if known_days else None
        existing.calculate_observability()

    def mark_visual_inspected(self, ad_id: str, creative_format_observed: bool = False) -> bool:
        idx = self._ad_index.get(str(ad_id))
        if idx is None:
            return False
        ad = self.ads[idx]
        ad.visual_inspected = True
        ad.creative_format_observed = bool(creative_format_observed) or ad.creative_format_observed
        ad.calculate_observability()
        return True

    def coverage(self) -> Dict[str, Any]:
        returned = len(self.ads)
        total = self.estimated_total_count
        ratio = None
        if total and total > 0:
            ratio = min(1.0, returned / total)
        return {
            "ads_returned": returned,
            "estimated_total_count": total,
            "coverage_ratio": round(ratio, 4) if ratio is not None else None,
            "coverage_pct": round(ratio * 100, 1) if ratio is not None else None,
            "coverage_confidence": coverage_label(ratio),
            "duplicate_records_merged": self.duplicate_records_merged,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps([a.to_dict() for a in self.ads], ensure_ascii=False, indent=indent)

    def summary(self) -> Dict[str, Any]:
        known_days = [a.days_running for a in self.ads if a.days_running is not None]
        obs_counts = {k: sum(1 for a in self.ads if a.observability == k) for k in ("High", "Medium", "Low")}
        observed_scores = [a.observability_score for a in self.ads]
        return {
            **self.coverage(),
            "pages": sorted({a.page_name for a in self.ads if a.page_name}),
            "known_duration_ads": len(known_days),
            "average_days_running": round(sum(known_days) / len(known_days), 1) if known_days else None,
            "missing_creative_body": sum(1 for a in self.ads if not a.creative_body),
            "missing_headline": sum(1 for a in self.ads if not a.headline),
            "missing_snapshot_url": sum(1 for a in self.ads if not a.snapshot_url),
            "observability_counts": obs_counts,
            "average_observability_score": round(sum(observed_scores) / len(observed_scores), 1) if observed_scores else None,
            "note": (
                "Repeated ad IDs are merged before coverage/share calculations. "
                "A snapshot URL is availability only; visual evidence counts only after inspection."
            ),
        }


if __name__ == "__main__":
    p = AdLibraryParser()
    p.add_from_mcp_results({"estimated_total_count": 2, "ads": [
        {"id": "1", "ad_creative_link_title": "A"},
        {"id": "2", "ad_creative_link_title": "B"},
    ]})
    p.add_from_mcp_results({"estimated_total_count": 1, "ads": [
        {"id": "1", "ad_creative_body": "More evidence"},
    ]})
    print(json.dumps(p.summary(), ensure_ascii=False, indent=2))
