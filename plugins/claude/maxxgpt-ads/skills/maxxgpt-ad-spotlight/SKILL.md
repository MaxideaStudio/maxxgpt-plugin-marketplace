---
name: maxxgpt-ad-spotlight
description: >-
  แสดง "โฆษณาแนะนำ" (Ad Spotlight) ของบัญชี Meta (Facebook/Instagram) ที่ผูกกับ MaxxGPT —
  ระบบคัดมาให้อัตโนมัติทุกคืน แล้วสรุปเป็นแดชบอร์ด 3 ช่วงเวลา (เมื่อวาน / 3 วันก่อน / 7 วันก่อน)
  แต่ละช่วงมี: โฆษณาที่ควรปิด · โฆษณาที่ควรผลักดัน (แยกยอดซื้อ/ทักแชท) · ครีเอทีฟที่โดดเด่น
  (แยก CTR/ทักแชท/ยอดซื้อ) — คัดเฉพาะโฆษณาที่ใช้จ่าย ≥ 350 ให้แล้วจากหลังบ้าน.
  ถ้าบัญชียังไม่เคยรัน สั่งรันสด (async) ให้ได้. Show the account's auto-picked "spotlight" ads
  as a dashboard. ใช้ skill นี้ทุกครั้งที่ผู้ใช้พูดถึง: โฆษณาแนะนำ / ad spotlight / สปอตไลต์ /
  ตัวไหนน่าสนใจ / ตัวไหนควรปิดควรดัน (ภาพรวมเร็ว) / ครีเอทีฟเด่น / โฆษณาเด่นคืนนี้ —
  แม้ผู้ใช้จะไม่พูดคำว่า "skill" ตรงๆ. (ต้องมี connector MaxxGPT)
---

# MaxxGPT — Ad Spotlight (โฆษณาแนะนำ)

พา user จาก "มีแอดตัวไหนน่าสนใจบ้าง" ไปเป็น **แดชบอร์ดโฆษณาแนะนำ** ของบัญชีที่ผูกกับ MaxxGPT —
คัดมาให้อัตโนมัติทุกคืน — แล้วอยู่ต่อเพื่อตอบคำถามเจาะลึกจากข้อมูลชุดเดียวกัน.

> ## 🔴 กฎเหล็ก (อ่านก่อนเริ่มทุกครั้ง)
>
> 1. **เรียก MCP tool ทีละตัว ห้ามยิงขนาน** — ยิงพร้อมกันจะได้ error `The connector's server
>    isn't responding.` ที่ดูเหมือน server พังทั้งที่ไม่ใช่ · เจอ error นี้ให้สงสัยวิธีเรียกของตัวเองก่อน
> 2. **ตัวเลขทุกตัวต้องมาจาก `data` จริงเท่านั้น** — **อ่านชื่อคอลัมน์จาก `fields` ของ section นั้น ๆ**
>    (Inbox กับ Purchase คอลัมน์ไม่เหมือนกัน — ดู output-shape.md) · คีย์ไหนไม่มีก็ตัดคอลัมน์นั้นทิ้ง
>    ห้ามเดา ห้ามคำนวณเมตริกใหม่ที่ปลายทางไม่ได้ให้
> 3. **การจัด "ควรปิด (Bad) / ควรผลักดัน (Good)" เป็นของปลายทาง ห้ามตัดสินเอง** —
>    เราแสดงตามถังที่ระบบจัดมา · **สกิลนี้ไม่ปิดโฆษณา ไม่แก้งบให้** ได้แค่แสดง
> 4. **ห้ามเทข้อมูลดิบทั้งก้อนลงแชท** — เอา **6 แถวแรก/ถัง** (`Good` / `Content_*` เรียงมาแล้ว อย่าเรียงใหม่ · `Bad` ไม่ได้เรียง ให้เรียงเองตาม `Spend` มาก→น้อย) ·
>    ข้อมูลเต็มยังอยู่กับเราไว้ตอบคำถามต่อ
> 5. 🔴 **`ad_name` ที่เป็น `"รวม"` คือ *ชื่อโฆษณาจริง* (มี ad_id/post_url/รูปของตัวเอง) ไม่ใช่ยอดรวม** —
>    **แสดงและนับตามปกติ ห้ามตัดทิ้ง** (เว็บจริงนับรวมมันด้วย — ตัดออก = จำนวนรายการไม่ตรงกับเว็บ)
> 6. **ห้ามสร้าง widget / ฟอร์ม HTML / การ์ด UI เด็ดขาด** — ห้ามเรียก tool แสดงวิชวลทุกตัว
>    (`visualize` · `show_widget` · `render-ui` · Artifact) และ**ห้ามเขียน HTML/ฟอร์มเอง**
>    ถามด้วย **tool `AskUserQuestion` (ปุ่มตัวเลือก)** เท่านั้น · เรียกไม่ได้จริง ๆ =
>    **ถามเป็นข้อความแบบเลขข้อ (1 / 2 / 3) แล้วหยุดรอ user ตอบ** ห้ามเดาเองแล้วยิงต่อ

