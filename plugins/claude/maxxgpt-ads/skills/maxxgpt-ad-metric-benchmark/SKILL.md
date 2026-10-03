---
name: maxxgpt-ad-metric-benchmark
description: >-
  เทียบเมตริกโฆษณา Meta (Facebook/Instagram) ของบัญชีที่ผูกกับ MaxxGPT แบบ "จัดระดับ" —
  CTR · CTR (ลิงก์คลิก) · Engagement rate · CPM · Frequency · Cost per result ของแต่ละโฆษณา
  เทียบกับค่ากลางของบัญชีเอง แล้วตีเป็น High / Medium / Low. เป็นงาน 2 สเต็ป: (1) ดูภาพรวมเพื่อ
  เลือก Result ที่จะเจาะ (แยกตาม Objective + Result indicator) → (2) เจาะ Result นั้นเป็นตาราง
  เทียบระดับรายโฆษณา. เลือกช่วงเวลามาในแชทได้เลย (ไม่บอกก็ถามให้) แล้วสรุปเป็นข้อความ + ตารางระดับ พร้อมให้ถามต่อได้.
  Benchmark each Meta ad's CTR/Frequency/CPM/Engagement/Cost-per-result against the account's own
  spread and tag it High/Medium/Low. ใช้ skill นี้ทุกครั้งที่ผู้ใช้พูดถึง: benchmark โฆษณา /
  เทียบเมตริก / ตัวไหน CTR สูง-ต่ำ / frequency เกินไหม / CPM แพงไป / โฆษณาตัวไหนถือคนอยู่ /
  จัดระดับโฆษณา High Medium Low / เทียบ ad กับค่ากลางบัญชี — แม้ผู้ใช้จะไม่พูดคำว่า "skill" ตรงๆ.
  (ต้องมี connector MaxxGPT)
---

# MaxxGPT — Ad Metric Benchmark (เทียบเมตริกโฆษณา + จัดระดับ)

พา user จาก "อยากรู้ว่าโฆษณาตัวไหน CTR/CPM/Frequency ดี-แย่กว่าค่ากลาง" ไปจนได้ **ตารางจัดระดับ
รายโฆษณา (High / Medium / Low)** ของบัญชีที่ผูกกับ MaxxGPT แล้วอยู่ต่อเพื่อตอบคำถามเจาะลึก

**นี่เป็นงาน 2 สเต็ป** (2 tool คนละตัว) — ต้องทำตามลำดับ:

```
STEP 1  ad_benchmark_overview(date_start, date_end)  → ภาพรวมแยกตาม Objective + Result indicator
        └─ เลือก Result indicator หนึ่งค่าจากในภาพรวม
STEP 2  ad_benchmark_metrics(date_start, date_end, indicator=<ค่าที่เลือก>)
        └─ ตารางเทียบระดับรายโฆษณา 6 เมตริก (CTR · CTR link · Engagement · CPM · FRQ · Cost/result)
```

> ## 🔴 กฎเหล็ก 7 ข้อ (อ่านก่อนเริ่มทุกครั้ง)
>
> 1. **เรียก MCP tool ทีละตัว ห้ามยิงขนาน** — ยิงพร้อมกันจะได้ error `The connector's server isn't
>    responding.` ที่**ดูเหมือน server พังทั้งที่ไม่ใช่** · เจอ error นี้ให้สงสัยวิธีเรียกของตัวเองก่อน
> 2. **ต้องทำ 2 สเต็ปตามลำดับ** — `ad_benchmark_metrics` **ต้องมี `indicator`** ที่ได้จาก
>    `ad_benchmark_overview` ก่อนเสมอ · **ห้ามเดา `indicator` เอง** (เดาแล้วผลจะว่าง)
> 3. **ทั้ง 2 สเต็ปเป็นงาน async** — ยิง tool ได้ `job_id` แล้วต้อง **poll `get_job` เองจนจบ** ตาม
>    `poll_hint.poll_after_seconds` · **ห้ามจบ turn คืนงานให้ user ระหว่างรอ**
> 4. **ห้ามเทข้อมูลดิบทั้งก้อนลงแชท** — พิมพ์ตารางแค่ ~10 แถวต่อเมตริกเสมอ (ดู § ตัดข้อมูล)
>    ข้อมูลเต็มยังอยู่กับเราไว้ตอบคำถามต่อ
> 5. **ตัวเลขทุกตัวต้องมาจาก `data` จริงเท่านั้น** — คีย์ไหนไม่มีก็ตัดคอลัมน์นั้นทิ้ง **ห้ามเดา
>    ห้ามคำนวณเมตริกใหม่ที่ปลายทางไม่ได้ให้**
> 6. **"ระดับ" เป็นการเทียบกันเองในบัญชีนี้ ไม่ใช่มาตรฐานกลาง** — `High` = สูงกว่าค่ากลางของ
>    *ad ตัวอื่นในบัญชีนี้ ช่วงนี้ Result นี้* ไม่ใช่ "ดีตามมาตรฐานอุตสาหกรรม" · อธิบายแบบนี้กับ user เสมอ
> 7. **ห้ามสร้าง widget / ฟอร์ม HTML / การ์ด UI เด็ดขาด** — ห้ามเรียก tool แสดงวิชวลทุกตัว
>    (`visualize` · `show_widget` · `render-ui` · Artifact) และ**ห้ามเขียน HTML/ฟอร์มเอง**
>    ถามด้วย **tool `AskUserQuestion` (ปุ่มตัวเลือก)** เท่านั้น · เรียกไม่ได้จริง ๆ =
>    **ถามเป็นข้อความแบบเลขข้อ (1 / 2 / 3) แล้วหยุดรอ user ตอบ** ห้ามเดาเองแล้วยิงต่อ

