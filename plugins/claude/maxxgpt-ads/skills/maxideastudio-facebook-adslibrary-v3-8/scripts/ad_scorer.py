#!/usr/bin/env python3
"""Evidence-gated study-priority scoring for Ads Library competitive intelligence v3.8."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping, Optional

STRATEGIC_FACTORS = (
    "creative_differentiation",
    "value_proposition",
    "cta_clarity",
    "emotional_appeal",
    "social_proof",
)


@dataclass
class StudyPriority:
    strategic_factor_scores: Dict[str, Optional[float]]
    factor_evidence_present: Dict[str, bool]
    blocked_factors: Dict[str, str]
    strategic_quality_score: Optional[float]
    market_signal_score: Optional[float]
    reach_potential: str
    study_priority_score: Optional[float]
    status: str
    evidence_confidence: str
    longevity_policy: str = "oldest_active_instance_for_market_signal"
    caveat: str = (
        "Study Priority is an AI research-priority score, not proven ad performance, "
        "profitability, reach, CPA, CTR, or ROAS."
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AdScorer:
    @staticmethod
    def longevity_signal(days_running: Optional[int]) -> str:
        if days_running is None:
            return "N/A"
        if days_running <= 7:
            return "New Experiment"
        if days_running <= 30:
            return "Recent"
        if days_running <= 90:
            return "Sustained"
        if days_running <= 180:
            return "Long-running"
        return "Very Long-running"

    @staticmethod
    def longevity_score(days_running: Optional[int]) -> Optional[float]:
        if days_running is None:
            return None
        if days_running <= 7:
            return 2.5
        if days_running <= 30:
            return 5.0
        if days_running <= 90:
            return 7.0
        if days_running <= 180:
            return 8.5
        return 9.5

    @staticmethod
    def repetition_signal(cluster_size: Optional[int]) -> str:
        if cluster_size is None:
            return "N/A"
        if cluster_size <= 1:
            return "Single instance"
        if cluster_size <= 3:
            return "Repeated"
        if cluster_size <= 7:
            return "Frequently repeated"
        return "Heavily repeated"

    @staticmethod
    def repetition_score(cluster_size: Optional[int]) -> Optional[float]:
        if cluster_size is None:
            return None
        if cluster_size <= 1:
            return 3.0
        if cluster_size <= 3:
            return 5.5
        if cluster_size <= 7:
            return 7.5
        return 9.0

    @staticmethod
    def _validate_score(value: Optional[float]) -> Optional[float]:
        if value is None:
            return None
        value = float(value)
        if not 0 <= value <= 10:
            raise ValueError("Score must be between 0 and 10, or None/N/A.")
        return value

    @staticmethod
    def _validate_reach(value: Optional[str]) -> str:
        if value is None:
            return "N/A"
        normalized = str(value).strip().title()
        allowed = {"Low", "Medium", "High", "N/A"}
        if normalized not in allowed:
            raise ValueError("reach_potential must be Low, Medium, High, or N/A")
        return normalized

    @staticmethod
    def _confidence_rank(value: str) -> int:
        return {"Low": 0, "Medium": 1, "High": 2}.get(value, 0)

    @staticmethod
    def _has_evidence(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, tuple, set, dict)):
            return bool(value)
        return bool(value)

    @classmethod
    def aggregate_study_priority(
        cls,
        *,
        creative_differentiation: Optional[float] = None,
        value_proposition: Optional[float] = None,
        cta_clarity: Optional[float] = None,
        emotional_appeal: Optional[float] = None,
        social_proof: Optional[float] = None,
        days_running: Optional[int] = None,
        cluster_longevity_days: Optional[int] = None,
        cluster_size: Optional[int] = None,
        reach_potential: Optional[str] = None,
        evidence_confidence: str = "Medium",
        factor_evidence: Optional[Mapping[str, Any]] = None,
        strict_evidence: bool = True,
    ) -> StudyPriority:
        """Aggregate research-priority signals.

        In strict_evidence mode (default), a strategic factor is only scored when
        factor_evidence contains truthy supporting evidence for that factor. Missing
        evidence converts the factor to N/A rather than allowing unsupported scores.

        Cluster longevity uses the oldest active instance. Pass it as
        cluster_longevity_days. days_running remains as a backward-compatible fallback.
        """
        evidence_confidence = str(evidence_confidence).title()
        if evidence_confidence not in {"Low", "Medium", "High"}:
            raise ValueError("evidence_confidence must be Low, Medium, or High")

        raw_scores = {
            "creative_differentiation": creative_differentiation,
            "value_proposition": value_proposition,
            "cta_clarity": cta_clarity,
            "emotional_appeal": emotional_appeal,
            "social_proof": social_proof,
        }
        evidence_map = dict(factor_evidence or {})
        gated: Dict[str, Optional[float]] = {}
        evidence_present: Dict[str, bool] = {}
        blocked: Dict[str, str] = {}

        for name in STRATEGIC_FACTORS:
            score = cls._validate_score(raw_scores[name])
            has_evidence = cls._has_evidence(evidence_map.get(name))
            evidence_present[name] = has_evidence
            if score is None:
                gated[name] = None
            elif strict_evidence and not has_evidence:
                gated[name] = None
                blocked[name] = "Score supplied without factor-level evidence; converted to N/A."
            else:
                gated[name] = score

        available = [v for v in gated.values() if v is not None]
        strategic_score = round(sum(available) / len(available), 2) if len(available) >= 3 else None

        longevity_days = cluster_longevity_days if cluster_longevity_days is not None else days_running
        market_parts = [
            cls.longevity_score(longevity_days),
            cls.repetition_score(cluster_size),
        ]
        market_known = [v for v in market_parts if v is not None]
        market_score = round(sum(market_known) / len(market_known), 2) if market_known else None
        reach = cls._validate_reach(reach_potential)

        if cls._confidence_rank(evidence_confidence) < cls._confidence_rank("Medium"):
            composite = None
            status = "Insufficient Evidence"
        elif strategic_score is None or market_score is None:
            composite = None
            status = "Insufficient Evidence"
        else:
            composite = round(0.70 * strategic_score + 0.30 * market_score, 2)
            status = "AI Recommended for Study" if composite >= 7.0 else "Not Priority for Study"

        return StudyPriority(
            strategic_factor_scores=gated,
            factor_evidence_present=evidence_present,
            blocked_factors=blocked,
            strategic_quality_score=strategic_score,
            market_signal_score=market_score,
            reach_potential=reach,
            study_priority_score=composite,
            status=status,
            evidence_confidence=evidence_confidence,
        )

    @classmethod
    def aggregate_ai_scores(cls, **scores: Optional[float]) -> StudyPriority:
        """Legacy helper. Kept for compatibility, but remains evidence-conservative."""
        evidence = {name: scores.get(name) is not None for name in STRATEGIC_FACTORS}
        return cls.aggregate_study_priority(
            creative_differentiation=scores.get("creative_differentiation"),
            value_proposition=scores.get("value_proposition"),
            cta_clarity=scores.get("cta_clarity"),
            emotional_appeal=scores.get("emotional_appeal"),
            social_proof=scores.get("social_proof"),
            factor_evidence=evidence,
            strict_evidence=False,
            evidence_confidence="Medium",
        )


if __name__ == "__main__":
    demo = AdScorer.aggregate_study_priority(
        creative_differentiation=7.5,
        value_proposition=8.5,
        cta_clarity=8.0,
        emotional_appeal=7.0,
        social_proof=7.5,
        cluster_longevity_days=95,
        cluster_size=4,
        reach_potential="High",
        evidence_confidence="High",
        factor_evidence={
            "creative_differentiation": ["visual inspected", "cluster comparison"],
            "value_proposition": ["headline", "body"],
            "cta_clarity": ["body CTA"],
            "emotional_appeal": ["headline", "visual"],
            "social_proof": ["testimonial", "numeric proof"],
        },
    )
    print(demo.to_dict())
