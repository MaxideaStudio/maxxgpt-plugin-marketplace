#!/usr/bin/env python3
"""Descriptive multi-advertiser aggregation for Ads Library v3.8."""

from __future__ import annotations
import json
from collections import Counter
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional


@dataclass
class AdvertiserAnalysis:
    advertiser_name: str
    advertiser_id: Optional[str] = None
    active_ads_returned: int = 0
    estimated_total_count: Optional[int] = None
    coverage_pct: Optional[float] = None
    coverage_confidence: str = "Unknown"
    observability_confidence: str = "Unknown"
    clusterable_ads: int = 0
    unclusterable_ads: int = 0
    observed_unique_clusters: int = 0
    unique_clusters: int = 0  # backward-compatible alias for observed_unique_clusters
    dominant_angles: List[str] = field(default_factory=list)
    largest_cluster_ad_share: Optional[float] = None
    largest_category_cluster_share: Optional[float] = None
    long_running_clusters: int = 0
    new_experiments: int = 0
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BatchProcessor:
    """Compare advertisers without inferring which one performs better."""

    def __init__(self):
        self.analyses: List[AdvertiserAnalysis] = []

    def add_analysis(self, analysis: AdvertiserAnalysis) -> None:
        self.analyses.append(analysis)

    @staticmethod
    def dominant(values: List[Optional[str]], n: int = 3) -> List[str]:
        counts = Counter(v for v in values if v)
        return [label for label, _ in counts.most_common(n)]

    def comparison_table(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self.analyses]

    def cross_brand_observations(self) -> Dict[str, Any]:
        if not self.analyses:
            return {}
        return {
            "advertisers_compared": len(self.analyses),
            "shared_dominant_angles": self._shared_angles(),
            "note": (
                "Comparison is descriptive and confidence should be adjusted for coverage/observability. "
                "Ads Library alone cannot establish better ROAS, CPA, CTR, reach, or profitability."
            ),
        }

    def _shared_angles(self) -> List[str]:
        angle_counts = Counter()
        for a in self.analyses:
            angle_counts.update(set(a.dominant_angles))
        threshold = 2 if len(self.analyses) > 1 else 1
        return [angle for angle, count in angle_counts.items() if count >= threshold]

    def to_json(self, indent: int = 2) -> str:
        return json.dumps({
            "advertisers": self.comparison_table(),
            "cross_brand": self.cross_brand_observations(),
        }, ensure_ascii=False, indent=indent)


if __name__ == "__main__":
    p = BatchProcessor()
    p.add_analysis(AdvertiserAnalysis(
        advertiser_name="Brand A",
        active_ads_returned=50,
        estimated_total_count=179,
        coverage_pct=27.9,
        coverage_confidence="Low",
        observability_confidence="Medium",
        clusterable_ads=31,
        unclusterable_ads=19,
        observed_unique_clusters=12,
        unique_clusters=12,
        dominant_angles=["Price", "Risk Reduction"],
        largest_cluster_ad_share=18.0,
    ))
    print(p.to_json())