## Connector ที่ต้องมี · Required connector

| Connector | URL | ใช้ทำอะไร |
|---|---|---|
| **MaxxGPT** | `https://mcp.maxxgpt.ai/mcp` | `get_account_info` · `ad_benchmark_overview` · `ad_benchmark_metrics` · `get_job` |

> ### 🔁 เจอ connector ที่ชี้ไปโดเมนเก่า
> `https://mcp-beta.maxxgpt.ai/mcp` เป็น**โดเมนเดิม ใช้แก้ขัดได้** — เจอ connector ของ user ตั้งไว้แบบนั้น
> **ทำงานต่อได้ตามปกติ ห้ามหยุดงานเพื่อให้เขาไปเปลี่ยนก่อน** ·
> แต่ให้บอกหนึ่งบรรทัดตอนจบว่าโดเมนหลักคือ `https://mcp.maxxgpt.ai/mcp` และแนะนำให้ย้าย ·
> **บอกครั้งเดียวต่อ session พอ อย่าทวงซ้ำทุกรอบ**

ไม่มี connector นี้ = แจ้ง user พร้อม URL แล้วหยุด อย่าเดินหน้าด้วยการเดา ·
**ชื่อ tool ของแต่ละ user อาจไม่ตรงเป๊ะ** (เปลี่ยนชื่อเองได้) → จับคู่จาก *ความสามารถ* ไม่ใช่ชื่อเป๊ะ ๆ

> **บัญชีโฆษณา · เพจ (MaxxGPT V4)** — ไม่ส่งอะไร = tool ใช้บัญชี/เพจที่ user เลือกไว้ในเว็บ MaxxGPT · สกิลนี้ส่ง `ad_account_id` ที่ได้จากขั้น 0 ทุกครั้ง ·
> tool ที่ทำงานกับบัญชีโฆษณารับ `ad_account_id` (`act_…`) และ `page_id` แบบ **optional** เพื่อรันกับบัญชี/เพจอื่นที่ user ผูกไว้ **เฉพาะครั้งนั้น** (ไม่เปลี่ยนค่าที่เลือกในเว็บ · `get_job` / `search_interest` / `suggest_interest` ไม่มีสอง argument นี้) ·
> id ต้องมาจาก `list_ad_accounts` / `list_pages` เท่านั้น — **ห้ามเดา** · ส่งตัวที่ไม่ได้ผูก = `AD_ACCOUNT_NOT_ALLOWED` / `PAGE_NOT_ALLOWED` (ไม่ fallback เงียบ) ·
> user มีหลายบัญชีแล้วไม่ระบุ → ถามก่อนตามขั้น 0 (ห้ามเลือกให้เอง) แล้วบอกชื่อบัญชีที่ใช้ในหัวรายงาน (คำตอบแนบ `ad_account {id,name,source}` — `source: requested` = มาจากที่ส่ง · ยกเว้น `get_job` · `get_dashboard_demographics` แนบตั้งแต่ MCP 1.23.2) · ส่ง `ad_account_id` ให้ tool ใด ต้องส่งค่าเดียวกันให้ `get_account_info` ด้วย และเรียก `get_account_info` ใหม่เมื่อเปลี่ยนบัญชี (สกุลเงิน/โซนเวลาเป็นของบัญชีนั้น)
>
> **ตั้งค่าบัญชี/เพจได้ที่หน้าเว็บ MaxxGPT เท่านั้น** — MCP เชื่อมต่อ Meta, ผูก, ถอด หรือเปลี่ยนบัญชี/เพจที่เลือกไว้ให้ไม่ได้ (`ad_account_id` / `page_id` ใช้แค่ครั้งนั้น ไม่เปลี่ยนค่าในเว็บ) · ยังไม่ผูกบัญชี · ผูกเกินโควตา · หรือ user ต้องการบัญชีที่ไม่อยู่ใน `list_ad_accounts` → บอกให้ไปทำในเว็บ MaxxGPT (เมนู ☰ → บัญชีโฆษณาและเพจ) แล้วค่อยกลับมาสั่งใหม่ · **ห้ามบอกว่าจะผูกหรือตั้งค่าให้**
>
> **รหัสที่ต้องรู้จัก (V4):** `NO_AD_ACCOUNT` (428) = ยังไม่ต่อ Meta / ยังไม่เลือกบัญชี → ให้ user เปิดเว็บ MaxxGPT ต่อ Meta แล้วเลือกบัญชี ·
> `reason: OVER_QUOTA` = ผูกบัญชีโฆษณาหรือเพจเกินโควตาแพ็กเกจ (`ad_account_quota.over_quota` / `page_quota.over_quota`) → ให้ไปกด "จัดการบัญชี" ในเว็บเลือกตัวที่จะเก็บก่อน **อย่า retry** ·
> `NOT_ENTITLED` (403) = แพ็กเกจไม่รวมฟีเจอร์ (tool ที่สกิลนี้ใช้ยังไม่มีตัวไหนตอบรหัสนี้) · `SUBSCRIPTION_EXPIRED` (403) = แพ็กเกจหมดอายุ → ให้ต่ออายุในเว็บ MaxxGPT (ล็อกอินใหม่ไม่ช่วย) · `NO_SESSION` / `USER_NOT_FOUND` (401) = connector ไม่รู้จักผู้ใช้ → ให้เชื่อมต่อ connector MaxxGPT ใหม่ · `JOB_RUNNING_FOR_OTHER_ACCOUNT` = งานชนิดเดียวกันกำลังรันให้อีกบัญชีของ user นี้ รอจบก่อน · `JOB_NOT_FOUND` = `job_id` ไม่ใช่ของ user นี้

