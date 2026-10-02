# หน้าตาข้อมูลที่ได้จาก `get_job`

> ## 🔴 ต่างจากรายงานตัวอื่นทั้งหมด — ชุดนี้เป็น **2D array ไม่ใช่ array ของ object**
>
> ```
> { "ad":       [ ["Ad name","Ad ID",…],   ["โฆษณา A","1234",…], … ],
>   "adset":    [ ["Adset name",…],        […], … ],
>   "campaign": [ ["Campaign name",…],     […], … ] }
> ```
>
> **แถวแรกของทุกก้อนคือชื่อคอลัมน์** แถวถัดไปคือข้อมูล →
> ต้องจับคู่ `header[i]` กับ `row[i]` เองก่อนใช้ · **ห้ามอ่านเป็น object ตรง ๆ**
> · ก้อนที่มีแค่แถวเดียว (เหลือแต่หัวตาราง) = ไม่มีข้อมูล

`data` จาก `get_job` อาจมาเป็น **สตริง JSON → parse ก่อน** · `{}` ว่าง = ไม่มีข้อมูล (ไม่ใช่ error)

## ชื่อคอลัมน์ (ตามที่ปลายทางตั้งมา — เป็นภาษาอังกฤษแบบ Ads Manager)

| ลำดับ | ระดับ ad | ระดับ ad set | ระดับ campaign |
|---|---|---|---|
| 1 | `Ad name` | `Adset name` | `Campaign name` |
| 2 | `Ad ID` | `Adset ID` | `Campaign ID` |
| 3 | `Ad delivery status` | `Campaign name` | `Objective` |
| 4 | `Adset name` | `Campaign ID` | `Amount spent (THB)` |
| 5 | `Adset ID` | `Objective` | `Result` |
| 6 | `Campaign name` | `Amount spent (THB)` | `Result indicator` |
| 7 | `Campaign ID` | `Result` | `Cost per results` |
| 8+ | `Objective` แล้วต่อด้วยชุดเมตริกเดียวกันทุกระดับ | | |

**ชุดเมตริกที่เหมือนกันทุกระดับ (เรียงตามลำดับจริง):**

`Amount spent (THB)` · `Result` · `Result indicator` · `Cost per results` · `Reach` · `Impressions` ·
`Frequency` · `CPM (cost per 1000 impresstion)` · `Clicks (All)` · `CTR (All)` · `Link clicks` ·
`Post comments` · `Post saves` · `Post shares` · `Video plays` · `Video plays at 95%` ·
`Messaging conversations started` · `Cost per Messaging conversation started` · `New messaging contacts` ·
`Outbound clicks` · `Website Landing page views` · `Purchase` · `Purchase value` · `Purchase Meta` ·
`Purchase value Meta` · `Purchase CPAS` · `Purchase value CPAS`

ระดับ ad มี **`Post URL`** ปิดท้ายอีกหนึ่งคอลัมน์ (รวม 36 คอลัมน์) · ad set 32 · campaign 30

> ⚠️ **สะกดตามของจริงเป๊ะ ๆ เวลาอ้างถึงคอลัมน์:**
> · `CPM (cost per 1000 impresstion)` — **สะกดผิดแบบนี้ในระบบจริง ห้ามแก้ให้ถูก** ไม่งั้นหาคอลัมน์ไม่เจอ
> · `Amount spent (THB)` — **ป้ายเขียน THB ตายตัว** ไม่ได้เปลี่ยนตามสกุลเงินของบัญชี →
>   เวลาแสดงผลให้ใช้สกุลเงินจริงจาก `get_account_info` และอย่าไปเชื่อป้ายนี้
> · `Clicks (All)` / `CTR (All)` มีวงเล็บ · `Result indicator` มีเว้นวรรค ไม่มีขีดล่าง

## ความหมายที่ต้องรู้เวลาอธิบายให้ user

| คอลัมน์ | คืออะไร |
|---|---|
| `Result` + `Result indicator` | ผลลัพธ์หลักที่ Meta นับให้แคมเปญนั้น + ชื่อของผลลัพธ์นั้น — **แต่ละแคมเปญนับคนละอย่าง** จึงเอามาบวกรวมข้ามแคมเปญไม่ได้ |
| `Cost per results` | `Amount spent ÷ Result` ของแถวนั้น · ผลลัพธ์ชนิด `reach` / `impressions` คิดเป็นต้นทุนต่อ 1,000 (แบบ Ads Manager) |
| `Purchase` vs `Purchase Meta` vs `Purchase CPAS` | ยอดซื้อรวม · ที่มาจากพิกเซล Meta · ที่มาจาก catalog segment (CPAS) — **อย่าบวกซ้อนกัน** |
| `Ad delivery status` | สถานะการส่งจริง — `ACTIVE` · **`COMPLETED`** (ad set/แคมเปญเลยวันสิ้นสุดแล้ว = "เสร็จสมบูรณ์" ใน Ads Manager) · **`CAMPAIGN_PAUSED`** (แคมเปญถูกปิด ตัวโฆษณาเองไม่ได้ปิด) · `PAUSED` · `ADSET_PAUSED` ฯลฯ · `-` = จับคู่ข้อมูลสถานะไม่ได้ |
| `Post URL` | ลิงก์โพสต์จริงของโฆษณา · ว่างได้ |

### 🔴 สองกับดักที่ทำให้สรุปผิด

1. **`Result indicator` ต่างกันจริงในบัญชีเดียวกัน** — เจอมาแล้วในข้อมูลจริง: แคมเปญหนึ่งนับ
   `video_thruplay_watched_actions` (หลักพัน) อีกแคมเปญนับ
   `actions:onsite_conversion.messaging_conversation_started_7d` (หลักหน่วย) →
   **บวก `Result` รวมกันคือเลขที่ไม่มีความหมาย** · จะรวมได้ต้องรวมเฉพาะแถวที่ `Result indicator` ตรงกัน
   แล้วบอก user ว่ารวมของอะไร
2. **`Cost per results` = `0` เมื่อ `Result = 0`** (ไม่ใช่ `null`) → เรียง "ต้นทุนถูกสุด" จากน้อยไปมากตรง ๆ
   แล้วแถวที่ไม่ได้ผลเลยจะขึ้นอันดับ 1 · **ตัดแถวที่ `Result = 0` ออกก่อนเรียงเสมอ**

## ช่วงวันที่

**ช่วงที่จบวันนี้ใช้ได้** — ปลายทางไม่ปฏิเสธ แต่ตัวเลขของวันที่ยังไม่ปิดวันยังไม่ครบ
(รายงานจะไม่ตรงกับที่โหลดจากเว็บภายหลัง) ·
**เขียนในหมายเหตุทุกครั้งที่ช่วงที่ขอรวมวันนี้**

## ขนาดข้อมูล

นี่คือ payload **ใหญ่ที่สุด** ในบรรดารายงานทั้งหมด — ทุกโฆษณาที่มีทั้งยอดใช้จ่ายและ impression × 36 คอลัมน์ ไม่มีการกรองอื่น
→ ห้ามพิมพ์ทั้งตารางลงแชทโดยไม่ถามก่อน (ดู SKILL.md § 5)
