# publish manifest & การแก้ปัญหา — interest-explorer.html

ไฟล์ HTML ทำงานได้ทันทีเมื่อวางในสภาพแวดล้อม Artifact **แต่ไม่ใช่ทั้งหมดของเรื่อง** —
ของสำคัญบางอย่างอยู่นอกไฟล์ เป็น argument ของตอน publish. หน้านี้คือรายการทั้งหมดของสิ่งนั้น.

## manifest ที่ต้องส่งตอน publish

```json
{
  "mcp": {
    "servers": [
      { "server": "<ชื่อ connector จริงของ user — ตัวเดียว>",
        "tools": ["search_interest", "suggest_interest"] }
    ]
  },
  "db": {},
  "downloads": true,
  "sample": {}
}
```

> 🔴 **ชื่อเดียวเท่านั้น** — เคยลองใส่ชื่อสำรอง 4 ตัวแล้วต้องถอยกลับ (2026-09-05):
> กล่อง "This artifact uses connectors" พิมพ์หนึ่งแถวต่อหนึ่งชื่อที่ประกาศ ชื่อที่ user ไม่มี
> ขึ้น *"No matching connector found" + ปุ่ม Add custom* และกล่อง**เด้งถามซ้ำทุกครั้งที่เปิดหน้า**

| ตัว | หน้าใช้ทำอะไร | ไม่ประกาศแล้วเป็นยังไง |
|---|---|---|
| `mcp` | ค้น interest + ดึงตัวที่เกี่ยวข้อง | หน้าเปิดได้ แต่ขึ้น "ยังเรียกข้อมูลไม่ได้" ทุกกรณี |
| `db` | ชุดที่บันทึกไว้ | ปุ่มบันทึก disable + ขึ้นเหตุผล (เดิมเคยกดแล้วเงียบ) |
| `downloads` | ปุ่มดาวน์โหลด CSV | ปุ่ม disable (sandbox บล็อก `<a download>` เอง จึงไม่มีทางอื่น) |
| `sample` | การ์ด "ให้ Claude หา interest ให้" | การ์ดซ่อนตัวเองทั้งใบ ที่เหลือใช้ได้ปกติ |

อย่างอื่นที่อยู่นอกไฟล์เหมือนกัน:

- **`favicon: "🎯"`** — ส่งเฉพาะ **publish ครั้งแรก** · update ห้ามส่ง (ไอคอนคือสิ่งที่ user
  ใช้หาแท็บของตัวเอง เปลี่ยนแล้วเหมือนคนละหน้า)
- **`contract`** — หน้านี้ปักที่ `0.2.39` · **ไม่ต้องส่ง** ปล่อยให้ carry forward เอง
- **`url`** — ต้องส่งเมื่อ update ของเดิม ไม่งั้นได้ artifact ใหม่คนละตัว
- **ไม่มี doctype / html / head / body ในไฟล์** — publish ห่อให้เอง ห้ามเติมเข้าไป

## ชื่อ connector

**ทะเบียนคนละอันกับที่ปลั๊กอินประกาศ** — `plugin/maxxgpt-ads/.mcp.json` ประกาศ MCP server
ชื่อ `maxxgpt` (URL `https://mcp.maxxgpt.ai/mcp`) แต่นั่นเป็น **local MCP server ของ Claude Code**
ซึ่ง **artifact เรียกไม่ได้** — สเปกระบุว่า `server` รับเฉพาะ **claude.ai connector**
(local MCP server กับ server ของแอปเองไม่นับ) · สองชื่อนี้ไม่ต้องตรงกันและมักไม่ตรง
(ตัวอย่างจริง: ปลั๊กอิน = `maxxgpt` · connector ของ user = `MaxxGPT MCP`)

> ⚠️ **ยิง tool ในแชทได้ ≠ publish แล้วใช้ได้** — user ที่มีแต่ server จากปลั๊กอินจะรันสกิลได้
> แต่หน้าที่ publish จะขึ้น "ยังเรียกข้อมูลไม่ได้" · ต้องให้เขาเพิ่ม connector ที่
> claude.ai → Settings → Connectors ก่อน


