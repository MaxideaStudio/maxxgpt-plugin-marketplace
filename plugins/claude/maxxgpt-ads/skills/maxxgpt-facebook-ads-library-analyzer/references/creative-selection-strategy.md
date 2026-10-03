# Creative Selection Strategy — v3.8

This framework explains how to infer the competitor's creative portfolio strategy from public Ads Library evidence. It is AI analysis, not private performance data.

## 1. Pain vs Gain
Classify every unique creative cluster:
- Pain-led
- Gain-led
- Mixed
- Neutral / informational

Extract the exact problem or desired outcome being emphasized. Aggregate by cluster, not only by raw ad count, so duplicated variants do not distort the mix. Always compare Ad Share with Unique Cluster Share when volume concentration may be caused by duplicate/variant ads.

## 2. Commercial Focus Model
Do not assume every advertiser has one Hero Product. Separate:

### Hero Product / Service
The specific product, service, course, category, or SKU receiving the strongest current ad emphasis.

### Hero Offer
The specific commercial proposition attached to a product/service, such as a discount, bundle, free class, package, or fixed-price promotion.

### Hero Acquisition Mechanism
A repeatable front-door device that lowers the barrier to the first conversion step across multiple products/services, such as:
- low-cost survey / inspection fee
- free consultation
- free trial
- free webinar
- diagnostic check
- quotation / site visit

A cross-category acquisition mechanism should NOT be mislabeled as a single Hero Product.

Classify the portfolio as one or more of:
- Product-led
- Offer-led
- Acquisition-mechanism-led
- Portfolio-led / Multi-category

Infer the model using a combination of:
- active-ad share by product/service category
- unique cluster share
- variant count
- recency
- repeated messaging
- repeated offer structures
- the same entry incentive across multiple categories
- multi-format presence when visible

If no product clearly dominates, explicitly state `No clear single Hero Product observed`.
The output is a current **advertising emphasis**, not evidence of best-selling or most profitable status.

## 3. Creative Angle Taxonomy
Recommended tags:
- Pain / problem awareness
- Gain / aspiration / outcome
- Urgency / scarcity
- Price / promotion / value
- Authority / expertise
- Social proof / case study
- Demonstration
- Education / insight
- Comparison
- Objection handling
- Novel mechanism / new way
- Convenience / speed / simplicity
- Risk reduction / reassurance
- FOMO / timing / trend
- Identity / status / belonging

Multiple angle tags are allowed, but identify one Primary Angle whenever evidence supports it.

## 4. Portfolio Selection Logic
Interpret the mix across:
- Exploit vs Explore
- Angle concentration vs breadth
- Hook variation vs angle variation
- Offer consistency vs testing
- Proof-heavy vs claim-heavy
- Funnel balance
- Seasonal vs evergreen
- Rotation cadence

## 5. Strengths & Weaknesses
Judge the strategy from a marketer's perspective while clearly labeling inference. Every point requires evidence and confidence.

Potential strengths:
- clear positioning
- strong pain/gain fit
- repeated memorable mechanism
- offer clarity
- proof depth
- format diversity
- disciplined variation
- funnel coverage

Potential weaknesses:
- fatigue risk
- narrow angle portfolio
- generic claims
- weak proof
- unclear CTA
- insufficient objection handling
- repetitive hooks
- insufficient format diversity
- seasonal overdependence

## 6. Opportunity Map
Turn the diagnosis into four action buckets:
- Keep / Adapt
- Test
- Avoid / Watch
- Validate

Recommendations should propose experiments, not guaranteed outcomes. State the first-party KPI that would validate each test.


## 7. Evidence Confidence Guardrail
- Portfolio-level shares must inherit dataset coverage confidence.
- Visual claims require actual snapshot inspection.
- Absence claims become `not observed in the retrieved sample` when coverage is incomplete.
- Hero/angle conclusions should be downgraded when Ad Share is high but Unique Cluster Share is not.