## Connector ที่ต้องมี · Required connector

| Connector | URL | ใช้ทำอะไร |
|---|---|---|
| **MaxxGPT** | `https://mcp.maxxgpt.ai/mcp` | `get_account_info` · `spotlight_get` · `spotlight_run` · `get_job` |

> ### 🔁 เจอ connector ที่ชี้ไปโดเมนเก่า
> `https://mcp-beta.maxxgpt.ai/mcp` เป็น**โดเมนเดิม ใช้แก้ขัดได้** — เจอ connector ของ user ตั้งไว้แบบนั้น
> **ทำงานต่อได้ตามปกติ ห้ามหยุดงานเพื่อให้เขาไปเปลี่ยนก่อน** ·
> แต่ให้บอกหนึ่งบรรทัดตอนจบว่าโดเมนหลักคือ `https://mcp.maxxgpt.ai/mcp` และแนะนำให้ย้าย ·
> **บอกครั้งเดียวต่อ session พอ อย่าทวงซ้ำทุกรอบ**

ไม่มี connector นี้ = แจ้ง user พร้อม URL แล้วหยุด · **ชื่อ tool อาจไม่ตรงเป๊ะ** → จับคู่จาก
*ความสามารถ* ไม่ใช่ชื่อเป๊ะ ๆ.

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

## ⚡ ทางลัด · มี `job_id` มาแล้ว

**ถ้าข้อความของ user มี `job_id` ของ `spotlight_run` ติดมา ให้ข้ามการยิง `spotlight_run` ใหม่**
(ยิงซ้ำจะได้ `JOB_ALREADY_RUNNING` อยู่ดี)

**นับว่า "มี job_id" เมื่อ:** user พิมพ์/วางมาตรง ๆ (`job_id=…` · `[job_id=…]` · "ดูผลจากจ็อบ …" ·
วาง id ดิบ ๆ มาพร้อมบอกให้วิเคราะห์) · สกิลอื่นหรือเทิร์นก่อนหน้าส่งต่อมาให้ · งานตั้งเวลา/ระบบภายนอกแนบมา

### 🔴 หัวข้อนี้ต่างจากสกิลวิเคราะห์ตัวอื่น: ผลที่ใช้แสดง **ไม่ได้อ่านจาก `get_job`**

```
job_id ที่ได้มา ──► get_job(job_id) ──► poll จน success ──► spotlight_get ──► ตัด+แสดงผล
```

1. **`get_job(job_id)`** แล้ว poll ตาม `poll_hint.poll_after_seconds` จน `job_status:"success"`
   **ห้ามจบ turn ระหว่างรอ**
2. **จบแล้วต้องเรียก `spotlight_get` เพื่ออ่านผล** — `data` ของ `get_job` ตัวนี้คือผลดิบก้อนใหญ่ที่ยังไม่ได้ trim
   (ตาราง 2 มิติ มีลิงก์รูป/พรีวิวยาว ๆ ติดมา) **ห้ามอ่านผลสปอตไลต์จาก `get_job`** ให้ใช้ `spotlight_get` ที่ trim แล้วเท่านั้น
3. **`get_account_info`** ยังต้องเรียก (1 ครั้งต่อ session ต่อบัญชี) เพื่อเอาสกุลเงิน + สถานะบัญชี
4. `code: JOB_NOT_FOUND` = job_id ผิดหรือเป็นของ user คนอื่น → **ห้าม poll ซ้ำ** ·
   ลอง `spotlight_get` ตรง ๆ ดูก่อน (บัญชีอาจมีผลของรอบกลางคืนอยู่แล้ว) ถ้าไม่มีค่อยเสนอรันสดใหม่
5. `job_status: failed` = งานเก่าตายแล้ว → `spotlight_get` ดูว่ามีผลเก่าไหม ไม่มีค่อยเสนอรันใหม่
6. **ถ้า job_id ที่ส่งมาไม่ใช่ของ spotlight** (`function_name` ไม่ใช่ `recomendedDashboard`) =
   เป็นผลของสกิลวิเคราะห์ตัวอื่น → ชี้สกิลที่ตรงจากตารางข้างล่าง **ห้ามฝืนแปลงเป็นสปอตไลต์**

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
0  list_ad_accounts → get_account_info ──► ชื่อบัญชี + สกุลเงิน (ไว้จัดรูปเงิน) + สถานะ
1  spotlight_get (sync) ──► { success, data:{1d,3d,7d,Last_Update}, as_of, run_date, ad_account }
     └─ ถ้า FUNCTION_NOT_RUN → spotlight_run (async) → poll get_job จนจบ → spotlight_get ซ้ำ
