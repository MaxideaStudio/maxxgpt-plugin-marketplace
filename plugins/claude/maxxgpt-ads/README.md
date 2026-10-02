# maxxgpt-ads

ชุดเครื่องมือวิเคราะห์และวางแผนโฆษณา Meta (Facebook/Instagram) ผ่าน MaxxGPT — รวม 22 skill เข้าเป็น plugin เดียว ติดตั้งทีเดียวใช้ได้ครบ
(กลุ่มวิเคราะห์ 17 ตัว ใช้ข้อมูลบัญชีโฆษณาผ่าน MaxxGPT · กลุ่มวางแผน 5 ตัวของ MaxideaStudio ทำงานจากข้อมูลที่ผู้ใช้ให้มา)

## Skills

### วางแผนและครีเอทีฟ (MaxideaStudio) — เพิ่มใน 0.8.0

| Skill | ทำอะไร |
|-------|--------|
| `maxideastudio-facebook-ads-business-analyst-v2` | วิเคราะห์ธุรกิจ กลุ่มลูกค้า คู่แข่ง แล้ววางแผน Facebook/Instagram Ads จากข้อความ ไฟล์ หรือลิงก์ธุรกิจ |
| `maxideastudio-facebook-adslibrary-v3-8` | ส่องโฆษณาคู่แข่งจาก Meta Ads Library — Creative Angle · Pain/Gain · Offer · โฆษณาที่ควรศึกษาต่อ (ใช้ connector Meta Ads ถ้ามี) |
| `maxideastudio-content-angle-idea` | แตก Content Angle จาก Pain / Gain พร้อม Hook · Message · Format · Funnel · CTA |
| `maxideastudio-image-breakdown` | แกะภาพโฆษณา — โครงภาพ · สี · ฟอนต์/เลย์เอาต์ · จุดแข็งจุดอ่อน · prompt สร้างภาพใหม่ |
| `maxideastudio-video-breakdown` | แกะวิดีโอโฆษณาทีละฉาก — Hook · Marketing Logic · ข้อเสนอปรับปรุง · prompt สร้างวิดีโอ |

skill กลุ่มนี้ **ไม่เรียก MaxxGPT** และไม่ได้ใช้กติกาถาม-ตอบแบบกลุ่มวิเคราะห์ (ไม่มีบล็อกบัญชี/รหัส error ของ V4)

### ดูผลโฆษณา — แยกสกิลตามหัวข้อ

| Skill | ทำอะไร |
|-------|--------|
| `maxxgpt-analysis-video-ads` | โฆษณาวิดีโอ — ยอดเล่น · ดูถึง 95% · อัตราดูจบ |
| `maxxgpt-analysis-post-engagement` | เอนเกจโพสต์ — เอนเกจ · อัตราเอนเกจ · คอมเมนต์/แชร์ |
| `maxxgpt-analysis-message` | ทักแชท/อินบ็อกซ์ — จำนวนแชท · ต้นทุนต่อแชท · อัตราปิดการขายจากแชท |
| `maxxgpt-analysis-purchase-meta` | ยอดซื้อผ่านพิกเซล Meta — ยอดซื้อ · มูลค่า · ROAS |
| `maxxgpt-analysis-purchase-cpas` | ยอดซื้อแบบแคตตาล็อก CPAS (collaborative ads) |
| `maxxgpt-analysis-leads` | ลูกค้ามุ่งหวัง — จำนวนลีด · ต้นทุนต่อลีด |
| `maxxgpt-performance-analysis` | **เมนูรวม 6 หัวข้อดูผล** — ใช้ตอนผู้ใช้ยังไม่ระบุว่าจะดูหัวข้อไหน |

### จัดอันดับโฆษณา (เกณฑ์ MaxideaStudio)