---

## ⚡ ทางลัด · มี `job_id` มาแล้ว = ข้ามไปต่อจากตรงนั้นเลย

**ถ้าข้อความของ user มี `job_id` ติดมา ให้ข้ามการยิง tool ของสเต็ปนั้นไปเลย** — สกิลนี้เป็นงาน 2 สเต็ป
job หนึ่งใบเป็นได้ทั้งสเต็ป 1 และสเต็ป 2 → **ต้องดูจาก `function_name` (หรือ `data`) ก่อนว่าเป็นใบไหน**

**นับว่า "มี job_id" เมื่อ:** user พิมพ์/วางมาตรง ๆ (`job_id=…` · `[job_id=…]` · "ดูผลจากจ็อบ …" ·
วาง id ดิบ ๆ มาพร้อมบอกให้วิเคราะห์) · สกิลอื่นหรือเทิร์นก่อนหน้าส่งต่อมาให้ · งานตั้งเวลา/ระบบภายนอกแนบมา

### ทำตามนี้

1. **`get_job(job_id)` ทันที** — `processing` ก็ poll ต่อตามปกติ (`data` อาจเป็นสตริง JSON → parse ก่อน)
2. **`get_account_info`** ยังต้องเรียก (1 ครั้งต่อ session ต่อบัญชี) เพื่อเอาสกุลเงิน + ชื่อบัญชีไปใส่หัวเรื่อง
3. **ดูว่าเป็น job ของสเต็ปไหน:**

| `function_name` / `data` หน้าตาแบบนี้ | คือ | ทำต่อยังไง |
|---|---|---|
| `resultOverAll` · มีคีย์ `OV` | **สเต็ป 1 · overview** | ข้ามขั้น 2 ไปทำ **ขั้น 3** เลย — สรุป `OV` แล้วให้ user เลือก `Result_indicator` |
| `CtrCpmFrq` · มีบล็อก `CTR` `CTR_LINK_CLICK` `Engagement_Rate` `CPM` `FRQ` `Cost_Per_Result` + คู่ `*_AD` | **สเต็ป 2 · metrics** | ข้ามขั้น 2-4 ไปทำ **ขั้น 5** เลย — แสดงตารางเทียบระดับ |
| ไม่ใช่ทั้งสองแบบ | เป็นของสกิลอื่น | ห้ามฝืนแปลง ชี้สกิลที่ตรงจากตารางข้างล่าง |

4. 🔴 **ได้ job สเต็ป 1 มาแล้วจะยิงสเต็ป 2 ต่อ — ต้องรู้ช่วงวันที่ก่อน**
   `ad_benchmark_metrics` **ต้องใช้ช่วงวันเดียวกับ overview** แต่ `get_job` ไม่ได้บอกช่วงมาด้วย →
   **ห้ามเดาช่วงวัน** · user ไม่ได้บอกมา = **ถามก่อนยิงสเต็ป 2** (ยิงด้วยช่วงผิด = ได้ตัวเลขคนละชุดโดยไม่มีใครรู้)
