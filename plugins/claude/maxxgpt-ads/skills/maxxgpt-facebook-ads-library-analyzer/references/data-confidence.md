# Data Confidence & Evidence Rules — v3.8

The purpose of this layer is to stop the analysis from sounding more certain than the retrieved evidence allows.

## 1. Dataset Coverage

Calculate:

`coverage = ads_returned / estimated_total_count`

Cap at 100% and label:
- **High coverage:** >= 80%
- **Medium coverage:** 40–79%
- **Low coverage:** < 40%
- **Unknown:** estimated total unavailable

Coverage describes how much of the currently estimated Ads Library set was retrieved. It does **not** prove the returned sample is random or representative.

When coverage is Low:
- describe distributions as **"within the retrieved sample"**
- do not claim `the whole portfolio is X% pain-led`
- avoid definitive `competitor does not use...`; say **`not observed in the retrieved sample`**
- reduce confidence on Hero Product, angle-share, content-mix, and Creative Gap conclusions unless additional targeted searches support them


## 1A. Retrieval Deduplication

Before calculating coverage or shares, merge repeated records with the same Meta/library `ad_id`. Multi-query workflows frequently retrieve the same ad more than once.

Rules:
- deduplicate by `ad_id` before `ads_returned`, Coverage, Ad Share, or Cluster Share
- merge complementary non-empty evidence from duplicate records
- preserve the broadest observed `estimated_total_count`; do not let a narrow follow-up query overwrite it
- report duplicate records merged/removed when material

## 2. Ad-Level Observability

Use observable evidence, not the mere existence of an ad record.

Suggested observability points:
- headline returned: 25
- creative body returned: 30
- visual actually inspected: 30
- delivery start date returned: 10
- snapshot URL available: 5

Labels:
- **High observability:** 75–100
- **Medium observability:** 45–74
- **Low observability:** 0–44

A snapshot URL alone is **not** visual evidence. Mark `visual inspected = yes` only after actually viewing the creative.


## 3. Clusterability Confidence

Clustering confidence is separate from dataset coverage. A dataset can have 96% coverage but still have weak concept visibility if many ads have no usable creative evidence.

Calculate:

`clusterability = clusterable_ads / ads_returned`

Rules:
- an ad with no headline/body and no inspected visual evidence is **Unclusterable**
- Unclusterable does **not** mean unique
- never add one unique cluster per missing creative
- report **Observed Unique Clusters** only from clusterable ads
- if clusterability is < 70%, concept-diversity / Unique Cluster Share conclusions should normally be no higher than Medium confidence unless visual inspection resolves the unknown ads

Example:
`50 ads retrieved; 28 clusterable (56%); 22 unclusterable; 7 observed unique clusters among clusterable ads.`

## 4. Inference Confidence Ceiling

An AI inference should not be more confident than its evidence.

Examples:
- Headline only, visual not inspected -> Pain/Gain may be Medium; format/proof/visual differentiation should be Low or N/A.
- Low portfolio coverage -> angle-share and Creative Gap should be Low/Medium confidence even if individual ads are clear.
- High-observability cluster repeated across many ads -> message/offer inference can be High confidence, but profitability remains unknown.

## 5. Data Confidence Line

Simple Reports should include one concise limitation line only when it materially affects the conclusion:

`พบ 50 จากประมาณ 179 Ads และมี 31 ตัวที่อ่านข้อความได้ จึงใช้ข้อสรุปด้าน Creative เป็นภาพเบื้องต้นจากชุดที่ดึงมา`

Do not turn this into a long disclaimer unless it changes the conclusion.

## 6. Claim Language

Prefer:
- `observed in the retrieved sample`
- `AI-inferred`
- `not observed in the retrieved sample`
- `appears concentrated around...`
- `worth validating with first-party data`

Avoid unsupported absolutes:
- `does not use`
- `best-performing`
- `winner`
- `highest reach`
- `this strategy works`