| Skill | ทำอะไร |
|-------|--------|
| `maxxgpt-rank-top-ads` | Top Rank — ตัวที่ทำได้ดี (เลือกวัดด้วย inbox / lead / purchase / ROAS) |
| `maxxgpt-rank-bottom-ads` | คัดแยกโฆษณาตามเป้าผลลัพธ์ที่เลือกเป็น 🔴 ควรปิด / 🟡 เฝ้าดู / 🟢 เก็บไว้ |
| `maxxgpt-rank-rising-stars` | ดาวรุ่ง — CTR สูงแต่ยอดแสดงผลยังน้อย |
| `maxxgpt-rank-audience-growth` | ยังขยายกลุ่มเป้าหมายได้อีก — CPM ถูก ความถี่ต่ำ |
| `maxxgpt-analyze-by-maxidea` | **เมนูรวม 4 หัวข้อจัดอันดับ** — ใช้ตอนผู้ใช้ยังไม่ระบุว่าจะดูมุมไหน |

### อื่น ๆ

| Skill | ทำอะไร |
|-------|--------|
| `maxxgpt-ad-metric-benchmark` | เทียบเมตริกแต่ละโฆษณา (CTR · Frequency · CPM · Engagement · Cost/result) กับค่ากลางของบัญชี แล้วตีระดับ High/Medium/Low |
| `maxxgpt-ad-spotlight` | โฆษณาแนะนำรายคืน — ควรปิด / ควรดัน / ครีเอทีฟเด่น แยกตามช่วงเวลา |
| `maxxgpt-export-report` | ส่งออกรายงานผลโฆษณาแบบดิบ |
| `maxxgpt-interest-explorer` | ส่งมอบ **หน้าเครื่องมือค้น interest** เป็น Artifact ส่วนตัว — ค้นคำ · ไล่ดูตัวที่เกี่ยวข้อง · เก็บเป็นชุด · บอกว่าขายอะไรแล้วให้ Claude หาคำค้นให้ |
| `maxxgpt-audience-heatmap` | ส่งมอบ **หน้าแผนที่ความร้อนกลุ่มเป้าหมาย (อายุ × เพศ)** เป็น Artifact ส่วนตัว — กลุ่มไหนต้นทุนต่อผลถูกสุด/ROAS สูงสุด · สลับ 3 ช่วงเวลา · ให้ Claude แนะนำการตั้ง ad set |

> **สกิลวิเคราะห์ทุกตัวรับ `job_id` ได้** — ถ้ามี `job_id` ของงานที่รันไว้แล้ว สกิลจะดึงผลนั้นมาวิเคราะห์ทันที
> โดยไม่ยิงงานใหม่ (ประหยัดเวลา 1-5 นาทีต่อรอบ)

## Connectors ที่ต้องเปิดใช้

Plugin นี้ประกาศ connector 2 ตัวใน `.mcp.json` — ผูกให้อัตโนมัติตอนติดตั้ง ผู้ใช้แค่ล็อกอิน OAuth:

| Connector | URL | ใครใช้ | หมายเหตุ |
|-----------|-----|--------|----------|
| **MaxxGPT** (`maxxgpt`) | `https://mcp.maxxgpt.ai/mcp` | skill กลุ่มวิเคราะห์ทั้ง 17 ตัว | โดเมนเดิม `https://mcp-beta.maxxgpt.ai/mcp` ยังใช้แก้ขัดได้ แต่ควรย้ายมาโดเมนหลัก |
| **Meta Ads** (`meta-ads`) | `https://mcp.facebook.com/ads` | `maxideastudio-facebook-adslibrary-v3-8` ตัวเดียว (tool `ads_library_search`) | เพิ่มใน 0.8.0 · เป็น connector ของ Meta เอง · ไม่ล็อกอินก็ยังใช้ skill อื่นได้ครบ |

> **หมายเหตุ:** skill กลุ่มวิเคราะห์ใช้ MaxxGPT ตัวเดียว ไม่แตะ Meta Ads / Google Drive (ตั้งแต่ 0.6.0) ·
> สิทธิ์ที่หน้าล็อกอินของ Meta ขอเป็นชุดที่ server ของ Meta กำหนด (รวมสิทธิ์จัดการโฆษณา) แม้ skill ในชุดนี้จะเรียกแค่ `ads_library_search` เพื่ออ่าน Ads Library ·
> skill วางแผนอีก 4 ตัวไม่ใช้ connector ·
> **แพ็กเกจฝั่ง ChatGPT ไม่มี `meta-ads`** (ตั้งแต่ 0.8.1) — ผู้ใช้ ChatGPT ต่อ Meta Ads ในบัญชีของตัวเอง