5. **ได้ job สเต็ป 2 มา — `indicator` ก็ไม่ได้ติดมาเหมือนกัน** → เขียนใน `note` ว่าไม่ทราบว่าเทียบจาก
   result indicator ตัวไหนและช่วงวันไหน **ห้ามเดา** · user บอกมาก็ใส่ตามนั้น
6. **ช่วงวันที่และบัญชีของ job: `get_job` ไม่ได้คืนมาด้วย** — 🔴 **ห้ามเดา ห้ามใส่ช่วงมั่ว ๆ ในหัวเรื่อง**
   · user บอกช่วงมาด้วย = ใช้ตามนั้น · ไม่บอก = เว้นช่วงวันที่ในหัวเรื่องไว้ แล้วเขียนในหมายเหตุว่า
   "ผลชุดนี้มาจาก job ที่ส่งมา — ระบบไม่ได้แนบช่วงวันที่มาด้วย" ·
   ชื่อบัญชีในหัวเรื่องคือบัญชีจาก `get_account_info` ตอนนี้ — เขียนในหมายเหตุด้วยว่า **ไม่ยืนยันว่า job นี้รันกับบัญชีนั้น**
7. `code: JOB_NOT_FOUND` = **job_id ผิด เป็นของ user คนอื่น หรือเป็น job_id จากระบบเดิมก่อน V4** (job ผูกกับ login) →
   บอกตรง ๆ แล้วเสนอรันใหม่ตามขั้น 1-2 ปกติ · **ห้าม poll ซ้ำ** (`poll_hint.poll_after_seconds` = 0)
8. `job_status: failed` = งานเก่าล้มไปแล้ว → อ่าน `data.error` (ดู "งานล้ม / error" ในขั้น 2) ก่อนเสนอรันใหม่ · `OV` เป็น `[]` หรือ `*_AD` ว่างทุกตาราง = ช่วงนั้นไม่มีข้อมูล ไม่ใช่ error ·
   `job_status: success` แต่ `data` เป็น `null` = ผลหมดอายุแล้ว (ระบบเก็บผล 7 วัน) → เสนอรันใหม่

### ตารางลายเซ็น — job_id นี้เป็นของหัวข้อไหน

**ดู `function_name` ก่อนเสมอ** — `get_job` คืนค่านี้มาด้วย และใช้ได้แม้ `data` เป็น `{}`

| `function_name` | หัวข้อ | สกิลที่ควรใช้ |
|---|---|---|
| `badInbox` · `badLead` · `badPurchase` | Bottom Rank (วัดด้วย inbox / lead / purchase) | `maxxgpt-rank-bottom-ads` |
| `topStar` | Rising Stars | `maxxgpt-rank-rising-stars` |
| `topAware` | Audience Growth | `maxxgpt-rank-audience-growth` |
| `goodInbox` · `goodLead` · `goodPurchase` · `goodROAS` | Top Rank (วัดด้วย inbox / lead / purchase / roas) | `maxxgpt-rank-top-ads` |
| `videoAdsAnalysis` | โฆษณาวิดีโอ | `maxxgpt-analysis-video-ads` |
| `postEngagement` | เอนเกจโพสต์ | `maxxgpt-analysis-post-engagement` |
| `messageAnalysis` | ทักแชท | `maxxgpt-analysis-message` |
| `leadAdsAnalysis` | ลีด | `maxxgpt-analysis-leads` |
| `purchaseAnalysisMETA` | ยอดซื้อ Meta | `maxxgpt-analysis-purchase-meta` |
| `purchaseAnalysisCPAS` | ยอดซื้อ CPAS | `maxxgpt-analysis-purchase-cpas` |
| `resultOverAll` | Ad Metric Benchmark (สเต็ป 1) | `maxxgpt-ad-metric-benchmark` |
| `CtrCpmFrq` | Ad Metric Benchmark (สเต็ป 2) | `maxxgpt-ad-metric-benchmark` |
| `exportAds` | รายงานโฆษณาแบบดิบ | `maxxgpt-export-report` |
| `recomendedDashboard` | Ad Spotlight (ผลจริงอ่านจาก `spotlight_get`) | `maxxgpt-ad-spotlight` |

**ไม่มี `function_name` ในคำตอบ** = ใช้ลายเซ็นใน `data` แทน:

