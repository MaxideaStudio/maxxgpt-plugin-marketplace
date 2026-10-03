# Evidence-Aware Scoring Framework — v3.8

v3.8 separates **creative quality**, **market signals**, and **message reach potential**. The goal is to prioritize what is worth studying without pretending Ads Library reveals performance.

## A. Strategic Quality Score (0–10)

Score only when evidence exists:
1. Creative Differentiation
2. Value Proposition Clarity
3. CTA Clarity
4. Emotional Appeal
5. Social Proof / Proof Quality

Rules:
- factor = 0–10 or N/A
- require at least **3 of 5** strategic factors to calculate Strategic Quality
- do not insert neutral scores for missing data
- every numeric factor requires factor-level supporting evidence
- if a factor score is supplied without evidence, convert it to N/A
- if visual evidence is required and the visual was not inspected, use N/A
- record which factors were blocked by missing evidence

## B. Market Signal Score (0–10)

Market Signal is descriptive, not performance.

### Longevity
For a creative **cluster**, use the **oldest active instance** as the Market Signal longevity input. Report the median days-running as context when useful. This avoids ambiguous averaging while preserving visibility into whether one very old instance is masking mostly-new variants.

Suggested deterministic mapping:
- 0–7 days: 2.5 — New Experiment
- 8–30 days: 5.0 — Recent
- 31–90 days: 7.0 — Sustained
- 91–180 days: 8.5 — Long-running
- 181+ days: 9.5 — Very Long-running

### Repetition
Use **cluster size**, not raw headline count alone:
- 1 ad: 3.0 — Single instance
- 2–3: 5.5 — Repeated
- 4–7: 7.5 — Frequently repeated
- 8+: 9.0 — Heavily repeated

`Market Signal Score = average of available Longevity + Repetition signals.`

A high Market Signal Score means the message is sustained/repeated in the retrieved evidence. It does **not** mean high ROAS, low CPA, or strong sales.

## C. Reach Potential — Qualitative Only

Reach Potential is **Low / Medium / High / N/A**, never a faux-precise numeric score.

Estimate from:
- breadth of problem/desire
- clarity and immediacy
- ease of understanding
- accessibility of the offer
- repeatability across contexts
- format only when observed

Always label it `AI-estimated Message Reach Potential`, not actual Meta reach or impressions.

## D. Study Priority Score

When evidence confidence is at least Medium and both Strategic Quality and Market Signal are available:

`Study Priority = 70% Strategic Quality + 30% Market Signal`

Threshold:
- >= 7.0 => **AI Recommended for Study**
- < 7.0 => **Not Priority for Study**
- Low evidence confidence or insufficient strategic factors => **Insufficient Evidence**

This replaces the v3.5 simple seven-factor average. It intentionally prevents an old ad from ranking highly only because it has longevity.

## E. Ad vs Cluster Scoring

Prefer scoring a **creative cluster** and show one representative ad. Duplicated ads should not each occupy a top slot.

For each Top 3–5 result, show:
- Strategic Quality
- Market Signal
- Reach Potential (Low/Medium/High)
- Study Priority
- evidence confidence
- direct representative Ad Library link

## F. Hero / Angle Share Guardrail

Never use raw Ad Share alone to declare a Hero Product or dominant angle.

Report both when possible:
- **Ad Share** = share of retrieved ad records
- **Unique Cluster Share** = share of distinct creative concepts/clusters

If they disagree, explain the difference. Example:
`Course A is 60% of ad records but only 25% of unique clusters, suggesting heavy duplication/rotation rather than 60% concept diversity.`