## การใช้งาน

แต่ละ skill trigger อัตโนมัติจากคำพูดผู้ใช้ (ดู trigger phrases ใน frontmatter ของแต่ละ `SKILL.md`) เช่น
- "ดูผลแอดหน่อย" (ไม่ระบุหัวข้อ) → `maxxgpt-performance-analysis` (เปิดเมนูให้เลือก)
- "ต้นทุนต่อแชทเดือนนี้เท่าไร" → `maxxgpt-analysis-message`
- "คลิปไหนคนดูจบ" → `maxxgpt-analysis-video-ads`
- "แอดตัวไหนควรปิด" → `maxxgpt-rank-bottom-ads`
- "ตัวไหนควรเพิ่มงบ" → `maxxgpt-rank-rising-stars`
- "เทียบเมตริกโฆษณา / benchmark" → `maxxgpt-ad-metric-benchmark`
- "โฆษณาแนะนำคืนนี้" → `maxxgpt-ad-spotlight`
- "หา interest / ขอ interest id / ควร target ใคร" → `maxxgpt-interest-explorer`
- "อายุไหนดี / เพศไหนคุ้มกว่า / ควรตั้งอายุเท่าไรใน ad set" → `maxxgpt-audience-heatmap`

## เรื่องที่ตั้งใจไม่มีในชุดนี้

**ไม่มี skill กลุ่ม "สร้าง/ยิงแอด" เลย** — `maxxgpt-meta-ad` (ยิงแอดทีละตัวจาก Google Drive) ถอดออกตั้งแต่ 0.3.0
และ `maxxgpt-auto-creation-ads` (สร้างแอดอัตโนมัติตามตารางเวลา) ถอดออกที่ 0.6.0 ·
ทั้งคู่ไม่ได้ถูกลบทิ้ง ยังอยู่ที่ `skill/maxxgpt-meta-ad/` และ `skill/maxxgpt-auto-creation-ads/` ของ repo
(พร้อมไฟล์แพ็ก `.skill` แจกเดี่ยวได้) · ชุดนี้จึง **ไม่เขียนอะไรลงบัญชีโฆษณา** — มีแต่วิเคราะห์กับวางแผน

**ไม่มี widget / การ์ด HTML** — ตั้งแต่ 0.6.0 ทุก skill ในชุดนี้ **ถามด้วยปุ่มตัวเลือกจาก tool `AskUserQuestion`**
แล้ว **ตอบเป็นข้อความ + ตาราง markdown** เท่านั้น · ทุก skill มี **กฎเหล็กห้ามสร้าง widget/ฟอร์ม HTML** เขียนไว้ชัด — เรียก `AskUserQuestion` ไม่ได้จริง ๆ ค่อยถามเป็นข้อความแบบเลขข้อ (ไฟล์ `assets/*.html` และ `references/widget-spec.md` ถูกถอดออก
แทนที่ด้วย `references/output-format.md` ที่กำหนดว่าถามอะไรบ้าง + ผลลัพธ์ต้องมีหน้าตายังไง) ·
ยกเว้น `maxxgpt-interest-explorer` กับ `maxxgpt-audience-heatmap` ที่ส่งมอบเป็น **Artifact** (คนละเรื่องกับ widget)


**ไม่มีเกณฑ์ตัวเลขมาตรฐาน** (เช่น "CTR ควรเกินเท่าไร" / "ROAS เท่าไรถือว่าผ่าน") — เป็นการตัดสินใจของเจ้าของระบบ
ไม่ใช่ของที่ยังทำไม่เสร็จ เพราะค่าที่ "ดี" ขึ้นกับแต่ละบัญชี/ธุรกิจ/สินค้า ไม่มีสูตรกลาง ·
สกิลจึงอ่านผลด้วยการ **เทียบภายในชุดข้อมูลของบัญชีเอง** และถ้าอยากได้ระดับ High/Medium/Low จริง ๆ
ให้ใช้ `maxxgpt-ad-metric-benchmark` ซึ่งเทียบกับค่ากลางของบัญชีนั้น ๆ

## MaxxGPT V4 (0.7.0)

