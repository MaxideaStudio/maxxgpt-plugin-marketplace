# MaxxGPT Plugin Marketplace

ปลั๊กอินของ [MaxxGPT](https://maxxgpt.ai) สำหรับ Claude และ ChatGPT — วิเคราะห์และวางแผนโฆษณา Meta (Facebook / Instagram) จากในแชท

ต้องมีบัญชี MaxxGPT ที่ผูกบัญชีโฆษณา Meta ไว้แล้ว · ตอนติดตั้ง `maxxgpt-ads` จะให้ล็อกอิน MaxxGPT ผ่าน OAuth (`https://mcp.maxxgpt.ai/mcp`) สำหรับ skill วิเคราะห์

skill ส่องโฆษณาคู่แข่งจาก Ads Library ใช้ Meta Ads (`https://mcp.facebook.com/ads`) — ไม่มีก็ยังใช้ skill อื่นได้ครบ:

- **Claude**: ปลั๊กอินผูก Meta Ads มาให้ ล็อกอินเพิ่มอีกหนึ่งที่
- **ChatGPT**: ปลั๊กอินไม่ได้ผูกมาให้ ให้ต่อ Meta Ads ในบัญชี ChatGPT ของคุณเองก่อนใช้ skill นี้

ปลั๊กอินบางตัวมีเฉพาะฝั่ง Claude — ดูรายการในหัวข้อ "ปลั๊กอิน" ด้านล่าง

## ติดตั้ง — Claude

Claude Code:

```bash
claude plugin marketplace add MaxideaStudio/maxxgpt-plugin-marketplace
```

```bash
claude plugin install maxxgpt-ads@maxxgpt
```

แอป Claude: ดาวน์โหลด [`downloads/maxxgpt-ads-claude.zip`](https://github.com/MaxideaStudio/maxxgpt-plugin-marketplace/raw/main/downloads/maxxgpt-ads-claude.zip) แล้วอัปโหลดในหน้า Plugins

## ติดตั้ง — ChatGPT

แอป ChatGPT บนเครื่อง: Settings → Plugins → Add → **Add a marketplace** → ช่อง Source ใส่ `MaxideaStudio/maxxgpt-plugin-marketplace` แล้วติดตั้ง `maxxgpt-ads` จากรายการ

Codex CLI:

```bash
codex plugin marketplace add MaxideaStudio/maxxgpt-plugin-marketplace
```

ChatGPT บนเว็บ: ดาวน์โหลด [`downloads/maxxgpt-ads-chatgpt.zip`](https://github.com/MaxideaStudio/maxxgpt-plugin-marketplace/raw/main/downloads/maxxgpt-ads-chatgpt.zip) แล้วไปที่ Plugins → Add → **Upload plugin archive**

## ปลั๊กอิน

### maxxgpt-ads 0.9.0

ชุดเครื่องมือวิเคราะห์และวางแผนโฆษณา Meta (Facebook/Instagram) ผ่าน MaxxGPT — วิเคราะห์: ดูผลโฆษณาแยกรายหัวข้อ 6 หมวด, จัดอันดับโฆษณา 4 มุม, เทียบเมตริกกับค่ากลางบัญชี, โฆษณาแนะนำ, ส่งออกรายงาน, หน้าเครื่องมือค้น interest และแผนที่ความร้อนกลุ่มเป้าหมายอายุ×เพศ · วางแผน: วิเคราะห์ธุรกิจ-ลูกค้า-คู่แข่ง, ส่องโฆษณาคู่แข่งจาก Ads Library, แตก Content Angle, แกะภาพและวิดีโอโฆษณา

Claude 22 skill · ChatGPT 20 skill

- `maxideastudio-content-angle-idea`
- `maxideastudio-facebook-ads-business-analyst-v2`
- `maxideastudio-facebook-adslibrary-v3-8`
- `maxideastudio-image-breakdown`
- `maxideastudio-video-breakdown`
- `maxxgpt-ad-metric-benchmark`
- `maxxgpt-ad-spotlight`
- `maxxgpt-analysis-leads`
- `maxxgpt-analysis-message`
- `maxxgpt-analysis-post-engagement`
- `maxxgpt-analysis-purchase-cpas`
- `maxxgpt-analysis-purchase-meta`
- `maxxgpt-analysis-video-ads`
- `maxxgpt-analyze-by-maxidea`
- `maxxgpt-export-report`
- `maxxgpt-performance-analysis`
- `maxxgpt-rank-audience-growth`
- `maxxgpt-rank-bottom-ads`
- `maxxgpt-rank-rising-stars`
- `maxxgpt-rank-top-ads`

เฉพาะ Claude:

- `maxxgpt-audience-heatmap`
- `maxxgpt-interest-explorer`

### maxxgpt-artifact 0.4.0

เว็บ MaxxGPT Workspace สำหรับลูกค้า MaxxGPT: Interest Finder, Audience Heatmap, Ad Launcher, Creative Fatigue, Budget Scaling และ Kill Switch ในหน้าเดียว · พิมพ์ "ติดตั้งเว็บ MaxxGPT" เพื่อติดตั้ง หรือ "อัปเดตเว็บ MaxxGPT" หลังอัปเดตปลั๊กอิน

Claude 2 skill · ไม่มีฝั่ง ChatGPT

- `maxxgpt-artifact-launch`
- `maxxgpt-artifact-setup`

## โครงสร้าง

```
.claude-plugin/marketplace.json     แคตตาล็อกที่ Claude อ่าน
.agents/plugins/marketplace.json    แคตตาล็อกที่ ChatGPT / Codex อ่าน
plugins/claude/<plugin>/            แพ็กเกจฝั่ง Claude
plugins/chatgpt/<plugin>/           แพ็กเกจฝั่ง ChatGPT (เฉพาะปลั๊กอินที่รองรับ)
downloads/                          ไฟล์ ZIP สำหรับอัปโหลดเอง
```

repo นี้เป็นตัวแจกอย่างเดียว เนื้อหาถูกสร้างจากต้นฉบับโดยอัตโนมัติ — การแก้ไขที่นี่จะถูกเขียนทับในรอบถัดไป
