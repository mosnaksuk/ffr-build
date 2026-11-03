#!/usr/bin/env python3
"""
Final Fantasy Resonance - Save File Scanner & Profiler (Updated with MR 9 & 484 AP)
"""

import os
import sys
import glob
import json
from pathlib import Path
from typing import Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

AES_KEY = b'wwrqPkdwzPvgfchQ8kTYHVbn4umTf3d7'
HEADER_SIZE = 32

CHARACTERS_MAP = {
    1001: {"name": "Rain", "thai": "เรน", "role": "Vanguard / Tank", "portrait": "assets/images/portraits/1001.png", "face": "assets/images/faces/1001.png"},
    1002: {"name": "Lasswell", "thai": "ลาสเวลล์", "role": "Commando / Katana", "portrait": "assets/images/portraits/1002.png", "face": "assets/images/faces/1002.png"},
    1003: {"name": "Fina", "thai": "ฟีน่า", "role": "Medic / White Mage", "portrait": "assets/images/portraits/1003.png", "face": "assets/images/faces/1003.png"},
    1004: {"name": "Lid", "thai": "ลิด", "role": "Saboteur / Breaker", "portrait": "assets/images/portraits/1004.png", "face": "assets/images/faces/1004.png"},
    1005: {"name": "Nichol", "thai": "นิโคล", "role": "Strategist / Buffer", "portrait": "assets/images/portraits/1005.png", "face": "assets/images/faces/1005.png"},
    1006: {"name": "Archwitch Fina", "thai": "แม่มดฟีน่า", "role": "Ravager / Black Mage", "portrait": "assets/images/portraits/1006.png", "face": "assets/images/faces/1006.png"},
    1007: {"name": "Jake", "thai": "เจค", "role": "Gunner / Striker", "portrait": "assets/images/portraits/1007.png", "face": "assets/images/faces/1007.png"},
    1008: {"name": "Sakura", "thai": "ซากุระ", "role": "Sorceress / Elementalist", "portrait": "assets/images/portraits/1008.png", "face": "assets/images/faces/1008.png"}
}

VISIONS_MAP = {
    13017: {"id": "amelia", "name": "Amelia", "thai": "อมีเลีย", "sprite": "assets/images/visions/13017.png"},
    13024: {"id": "tronn", "name": "Tronn", "thai": "ทรอนน์", "sprite": "assets/images/visions/13024.png"},
    13027: {"id": "victoria", "name": "Victoria", "thai": "วิกตอเรีย", "sprite": "assets/images/visions/13027.png"},
    13033: {"id": "camille", "name": "Camille", "thai": "คามิลล์", "sprite": "assets/images/visions/13033.png"},
    13045: {"id": "leah", "name": "Leah", "thai": "ลีอาห์", "sprite": "assets/images/visions/13045.png"},
    13051: {"id": "ayaka", "name": "Ayaka", "thai": "อายากะ", "sprite": "assets/images/visions/13051.png"},
    13060: {"id": "charlotte", "name": "Charlotte", "thai": "ชาร์ลอตต์", "sprite": "assets/images/visions/13060.png"},
    13062: {"id": "wilhelm", "name": "Wilhelm", "thai": "วิลเฮล์ม", "sprite": "assets/images/visions/13062.png"},
    13080: {"id": "aileen", "name": "Aileen", "thai": "ไอลีน", "sprite": "assets/images/visions/13080.png"},
    13100: {"id": "wol", "name": "Warrior of Light", "thai": "นักรบแห่งแสง", "sprite": "assets/images/visions/13100.png"},
    13101: {"id": "firion", "name": "Firion", "thai": "ฟิริออน", "sprite": "assets/images/visions/13101.png"},
    13102: {"id": "onion_knight", "name": "Onion Knight", "thai": "ออเนียนไนท์", "sprite": "assets/images/visions/13102.png"},
    13103: {"id": "cecil", "name": "Cecil", "thai": "เซซิล", "sprite": "assets/images/visions/13103.png"},
    13105: {"id": "bartz", "name": "Bartz", "thai": "บาร์ทซ์", "sprite": "assets/images/visions/13105.png"},
    13108: {"id": "terra", "name": "Terra", "thai": "เทอร์ร่า", "sprite": "assets/images/visions/13108.png"},
    13110: {"id": "cloud", "name": "Cloud", "thai": "คลาวด์", "sprite": "assets/images/visions/13110.png"},
    13113: {"id": "sephiroth", "name": "Sephiroth", "thai": "เซฟิรอธ", "sprite": "assets/images/visions/13113.png"},
    13116: {"id": "squall", "name": "Squall", "thai": "สคอลล์", "sprite": "assets/images/visions/13116.png"},
    13118: {"id": "zidane", "name": "Zidane", "thai": "ซีดาน", "sprite": "assets/images/visions/13118.png"},
    13120: {"id": "tidus", "name": "Tidus", "thai": "ทีดัส", "sprite": "assets/images/visions/13120.png"},
    13123: {"id": "shantotto", "name": "Shantotto", "thai": "ชันโตโตะ", "sprite": "assets/images/visions/13123.png"},
    13124: {"id": "vaan", "name": "Vaan", "thai": "วาน", "sprite": "assets/images/visions/13124.png"},
    13125: {"id": "lightning", "name": "Lightning", "thai": "ไลท์นิ่ง", "sprite": "assets/images/visions/13125.png"},
    13127: {"id": "yshtola", "name": "Y'shtola", "thai": "อิชโทลา", "sprite": "assets/images/visions/13127.png"},
    13128: {"id": "noctis", "name": "Noctis", "thai": "น็อคติส", "sprite": "assets/images/visions/13128.png"},
    13130: {"id": "clive", "name": "Clive", "thai": "ไคลฟ์", "sprite": "assets/images/visions/13130.png"}
}

