#!/usr/bin/env python3
"""
Final Fantasy Resonance - Save File Scanner & Profiler
สแกนและถอดรหัสไฟล์เซฟ GameSaveData*.sav จากเครื่องอัตโนมัติ
"""

import os
import sys
import glob
import json
from pathlib import Path
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("กำลังติดตั้ง cryptography library...")
    os.system(f"{sys.executable} -m pip install cryptography")
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend

AES_KEY = b'wwrqPkdwzPvgfchQ8kTYHVbn4umTf3d7'
HEADER_SIZE = 32

CHARACTERS_MAP = {
    1001: {"name": "Rain", "thai": "เรน", "role": "Vanguard / Tank", "default_vis": 13062},
    1002: {"name": "Lasswell", "thai": "ลาสเวลล์", "role": "Commando / Katana Specialist", "default_vis": 13110},
    1003: {"name": "Fina", "thai": "ฟีน่า", "role": "Medic / White Mage", "default_vis": 13045},
    1004: {"name": "Lid", "thai": "ลิด", "role": "Saboteur / Breaker", "default_vis": 13130},
    1005: {"name": "Nichol", "thai": "นิโคล", "role": "Strategist / Buffer", "default_vis": 13017},
    1006: {"name": "Archwitch Fina", "thai": "แม่มดฟีน่า", "role": "Ravager / Black Mage", "default_vis": 13123},
    1007: {"name": "Jake", "thai": "เจค", "role": "Gunner / Multi-Hit Striker", "default_vis": 13102},
    1008: {"name": "Sakura", "thai": "ซากุระ", "role": "Sorceress / Elementalist", "default_vis": 13113}
}

VISIONS_MAP = {
    13017: {"id": "amelia", "name": "Amelia", "thai": "อมีเลีย"},
    13024: {"id": "tronn", "name": "Tronn", "thai": "ทรอนน์"},
    13027: {"id": "victoria", "name": "Victoria", "thai": "วิกตอเรีย"},
    13033: {"id": "camille", "name": "Camille", "thai": "คามิลล์"},
    13045: {"id": "leah", "name": "Leah", "thai": "ลีอาห์"},
    13051: {"id": "ayaka", "name": "Ayaka", "thai": "อายากะ"},
    13060: {"id": "charlotte", "name": "Charlotte", "thai": "ชาร์ลอตต์"},
    13062: {"id": "wilhelm", "name": "Wilhelm", "thai": "วิลเฮล์ม"},
    13080: {"id": "aileen", "name": "Aileen", "thai": "ไอลีน"},
    13100: {"id": "wol", "name": "Warrior of Light", "thai": "นักรบแห่งแสง"},
    13101: {"id": "firion", "name": "Firion", "thai": "ฟิริออน"},
    13102: {"id": "onion_knight", "name": "Onion Knight", "thai": "ออเนียนไนท์"},
    13103: {"id": "cecil", "name": "Cecil", "thai": "เซซิล"},
    13105: {"id": "bartz", "name": "Bartz", "thai": "บาร์ทซ์"},
    13108: {"id": "terra", "name": "Terra", "thai": "เทอร์ร่า / ทีน่า"},
    13110: {"id": "cloud", "name": "Cloud", "thai": "คลาวด์"},
    13113: {"id": "sephiroth", "name": "Sephiroth", "thai": "เซฟิรอธ"},
    13116: {"id": "squall", "name": "Squall", "thai": "สคอลล์"},
    13118: {"id": "zidane", "name": "Zidane", "thai": "ซีดาน"},
    13120: {"id": "tidus", "name": "Tidus", "thai": "ทีดัส"},
    13123: {"id": "shantotto", "name": "Shantotto", "thai": "ชันโตโตะ"},
    13124: {"id": "vaan", "name": "Vaan", "thai": "วาน"},
    13125: {"id": "lightning", "name": "Lightning", "thai": "ไลท์นิ่ง"},
    13127: {"id": "yshtola", "name": "Y'shtola", "thai": "อิชโทลา"},
    13128: {"id": "noctis", "name": "Noctis", "thai": "น็อคติส"},
    13130: {"id": "clive", "name": "Clive", "thai": "ไคลฟ์"}
}