หลังบ้านของ `https://mcp.maxxgpt.ai/mcp` ย้ายจาก n8n มาเป็น V4 (monorepo นี้ · `apps/mcp` + `apps/worker`) — **URL · ชื่อ tool · รูปแบบผลลัพธ์ทุกตัวเหมือนเดิม** สิ่งที่เพิ่มและทุก skill รู้จักแล้วตั้งแต่ 0.7.0:

- **บัญชี/เพจเลือกได้ต่อครั้ง** — tool ที่ทำงานกับบัญชีโฆษณารับ `ad_account_id` / `page_id` แบบ optional (ยกเว้น `get_job` · `search_interest` · `suggest_interest`) · ไม่ส่ง = ใช้ที่เลือกในเว็บ · id ต้องมาจาก `list_ad_accounts` / `list_pages` · คำตอบแนบ `ad_account {id,name,source}` (ยกเว้น `get_job` · `get_dashboard_demographics` แนบตั้งแต่ MCP 1.23.2)
- **โควตาบัญชีและเพจต่อแพ็กเกจ** — `NO_AD_ACCOUNT` (428) + `reason: OVER_QUOTA` = ผู้ใช้ต้องไปเลือกบัญชี/เพจที่จะเก็บในเว็บก่อน · `SUBSCRIPTION_EXPIRED` (403) = แพ็กเกจหมดอายุ · `NOT_ENTITLED` (403) = แพ็กเกจไม่รวมฟีเจอร์ (tool ที่ skill ชุดนี้ใช้ยังไม่มีตัวไหนตอบรหัสนี้)
- **งานผูกกับบัญชี** — `JOB_RUNNING_FOR_OTHER_ACCOUNT` · `JOB_NOT_FOUND` ถ้า `job_id` ไม่ใช่ของผู้ใช้นี้
- `worker_ping` (ใหม่ · ไม่คิดเครดิต) เอาไว้พิสูจน์ว่า MCP → คิว → worker ต่อกันอยู่

## 0.8.0 — เพิ่มกลุ่มวางแผน

เพิ่ม skill ของ MaxideaStudio 5 ตัว (ตารางบนสุด) · เนื้อหาตามที่ทีมส่งมา แก้เฉพาะส่วน "ดาวน์โหลดจากลิงก์" ของ
`maxideastudio-image-breakdown` และตัวอย่างการใช้งานของ `maxideastudio-video-breakdown` ให้ไม่ผูกกับเครื่องใดเครื่องหนึ่ง
(ของเดิมสั่งเปิดเบราว์เซอร์แล้วบันทึกลง `/home/ubuntu/Downloads/`) · skill กลุ่มวิเคราะห์ 17 ตัวไม่เปลี่ยน

## 0.8.1 — Meta Ads เฉพาะฝั่ง Claude

แพ็กเกจฝั่ง ChatGPT ถอด `meta-ads` ออกจาก `.mcp.json` — ChatGPT desktop ล็อกอินกับ `https://mcp.facebook.com/ads` ผ่านปลั๊กอินไม่ได้
(Meta ไม่รับการลงทะเบียนจากแอปบนเครื่อง) ผู้ใช้เห็นปุ่ม Authenticate ที่กดแล้ว error · ฝั่ง Claude ยังประกาศไว้ตามเดิม · เนื้อหา skill ไม่เปลี่ยน

## 0.8.2 — อัตราการซื้อในแผนที่ความร้อน

`maxxgpt-audience-heatmap`: ช่อง "อัตราการซื้อ" ในรายละเอียดของแต่ละช่องแสดงสูงเกินจริง 1,000 เท่า — `Conversion_Purchase_Rate`
ที่ MaxxGPT ส่งมาเป็น "การซื้อต่อ 1,000 impression" แต่หน้าเว็บเอาไปแสดงเป็นเปอร์เซ็นต์ตรง ๆ · แก้ให้หาร 1,000 ก่อน ·
ผู้ใช้ที่ publish หน้านี้ไว้แล้วต้องสั่ง skill ให้ publish ทับอีกครั้งถึงจะได้ตัวที่แก้ · skill อื่นไม่เปลี่ยน

## 0.9.0 — ข้อความใน skill ตรงกับ MaxxGPT MCP รุ่น V4 (1.23.1)

