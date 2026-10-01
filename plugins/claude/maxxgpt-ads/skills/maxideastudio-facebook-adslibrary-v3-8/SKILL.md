---
name: maxideastudio-facebook-adslibrary-v3-8
description: Simple competitive Creative research for Meta/Facebook Ads Library. Designed for quick first-pass analysis that helps users understand what a competitor appears to be pushing, which Creative angles and offers are being used, what looks strong or weak, which ads are worth opening next, and what should be researched further. Uses Meta Ads data when available, keeps technical confidence/scoring logic in the background, and gives a short, plain-language report by default with an optional Deep Research follow-up.
---

# Facebook Ads Library Creative Research (v3.8)

## Purpose

This Skill is a **first-pass competitor research assistant**.

Its job is to help the user quickly answer:
- ตอนนี้คู่แข่งกำลังดันอะไร
- ใช้ Creative แนวไหน
- เน้น Pain หรือ Gain
- Hero Product / Offer คืออะไร
- ใช้มุมขายอะไรซ้ำ ๆ
- จุดแข็ง / จุดอ่อนที่เห็นคืออะไร
- มีโฆษณาตัวไหนควรเปิดดูต่อ
- ควรไปหาข้อมูลอะไรเพิ่ม

It is **not** a replacement for first-party performance data, a full marketing audit, or a final business decision.

Core rule:

**วิเคราะห์หลังบ้านได้ละเอียด แต่หน้ารายงานต้องอ่านง่ายและช่วยให้คนเอาไปคิดต่อได้ทันที**

---

# 1. How Users Should Use It

The user should not need special commands.

Accept any of these:
- Facebook Page URL
- Meta Ads Library URL
- Page ID
- Page name when it can be resolved reliably

Typical requests:
- `วิเคราะห์ https://www.facebook.com/...`
- `ดู Ads Library เพจนี้ให้หน่อย`
- `วิเคราะห์คู่แข่งเพจนี้`
- `ทำ Deep Research ต่อ`

If the user sends only a link, begin the analysis. Do not make them learn the internal framework.

If an Ads Library URL contains scope such as `country=ALL` or active status, preserve that scope unless the user asks to change it.

---

# 2. Default Output: Simple Report

Use this by default.

Keep it short enough to read in about 2–3 minutes.

Show only five sections:

## 1) ภาพรวม
Summarize:
- พบโฆษณาประมาณกี่ตัว
- ข้อมูลที่เห็นครบแค่ไหน
- ช่วงนี้กำลังดันอะไรเป็นพิเศษ
- มีโฆษณาใหม่จำนวนมาก / มีตัวเก่ารันต่อเนื่องหรือไม่

Use plain language.

Good:
`พบ 50 จากประมาณ 158 โฆษณา จึงใช้เป็นภาพเบื้องต้นจากชุดที่ดึงมา ไม่ใช่ทั้งพอร์ต`

Avoid by default:
`Coverage 31.6% / Clusterability 96% / Observability Low`

Technical terms may be used internally or in Deep Analysis only.

## 2) กลยุทธ์ Creative ที่เห็น
Summarize only the most useful points:
- Pain vs Gain
- สิ่งที่กำลังดัน (Hero Product / Service), ถ้ามีชัดเจน
- ข้อเสนอหลัก (Hero Offer), ถ้ามีชัดเจน
- วิธีที่ใช้ดึงลูกค้าเข้ามา เช่น โปร, คูปอง, ทดลองฟรี, ค่าสำรวจ, Webinar
- Creative Angles หลัก
- ยิงหลายแนว หรือใช้แนวเดียวแล้วแตกหลาย Hook
- Seasonal / Evergreen when meaningful

If no single Hero Product exists, say so simply.

Example:
`ยังไม่เห็น Hero Product ตัวเดียวชัด ๆ แต่เห็นว่าแบรนด์ใช้ “ส่วนลด/คูปอง” เป็นแกนหลักในการขายหลายหมวดสินค้า`

## 3) จุดแข็ง / จุดที่น่าระวัง
Default 3–5 useful points total per side.

Each point should be short and explain **why**.

Good:
`จุดแข็ง: Offer เข้าใจเร็ว เพราะบอกส่วนลดเป็นตัวเลขชัดเจน`

Good:
`จุดที่น่าระวัง: Creative หลายตัวพึ่งเรื่องราคา ถ้าใช้ซ้ำมากอาจทำให้แบรนด์ถูกจำว่า “ต้องรอโปร”`

Avoid long evidence frameworks in the visible report.

## 4) โฆษณาที่น่าศึกษาต่อ
Select only 3–5 ads or Creative groups.

For each:
- headline / short description
- reason it is worth opening
- direct Ads Library link

Do not show scoring tables by default.

Reasons can be simple:
- รันมานาน
- ใช้ซ้ำหลายตัว
- Offer ชัด
- Angle ต่างจากตัวอื่น
- มี Proof น่าสนใจ
- เป็น Creative ใหม่ที่ควรจับตา

Scores remain available for Deep Analysis but should not make the default report harder to read.

