# หน้าตาข้อมูลที่ได้จาก `get_job` — ต่อหัวข้อ

อ่านไฟล์นี้ตอนจะแปลงผลเป็นตาราง เพื่อรู้ว่าจะหยิบคีย์ไหน

> ## 🔑 กฎเดียวที่ห้ามข้าม
> **อ่านชื่อคีย์จากแถวจริงเสมอ** (`Object.keys(rows[0])`) แล้วค่อยเลือกคอลัมน์ตามตารางข้างล่าง ·
> ตารางนี้คือ *สิ่งที่คาดว่าจะเจอ* ไม่ใช่สัญญาตายตัว — ปลายทางเป็น flow ของเว็บ MaxxGPT
> ที่แก้ไขได้โดยไม่ผ่านสกิลนี้ · **คีย์ไหนไม่มี = ข้ามคอลัมน์นั้นไป ห้ามเดาค่า ห้ามคำนวณแทน**

## รูปแบบรวม

`data` ที่ได้จาก `get_job` เป็น object เดียว (บางครั้งมาเป็น **สตริง JSON** → ต้อง parse ก่อน)

```
{ "Ad":[...], "Adset":[...], "Campaign":[...], "Objective":[...],
  "Age":[...], "Gender":[...], "Device":[...], "Position":[...], "Platform":[...],
  "Target":[...], "Recomment":{...} }
```

- แต่ละคีย์เป็น **array ของ object** (1 object = 1 แถว) ยกเว้น `Recomment`
- **`data` เป็น `{}` ว่าง = ช่วงนั้นไม่มีข้อมูลที่เข้าเกณฑ์** (ไม่ใช่ error) → แสดงการ์ดผลว่างพร้อม `note` บอกเหตุผล
- แถวระดับ **Ad มี `post_url`** ติดมาด้วย (บางแถวเป็นค่าว่างได้ = ดึงโพสต์ไม่ได้)

## คีย์บนสุดที่แต่ละหัวข้อมี

| หัวข้อ (`topic`) | tool | Age/Gender | Recomment |
|---|---|---|---|
| `video` | `analysis_video_ads` | ✅ | ✅ |
| `posteng` | `analysis_post_engagement` | ✅ | ✅ |
| `message` | `analysis_message` | ✅ | ✅ |
| `purchase_meta` | `analysis_purchase_meta` | ✅ | — |
| `purchase_cpas` | `analysis_purchase_cpas` | **—** | — |
| `leads` | `analysis_lead_ads` | ✅ | ✅ |

ทุกหัวข้อมี `Ad` / `Adset` / `Campaign` / `Objective` / `Device` / `Position` / `Platform` / `Target` เสมอ

## คอลัมน์ของแถว Ad / Adset / Campaign

คอลัมน์ฐานที่มีทุกหัวข้อ: `<level>_id`, `<level>_name`, `Spend`, `Impression`, `Clicks`, `CTR`
(ระดับ ad ใช้ `ad_id`/`ad_name`, ad set ใช้ `adset_id`/`adset_name`, แคมเปญใช้ `campaign_id`/`campaign_name`)

| หัวข้อ | คอลัมน์เฉพาะที่เพิ่มมา | เมตริกหลัก (ใช้เรียงลำดับ) | ต้นทุนต่อผล |
|---|---|---|---|
| `video` | `Inbox` `Video_plays` `Video_play_95` `Link_Clicks` `Landing_Page_View` `Purchase` `Purchase_Value` `Completion_Rate` `ROAS` | `Video_plays` | — (ใช้ `Spend ÷ Video_plays` ไม่ได้ ให้โชว์ `Completion_Rate` แทน) |
| `posteng` | `Post_Engagement` `Link_Clicks` `Landing_Page_View` `Comment` `Share` `post_engagement_rate` | `Post_Engagement` | — |
| `message` | `Inbox` `MSS_VIEW` `Purchase` `Purchase_Value` `Inbox_Rate` `Purchase_by_Inbox_Rate` `Purchase_Value_Per_Inbox` `Cost_Per_Inbox` | `Inbox` | **`Cost_Per_Inbox`** |
| `purchase_meta` | `Purchase` `Purchase_Value` `ROAS` | `Purchase` | — (โชว์ `ROAS`) |
| `purchase_cpas` | `Purchase` `Purchase_Value` `ROAS` | `Purchase` | — (โชว์ `ROAS`) |
| `leads` | `Lead` `Cost_per_lead` | `Lead` | **`Cost_per_lead`** |

⚠️ ชื่อคอลัมน์สะกดตามของจริง — `Cost_Per_Inbox` (P ใหญ่) แต่ `Cost_per_lead` (p เล็ก) ·
`Impression` ไม่มี s · `CTR_LINK_CLCIKS` ในชุด Recomment สะกดผิดแบบนั้นในโค้ดจริง **ห้ามแก้ให้ถูก**
เพราะจะอ่านค่าไม่เจอ

### 🔴 กับดักที่ทำให้อันดับผิด: ต้นทุนต่อผล = `0` เมื่อไม่มีผลลัพธ์

แถวที่ `Inbox = 0` จะได้ **`Cost_Per_Inbox = 0` ไม่ใช่ `null`** (เช่นเดียวกับ `Cost_per_lead`) →
ถ้าเรียง "ต้นทุนต่อผลถูกสุด" จากน้อยไปมากตรง ๆ **แถวที่ไม่ได้ผลอะไรเลยจะขึ้นเป็นอันดับ 1**