ไล่ตรวจ skill กลุ่มวิเคราะห์ทั้ง 17 ตัวเทียบกับโค้ดของ MCP ทีละข้อ แล้วแก้จุดที่ skill บอก Claude ผิดหรือไม่ครบ · ชื่อ tool และ argument ไม่เปลี่ยน

- **สูตร Score** ของ Rising Stars (CTR สูง 40% + Impression น้อย 60%) และ Audience Growth (CPM ต่ำ 40% + Frequency ต่ำ 60%) — เดิมเขียนเป็นสูตรของ Top Rank
- **Top Rank** คืนไม่เกิน 5 แถวต่อระดับ · เมตริก purchase / roas ไม่มีคอลัมน์ต้นทุนต่อผล · **Bottom Rank** คัดเฉพาะโฆษณาที่ตั้งเป้าเป็นผลลัพธ์ชนิดที่เลือก ไม่ใช่ทั้งบัญชี
- **`job_id` ที่ส่งมา** ดูจาก `function_name` ของ `get_job` ก่อน (ตารางลายเซ็นเหลือเป็นทางสำรอง) · `data: null` = ผลหมดอายุ (เก็บ 7 วัน)
- **รหัส error** เป็นของ V4: งานที่ล้มอ่าน `data.error` (`META_TOKEN_INVALID` · `META_RATE_LIMITED` · `META_PERMISSION_DENIED` · `time_out`) · `SUBSCRIPTION_EXPIRED` · ข้อความ `Rate limit reached` · ตัดรหัสของระบบเดิมที่ไม่มีแล้ว และตัดประโยคที่บอกว่างานที่ time_out พลิกเป็นสำเร็จเองได้
- **`get_account_info`** มี `synced_at` · `account_status` / `timezone_name` เป็นค่าที่ MaxxGPT อ่านจาก Meta ล่าสุด · เปลี่ยนบัญชีต้องเรียกใหม่ด้วย `ad_account_id` เดียวกัน
- **Export** รับช่วงที่จบวันนี้ได้ (ตัวเลขวันนี้ยังไม่ครบ) · **Benchmark** สเต็ป 1 คืน `{ OV }` อย่างเดียว · **Spotlight** บอกรูปของ Good / Bad และเวลาที่ `spotlight_run` ใช้ได้ถึง 15 นาที
- แถวระดับโฆษณา / ad set ไม่มีชื่อแคมเปญติดมา ให้กำกับด้วย id (อยากได้ชื่อแคมเปญใช้ `maxxgpt-export-report`)
- หน้า **interest explorer** และ **audience heatmap**: คำตอบ error ของ MaxxGPT (ยังไม่ผูกบัญชี · เกินโควตา · แพ็กเกจหมดอายุ · เรียกถี่เกิน) ขึ้นเป็นข้อความบอกสาเหตุ ไม่ใช่ "ไม่พบผลลัพธ์" · heatmap ใช้สัญลักษณ์เงินตามสกุลของบัญชี และบอกว่าต้นทุนต่อการเข้าถึงคิดต่อ 1,000 คน · ผู้ใช้ที่ publish สองหน้านี้ไว้แล้วต้องสั่ง skill ให้ publish ทับ

## 0.9.1 — `get_dashboard_demographics` บอกบัญชีและเวลาของข้อมูล (MCP 1.23.2)

ตั้งแต่ MaxxGPT MCP 1.23.2 คำตอบของ `get_dashboard_demographics` มี `ad_account` (บัญชีของตาราง) และ `as_of` (เวลาที่ MaxxGPT ดึงจาก Meta ·
cache ต่อบัญชีไม่เกิน 60 นาที · `stale: true` = ดึงรอบใหม่ไม่สำเร็จ ใช้ชุดเก่า) ข้างตาราง 3 ช่วง เหมือน tool อื่น · skill 17 ตัวแก้ประโยคที่เคยบอกว่า
tool นี้ไม่แนบ `ad_account` · ตาราง ชื่อ tool และ argument ไม่เปลี่ยน · หน้าที่ publish ไว้แล้วไม่ต้อง publish ทับ

## Version

0.9.1
