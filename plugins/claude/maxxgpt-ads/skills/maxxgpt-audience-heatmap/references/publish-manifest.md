# publish manifest & การแก้ปัญหา — audience-heatmap.html

ไฟล์ HTML ทำงานได้ทันทีเมื่อวางในสภาพแวดล้อม Artifact **แต่ไม่ใช่ทั้งหมดของเรื่อง** —
ของสำคัญบางอย่างอยู่นอกไฟล์ เป็น argument ของตอน publish. หน้านี้คือรายการทั้งหมดของสิ่งนั้น.

## manifest ที่ต้องส่งตอน publish

```json
{
  "mcp": {
    "servers": [
      { "server": "<ชื่อ connector จริงของ user — ตัวเดียว>",
        "tools": ["get_dashboard_demographics", "get_account_info"] }
    ]
  },
  "sample": {}
}
```

> 🔴 **ชื่อเดียวเท่านั้น** — กล่อง "This artifact uses connectors" พิมพ์หนึ่งแถวต่อหนึ่งชื่อ
> ที่ประกาศ ชื่อที่ user ไม่มีขึ้น *"No matching connector found" + ปุ่ม Add custom*
> และกล่อง**เด้งถามซ้ำทุกครั้งที่เปิดหน้า**

| ตัว | หน้าใช้ทำอะไร | ไม่ประกาศแล้วเป็นยังไง |
|---|---|---|
| `mcp` → `get_dashboard_demographics` | ตารางความร้อนทั้งหน้า | หน้าเปิดได้ แต่ค้างที่ "ยังเชื่อมต่อ MaxxGPT ไม่ได้" |
| `mcp` → `get_account_info` | แถบบัญชี + ปุ่มเปิดบัญชีโฆษณา/เปิดเพจ | **แถบไม่โผล่เงียบ ๆ ไม่มี error** ส่วนที่เหลือทำงานปกติ → หา bug ยาก |
| `sample` | ปุ่ม "แนะนำการตั้ง ad set" | ปุ่ม disable แล้วเปลี่ยนข้อความเป็น "ถาม Claude ไม่ได้ในมุมมองนี้" |

**ไม่มี `db` · ไม่มี `downloads`** — หน้านี้ไม่เก็บ state อะไรของ user เลย ทุกอย่างดึงสด
(อย่าเผลอเติมเข้าไปเพราะเห็น interest-explorer มี)

อย่างอื่นที่อยู่นอกไฟล์เหมือนกัน:

- **`favicon: "🎯"`** — ส่งเฉพาะ **publish ครั้งแรก** · update ห้ามส่ง (ไอคอนคือสิ่งที่ user
  ใช้หาแท็บของตัวเอง เปลี่ยนแล้วเหมือนคนละหน้า)
- **`contract`** — **ไม่ต้องส่ง** ปล่อยให้ carry forward เอง (ต้นฉบับพัฒนาบน `0.2.41`)
- **`url`** — ต้องส่งเมื่อ update ของเดิม ไม่งั้นได้ artifact ใหม่คนละตัว
- **ไม่มี doctype / html / head / body ในไฟล์** — publish ห่อให้เอง ห้ามเติมเข้าไป

## ชื่อ connector

**ทะเบียนคนละอันกับที่ปลั๊กอินประกาศ** — `plugin/maxxgpt-ads/.mcp.json` ประกาศ MCP server
ชื่อ `maxxgpt` (URL `https://mcp.maxxgpt.ai/mcp`) แต่นั่นเป็น **local MCP server ของ Claude Code**
ซึ่ง **artifact เรียกไม่ได้** — สเปกระบุว่า `server` รับเฉพาะ **claude.ai connector**
· สองชื่อนี้ไม่ต้องตรงกันและมักไม่ตรง
(ตัวอย่างจริง: ปลั๊กอิน = `maxxgpt` · connector ของ user = `MaxxGPT MCP`)

`server` รับ **ชื่อที่แสดง** อย่างเดียว — ไม่รับ id ไม่รับ URL และ **หน้าเว็บมองไม่เห็น URL
ของ connector เลย** การจับคู่ด้วย URL จึงทำไม่ได้ทั้งตอน publish และตอนรัน →
**จับคู่ด้วยลายเซ็นของ tool**: หา connector ที่มีทั้ง `get_dashboard_demographics`
และ `get_account_info` แล้วประกาศชื่อนั้นชื่อเดียว.

การจับคู่ทำ **สองชั้น** เหมือน interest-explorer:

1. **ตอน publish (สกิลทำ — เป็นการค้นหา)** — หา connector ที่มีทั้งสอง tool แล้วประกาศ
   ชื่อนั้นชื่อเดียวใน manifest
