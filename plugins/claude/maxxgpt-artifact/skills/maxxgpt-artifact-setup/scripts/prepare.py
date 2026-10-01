#!/usr/bin/env python3
"""Prepare one MaxxGPT site for publishing on the customer's account.

    python3 prepare.py workspace --connector maxxgpt="MaxxGPT MCP" --connector meta="Meta ads" \
        [--connector drive="Google Drive"] --out /tmp/maxxgpt-setup

It checks the page shipped in this plugin against the sha256 in sites/manifest.json,
copies it to --out (and checks the copy), and fills the capabilities template with the
customer's connector names. It prints one JSON object: what to publish and with which
capabilities. On any problem it prints {"ok": false, "error": ...} and exits 2; the
error text is Thai and meant to be passed to the customer as it is.

Standard library only, Python 3.8+.
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[3]
SITES = PLUGIN / "sites"
DEFAULT_OPTIONAL_NAME = {"drive": "Google Drive"}  # owner decision 2026-09-23: declare Drive for everyone


class Stop(Exception):
    pass


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_connectors(pairs):
    names = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise Stop("รูปแบบ --connector ต้องเป็น ชื่อกลุ่ม=ชื่อ connector เช่น meta=\"Meta ads\" แต่ได้ " + repr(pair))
        key, name = pair.split("=", 1)
        key, name = key.strip(), name.strip()
        if not name or "{{" in name or "}}" in name:
            raise Stop("ชื่อ connector ของ " + key + " ว่างหรือไม่ถูกต้อง")
        if key in names:
            raise Stop("ใส่ชื่อ connector ของ " + key + " ซ้ำสองครั้ง")
        names[key] = name
    return names


def fill(value, names):
    if isinstance(value, dict):
        return {k: fill(v, names) for k, v in value.items()}
    if isinstance(value, list):
        return [fill(v, names) for v in value]
    if isinstance(value, str) and value.startswith("{{CONNECTOR:") and value.endswith("}}"):
        return names[value[len("{{CONNECTOR:"):-2]]
    return value


def prepare(site_id, pairs, out_dir):
    manifest_path = SITES / "manifest.json"
    if not manifest_path.is_file():
        raise Stop("ไม่พบไฟล์ของเว็บในปลั๊กอิน (sites/manifest.json) ปลั๊กอินติดตั้งไม่ครบ ให้ติดตั้งปลั๊กอิน maxxgpt-artifact ใหม่")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    site = manifest.get("sites", {}).get(site_id)
    if not site:
        raise Stop("ปลั๊กอินรุ่นนี้ไม่มีเว็บ " + site_id + " มีแค่ " + ", ".join(sorted(manifest.get("sites", {}))))

    page = SITES / site["page"]
    if not page.is_file() or sha256(page) != site["sha256"] or page.stat().st_size != site["bytes"]:
        raise Stop("ไฟล์หน้าเว็บในปลั๊กอินไม่ตรงกับที่ทีมปล่อย (sha256 ไม่ตรง) ห้าม publish ให้ติดตั้งปลั๊กอิน maxxgpt-artifact ใหม่")

    names = parse_connectors(pairs)
    wanted = site["connectors"]
    unknown = sorted(set(names) - set(wanted))
    if unknown:
        raise Stop("เว็บนี้ไม่ได้ใช้ connector กลุ่ม " + ", ".join(unknown))
    for key, spec in wanted.items():
        if key not in names:
            if spec.get("optional") and key in DEFAULT_OPTIONAL_NAME:
                names[key] = DEFAULT_OPTIONAL_NAME[key]
            else:
                raise Stop("ยังไม่ได้ใส่ชื่อ connector ของ " + key + " (ต้องมี tool " + spec["probe"] + ")")
    taken = {}
    for key, name in names.items():
        if name in taken:
            raise Stop("connector " + repr(name) + " ถูกใส่ให้ทั้ง " + taken[name] + " และ " + key + " ต้องเป็นคนละตัวกัน")
        taken[name] = key

    template = json.loads((SITES / site["capabilities"]).read_text(encoding="utf-8"))
    caps = fill(template, names)
    if "{{" in json.dumps(caps, ensure_ascii=False):
        raise Stop("ใส่ชื่อ connector ไม่ครบทุกช่อง")

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    copy = out / site["page"]
    shutil.copyfile(str(page), str(copy))
    if sha256(copy) != site["sha256"]:
        raise Stop("คัดลอกไฟล์หน้าเว็บแล้วไฟล์เพี้ยน ลองใหม่อีกครั้ง")
    caps_path = out / (site_id + "-capabilities.json")
    caps_path.write_text(json.dumps(caps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "ok": True, "site": site_id, "title": site["title"], "version": site["version"],
        "page": str(copy), "sha256": site["sha256"], "capabilities": caps,
        "connectors": names,
        "probes": {k: {"connector": names[k], "tool": spec["probe"], "optional": bool(spec.get("optional"))}
                   for k, spec in wanted.items()},
    }


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Thai text on any console
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Prepare a MaxxGPT site for publishing.")
    ap.add_argument("site")
    ap.add_argument("--connector", action="append", metavar="KEY=NAME")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        result = prepare(args.site, args.connector, args.out)
    except Stop as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
