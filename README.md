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

อัปโหลดปลั๊กอินเองก็ได้: [`downloads/maxxgpt-ads-chatgpt.zip`](https://github.com/MaxideaStudio/maxxgpt-plugin-marketplace/raw/main/downloads/maxxgpt-ads-chatgpt.zip) → Plugins → Add → **Upload plugin archive** — ปลั๊กอินนี้มี MaxxGPT (MCP) ในตัว ChatGPT จึงติดป้าย **Desktop only** ใช้ได้เฉพาะแอปบนเครื่อง

### ChatGPT บนเว็บ

ใช้ชุดสกิลแทนปลั๊กอิน (ไม่มี MCP ในตัว) แล้วเพิ่ม MaxxGPT เอง:

1. ดาวน์โหลด [`downloads/maxxgpt-ads-web-chatgpt.zip`](https://github.com/MaxideaStudio/maxxgpt-plugin-marketplace/raw/main/downloads/maxxgpt-ads-web-chatgpt.zip)
2. แถบซ้าย Skills → Create → **Upload from your computer** → เลือกไฟล์ ZIP (ได้ทุกสกิลแยกตัว)
3. พิมพ์ "ติดตั้ง MaxxGPT" ในแชท — สกิล `maxxgpt-install` จะพาเพิ่ม MaxxGPT ที่ Plugins → Add → **Create custom MCP server** (`https://mcp.maxxgpt.ai/mcp` · OAuth · ล็อกอินด้วยบัญชี MaxxGPT)

## ปลั๊กอิน

### maxxgpt-ads 0.11.0

ชุดเครื่องมือวิเคราะห์และวางแผนโฆษณา Meta (Facebook/Instagram) ผ่าน MaxxGPT — วิเคราะห์: ดูผลโฆษณาแยกรายหัวข้อ 6 หมวด, จัดอันดับโฆษณา 4 มุม, เทียบเมตริกกับค่ากลางบัญชี, โฆษณาแนะนำ และส่งออกรายงาน · วางแผน: วิเคราะห์ธุรกิจ-ลูกค้า-คู่แข่ง, ส่องโฆษณาคู่แข่งจาก Ads Library, แตก Content Angle, แกะภาพและวิดีโอโฆษณา

Claude 20 skill · ChatGPT 20 skill

- `maxxgpt-ad-metric-benchmark`
- `maxxgpt-ad-spotlight`
- `maxxgpt-analysis-leads`
- `maxxgpt-analysis-message`
- `maxxgpt-analysis-post-engagement`
- `maxxgpt-analysis-purchase-cpas`
- `maxxgpt-analysis-purchase-meta`
- `maxxgpt-analysis-video-ads`
- `maxxgpt-analyze-by-maxidea`
- `maxxgpt-business-analyzer`
- `maxxgpt-content-angle-ideas`
- `maxxgpt-export-report`
- `maxxgpt-facebook-ads-library-analyzer`
- `maxxgpt-image-breakdown`
- `maxxgpt-performance-analysis`
- `maxxgpt-rank-audience-growth`
- `maxxgpt-rank-bottom-ads`
- `maxxgpt-rank-rising-stars`
- `maxxgpt-rank-top-ads`
- `maxxgpt-video-breakdown`

ChatGPT บนเว็บ: [`downloads/maxxgpt-ads-web-chatgpt.zip`](https://github.com/MaxideaStudio/maxxgpt-plugin-marketplace/raw/main/downloads/maxxgpt-ads-web-chatgpt.zip) — 21 skill (ชุดเดียวกับฝั่ง ChatGPT ไม่มี MCP ในตัว) เพิ่ม:

- `maxxgpt-install`

### maxxgpt-artifact 0.6.0

เว็บ MaxxGPT Workspace สำหรับลูกค้า MaxxGPT: Ad Launcher, Interest Finder, Audience Heatmap, Creative Fatigue, Budget Scaling และ Kill Switch ในหน้าเดียว · พิมพ์ "ติดตั้งเว็บ MaxxGPT" เพื่อติดตั้ง หรือ "อัปเดตเว็บ MaxxGPT" หลังอัปเดตปลั๊กอิน

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