2  ตัดข้อมูล (6 แถว/ถัง) + คำนวณสรุป
3  พิมพ์สรุป + ตาราง markdown ──►  อยู่ต่อเพื่อตอบคำถามจากข้อมูลชุดเดิม
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

**0.2 · `get_account_info`** พร้อม `ad_account_id` จาก 0.1 — เรียก**หนึ่งครั้งต่อ session ต่อบัญชี** เก็บ ชื่อบัญชี / สกุลเงิน / สถานะ.
- สกุลเงิน → ใช้ต่อท้ายตัวเลขเงินทุกตัว (หาไม่เจอเว้นว่าง **ห้ามเดาว่า THB**)
- สถานะบัญชีไม่ ACTIVE (`account_status` ≠ `1` และไม่ใช่ `null`) → เขียนเตือนไว้ในหมายเหตุ ·
  ค่านี้คือค่าที่ MaxxGPT อ่านจาก Meta ล่าสุด ณ `ad_account.synced_at` (`null` = ยังไม่เคยอ่าน ไม่ใช่บัญชีมีปัญหา)

### ขั้น 1 · ดึงผล
เรียก **`spotlight_get`** (ไม่มี argument บังคับ — ไม่ส่ง `ad_account_id` = บัญชีที่เลือกในเว็บ, ช่วงเป็น preset ตายตัว).

| ผล | ทำอะไร |
|---|---|
| `success:true` + `data` | ไปขั้น 2 · **`data` อาจมาเป็นสตริง JSON → parse ก่อน** |
| `code:FUNCTION_NOT_RUN` (404) | บัญชียังไม่เคยรัน → **ถามด้วย `AskUserQuestion`** (`รันเลย` / `ไว้ก่อน`) · ตอบรันเลย = `spotlight_run` แล้ว poll (ดูล่าง) |
| `code:NO_AD_ACCOUNT` (428) | ยังไม่ต่อ Meta / ยังไม่เลือกบัญชี / เกินโควตา (ดู `reason`) → ให้ user ไปจัดการในเว็บ MaxxGPT |
| `code:SUBSCRIPTION_EXPIRED` (403) | แพ็กเกจหมดอายุ — ให้ต่ออายุในเว็บ MaxxGPT |
| `code:SERVER_ERROR` (500) | หลังบ้านอ่านผลไม่สำเร็จ ลองใหม่ภายหลัง |
| ข้อความ `Rate limit reached …` | รอตามจำนวนวินาทีที่ข้อความบอก แล้วทำต่อเอง (`spotlight_get` 60 ครั้ง/ชั่วโมง · `spotlight_run` 12 ครั้ง/ชั่วโมง) |

**รันสด (spotlight_run):** async → ได้ `{ job_id, code }`.
- วน `get_job(job_id)` ตาม `poll_hint.poll_after_seconds` จน `job_status:"success"`
  **ห้ามจบ turn คืนงานให้ user ระหว่างรอ** — พิมพ์บรรทัดสั้น ๆ ว่ายังทำงานอยู่แล้ว poll ต่อ
- จบแล้ว **ห้ามอ่านผลจาก get_job** (เป็นก้อนดิบที่ยังไม่ trim) → เรียก **`spotlight_get` อีกครั้ง** เพื่ออ่าน
- `JOB_ALREADY_RUNNING` = มีงานค้าง ใช้ `job_id` เดิม poll ต่อได้เลย
- `spotlight_run` ใช้เวลาได้ถึง **15 นาที** — คำแนะนำใน `poll_hint` ที่ว่างานสั้นจะถูกตัดที่ 5 นาทีไม่ใช้กับงานนี้ ให้ poll ต่อ
- `job_status: failed` → อ่าน `data.error`: `META_TOKEN_INVALID` = การเชื่อมต่อ Meta หมดอายุ ให้ user ต่อ Meta ใหม่ในเว็บ MaxxGPT (รันซ้ำไม่ช่วย) ·
  `META_RATE_LIMITED` = รอ 2-3 นาทีแล้วค่อยรันใหม่ · `time_out` = เกิน 15 นาที เสนอรันใหม่ภายหลัง

### ขั้น 2-3 · ตัดข้อมูล แล้วพิมพ์ผล
อ่าน [references/output-shape.md](references/output-shape.md) เพื่อจับคู่ section → ตารางที่ต้องพิมพ์
แล้วพิมพ์เป็นข้อความ + ตาราง markdown ตาม
[references/output-format.md](references/output-format.md) § ตอบ.

**ไม่มี widget ไม่มีการ์ด HTML** — ผลออกมาเป็นข้อความ + ตารางในแชทเท่านั้น.

## § กติกาตัดข้อมูล + วางตาราง (ห้ามข้าม)