| ลายเซ็นใน `data` | หัวข้อ | สกิลที่ควรใช้ |
|---|---|---|
| `Ad` เป็น **object** `{Close,Watch,Keep}` | Bottom Rank | `maxxgpt-rank-bottom-ads` |
| แถวมี `Score` + `CPC` · **ไม่มี `CPM`** และไม่มีคอลัมน์ผลลัพธ์ | Rising Stars | `maxxgpt-rank-rising-stars` |
| แถวมี `Score` + `Reach` + `Frequency` + `CPM` + `CPC` | Audience Growth | `maxxgpt-rank-audience-growth` |
| แถวมี `Score` + `CPM` · ไม่มี `Reach`/`CPC` (`Cost_per_*` `per` ตัวเล็ก มีเฉพาะเมตริก inbox / lead) | Top Rank | `maxxgpt-rank-top-ads` |
| แถวมี `Video_plays` + `Completion_Rate` | โฆษณาวิดีโอ | `maxxgpt-analysis-video-ads` |
| แถวมี `Post_Engagement` + `post_engagement_rate` | เอนเกจโพสต์ | `maxxgpt-analysis-post-engagement` |
| แถวมี `Inbox` + `MSS_VIEW` + `Cost_Per_Inbox` (`Per` ตัวใหญ่) | ทักแชท | `maxxgpt-analysis-message` |
| แถวมี `Lead` + `Cost_per_lead` | ลีด | `maxxgpt-analysis-leads` |
| แถวมี `Purchase`/`Purchase_Value`/`ROAS` **และ** มีคีย์ `Age`/`Gender` | ยอดซื้อ Meta | `maxxgpt-analysis-purchase-meta` |
| แถวมี `Purchase`/`Purchase_Value`/`ROAS` **แต่ไม่มี** คีย์ `Age`/`Gender` และไม่มี `Score` | ยอดซื้อ CPAS | `maxxgpt-analysis-purchase-cpas` |
| `data` มีคีย์ `OV` | Ad Metric Benchmark (สเต็ป 1) | `maxxgpt-ad-metric-benchmark` |
| `data` มีบล็อก `CTR`/`CPM`/`FRQ` + `*_AD` | Ad Metric Benchmark (สเต็ป 2) | `maxxgpt-ad-metric-benchmark` |

⚠️ `purchase_meta` กับ `purchase_cpas` คอลัมน์เหมือนกันเป๊ะ ถ้าไม่มี `function_name` จะแยกได้แค่จากคีย์ `Age`/`Gender` —
**ถ้าไม่มั่นใจให้บอก user ตรง ๆ ว่าเดาว่าเป็นหัวข้อไหน แล้วให้ยืนยัน** อย่าเงียบแล้วเดา

---

## ผังการทำงาน · Flow

```
0  list_ad_accounts → get_account_info ──► ชื่อบัญชี + สกุลเงิน + โซนเวลา (ครั้งเดียวต่อ session ต่อบัญชี)
1  ถามเลือกช่วงเวลา ด้วย AskUserQuestion  ◄── ข้ามได้ถ้า user บอกช่วงมาแล้ว
2  ad_benchmark_overview(date_start,date_end) → job_id → poll get_job จน success
3  พิมพ์ตารางภาพรวม + ถาม Result indicator ด้วย AskUserQuestion
4  ad_benchmark_metrics(date_start,date_end,indicator) → job_id → poll get_job จน success
5  พิมพ์ตารางเทียบระดับ 6 เมตริก (markdown)   ──►  อยู่ต่อเพื่อตอบคำถาม
```

### ขั้น 0 · รู้ก่อนว่าบัญชีไหน

**0.1 · `list_ad_accounts`** (ครั้งแรกของ session · อ่านจากฐานข้อมูล MaxxGPT ไม่ยิง Meta) — ได้ทุกบัญชีที่ user ผูกไว้ (`ad_accounts[]` · `is_active` = ตัวที่เลือกไว้ในเว็บ) + `active_ad_account_id` + `ad_account_quota`

| เจอแบบนี้ | ทำอย่างนี้ |
|---|---|
| `ad_accounts` ว่าง หรือ `ad_account_quota.over_quota: true` | บอก user ให้ไปตั้งที่เว็บ MaxxGPT (ยังไม่ผูก = เชื่อมต่อ Meta แล้วเลือกบัญชี · เกินโควตา = เลือกบัญชีที่จะเก็บ) แล้ว**หยุด** — MCP ทำแทนไม่ได้ |
| user บอกบัญชีมาแล้ว (ชื่อหรือเลข) | จับคู่กับรายการ · ไม่เจอ = บอกว่าบัญชีนั้นยังไม่ได้ผูกใน MaxxGPT ให้ไปผูกที่เว็บก่อน · **ห้ามใช้บัญชีอื่นแทนเงียบ ๆ** |
| มีบัญชีเดียว | ใช้บัญชีนั้น ไม่ต้องถาม |
| หลายบัญชี และ user ไม่ได้ระบุ | ถามด้วย `AskUserQuestion` (รวมกับคำถามของขั้น 1 ได้) · ตัวเลือก = ชื่อบัญชี + `act_…` · ตัวที่ `is_active` อยู่บนสุด ติดว่า "(ที่เลือกไว้ในเว็บ)" · เกิน 4 บัญชี = ใส่ 3 ตัวแรก ที่เหลือให้พิมพ์ใน Other · ไม่มี `AskUserQuestion` = พิมพ์รายการเป็นเลขข้อให้ตอบ |
| connector ไม่มี `list_ad_accounts` (MaxxGPT รุ่นก่อน V4) | ข้าม 0.1 ใช้บัญชีที่เลือกไว้ในเว็บ ไม่ส่ง `ad_account_id` |