**กติกา:** ก่อนเรียง/หา "ตัวที่ถูกที่สุด" ทุกครั้ง ให้ **ตัดแถวที่เมตริกหลัก = 0 ออกก่อน** ·
เวลาแสดงในตาราง แถวพวกนี้แสดง `0` ตามจริงได้ แต่ **ห้ามเรียกว่า "ต้นทุนต่ำ"**

### ความหมายของคอลัมน์อัตราส่วน (อย่าอธิบายผิด)

| คอลัมน์ | สูตรจริง | หมายเหตุ |
|---|---|---|
| `Inbox_Rate` | `Inbox ÷ MSS_VIEW × 100` | **หารด้วยยอดเปิดดูข้อความ ไม่ใช่ยอดแสดงผล** → **เกิน 100% ได้ปกติ** (เช่น 255%) |
| `Purchase_by_Inbox_Rate` | `Purchase ÷ Inbox × 100` | สัดส่วนแชทที่ปิดการขายได้ |
| `Purchase_Value_Per_Inbox` | `Purchase_Value ÷ Inbox` | เป็นจำนวนเงิน ไม่ใช่ % |
| `CTR` | `Clicks × 100 ÷ Impression` | เปอร์เซ็นต์อยู่แล้ว |

## `Recomment` — โฆษณาที่ระบบชี้ว่าดีที่สุด

```
"Recomment": {
  "Ad":       {"Normal": {…แถวเดียว…}, "With_Purchase": {…แถวเดียว…}},
  "Adset":    {"Normal": {…}, "With_Purchase": {…}},
  "Campaign": {"Normal": {…}, "With_Purchase": {…}}
}
```

- เป็น **object แถวเดียว ไม่ใช่ array**
- ⚠️ **คีย์ `With_Purchase` หายไปทั้งคีย์ได้** เมื่อไม่มีแถวไหนมี `Purchase ≥ 1` (ของจริงเจอใน `video`)
  → เช็คว่ามีคีย์ก่อนอ่านเสมอ · `Normal` ก็หายได้ถ้าไม่มีแถวผ่านเกณฑ์
- แถวในนี้ **กรองมาแล้ว**: `Impression ≥ 3000` และมีผลลัพธ์ ≥ 1 → ไม่ตรงกับจำนวนแถวใน `Ad`
- มีคอลัมน์เพิ่มที่ `Ad` ปกติไม่มี: `Score` (คะแนนถ่วงน้ำหนัก), `ROAS`, `CTR_LINK_CLCIKS`, `Completion_Rate`,
  `Link_Clicks`, `Video_plays`, `Video_play_95`, `Landing_Page_View`
- `posteng` ต่างจากหัวข้ออื่น: กรองแค่ `Impression ≥ 3000` · ไม่มีคอลัมน์วิดีโอ · `ROAS` เป็น `0` เสมอ **ห้ามแสดง**
- ⚠️ **`Score` ตรงนี้เป็นสเกล 0-1** (เช่น `0.7957`) — **ต่างจาก `Score` ในสกิล analyze-by-maxidea ที่เป็น 0-100**
  → เวลาแสดงให้เขียนทศนิยม 2 ตำแหน่งตามที่ได้มา **ห้ามคูณ 100 เอง**
- `Normal` = จัดอันดับด้วย CTR ลิงก์ + อัตราผลลัพธ์ · `With_Purchase` = เฉพาะแถวที่มี `Purchase ≥ 1`
  แล้วถ่วงน้ำหนักยอดซื้อเข้าไปด้วย
- เอาไปวางใน `stats` ของการ์ด (เช่น "โฆษณาที่ดีที่สุด: <ad_name>") ไม่ต้องทำเป็นตาราง

## Breakdown (การ์ดเล็กด้านล่าง)

| คีย์ | 1 แถวคือ | คอลัมน์ |
|---|---|---|
| `Age` | ช่วงอายุ | ช่องแรกคือช่วงอายุ + เมตริกหลัก |
| `Gender` | เพศ | ช่องแรกคือเพศ + เมตริกหลัก |
| `Device` | อุปกรณ์ (`impression_device`) | ชื่ออุปกรณ์ + เมตริกหลัก |
| `Position` | ตำแหน่งวางโฆษณา (`platform_position`) | ชื่อตำแหน่ง + เมตริกหลัก |
| `Platform` | แพลตฟอร์ม (`publisher_platform`) | facebook / instagram / … + เมตริกหลัก |
| `Objective` | objective ของแคมเปญ | `Objective` + เมตริกหลัก |
| `Target` | กลุ่มเป้าหมายที่ยิง | `ID` `Name` `Type` `<เมตริกหลัก>` `Adset_IDs` |

breakdown ทุกชุดมีไม่กี่แถว → **ใส่ครบทุกแถวได้** ไม่ต้องตัด (ต่างจาก Ad/Adset/Campaign)

## จำนวนแถวที่ต้องคาด

`Ad` มาจาก Graph insights ระดับ ad `limit=500` → บัญชีใหญ่ช่วง 30 วันมีได้ **หลักร้อยแถว × ~18 คอลัมน์**
→ **ห้ามเทลงแชททั้งก้อน** (ดูกฎการตัดใน SKILL.md § 5)