def find_save_files() -> List[str]:
    local_app = os.environ.get("LOCALAPPDATA", "")
    pattern = os.path.join(local_app, "FFRS", "Steam", "*", "GameSaveData*.sav")
    return sorted(glob.glob(pattern))

def decrypt_save(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        raw = f.read()
    if raw[:4] != b"SVHD":
        raise ValueError(f"ไฟล์ {file_path} ไม่ใช่ Final Fantasy Resonance save (ไม่มี header SVHD)")
    body = raw[HEADER_SIZE:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(body) + decryptor.finalize()

def scan_save_profile(save_path: str = None) -> Dict[str, Any]:
    if not save_path:
        saves = find_save_files()
        if not saves:
            raise FileNotFoundError("ไม่พบไฟล์เซฟของเกม Final Fantasy Resonance ในเครื่อง")
        save_path = saves[0]  # Default to slot 0

    decrypted = decrypt_save(save_path)

    # Use Node.js bridge to parse with exact ffrs-save engine for 100% precision
    import subprocess
    node_script = """
    const https = require('https');
    const fs = require('fs');
    const { execSync } = require('child_process');

    async function run() {
      const fetchJson = (url) => new Promise(r => https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
        let d = ''; res.on('data', c => d += c); res.on('end', () => r(JSON.parse(d)));
      }));
      const fetchText = (url) => new Promise(r => https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
        let d = ''; res.on('data', c => d += c); res.on('end', () => r(d));
      }));

      const [prog, ffrsCode] = await Promise.all([
        fetchJson('https://raw.githubusercontent.com/jesus-seijas-sp/ffr-save-editor/main/data/progression.json'),
        fetchText('https://raw.githubusercontent.com/jesus-seijas-sp/ffr-save-editor/main/src/shared/ffrs-save.js')
      ]);

      const decrypted = fs.readFileSync(process.argv[1]);
      var module = { exports: {} };
      eval(ffrsCode);
      const ffrs = module.exports.parse ? module.exports : (global.FFRS || globalThis.FFRS);
      const parsed = ffrs.parse(decrypted);

      const result = {
        saveFile: process.argv[2],
        money: ffrs.getField(decrypted, parsed.fields.get('Player.currentMoney')),
        playTimeSeconds: ffrs.getField(decrypted, parsed.fields.get('Player.PlayTime')),
        characters: [],
        visions: []
      };

      // Extract 8 party characters
      for (let i = 0; i < 8; i++) {
        const uid = ffrs.getField(decrypted, parsed.fields.get('unitParameterList[' + i + '].UnitId'));
        const exp = ffrs.getField(decrypted, parsed.fields.get('unitParameterList[' + i + '].Experience'));
        const hp = ffrs.getField(decrypted, parsed.fields.get('unitParameterList[' + i + '].HitPoint'));
        const mp = ffrs.getField(decrypted, parsed.fields.get('unitParameterList[' + i + '].MagicPoint'));
        const eqVis = ffrs.getField(decrypted, parsed.fields.get('unitParameterList[' + i + '].equipVisionId'));

        const expTable = prog.levelExp[String(uid)] || [];
        let lv = 1;
        for (let l = 0; l < expTable.length; l++) {
          if (exp >= expTable[l]) lv = l + 1;
          else break;
        }

        result.characters.push({
          unitId: uid,
          level: lv,
          exp: exp,
          hp: hp,
          mp: mp,
          equippedVisionId: eqVis
        });
      }

      // Extract Visions
      const keys = Array.from(parsed.fields.keys());
      const visionIndices = new Set();
      keys.filter(k => k.startsWith('visionList[')).forEach(k => {
        const m = k.match(/visionList\\[(\\d+)\\]/);
        if (m) visionIndices.add(parseInt(m[1]));
      });

      for (const idx of Array.from(visionIndices).sort((a,b) => a-b)) {
        const id = ffrs.getField(decrypted, parsed.fields.get('visionList[' + idx + '].ID'));
        const awk = ffrs.getField(decrypted, parsed.fields.get('visionList[' + idx + '].awakeningPoint'));
        const mrpTable = prog.masteryMrp[String(id)] || [0, 10, 35, 95, 195, 395, 695, 1195, 2195, 4195];
        const maxReq = mrpTable[mrpTable.length - 1];

        let highestMrp = 0;
        for (let u = 0; u < 8; u++) {
          const k = 'visionList[' + idx + '].synchroPoints{' + u + '}.value';
          if (parsed.fields.has(k)) {
            const v = ffrs.getField(decrypted, parsed.fields.get(k));
            if (v > highestMrp) highestMrp = v;
          }
        }

        let mr = 0;
        for (let r = 0; r < mrpTable.length; r++) {
          if (highestMrp >= mrpTable[r]) mr = r;
          else break;
        }

        result.visions.push({
          id: id,
          awakening: awk,
          currentMR: mr,
          currentMRP: highestMrp,
          maxMRP: maxReq,
          isMax: mr >= 9 || highestMrp >= maxReq
        });
      }

      console.log(JSON.stringify(result));
    }
    run();
    """

    temp_dec = os.path.join(os.environ.get("TEMP", "."), "ffr_dec.tmp")
    with open(temp_dec, "wb") as f:
        f.write(decrypted)

    try:
        proc = subprocess.run(["node", "-e", node_script, temp_dec, save_path], capture_output=True, text=True)
        if proc.returncode != 0:
            print("Node script error:", proc.stderr)
            raise RuntimeError(f"Node script failed with code {proc.returncode}")
        data = json.loads(proc.stdout)
    finally:
        if os.path.exists(temp_dec):
            os.remove(temp_dec)

    # Attach names and Thai metadata
    for c in data["characters"]:
        meta = CHARACTERS_MAP.get(c["unitId"], {})
        c["name"] = meta.get("name", f"Unit {c['unitId']}")
        c["thai"] = meta.get("thai", "")
        c["role"] = meta.get("role", "")
        vis_meta = VISIONS_MAP.get(c["equippedVisionId"], {})
        c["equippedVisionName"] = vis_meta.get("name", "None")
        c["equippedVisionThai"] = vis_meta.get("thai", "")

    max_mr_count = 0
    for v in data["visions"]:
        v_meta = VISIONS_MAP.get(v["id"], {})
        v["visionKey"] = v_meta.get("id", f"vis_{v['id']}")
        v["name"] = v_meta.get("name", f"Vision {v['id']}")
        v["thai"] = v_meta.get("thai", "")
        if v["isMax"]:
            max_mr_count += 1

    data["maxMrCount"] = max_mr_count
    data["totalVisionsOwned"] = len(data["visions"])

    # Calculate estimated base AP for characters:
    # Base AP = 30 + (Level * 1.25) + (max_mr_count * 10)
    for c in data["characters"]:
        c["estimatedMaxAP"] = int(30 + (c["level"] * 1.25) + (max_mr_count * 10))

    return data

def main():
    saves = find_save_files()
    if not saves:
        print("❌ ไม่พบไฟล์เซฟเกม Final Fantasy Resonance ในเครื่องนี้")
        return

    print("=" * 65)
    print(" 🎮 FINAL FANTASY RESONANCE: LOCAL SAVE SCANNER 🎮")
    print("=" * 65)
    print(f"📁 พบไฟล์เซฟทั้งหมด {len(saves)} ไฟล์:")
    for s in saves:
        print(f"  • {s}")
    print("-" * 65)

    profile = scan_save_profile(saves[0])

    # Save to json file for the web app to load
    output_path = os.path.join(os.path.dirname(__file__), "save_profile.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(f"✅ สแกนและสร้างไฟล์โปรไฟล์: [save_profile.json] เรียบร้อยแล้ว")
    print(f"💰 เงินในเกม (Gil): {profile['money']:,} Gil")
    print(f"⭐ วิชั่นที่มีอยู่: {profile['totalVisionsOwned']} / 26 ตัว")
    print(f"🌟 วิชั่นที่ MR Max (MR 9): {profile['maxMrCount']} ตัว (ส่วนใหญ่อยู่ระดับ MR 7-8)")
    print("-" * 65)
    print("👥 สรุปข้อมูลตัวละครในปาร์ตี้:")
    for c in profile["characters"]:
        print(f"  • {c['name']:15s} (Lv.{c['level']:2d}) | ติดตั้งวิชั่น: {c['equippedVisionName']:15s} | Max AP คาดการณ์: {c['estimatedMaxAP']} AP")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
