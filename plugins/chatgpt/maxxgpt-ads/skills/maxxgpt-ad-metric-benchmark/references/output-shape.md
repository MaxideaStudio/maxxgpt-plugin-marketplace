# โครงสร้างผลลัพธ์ที่ tool ส่งกลับ (อ่านก่อนพิมพ์ผล)

ทั้งสอง tool เป็น **async** → คืน `{ job_id, code }` แล้วต้อง `get_job` จน `job_status="success"` ·
`data` ของ job **อาจมาเป็นสตริง JSON → parse ก่อนใช้เสมอ**

> **คีย์สะกดตามนี้เป๊ะ ๆ** — ปลายทางสะกด `Impresstion` (ผิด) จริง, บาง key มีเว้นวรรค (`"Cost per result"`,
> `"Ad Name"`) · อ่านค่าตามชื่อจริง ห้าม "แก้ให้ถูก" เพราะจะอ่านไม่เจอ

---

## 1) `ad_benchmark_overview` → `data`

```json
{
  "OV": [ { …1 แถวต่อ Objective × Result indicator… } ]
}
```

มีคีย์ `OV` คีย์เดียว (ไม่มี `Gender` / `Age`) · `OV` เป็น `[]` = ช่วงนั้นไม่มีข้อมูล

### `OV[]` — ใช้เป็น "ตัวเลือก Result indicator" (สเต็ป 1)

| คีย์ | ความหมาย | รูปแบบตอนพิมพ์ |
|---|---|---|
| `Objective` | objective ของแคมเปญ (เช่น `OUTCOME_SALES`, `OUTCOME_ENGAGEMENT`) | text |
| `Result_indicator` | **ค่าที่ต้องส่งเป็น `indicator` ให้สเต็ป 2** เช่น `actions:onsite_conversion.messaging_conversation_started_7d` | text |
| `Result` | จำนวนผลลัพธ์รวมของกลุ่มนี้ | num |
| `Spend` | ยอดใช้จ่ายรวม | money |
| `Clicks` | คลิกรวม | num |
| `Impresstion` | **(สะกดผิดตามจริง)** impression รวม | num |
| `Reach` | reach รวม | num |
| `Purchase` | ยอดซื้อจากพิกเซล Meta (ไม่รวม CPAS — บัญชี CPAS ช่องนี้เป็น 0) | num |
| `CTR` | % (คำนวณจากยอดรวมแล้ว) | pct |
| `CPM` | ต้นทุนต่อพัน impression | money |
| `FRQ` | ความถี่เฉลี่ย (impression ÷ reach) | num |
| `"Cost per result"` | Spend ÷ Result | money |
| `"Cost per click"` | Spend ÷ Clicks | money |
| `"Cost per purchase"` | Spend ÷ Purchase | money |

> **หา Result indicator ที่เลือกได้ยังไง:** เอา `Result_indicator` ที่ไม่ซ้ำจาก `OV[]` — แต่ละค่าคือ 1 ปุ่มให้ user กด

---

## 2) `ad_benchmark_metrics` → `data`

ปลายทางกรองเฉพาะ ad ที่ตรง `indicator` และ **impression ≥ 1000** แล้วจัดระดับเทียบกันเองในบัญชี ·
มี **6 คู่คีย์** — แต่ละคู่ = สรุประดับ + ตารางรายโฆษณา:

```json
{
  "CTR": [ {level,Count,Min,Max} ],               "CTR_AD": [ {…รายโฆษณา…} ],
  "FRQ": [ … ],                                   "FRQ_AD": [ … ],
  "CPM": [ … ],                                   "CPM_AD": [ … ],
  "CTR_LINK_CLICK": [ … ],                        "CTR_LINK_CLICK_AD": [ … ],
  "Engagement_Rate": [ … ],                       "Engagement_Rate_AD": [ … ],
  "Cost_Per_Result": [ … ],                       "Cost_Per_Result_AD": [ … ]
}
```

### คีย์สรุป (`CTR`, `FRQ`, `CPM`, `CTR_LINK_CLICK`, `Engagement_Rate`, `Cost_Per_Result`)

array เรียง High → Medium → Low · แต่ละแถว:

| คีย์ | ความหมาย |
|---|---|
| `level` | `High` / `Medium` / `Low` (หรือระดับอื่นถ้ามี) |
| `Count` | จำนวน ad ในระดับนั้น |
| `Min` / `Max` | ช่วงค่าจริงของระดับนั้น (`null` ถ้าไม่มีข้อมูล) |

### คีย์รายโฆษณา (`*_AD`) — เรียงตามค่าเมตริกมาก→น้อยมาให้แล้ว (= High → Medium → Low)

คอลัมน์ร่วมทุกตาราง: `"Result Indicator" · "Objective" · "Ad ID" · "Ad Name" · "Adset ID" · "Campaign ID" · "Result" · "Spend" · "Purchase"`
แล้วต่อท้ายด้วย **คอลัมน์เมตริก + คอลัมน์ระดับ** ที่ชื่อ *ต่างกันในแต่ละตาราง*:

| คีย์ตาราง | ชื่อคอลัมน์เมตริก | ชื่อคอลัมน์ระดับ | fmt เมตริก |
|---|---|---|---|
| `CTR_AD` | `"CTR"` | `"Level of CTR"` | pct |
| `FRQ_AD` | `"FRQ"` | `"Level of FRQ"` | num |
| `CPM_AD` | `"CPM"` | `"Level of CPM"` | money |
| `CTR_LINK_CLICK_AD` | `"CTR (Link click)"` | `"Level of CTR (Link click)"` | pct |
| `Engagement_Rate_AD` | `"Engagement rate(%)"` | `"Level of Engagement rate(%)"` | pct |
| `Cost_Per_Result_AD` | `"Cost per result"` | `"Level of Cost per result"` | money |

> **ชื่อคอลัมน์เมตริกในตารางรายโฆษณา ≠ ชื่อคีย์ระดับบนสุด** — เช่น key `Engagement_Rate_AD` แต่คอลัมน์ชื่อ
> `"Engagement rate(%)"` · ตั้ง `columns[].key` ให้ตรงชื่อ *ในแถว* ไม่ใช่ชื่อ key ของ array

**ทิศทาง "ดี" ของแต่ละเมตริก** (ใช้เขียนคำอธิบาย ไม่ใช่ให้คำนวณใหม่เอง):
CTR / CTR (link) / Engagement rate → **สูง = ดี** · CPM / FRQ / Cost per result → **ต่ำ = ดี**

> คีย์สรุปทั้ง 6 ตัวนับจากตาราง `*_AD` ของเมตริกตัวเอง — ใช้ `Count`/`Min`/`Max` ได้ตรง ๆ ·
> ไม่มี ad ผ่านเกณฑ์ = `Count` 0 และ `Min`/`Max` เป็น `null` ทุกระดับ