บัญชีที่ได้คือ `ad_account_id` ของงานนี้ — **ส่งค่าเดียวกันให้ทุก tool ของ MaxxGPT ในสกิลนี้** (ยกเว้น `get_job`) · ไม่เปลี่ยนบัญชีที่เลือกไว้ในเว็บ · user ขอเปลี่ยนบัญชีกลางทาง = ทำ 0.2 ใหม่ด้วยบัญชีนั้น

**0.2 · `get_account_info`** พร้อม `ad_account_id` จาก 0.1 — เรียก**หนึ่งครั้งต่อ session ต่อบัญชี** เก็บ ชื่อบัญชี / `act_…` / สกุลเงิน / โซนเวลา ไว้ใช้ทุกขั้น
(แมป `ad_account.timezone_name` → `timezone`, `account_status` เป็นตัวเลข `1`=ใช้งานได้ · `null` = MaxxGPT ยังไม่เคยอ่านจาก Meta · สองค่านี้คือค่าที่ MaxxGPT อ่านจาก Meta ล่าสุด ณ `ad_account.synced_at` · เหมือนสกิล analysis)
โซนเวลาใช้คำนวณ **"วันนี้"** ตอนแปลงคำพูดเป็นช่วงวันที่ — หาไม่เจอใช้ `Asia/Bangkok` ·
สกุลเงินใช้ต่อท้ายตัวเลขเงินทุกตัว — หาไม่เจอเว้นว่าง **ห้ามเดาว่าเป็น THB**

### ขั้น 1 · เลือกช่วงเวลา

**ถ้า user บอกช่วงมาครบแล้ว ไม่ต้องถาม ยิง overview เลย** — บอกหนึ่งบรรทัดว่าใช้ช่วงไหน

**ถามยังไง — ใช้ tool `AskUserQuestion` (ปุ่มตัวเลือก) เสมอ · ห้ามสร้าง widget/ฟอร์ม HTML · ห้ามพิมพ์คำถามเปล่า ๆ:**
สเปกคำถาม/ตัวเลือกอยู่ใน [references/output-format.md](references/output-format.md) § ถาม — **ถามทุกอย่างที่ยังไม่รู้ในการเรียกครั้งเดียว** ·
ที่รู้แล้วห้ามถามซ้ำ · user กด "Other" พิมพ์ช่วงเองได้ → แปลงเป็นวันที่ตามตารางในไฟล์นั้น

### ขั้น 2 · ยิง overview

`ad_benchmark_overview(date_start, date_end)` (วันที่ `YYYY-MM-DD` ตามโซนเวลาบัญชี · `date_start ≤ date_end`)
→ ได้ `{ job_id, code }` · **`code`:**

| `code` | หมายถึง | ทำอะไรต่อ |
|---|---|---|
| `JOB_CREATED` | เริ่มงานใหม่แล้ว | poll ตามปกติ |
| `JOB_ALREADY_RUNNING` | **มีงาน overview ค้างอยู่ — `job_id` เป็นของงานเก่า (ช่วงวันเก่า)** | poll ต่อได้ แต่บอก user ตรง ๆ ว่าผลเป็นของช่วงก่อน แล้วเสนอรันใหม่หลังงานเก่าจบ |

**งานล้ม / error (ใช้กับทั้ง 2 สเต็ป):**

- `failed` + `data = {"error":"time_out"}` → เกินเพดานเวลา 5 นาที **ห้ามยิงซ้ำทันที**: บอก user ว่าช่วงที่ขอหนักไป แล้วเสนอย่นช่วงวันก่อนรันใหม่
- `failed` ที่ `data.error` เป็นค่าอื่น → **อย่ารันซ้ำเฉย ๆ** ให้อ่านรหัสก่อน: `META_TOKEN_INVALID` = การเชื่อมต่อ Meta หมดอายุ/ถูกยกเลิก →
  ให้ user ต่อ Meta ใหม่ในเว็บ MaxxGPT (รันซ้ำไม่ช่วย) · `META_RATE_LIMITED` = Meta จำกัดคำขอชั่วคราว รอ 2-3 นาทีแล้วค่อยรันใหม่ ·
  `META_PERMISSION_DENIED` = บัญชีที่ต่อไว้ไม่มีสิทธิ์ในบัญชีโฆษณานี้ · รหัสอื่น (`META_ERROR` ฯลฯ) = บอก `data.message` แล้วเสนอรันใหม่