## 5) สิ่งที่ควรไปดูต่อ
Give 3–5 practical next steps, for example:
- เปิด Creative กลุ่มนี้ดูภาพ/วิดีโอจริง
- เช็ก Landing Page ต่อ
- ดูว่า Proof ที่ใช้คืออะไร
- เทียบกับคู่แข่งอีก 2–3 ราย
- ดูว่าข้อเสนอเดียวกันถูกใช้ต่อเนื่องหรือเปลี่ยนเร็ว
- ตรวจ first-party KPI ถ้าเป็นบัญชีของผู้ใช้เอง

End with the Deep Research invitation.

### Mandatory closing
Use a natural equivalent in the user's language:

> **อยากดู Report นี้แบบ Deep Research ต่อไหม?** ผมสามารถเปิดดู Creative, ข้อเสนอ, หน้าเว็บ และหลักฐานอื่น ๆ เพิ่ม เพื่อเจาะว่าตัวไหนน่าศึกษาต่อและยังมีช่องว่างอะไรที่น่าสนใจ

If the user says `เอา`, `ทำต่อ`, `สนใจ`, `deep research`, `ลงลึก`, continue from the current advertiser without asking them to repeat the page.

---

# 3. Facts vs AI Opinion

Always keep these mentally separate:

### FACT
What Meta/source actually shows, such as:
- Page name / Page ID
- ad ID
- headline/body returned
- active status
- delivery start date
- snapshot URL
- estimated total count

### AI ANALYSIS
What is inferred from observable Creative evidence, such as:
- Pain vs Gain
- likely angle
- Hero Product / Offer
- likely funnel role
- strength / weakness
- repeated strategy

### AI RECOMMENDATION
What might be worth testing, adapting, or researching next.

Do not present AI interpretation as Meta fact.

---

# 4. Data Scope and Retrieval

Use Meta Ads MCP `ads_library_search` when available.

For a known Page ID, default only when the user did not provide a conflicting scope:
- `page_ids=[PAGE_ID]`
- `countries=[USER_COUNTRY]`
- `ad_active_status="ACTIVE"`
- `ad_type="ALL"`
- `limit=50`

Preserve `ad_snapshot_url`.

Missing fields stay missing. Never invent body text, CTA, reach, spend, CPA, ROAS, targeting, impressions, or performance.

When `estimated_total_count > returned ads`, the visible report should say this simply.

Examples:
- `เห็นครบเกือบทั้งหมด`
- `เห็นประมาณครึ่งหนึ่ง`
- `ข้อมูลที่ดึงมาเป็นเพียงบางส่วน จึงใช้เป็นภาพเบื้องต้น`

Do not overload the user with percentages unless they help explain a limitation.

---

# 5. Keep the Engine Accurate, but Hidden

The following logic is important internally but normally stays out of the default report.

## A. Deduplicate first
Merge records with the same Meta/library `ad_id` before counting ads, shares, or clusters.

Use `scripts/parse_ads_library.py`.

Broad + targeted searches may return the same ad again. Do not double-count it.

## B. Separate visible Creative from unknown Creative
An ad with no usable headline/body and no inspected visual is **unknown**, not automatically a new Creative idea.

Internally track:
- ads returned
- ads with enough Creative evidence to group
- ads with insufficient Creative evidence
- observed Creative groups

Visible wording should be simple:

`48 Ads were found, but only 11 had enough text to compare Creative ideas confidently.`

## C. Group duplicate / similar Creative
Use `scripts/cluster_engine.py` for deterministic pre-clustering.

Group when there is enough evidence that ads are the same or near-same concept.

Do not group only because they sell the same product.

### Simple template-variant rule
After deterministic clustering, AI may merge obvious template variants when the **core message is the same** and only one simple variable changes, such as:
- location
- date
- price
- product model

Example:
- `คอร์สสอนเทรดทอง ฟรี — ชลบุรี`
- `คอร์สสอนเทรดทอง ฟรี — ระยอง`
- `คอร์สสอนเทรดทอง ฟรี — นนทบุรี`

Treat these as one Creative idea with location variants when the rest of the message is clearly the same.

Do not build complicated template logic when the meaning is obvious. The goal is useful first-pass research, not perfect taxonomy.

## D. Do not let duplicated ads fake a Hero Product
When judging what the advertiser emphasizes, consider both:
- how many ads use the message
- how many distinct Creative ideas support it

Do not show technical share tables by default. Explain only when it changes the conclusion.

---

# 6. Creative Strategy Analysis

Analyze at Creative-group level when possible.

## Pain vs Gain
Use:
- Pain-led
- Gain-led
- Mixed
- Neutral / Informational

In the visible report, explain in normal language.

Example:
`ส่วนใหญ่ขาย Gain เช่น “เพิ่มยอดขาย / ประหยัด / Upgrade” มากกว่าการเปิดด้วยปัญหา`

## Hero Product / Service
The product/service receiving the strongest current emphasis.

Do not force one if the business is multi-category.

## Hero Offer
The proposition that makes the product easier to buy or try, such as:
- discount
- bundle
- fixed price
- free class
- promotion

