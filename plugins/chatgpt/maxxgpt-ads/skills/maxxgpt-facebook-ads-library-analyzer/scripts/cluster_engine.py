#!/usr/bin/env python3
"""Deterministic evidence-aware creative clustering for Ads Library v3.8.

Hardening changes:
- deduplicates repeated ad IDs before clustering
- ads with no observable copy remain UNCLUSTERABLE
- clustering is order-independent via a pairwise similarity graph + union-find
- Thai/space-poor copy uses character n-gram similarity in addition to token/sequence similarity
- cluster longevity is explicit: oldest active instance is the scoring signal; median is context
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from statistics import median
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

STOP_TOKENS = {"", "the", "a", "an", "and", "or", "of", "to", "for", "with"}


def normalize_text(text: Optional[str]) -> str:
    text = unicodedata.normalize("NFKC", text or "").lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\u0E00-\u0E7F%฿$.-]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: Optional[str]) -> Set[str]:
    return {t for t in normalize_text(text).split() if t not in STOP_TOKENS and len(t) > 1}


def char_ngrams(text: Optional[str], n: int = 3) -> Set[str]:
    s = re.sub(r"\s+", "", normalize_text(text))
    if not s:
        return set()
    if len(s) <= n:
        return {s}
    return {s[i:i+n] for i in range(len(s) - n + 1)}


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def text_similarity(a: Optional[str], b: Optional[str]) -> float:
    na, nb = normalize_text(a), normalize_text(b)
    if not na or not nb:
        return 0.0
    seq = SequenceMatcher(None, na, nb).ratio()
    token_jac = jaccard(tokens(na), tokens(nb))
    char_jac = jaccard(char_ngrams(na, 3), char_ngrams(nb, 3))
    # Character n-grams materially improve Thai near-duplicate detection, while max()
    # keeps short identical/near-identical strings easy to merge.
    return round(max(seq, token_jac, char_jac), 4)


def offer_signature(text: Optional[str]) -> Tuple[str, ...]:
    """Extract conservative commercial markers to reduce false near-duplicate merges."""
    s = normalize_text(text)
    markers: List[str] = []
    patterns = [
        r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*(?:บาท|฿|thb|%|percent)\b",
        r"\bfree\b|\bฟรี\b",
        r"flash sale|sale|ลด|โปร|โปรโมชั่น|promotion",
        r"\b\d+\s*(?:วัน|day|days|เดือน|month|months)\b",
    ]
    for p in patterns:
        for m in re.findall(p, s, flags=re.IGNORECASE):
            markers.append(m if isinstance(m, str) else " ".join(m))
    return tuple(sorted(set(markers)))


def _combined_copy(ad: Dict[str, Any]) -> str:
    headline = ad.get("headline") or ad.get("ad_creative_link_title") or ""
    body = ad.get("creative_body") or ad.get("ad_creative_body") or ""
    return f"{headline} {body}".strip()


def _ad_id(ad: Dict[str, Any]) -> str:
    return str(ad.get("ad_id") or ad.get("id") or ad.get("library_id") or "")


def is_copy_clusterable(ad: Dict[str, Any]) -> bool:
    return bool(normalize_text(_combined_copy(ad)))


def _parse_dt(value: Any) -> Optional[datetime]:
    if value in (None, ""):
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
            return datetime.fromtimestamp(int(value), tz=timezone.utc)
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError, OSError):
        return None


def _days_running(ad: Dict[str, Any], analysis_date: datetime) -> Optional[int]:
    raw = ad.get("days_running")
    if raw not in (None, ""):
        try:
            return max(0, int(raw))
        except (TypeError, ValueError):
            pass
    dt = _parse_dt(ad.get("delivery_start_time") or ad.get("ad_delivery_start_time"))
    if not dt:
        return None
    return max(0, (analysis_date - dt).days)


@dataclass
class CreativeCluster:
    cluster_id: str
    ad_ids: List[str]
    representative_ad_id: str
    representative_text: str
    ad_count: int
    ad_share_pct: float = 0.0
    ad_share_pct_of_returned: float = 0.0
    ad_share_pct_of_clusterable: float = 0.0
    longevity_days_oldest_active_instance: Optional[int] = None
    longevity_days_median_active_instance: Optional[float] = None
    longevity_policy: str = "oldest_active_instance_for_market_signal"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


class ClusterEngine:
    """Order-independent exact + near-duplicate clustering based on observable copy."""

    def __init__(self, near_duplicate_threshold: float = 0.82,
                 analysis_date: Optional[datetime] = None):
        if not 0.0 <= near_duplicate_threshold <= 1.0:
            raise ValueError("near_duplicate_threshold must be between 0 and 1")
        self.threshold = near_duplicate_threshold
        self.analysis_date = analysis_date or datetime.now(timezone.utc)
        if self.analysis_date.tzinfo is None:
            self.analysis_date = self.analysis_date.replace(tzinfo=timezone.utc)
        self.unclusterable_ad_ids: List[str] = []
        self.ads_returned: int = 0
        self.clusterable_ads: int = 0
        self.duplicate_records_removed: int = 0

    @staticmethod
    def _dedupe_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen: Dict[str, Dict[str, Any]] = {}
        no_id: List[Dict[str, Any]] = []
        for ad in rows:
            aid = _ad_id(ad)
            if not aid:
                no_id.append(ad)
                continue
            if aid not in seen:
                seen[aid] = ad
            else:
                # Enrich missing copy fields conservatively.
                existing = seen[aid]
                for key in ("headline", "ad_creative_link_title", "creative_body", "ad_creative_body",
                            "days_running", "delivery_start_time", "ad_delivery_start_time"):
                    if existing.get(key) in (None, "") and ad.get(key) not in (None, ""):
                        existing[key] = ad.get(key)
        return list(seen.values()) + no_id

    def _should_link(self, a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        ta, tb = _combined_copy(a), _combined_copy(b)
        nta, ntb = normalize_text(ta), normalize_text(tb)
        if not nta or not ntb:
            return False
        if nta == ntb:
            return True
        sig_a, sig_b = offer_signature(ta), offer_signature(tb)
        if sig_a and sig_b and sig_a != sig_b:
            return False
        return text_similarity(ta, tb) >= self.threshold

    def cluster(self, ads: Iterable[Dict[str, Any]]) -> List[CreativeCluster]:
        input_rows = [dict(a) for a in ads]
        rows = self._dedupe_rows(input_rows)
        self.duplicate_records_removed = len(input_rows) - len(rows)
        self.ads_returned = len(rows)

        clusterable_rows = [ad for ad in rows if is_copy_clusterable(ad)]
        unclusterable_rows = [ad for ad in rows if not is_copy_clusterable(ad)]
        # Sort before graph construction so IDs/representatives are stable across input order.
        clusterable_rows.sort(key=lambda ad: (normalize_text(_combined_copy(ad)), _ad_id(ad)))
        self.clusterable_ads = len(clusterable_rows)
        self.unclusterable_ad_ids = sorted(_ad_id(ad) for ad in unclusterable_rows)

        uf = _UnionFind(len(clusterable_rows))
        for i in range(len(clusterable_rows)):
            for j in range(i + 1, len(clusterable_rows)):
                if self._should_link(clusterable_rows[i], clusterable_rows[j]):
                    uf.union(i, j)

        components: Dict[int, List[Dict[str, Any]]] = {}
        for i, ad in enumerate(clusterable_rows):
            components.setdefault(uf.find(i), []).append(ad)

        groups = list(components.values())
        # Stable component ordering by normalized representative text then ad ID.
        def rep_for(group: List[Dict[str, Any]]) -> Dict[str, Any]:
            return sorted(group, key=lambda x: (-len(normalize_text(_combined_copy(x))), normalize_text(_combined_copy(x)), _ad_id(x)))[0]

        groups.sort(key=lambda g: (normalize_text(_combined_copy(rep_for(g))), _ad_id(rep_for(g))))

        total_returned = max(1, self.ads_returned)
        total_clusterable = max(1, self.clusterable_ads)
        out: List[CreativeCluster] = []
        for idx, group in enumerate(groups, 1):
            rep = rep_for(group)
            ids = sorted(_ad_id(x) for x in group)
            share_returned = round(len(group) / total_returned * 100, 1)
            share_clusterable = round(len(group) / total_clusterable * 100, 1)
            days = sorted(d for d in (_days_running(x, self.analysis_date) for x in group) if d is not None)
            oldest = max(days) if days else None
            med = round(float(median(days)), 1) if days else None
            out.append(CreativeCluster(
                cluster_id=f"C{idx:03d}",
                ad_ids=ids,
                representative_ad_id=_ad_id(rep),
                representative_text=_combined_copy(rep),
                ad_count=len(group),
                ad_share_pct=share_returned,
                ad_share_pct_of_returned=share_returned,
                ad_share_pct_of_clusterable=share_clusterable,
                longevity_days_oldest_active_instance=oldest,
                longevity_days_median_active_instance=med,
            ))
        return out

    def summary(self, clusters: List[CreativeCluster]) -> Dict[str, Any]:
        observed_unique = len(clusters)
        unclusterable = len(self.unclusterable_ad_ids)
        clusterability_pct = (
            round(self.clusterable_ads / self.ads_returned * 100, 1)
            if self.ads_returned else None
        )
        largest_returned = max((c.ad_share_pct_of_returned for c in clusters), default=0.0)
        largest_clusterable = max((c.ad_share_pct_of_clusterable for c in clusters), default=0.0)
        duplicate_or_variant = max(0, self.clusterable_ads - observed_unique)

        return {
            "ads_returned_after_dedup": self.ads_returned,
            "duplicate_records_removed": self.duplicate_records_removed,
            "clusterable_ads": self.clusterable_ads,
            "unclusterable_ads": unclusterable,
            "unclusterable_ad_ids": list(self.unclusterable_ad_ids),
            "clusterability_pct": clusterability_pct,
            "observed_unique_clusters": observed_unique,
            "unique_clusters": observed_unique,
            "duplicate_or_variant_ads_among_clusterable": duplicate_or_variant,
            "largest_cluster_ad_share_pct_of_returned": largest_returned,
            "largest_cluster_ad_share_pct_of_clusterable": largest_clusterable,
            "longevity_policy": "Use oldest active instance for Market Signal; report median as context.",
            "note": (
                "Clustering is order-independent. Unclusterable ads are unknown concepts, not unique concepts. "
                "Observed Unique Clusters derive only from clusterable ads."
            ),
        }


if __name__ == "__main__":
    sample = [
        {"id": "1", "headline": "เร่งยอดขายปลายปีด้วย 3 AI", "days_running": 10},
        {"id": "2", "headline": "เร่งยอดขายปลายปี ด้วย 3 AI", "days_running": 5},
        {"id": "3", "headline": "Website พร้อมใช้ 3,500 บาท", "days_running": 100},
        {"id": "4", "headline": "", "ad_creative_body": ""},
        {"id": "5"},
        {"id": "2", "headline": "เร่งยอดขายปลายปี ด้วย 3 AI", "days_running": 5},
    ]
    engine = ClusterEngine()
    clusters = engine.cluster(sample)
    print([c.to_dict() for c in clusters])
    print(engine.summary(clusters))