- **3 preset** เรียง `1d`(เมื่อวาน) → `3d`(3 วันก่อน) → `7d`(7 วันก่อน) เสมอ
- แต่ละถัง (`close.purchase`, `close.inbox`, `push.*`, `creative.*`) = **6 แถวแรก** (ไม่ตัดแถวไหนออก — `"รวม"` ก็เป็นโฆษณา · ถัง `push.*` ปลายทางคืนไม่เกิน 5 แถว)
- metric ต่อถัง — ใช้ตามตารางใน [output-shape.md](references/output-shape.md) · `value` **จัดรูปเป็นข้อความ**
  มาให้เสร็จ (ลูกน้ำ / `%` / สกุลเงิน / `Nx` สำหรับ ROAS)
- `Last_Update` (สตริงเวลา ISO เวลาไทย เช่น `2026-09-13T01:04:06.595+07:00`) — เขียนในหัวเรื่องเป็นข้อความอ่านง่าย (เช่น "อัปเดตล่าสุดเมื่อคืน") · ไม่ต้องกางรายตัว
- หมายเหตุ (bullet `⚠️` ใต้ตาราง) ใส่เมื่อ: เพิ่งรันสดเสร็จ · บัญชีไม่ ACTIVE · ทุกถังว่างทั้ง 3 preset
- **บรรทัดชวนถามต่อ (พิมพ์ปิดท้ายเสมอ):**
  ```
  ถามต่อได้: สรุปสุขภาพโฆษณาโดยรวม · ขอรันใหม่ให้เป็นข้อมูลล่าสุด · ขอตารางเต็มทุกแถว
  ```

### ผลว่าง
- ทุกถัง `close.*` ว่าง = **ข่าวดี** — เขียนว่า "👍 ไม่มีตัวที่เข้าข่ายควรปิด" แทนตารางเปล่า ไม่ใช่ error
- ว่างทั้ง 3 preset ทุกถัง = ช่วงนี้ไม่มีโฆษณาที่ผ่านเกณฑ์ spend ≥ 350 → เขียนหมายเหตุบอกเหตุผล
  แล้วเสนอรันสด (`spotlight_run`) เผื่อข้อมูลเก่า

---

## หลังแสดงผล — อยู่ต่อเพื่อตอบคำถาม

พิมพ์สรุปสั้น ๆ 2-4 บรรทัด แล้วบอกว่าถามต่อได้ — **อย่าเทข้อมูลดิบซ้ำลงในแชท**.
ตอบต่อจาก **ข้อมูลชุดเดิม** ห้ามยิง tool ซ้ำ เว้นแต่:

| user ขอ | ทำอะไร |
|---|---|
| ตัวเลข/เจาะแถว/ตารางเต็ม/ช่วงอื่นในชุดเดิม | ตอบจากข้อมูลเดิม ไม่ต้องยิงใหม่ |
| "ขอข้อมูลล่าสุด" / "รันใหม่" | `spotlight_run` → poll → `spotlight_get` |
| "ปิดตัวนี้" / "เพิ่มงบตัวนี้" | **สกิลนี้ทำไม่ได้** — บอกตรง ๆ ว่าดูได้อย่างเดียว ชี้ไป Ads Manager หรือสกิลจัดการงบ |
| อยากได้อันดับ/จัดกลุ่มลึกกว่านี้ | ชี้ไปสกิล **analyze-by-maxidea** (จัดอันดับ) หรือ **performance-analysis** (รายงานเต็ม) |

## ข้อควรระวังเรื่องตัวเลข
- **`CTR` เป็น %** อยู่แล้ว (`4.71` = 4.71%) — ห้ามคูณ 100 ซ้ำ · **`ROAS` เป็นเท่า** เขียน `"2.30x"` ไม่ใช่ %
- **เงินเป็นหน่วยปกติแล้ว** — ห้ามคูณ/หาร 100
- ต้นทุน/ผล = `0` แปลว่า "ไม่มีผลลัพธ์" ไม่ใช่ "ถูก" · **ROAS = `0` เมื่อยังไม่มียอดซื้อ** → แสดง `"0.00x"`
- 🔴 **Inbox section ≠ Purchase section**: `Inbox` มี `Inbox`+`Cost_per_Inbox` (ไม่มี ROAS) ·
  `Purchase` มี `Purchase`+`Purchase_Value`+`ROAS` (ไม่มี Inbox · `Cost_per_Purchase` มีเฉพาะถัง `Bad`) · ถัง `Good` ของทั้งสอง section มี `Score` เพิ่ม ·
  `Content_*` มีครบทั้งคู่ — **อ่านจาก `fields` เสมอ**
- ชื่อคอลัมน์ใช้ `Cost_per_Inbox` / `Cost_per_Purchase` (**`per` ตัวเล็ก**)
