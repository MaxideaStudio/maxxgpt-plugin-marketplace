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
| `maxxgpt-rank-bottom-ads` | คัดแยกทั้งบัญชีเป็น 🔴 ควรปิด / 🟡 เฝ้าดู / 🟢 เก็บไว้ |
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
> skill วางแผนอีก 4 ตัวไม่ใช้ connector

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

- **บัญชี/เพจเลือกได้ต่อครั้ง** — ทุก tool รับ `ad_account_id` / `page_id` แบบ optional · ไม่ส่ง = ใช้ที่เลือกในเว็บ · id ต้องมาจาก `list_ad_accounts` / `list_pages` · ทุกคำตอบแนบ `ad_account {id,name,source}`
- **โควตาบัญชีต่อแพ็กเกจ** — `NO_AD_ACCOUNT` (428) + `reason: OVER_QUOTA` = ผู้ใช้ต้องไปเลือกบัญชีที่จะเก็บในเว็บก่อน · `NOT_ENTITLED` (403) = แพ็กเกจไม่รวมฟีเจอร์
- **งานผูกกับบัญชี** — `JOB_RUNNING_FOR_OTHER_ACCOUNT` · `JOB_NOT_FOUND` ถ้า `job_id` ไม่ใช่ของผู้ใช้นี้
- `worker_ping` (ใหม่ · ไม่คิดเครดิต) เอาไว้พิสูจน์ว่า MCP → คิว → worker ต่อกันอยู่

## 0.8.0 — เพิ่มกลุ่มวางแผน

เพิ่ม skill ของ MaxideaStudio 5 ตัว (ตารางบนสุด) · เนื้อหาตามที่ทีมส่งมา แก้เฉพาะส่วน "ดาวน์โหลดจากลิงก์" ของ
`maxideastudio-image-breakdown` และตัวอย่างการใช้งานของ `maxideastudio-video-breakdown` ให้ไม่ผูกกับเครื่องใดเครื่องหนึ่ง
(ของเดิมสั่งเปิดเบราว์เซอร์แล้วบันทึกลง `/home/ubuntu/Downloads/`) · skill กลุ่มวิเคราะห์ 17 ตัวไม่เปลี่ยน

## Version

0.8.0