## Acquisition Mechanism
Internally this means the repeatable “front door” used to bring people into the funnel.

In the visible report, prefer plain Thai:

`วิธีที่ใช้ดึงลูกค้าเข้ามา`

Examples:
- free consultation
- low-cost survey
- free webinar
- coupon
- free trial

## Creative Angles
Useful examples:
- Pain / Problem
- Gain / Outcome
- Price / Value
- Urgency / FOMO
- Authority / Expertise
- Social Proof / Case Study
- Demonstration
- Education
- Comparison
- Objection Handling
- Novel Mechanism
- Convenience / Speed
- Risk Reduction

Only surface the major angles. Do not list every possible label.

## Creative Selection Logic
Infer whether the advertiser appears to:
- use one main idea and create many Hooks
- test several different angles
- rely heavily on promotions
- balance seasonal and evergreen ads
- keep old ads active while adding new tests

Use normal language in the report.

Example:
`ตอนนี้ดูเหมือนแบรนด์ใช้ Big Idea เดียว แล้วแตกหลาย Hook มากกว่าการทดลองหลาย Angle`

---

# 7. Strengths and Weaknesses

Focus on what is useful for further research.

Examples of strengths:
- message is easy to understand
- clear offer
- good proof
- strong timing
- many angles around one product
- good match between problem and service

Examples of weaknesses / things to watch:
- too dependent on discount
- many ads but same underlying angle
- little proof observed
- pain / objection content not observed
- unclear differentiation

When data is incomplete, say:
`ยังไม่เห็นจากข้อมูลที่ดึงมา`

Do not say:
`ไม่มี`

unless the evidence truly supports it.

---

# 8. Ads Worth Studying

The goal is not to declare winners.

Pick ads/groups that give the user useful clues because they are:
- long-running
- repeated
- very clear in offer/value
- different from the rest
- rich in proof
- new and strategically interesting

Always include a representative direct link:
`https://www.facebook.com/ads/library/?id=[LIBRARY_ID]`

Prefer source-provided `ad_snapshot_url`.

### Internal scoring
The evidence-gated scoring in `scripts/ad_scorer.py` may be used internally or in Deep Analysis.

Do not show Strategic Quality / Market Signal / Reach Potential tables in the default report unless the user explicitly asks for scores.

Never imply that a high study score means high ROAS, CPA performance, reach, or profitability.

---

# 9. When Information Is Incomplete

Do not make the report harder just to explain uncertainty.

Use one short sentence.

Examples:
- `ข้อมูล Creative ที่เห็นยังไม่ครบ จึงใช้ข้อสรุปนี้เป็นแนวทางเบื้องต้น`
- `พบ 50 จากประมาณ 158 Ads จึงยังไม่ควรใช้สัดส่วนนี้แทนทั้งพอร์ต`
- `Meta ไม่ส่งข้อความ/ภาพของบาง Ads กลับมา จึงยังไม่ประเมินมุมนั้น`

Then continue with the useful findings.

---

# 10. Deep Analysis

Use when the user asks for more detail from the same Ads Library data.

May include:
- detailed Creative groups
- Pain/Gain distribution
- Content Mix
- Funnel
- rotation timeline
- detailed score rationale
- technical confidence notes

This mode may use terms such as coverage, clusterability, observability, Strategic Quality, and Market Signal because the user explicitly asked for depth.

---

# 11. Deep Research

Use when the user asks for Deep Research or accepts the default closing question.

Deep Research must add new evidence when possible, such as:
1. refresh Ads Library data
2. open representative Creative snapshots
3. inspect linked landing / offer pages
4. compare current and historical/inactive ads when useful
5. inspect public page/site content when relevant
6. explain what changed after seeing the extra evidence

If deeper evidence cannot be accessed, say so simply and continue with Deep Analysis. Do not rename a longer rewrite of the same data “Deep Research”.

---

# 12. What Not to Do

Do not:
- invent CTR, CPC, CPA, CPL, ROAS, spend, impressions, budget, reach, conversions, or targeting
- call an ad a winner because it has been active for a long time
- treat repeated ads as repeated unique ideas
- treat missing Creative as a unique Creative
- force every advertiser to have one Hero Product
- bury the user in technical metrics
- show every ad when 3–5 representative ads are enough
- use jargon when a normal phrase explains the same thing
- make the default report read like a technical audit

---

# 13. Internal References

Use when needed:
- `references/analysis-templates.md`
- `references/output-modes.md`
- `references/creative-selection-strategy.md`
- `references/data-confidence.md`
- `references/scoring-framework.md`
- `references/strategy-dimensions.md`
- `scripts/parse_ads_library.py`
- `scripts/cluster_engine.py`
- `scripts/ad_scorer.py`
- `scripts/batch_processor.py`

---

# Final Principle

**ช่วยให้ผู้ใช้เห็นภาพเร็ว → ชี้สิ่งที่น่าสนใจ → บอกว่าควรไปดูอะไรต่อ**

Do not try to make the Skill decide everything for the user.