2. **ตอนรัน (หน้าเว็บทำเอง — เป็นการยืนยัน)** — `mcp.listTools()` คืน
   *manifest ∩ connector ที่คนเปิดต่อไว้จริง* พร้อมรายชื่อ tool → `pickServer()` หยิบตัวที่มี
   `get_dashboard_demographics` แล้วเขียนทับตัวแปร `SERVER` ให้ตรงกับของจริง

> ✅ **จึงไม่ต้องแก้เนื้อไฟล์** — `var SERVER = "MaxxGPT MCP"` ที่หัวสคริปต์เป็นแค่**ค่าสำรอง**
> ใช้เฉพาะตอน `listTools()` เรียกไม่ได้ (shell เก่า) · ถ้าชื่อ connector ของ user เป็นอย่างอื่น
> หน้าหาเจอเองตอนโหลด **ขอแค่ manifest ประกาศชื่อนั้นไว้** เพราะ `listTools()` คืนเฉพาะ
> ตัวที่อยู่ใน manifest เท่านั้น
>
> หา connector ที่มี tool ไม่เจอ → หน้าขึ้น "ยังเชื่อมต่อ MaxxGPT ไม่ได้" พร้อมบรรทัด
> **"ที่หน้านี้มองเห็นตอนนี้: …"** ที่ลิสต์ชื่อที่มันเห็น → เอาชื่อนั้นไป publish ทับ URL เดิม จบ ·
> ถ้าเจอ connector ที่ `authStatus === "needs_reauth"` จะขึ้นหน้าให้ไปเชื่อมใหม่แทน
> (แยกคนละอาการกับ "หาไม่เจอ")

## response ที่หน้านี้เขียนไว้รองรับ (ยิงของจริงมาแล้ว ไม่ได้เดา)

```
get_dashboard_demographics
  { status, success,
    d7_age_gender:        { fields:[…27 ชื่อคอลัมน์…], rows:[[…], …] },
    yesterday_age_gender: { …เหมือนกัน… },
    today_age_gender:     { …เหมือนกัน… } }

get_account_info
  { status, success,
    ad_account:{ id:"act_<n>", account_id:"<n>", name, account_status, currency, timezone_name },
    page:{ id, name } }
```

**เป็นตารางแบบคอลัมนาร์** — `rows[i][j]` คือค่าของ `fields[j]` · หน้าเว็บสร้าง index map จาก
`fields[]` ทุกครั้ง **ห้ามยึดตำแหน่งคอลัมน์ตายตัว** และ **ห้ามยึดโครงจากก้อนเดียว** —
`today_age_gender` มีแถวน้อยกว่าก้อนอื่นเพราะวันยังไม่จบ.

27 คอลัมน์: `Age_Range · Gender · Total_Spend · Impression · Reach · Clicks · Inbox ·
MSG_NEW_CONTACT · MSS_VIEW · Lead · Purchase · Purchase_Value · Video_plays · Video_play_95 ·
Link_Clicks · AVG_DAILY_SPEND · CPM · Cost_Per_Reach · CTR · Video_Completion_Rate ·
Cost_Per_Inbox · Cost_Per_Lead · AVG_DAILY_INBOX · AVG_DAILY_PURCHASE · Cost_Per_Purchase ·
ROAS · Conversion_Purchase_Rate`

**กับดักที่เจอจริง:**

- แถว `Age_Range = "Unknown"` มีมาด้วยและเป็นศูนย์ทั้งแถว — โค้ดกรองทิ้งด้วยเงื่อนไข
  "ไม่มีทั้ง spend/ผล/impression"
- **`ad_account.id` มี prefix `act_` แต่ Ads Manager ต้องการเลขล้วน** → ลิงก์ใช้ `account_id`
  ก่อน แล้ว fallback เป็น `id.replace(/^act_/,"")`
  · บัญชี = `https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=<เลขล้วน>`
  · เพจ = `https://www.facebook.com/<page.id>`
- **watch ของ `get_account_info` เป็นตัวเสริมล้วน** — รับเฉพาะ event `data` ไม่ต่อ error
  เข้าตัวจัดการหลัก **ห้ามแก้ให้ต่อเข้า** ไม่งั้นบัญชีล่มแล้วลาก heatmap ล้มตาม

## เกณฑ์ตัดสินในหน้า (ถ้าจะแก้ ต้องรู้ก่อน)

- `MIN_RESULTS = 3` และ `SPEND_FLOOR = 100` — ต่ำกว่านี้ช่องขึ้นลายทาง "ข้อมูลน้อย"
  **ไม่ถูกคิดในสเกลสี ไม่เข้าอันดับ และคำสั่งที่ส่งให้ Claude มีกติกาห้ามสรุปจากมัน**
- สเกลสีคิด min/max **จากช่องที่ผ่านเกณฑ์ในช่วงเวลาที่เลือกเท่านั้น** — สลับช่วงเวลา
  สีของช่องเดิมเปลี่ยนได้ เพราะฐานเทียบเปลี่ยน ไม่ใช่บั๊ก