`server` รับ **ชื่อที่แสดง** อย่างเดียว — ไม่รับ id ไม่รับ URL และ **หน้าเว็บมองไม่เห็น URL
ของ connector เลย** (`mcp.d.ts`: ServerInfo "carries no viewer-account identifiers,
no icon URLs, and no provenance fields. Deliberate and stable.") การจับคู่ด้วย URL จึงทำไม่ได้
ทั้งตอน publish และตอนรัน.

ที่ทำแทนคือ **จับคู่ด้วยลายเซ็นของ tool** สองชั้น:

1. **ตอน publish (สกิลทำ — เป็นการค้นหา)** — หา connector ที่มีทั้ง `search_interest` และ
   `suggest_interest` แล้วประกาศ **ชื่อนั้นชื่อเดียว** ·
   เบาะแสไว้ใช้หา ไม่ใช่ค่าที่เอาไปประกาศ: ชื่อมักมีคำว่า `MaxxGPT` · URL คือ
   `https://mcp.maxxgpt.ai/mcp` (ของเดิม `mcp-beta.maxxgpt.ai`) — ใช้ตอนต้องให้ user
   ไปเทียบเองที่ Settings → Connectors
2. **ตอนรัน (หน้าเว็บทำเอง — เป็นการยืนยัน)** — `mcp.listTools()` คืน
   *manifest ∩ connector ที่คนเปิดต่อไว้จริง* พร้อมรายชื่อ tool → `resolveServer()`
   หยิบตัวที่มีครบทั้งสอง tool · ชั้นนี้กันกรณี connector ชื่อตรงแต่ไม่ใช่ตัวจริง
   และแยก `needs_reauth` ออกจาก "หาไม่เจอ" ให้ข้อความ error ตรงอาการ

ชื่อสำรองที่ประกาศไว้แต่ user ไม่มี → ไม่โผล่ใน `listTools()` ก็จริง แต่**โผล่ในกล่องขออนุญาต**
และทำให้มันเด้งถามซ้ำ → **ประกาศชื่อเดียว** ที่หาเจอจริงเท่านั้น
ถ้า user เปลี่ยนชื่อ connector ทีหลัง หน้าจะขึ้น "ยังเรียกข้อมูลไม่ได้" พร้อมโชว์ชื่อที่มันมองเห็น
→ เอาชื่อนั้นไป publish ทับที่ URL เดิม จบ (ชุดที่บันทึกไว้ไม่หาย)

## response ที่หน้านี้เขียนไว้รองรับ (ยิงของจริงมาแล้ว ไม่ได้เดา)

```
search_interest  { status, success, count, interests: [
                     { id, name, type, audience_size_lower, audience_size_upper, path, topic } ] }
suggest_interest { status, success, count, suggestions: [ …เหมือนกัน แต่ไม่มี `type` ] }
```

`suggest_interest` ไม่มี `type` → หน้าเว็บ fallback ไปอ่าน `path[0]`
(`Interests` / `Behaviors` / `Demographics`) เพื่อแสดงป้ายประเภท.

**ขยะที่ Meta แถมมา**: `search?type=adinterest` ต่อท้ายผลทุกคำค้นด้วย interest กว้าง ๆ ชุดเดิม
(ตรวจแล้วกับคำค้น "Coffee": ลำดับ 0–15 เป็นกาแฟจริง ลำดับ 16–23 เป็นขยะ)
ฟังก์ชัน `score()` ในไฟล์จึงให้คะแนนจาก **ชื่อตรงกับคำค้น** (−8 และ −2 ต่อคำ) + **ลำดับที่ Meta
จัดมาเอง** แล้วค่อยบวกโบนัสเล็กน้อยจากจำนวนคำที่เจอ (−0.3) — ห้ามกลับไปเรียงด้วยจำนวนคำที่เจอ
อย่างเดียว เพราะขยะเจอครบทุกคำเสมอ.

โควตาหลังบ้าน: **200 ครั้ง/ชั่วโมง ต่อ tool**.

## แก้ปัญหา

| user บอกว่า | สาเหตุที่น่าจะเป็น | ทำอะไร |
|---|---|---|
| กดบันทึกชุดแล้วเงียบ ไม่มีอะไรเกิดขึ้น | ไม่ได้ประกาศ `db` ตอน publish | publish ใหม่ที่ URL เดิมพร้อม manifest ครบ |
| ขึ้น "ยังเรียกข้อมูลไม่ได้" ทั้งที่ต่อ connector แล้ว | ชื่อ connector ของเขาไม่อยู่ใน manifest | ดูบรรทัด "ที่หน้านี้มองเห็นตอนนี้" ใต้ข้อความ error → เอาชื่อนั้นใส่ manifest แล้ว publish ทับ |
| ไม่มีการ์ด "ให้ Claude หา interest ให้" | ไม่ได้ประกาศ `sample` หรือบัญชีเขาไม่อนุญาต | เช็ค manifest ก่อน · ถ้าครบแล้วคือฝั่งบัญชี ไม่ใช่บั๊ก |
| ปุ่มดาวน์โหลด CSV กดไม่ได้ | ไม่ได้ประกาศ `downloads` | publish ใหม่พร้อม manifest ครบ |
| ชุดที่เคยบันทึกหายหมด | publish เป็น artifact ตัวใหม่แทนที่จะ update ตัวเดิม | ของเดิมยังอยู่ที่ URL เก่า — หาด้วย `action:"list"` |
| แชร์ลิงก์ให้เพื่อนแล้วเปิดไม่ได้ | `mcp` ปิดการแชร์สาธารณะ | ไม่ใช่บั๊ก · เพื่อนต้อง publish หน้าของตัวเอง |
| ตัวอักษรที่พิมพ์ในช่อง "บอกว่าขายอะไร" มองไม่เห็นตอนโหมดมืด | wrapper ของ artifact ตรึง `:root{color-scheme:light}` และกฎ `color:inherit` ในไฟล์ไม่ได้ครอบ `textarea` → ตัวอักษรเป็นสีดำบนพื้นดำ | แก้แล้ว 2026-09-05: ไฟล์ประกาศ `color-scheme:light/dark` ในบล็อกธีมเอง + ใส่ `textarea` ในกฎ `button,input,select{color:inherit}` — อย่าถอดออก |

**อ่านข้อมูลที่ user บันทึกไว้กลับมาได้**: `Artifact action:"read_db"` `collection:"interest_sets"`
ที่ URL ของหน้าเขา — เอาชุดที่เขาเลือกไว้ไปใช้ต่อในแชทได้ เช่นส่งเข้า `create_campaign`.

**เทสจากฝั่งเราไม่ได้** — เปิด artifact แบบ top-level ทำให้ `claude.use()` คืน `null` เสมอ
โค้ด `window.claude.*` ทุกบรรทัดต้องให้ user เปิดใน claude.ai เองถึงจะรู้ว่าทำงาน.
