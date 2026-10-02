# รูปข้อมูลจาก `spotlight_get`

`spotlight_get` เป็น **sync** คืน `{ status, success, data, as_of, run_date, ad_account }` ตรง ๆ (ไม่มี job_id).
`data` มี 4 คีย์: `1d` (เมื่อวาน) · `3d` (3 วันก่อน) · `7d` (7 วันก่อน) · `Last_Update`.

> ค่าทั้งหมดผ่านการ trim ที่ backend แล้ว: คอลัมน์รูปหนัก (final_url, preview,
> creative_id, Caption) ถูกตัดออก **เหลือ `post_url`** และทุกตารางเป็นแบบ
> **columnar** `{ fields:[...], rows:[[...]] }` — อ่านค่าช่องที่ตำแหน่ง `j` จาก
> `fields[j]`. หลังบ้านคัดเฉพาะโฆษณาที่ **spend ≥ 350** มาให้แล้ว.

## แต่ละ preset (`1d`/`3d`/`7d`) มี 5 section

> 🔴 **คอลัมน์ (`fields`) ต่างกันแต่ละ section — อ่าน `fields` ของ section นั้นเสมอ อย่าจำ index ตายตัว**
> Inbox กับ Purchase **ไม่เหมือนกัน** (Inbox มี Cost_per_Inbox / Purchase มี ROAS+Purchase_Value · Cost_per_Purchase มีเฉพาะ `Bad` · `Good` มี Score เพิ่ม)

| section | ทรง | `fields` (หลัง trim) |
|---|---|---|
| `Inbox` | `{ Bad:{fields,rows}, Good:{fields,rows} }` | ad_id, ad_name, Spend, Impression, Clicks, **Inbox**, Purchase, CTR, CPM, **Cost_per_Inbox**, post_url · `Good` มี **Score** เพิ่มก่อน post_url |
| `Purchase` | `{ Bad:{...}, Good:{...} }` | ad_id, ad_name, Spend, Impression, Clicks, **Purchase**, **Purchase_Value**, CTR, CPM, **ROAS**, post_url · `Bad` มี **Cost_per_Purchase** เพิ่ม · `Good` มี **Score** เพิ่ม |
| `Content_CTR` | `{ fields, rows }` | ad_id, ad_name, Spend, Impression, Clicks, Inbox, Purchase, Purchase_Value, CTR, CPM, ROAS, Cost_per_Inbox, Cost_per_Purchase, post_url |
| `Content_INBOX` | `{ fields, rows }` | เหมือน Content_CTR |
| `Content_PURCHASE` | `{ fields, rows }` | เหมือน Content_CTR |

- **`Bad` = "ควรปิด" · `Good` = "ควรผลักดัน"** (ระบบจัดถังมาให้ ห้ามตัดสินเอง)
- `Content_*` = ครีเอทีฟเด่นเรียงมาแล้วตาม CTR / Inbox / Purchase ตามชื่อ
- `Good` เรียงมาแล้วตาม `Score` (0-100 = CPM ต่ำ 40% + CTR สูง 60%) และมีไม่เกิน 5 แถว · `Bad` ไม่ได้เรียง
- 🔴 **`ad_name` อาจเป็น `"รวม"` — นั่นคือ *ชื่อโฆษณาจริง* (มี ad_id + post_url + รูปของตัวเอง) ไม่ใช่ยอดรวม → แสดง/นับตามปกติ ห้ามตัดทิ้ง** (เว็บจริงก็นับรวมมันด้วย)
- `Last_Update` = เวลาที่คำนวณรอบนี้ เป็นสตริง ISO เวลาไทย (เช่น `2026-09-13T01:04:06.595+07:00`) · ระดับบนสุดของคำตอบมี `as_of` (เวลาเดียวกันแบบ UTC) และ `run_date` (`YYYY-MM-DD`) ด้วย

## จับคู่ section → ตารางที่ต้องพิมพ์ (ดู output-format.md)

| จาก `data[preset]` | ไป `presets[i]` | metric ที่ควรใส่ (ตามลำดับ) |
|---|---|---|
| `Purchase.Bad` | `close.purchase` | Spend (money) · Purchase (num) · **ROAS** (`Nx`) |
| `Inbox.Bad` | `close.inbox` | Spend (money) · Inbox (num) · Cost_per_Inbox (money) |
| `Purchase.Good` | `push.purchase` | Spend (money) · Purchase (num) · **ROAS** (`Nx`) |
| `Inbox.Good` | `push.inbox` | Spend (money) · Inbox (num) · Cost_per_Inbox (money) |
| `Content_CTR` | `creative.ctr` | CTR (pct) · Inbox (num) · Spend (money) |
| `Content_INBOX` | `creative.inbox` | Inbox (num) · Cost_per_Inbox (money) · Spend (money) |
| `Content_PURCHASE` | `creative.purchase` | Purchase (num) · ROAS (`Nx`) · Spend (money) |

- ทุกแถว: `name = ad_name`, `post_url = post_url` (ลิงก์เปิดโพสต์) · **`ad_name="รวม"` ก็เป็นโฆษณา — ใส่ตามปกติ**
- **เอาแค่ 6 อันดับแรก/ถัง** มาพิมพ์ (`Good` / `Content_*` เรียงมาแล้ว อย่าเรียงใหม่ · `Bad` ไม่ได้เรียง ให้เรียงเองตาม `Spend` มาก→น้อย) — ข้อมูลเต็มเก็บไว้ตอบต่อ
- ROAS ที่ปลายทางให้เป็น `0` เมื่อยังไม่มียอดซื้อ → แสดง `"0.00x"` ตรง ๆ (เว็บจริงก็โชว์ `0.0x`)

## รหัสผิดพลาด / สถานะพิเศษ

| กรณี | ความหมาย | ทำอะไร |
|---|---|---|
| `code: FUNCTION_NOT_RUN` (404) | บัญชีนี้ยังไม่เคยรัน | เสนอเรียก `spotlight_run` (async) แล้ว poll `get_job` จนจบ → เรียก `spotlight_get` อีกครั้ง |
| `code: NO_AD_ACCOUNT` (428) | ยังไม่ต่อ Meta / ยังไม่เลือกบัญชี / เกินโควตา (ดู `reason`) | ให้ user ไปจัดการในเว็บ MaxxGPT |
| `code: SUBSCRIPTION_EXPIRED` (403) | แพ็กเกจหมดอายุ | ให้ต่ออายุในเว็บ MaxxGPT |
| `code: SERVER_ERROR` (500) | หลังบ้านอ่านผลไม่สำเร็จ | ลองใหม่ภายหลัง |

## `spotlight_run` (async — ใช้เมื่อ FUNCTION_NOT_RUN หรือ user ขอข้อมูลล่าสุด)

คืน `{ job_id, code, progression }`:
- `code: JOB_CREATED` → poll `get_job(job_id)` ตาม `poll_hint` จน `job_status:"success"`
- `code: JOB_ALREADY_RUNNING` → มีงานค้างอยู่ ใช้ `job_id` เดิม poll ต่อ
- จบแล้ว **ไม่ได้อ่านผลจาก get_job** — ผลจริงต้องเรียก `spotlight_get` อีกครั้ง