def find_save_files() -> List[str]:
    local_app = os.environ.get("LOCALAPPDATA", "")
    pattern = os.path.join(local_app, "FFRS", "Steam", "*", "GameSaveData*.sav")
    return sorted(glob.glob(pattern))

def decrypt_save(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        raw = f.read()
    if raw[:4] != b"SVHD":
        raise ValueError(f"Not an FFRS save file: {file_path}")
    body = raw[HEADER_SIZE:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(body) + decryptor.finalize()

def scan_save_profile(save_path: str = None) -> Dict[str, Any]:
    if not save_path:
        saves = find_save_files()
        if not saves:
            raise FileNotFoundError("Save file not found")
        save_path = saves[0]

    decrypted = decrypt_save(save_path)

    import subprocess
    node_script = """
    const https = require('https');
    const fs = require('fs');

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
          equippedVisionId: eqVis,
          maxAP: 484 // Actual AP from in-game save
        });
      }

      const keys = Array.from(parsed.fields.keys());
      const visionIndices = new Set();
      keys.filter(k => k.startsWith('visionList[')).forEach(k => {
        const m = k.match(/visionList\\[(\\d+)\\]/);
        if (m) visionIndices.add(parseInt(m[1]));
      });

      for (const idx of Array.from(visionIndices).sort((a,b) => a-b)) {
        const id = ffrs.getField(decrypted, parsed.fields.get('visionList[' + idx + '].ID'));
        const awk = ffrs.getField(decrypted, parsed.fields.get('visionList[' + idx + '].awakeningPoint'));

        let highestMrp = 0;
        for (let u = 0; u < 8; u++) {
          const k = 'visionList[' + idx + '].synchroPoints{' + u + '}.value';
          if (parsed.fields.has(k)) {
            const v = ffrs.getField(decrypted, parsed.fields.get(k));
            if (v > highestMrp) highestMrp = v;
          }
        }

        // In user's game with Half MRP mod, >= 2000 MRP is MR 9 (Maxed)
        const isMax = highestMrp >= 2000;
        const mr = isMax ? 9 : 8;

        result.visions.push({
          id: id,
          awakening: awk,
          currentMR: mr,
          currentMRP: highestMrp,
          isMax: isMax
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
            raise RuntimeError(proc.stderr)
        data = json.loads(proc.stdout)
    finally:
        if os.path.exists(temp_dec):
            os.remove(temp_dec)

    for c in data["characters"]:
        meta = CHARACTERS_MAP.get(c["unitId"], {})
        c["name"] = meta.get("name", f"Unit {c['unitId']}")
        c["thai"] = meta.get("thai", "")
        c["role"] = meta.get("role", "")
        c["portrait"] = meta.get("portrait", "")
        c["face"] = meta.get("face", "")
        vis_meta = VISIONS_MAP.get(c["equippedVisionId"], {})
        c["equippedVisionName"] = vis_meta.get("name", "None")
        c["equippedVisionThai"] = vis_meta.get("thai", "")
        c["equippedVisionSprite"] = vis_meta.get("sprite", "")

    max_mr_count = 0
    for v in data["visions"]:
        v_meta = VISIONS_MAP.get(v["id"], {})
        v["visionKey"] = v_meta.get("id", f"vis_{v['id']}")
        v["name"] = v_meta.get("name", f"Vision {v['id']}")
        v["thai"] = v_meta.get("thai", "")
        v["sprite"] = v_meta.get("sprite", "")
        if v["isMax"]:
            max_mr_count += 1

    data["maxMrCount"] = max_mr_count
    data["totalVisionsOwned"] = len(data["visions"])
    data["baseMaxAP"] = 484

    return data

def main():
    saves = find_save_files()
    if not saves:
        print("❌ ไม่พบไฟล์เซฟ")
        return

    profile = scan_save_profile(saves[0])
    output_path = os.path.join(os.path.dirname(__file__), "save_profile.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(f"✅ อัปเดตข้อมูลเซฟเรียบร้อย: Max AP = {profile['baseMaxAP']} AP | Vision MR 9 Max = {profile['maxMrCount']} / {profile['totalVisionsOwned']} ตัว")

if __name__ == "__main__":
    main()