- tool ตอบ error แทน `job_id` → อ่าน `code` ตามกล่อง "รหัสที่ต้องรู้จัก (V4)" ข้างบน · วันที่ผิดรูป (ไม่ใช่ `YYYY-MM-DD`) ถูกปฏิเสธตั้งแต่ตอนเรียก tool
- ได้ข้อความ `Rate limit reached …` → รอตามจำนวนวินาทีที่ข้อความบอก แล้วทำต่อเอง **ห้ามจบ turn** (เริ่มงานได้ 60 ครั้ง/ชั่วโมงต่อ tool)

### ขั้น 3 · poll แล้วให้เลือก Result indicator

`get_job(job_id)` จน `job_status = success` (ตาม `poll_hint` · `data` อาจเป็นสตริง JSON → parse ก่อน) ·
อ่าน `data = { OV }` (โครงสร้างเต็ม: [references/output-shape.md](references/output-shape.md))

**`OV` = 1 แถวต่อ (Objective × Result indicator)** พร้อม Result / Spend / CTR / CPM / FRQ / Cost per result ·
`OV` เป็น `[]` = ช่วงนั้นไม่มีโฆษณาที่มี impression → บอก user แล้วเสนอช่วงอื่น (ไม่ต้องไปสเต็ป 2)

1. **พิมพ์ตาราง `OV` ให้ user เห็นตัวเลขก่อน** (ทุกแถว ปกติมีไม่กี่แถว) แล้ว**ถามด้วย `AskUserQuestion`
   ว่าจะเจาะ Result indicator ตัวไหน** — `label` = ชื่ออ่านง่าย · `description` = Objective + Result + Spend ของแถวนั้น
   (สเปกเต็มใน [references/output-format.md](references/output-format.md) § ถาม)
2. **แต่ค่าที่ส่งเข้า tool ต้องเป็นสตริงดิบเป๊ะ ๆ ที่ `OV` ส่งมา** เช่น `actions:onsite_conversion.messaging_conversation_started_7d`
   — เก็บ mapping ชื่ออ่านง่าย ↔ ค่าดิบไว้เอง · ห้ามพิมพ์ใหม่/ย่อตอนส่งเข้า tool
3. ถ้า user พิมพ์เลือกเองเป็นภาษาคน ("เอาตัวทักแชท") → จับคู่กับ `Result_indicator` ที่มีจริงใน `OV` แล้วใช้ค่าดิบตัวนั้น
4. มี Result indicator เดียว → ข้ามการถาม ยิง step 2 ต่อได้เลย บอกหนึ่งบรรทัดว่าเจาะตัวไหน

### ขั้น 4 · ยิง metrics

`ad_benchmark_metrics(date_start, date_end, indicator)` — **ช่วงวันเดิมกับ overview** · `indicator` = ค่าดิบที่เลือก
→ `{ job_id, code }` (code แบบเดียวกับข้างบน) · เกณฑ์ปลายทาง: เอาเฉพาะ ad ที่ตรง indicator และ **impression ≥ 1000** ·
ไม่มีตัวไหนผ่าน = `*_AD` ว่างทุกตาราง และคีย์สรุป `Count` = 0 ทุกระดับ (ไม่ใช่ error)

### ขั้น 5 · poll แล้วแสดงตารางเทียบระดับ

`get_job` จน success · อ่าน `data` ที่มี **6 คู่เมตริก** — แต่ละคู่ = สรุประดับ + ตารางรายโฆษณา:

| เมตริก | คีย์สรุป | คีย์รายโฆษณา | ทิศทาง "ดี" |
|---|---|---|---|
| CTR (%) | `CTR` | `CTR_AD` | สูง = ดี |
| CTR ลิงก์คลิก (%) | `CTR_LINK_CLICK` | `CTR_LINK_CLICK_AD` | สูง = ดี |
| Engagement rate (%) | `Engagement_Rate` | `Engagement_Rate_AD` | สูง = ดี |
| CPM | `CPM` | `CPM_AD` | **ต่ำ = ดี** |
| Frequency | `FRQ` | `FRQ_AD` | **ต่ำ = ดี (ยิ่งสูงยิ่งเสี่ยงคนเบื่อ)** |
| Cost per result | `Cost_Per_Result` | `Cost_Per_Result_AD` | **ต่ำ = ดี** |

พิมพ์ผลตาม [references/output-format.md](references/output-format.md) § ตอบ — **6 ตาราง (เมตริกละตาราง,
รายโฆษณา, ตัดเหลือ 10 แถว)** · สรุปรวม = การกระจายระดับ (High/Medium/Low นับกี่ตัว) จากคีย์สรุป

---

## § ตัดข้อมูลก่อนพิมพ์ตาราง (ห้ามข้าม)