- เมตริกแบบ `cost` กลับด้าน (ถูก = ดี = สีเข้ม) ส่วน `roas` ไม่กลับ — อยู่ใน `goodness()`
- แคช: `staleTime` 5 นาที · `refetchInterval` 10 นาที สำหรับ demographics ·
  บัญชี `staleTime` 1 ชม. ไม่ตั้ง refetch

## โทนสี / โลโก้ (ถ้าจะแก้หน้าตา)

- โลโก้ Maxidea Studio ฝังเป็น **data: URI** — CSP ของ artifact บล็อกรูปจากโดเมนภายนอก
  **ทุกตัวแบบเงียบ ๆ** ห้ามเปลี่ยนไปใช้ `<img src="https://…">`
- โหมดมืดของโลโก้ใช้ `filter:invert(1)` + `@media (prefers-color-scheme: light)` ปลดกลับ
- **`--accent` (#fbbc05) ใช้เป็นพื้นเท่านั้น** (ตัวอักษรบนมันคือ `--accent-ink` สีเข้ม) ·
  ตอนเป็นตัวอักษร/ไอคอน/เส้น focus ต้องใช้ **`--accent-text`** — #fbbc05 เป็นตัวหนังสือ
  บนพื้นสว่างอ่านไม่ออก
- **สีตัวอักษรในช่องตารางถูกตรึงไว้ทั้ง ramp โดยตั้งใจ** (`--cell-ink-strong` ≈
  `--cell-ink-weak`) — ของเดิมสลับสีที่ `g >= 0.55` ทำให้ช่องช่วงกลางอ่านไม่ออก ·
  ramp โหมดมืดจึงจบที่ทองหม่น `#7d5f0f` ไม่ใช่ `#fbbc05` เต็ม ๆ
  **จะดันให้สดกว่านี้ต้องกลับไปแก้เกณฑ์สลับสีใน JS ด้วย**

## แก้ปัญหา

| user บอกว่า | สาเหตุที่น่าจะเป็น | ทำอะไร |
|---|---|---|
| ค้างที่ "ยังเชื่อมต่อ MaxxGPT ไม่ได้" ทั้งที่ต่อ connector แล้ว | ชื่อ connector ของเขาไม่อยู่ใน manifest → `listTools()` เลยไม่คืนมา | ดูบรรทัด **"ที่หน้านี้มองเห็นตอนนี้"** ใต้ข้อความ error → เอาชื่อนั้นใส่ manifest แล้ว publish ทับ URL เดิม |
| ตารางขึ้นแต่ **ไม่มีแถบบัญชี/ไม่มีปุ่มเปิดบัญชี-เปิดเพจ** | ลืมประกาศ `get_account_info` ใน manifest | publish ใหม่ที่ URL เดิมพร้อม tools ครบสองตัว |
| ปุ่ม "แนะนำการตั้ง ad set" กดไม่ได้ | ไม่ได้ประกาศ `sample` หรือบัญชีเขาไม่อนุญาต | เช็ค manifest ก่อน · ถ้าครบแล้วคือฝั่งบัญชี ไม่ใช่บั๊ก |
| ขึ้น "ยังไม่มีข้อมูลให้แสดง" | ช่วงเวลาที่เลือกไม่มีแอดทำงาน (เจอบ่อยกับ "วันนี้" ตอนเช้า) | ให้สลับไป "7 วันล่าสุด" · ไม่ใช่บั๊ก |
| ช่องส่วนใหญ่เป็นลายทางหมด | บัญชีใช้จ่ายน้อย ยังไม่ถึงเกณฑ์ 3 ผล / ฿100 ต่อช่อง | อธิบายเกณฑ์ตรง ๆ · **อย่าลดเกณฑ์ให้** เพราะจะได้สีที่หลอกตา |
| อยากได้ช่วงวันที่อื่น | tool ไม่รับพารามิเตอร์วันที่ มีแค่ 3 ช่วง | ใช้สกิลรายงานตัวอื่นแทน (`maxxgpt-export-report` ฯลฯ) |
| แชร์ลิงก์ให้เพื่อนแล้วเปิดไม่ได้ | `mcp` ปิดการแชร์สาธารณะ | ไม่ใช่บั๊ก · เพื่อนต้อง publish หน้าของตัวเอง |

**เทสจากฝั่งเราไม่ได้** — เปิด artifact แบบ top-level ทำให้ `claude.use()` คืน `null` เสมอ
โค้ด `window.claude.*` ทุกบรรทัดต้องให้ user เปิดใน claude.ai เองถึงจะรู้ว่าทำงาน.
ถ้าจะดูแค่หน้าตา/สี มี hook ติดมาในไฟล์: เปิดไฟล์แล้วเรียก
`window.MAXX_HEATMAP._set(payload)` ใน console — ไม่มีข้อมูลจริงฝังอยู่ในไฟล์.