| ส่วน | ใส่อะไร |
|---|---|
| หน้า **overview (ให้เลือก)** · ตาราง | 1 ตาราง `OV` ครบทุกแถว (ปกติไม่กี่แถว) คอลัมน์: Objective · Result indicator · Result · Spend · CTR · CPM · FRQ · Cost/result |
| หน้า **overview** · คำถามปิดท้าย | ลิสต์ Result indicator ที่ไม่ซ้ำเป็นข้อ ๆ ให้เลือก (+ บอกว่าเปลี่ยนช่วงเวลาได้) |
| หน้า **ผลเทียบระดับ** · ตาราง | 6 ตาราง (เมตริกละตาราง) · **แต่ละตารางเอา 10 แถวแรก** — เรียงมาให้แล้วตามค่าเมตริกมาก→น้อย (= High → Medium → Low) · ตัดออกให้เขียนใต้ตารางว่า "แสดง 10 จาก N" |
| หน้า **ผลเทียบระดับ** · คอลัมน์ต่อตาราง | Ad Name · Spend · Result · เมตริกนั้น · **Level ของเมตริกนั้น** (5 คอลัมน์พอ) |
| สรุปรวม | การกระจายระดับของเมตริกหลัก เช่น "CTR: High 4 · Med 9 · Low 6" (จากคีย์สรุป `CTR` = `{level,Count,Min,Max}`) |

**ค่าในสรุปรวมมาจากคีย์สรุป** (`CTR`,`FRQ`,…) โดยตรง — แต่ละแถวคือ `{ level, Count, Min, Max }` ต่อระดับ ·
`Min`/`Max` = ช่วงค่าจริงของระดับนั้น (เขียนกำกับได้ เช่น "High: 2.1%–5.8%")

---

## ข้อควรระวังเรื่องตัวเลข (คีย์สะกดตามปลายทางเป๊ะ ๆ)

- 🔴 **`Impresstion` สะกดผิดแบบนี้จริงในข้อมูล overview** — ใช้ตามที่ปลายทางส่งมา อย่า "แก้" เป็น `Impression`
- **`CTR` / `CTR_LINK_CLICK` / `Engagement rate(%)` เป็นเปอร์เซ็นต์อยู่แล้ว** (เช่น `1.84` = 1.84%) → พิมพ์ต่อท้ายด้วย `%` **ห้ามคูณ 100 ซ้ำ**
- **`FRQ` เป็นจำนวนเท่า** (impression ÷ reach) → พิมพ์เป็นตัวเลข (ใส่ลูกน้ำ) · **`CPM` / Cost per result เป็นเงิน** → พิมพ์เป็นจำนวนเงิน 2 ตำแหน่ง + สกุลเงิน
- **หน่วยเงินเป็นหน่วยปกติแล้ว (ไม่ใช่สตางค์)** — ใช้ตามที่ได้มา ห้ามคูณ/หาร 100
- 🔴 **Cost per result / CPM = `0` มักแปลว่า "ไม่มีผล/ไม่มี impression พอ" ไม่ใช่ "ถูก"** — ตัดแถวที่ผลหลัก = 0
  ออกก่อนสรุปว่า "ตัวไหนถูกสุด" เสมอ
- **`Level of <metric>` มีค่า `High` / `Medium` / `Low` / `N/A`** — `N/A` = คำนวณระดับไม่ได้ (ค่าใช้ไม่ได้) ไม่ใช่ "แย่"
- **ระดับคำนวณจาก mean ± ส่วนเบี่ยงเบนมาตรฐานของบัญชีนี้เอง** → บัญชีที่ ad น้อยมาก ระดับจะไม่ค่อยมีความหมาย
  บอก user ตรง ๆ ถ้าเห็นว่าตัวอย่างน้อย

---

## หลังแสดงผล — อยู่ต่อเพื่อตอบคำถาม

หลังพิมพ์ตาราง **เขียนสรุปสั้น ๆ 2-4 บรรทัด** (เมตริกไหนน่าห่วง เช่น "มี ad frequency ระดับ High อยู่ 3 ตัว —
คนเริ่มเห็นซ้ำถี่") แล้วบอกว่าถามต่อได้ — **อย่าเทข้อมูลดิบซ้ำลงในแชท**

ตอบจาก **ข้อมูลชุดเดิม** ห้ามยิง tool ซ้ำ เว้นแต่:

| user ขอ | ทำอะไร |
|---|---|
| ตัวเลข/อันดับ/เจาะ ad ตัวใดตัวหนึ่ง/ตารางเต็ม | ตอบจากข้อมูลเดิม **ไม่ต้องยิงใหม่** |
| เปลี่ยน Result indicator (ช่วงเดิม) | ยิง `ad_benchmark_metrics` ด้วย indicator ใหม่ (ไม่ต้องยิง overview ซ้ำ ถ้าภาพรวมเดิมยังอยู่) |
| เปลี่ยนช่วงเวลา | เริ่มใหม่จาก `ad_benchmark_overview` ด้วยช่วงใหม่ |

ขอตารางเต็ม = พิมพ์ทุกแถวเป็น markdown ในแชท · ยาวมากให้แบ่งตามเมตริก แล้วถามว่าดูตัวไหนก่อน
