#!/usr/bin/env python3
"""
Final Fantasy Resonance - Vision & AP Build Optimizer CLI
รองรับการอ่านเซฟเกมในเครื่องโดยตรง พร้อมระบบคำนวณแยกตามตัวละคร และสายการเล่น
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Database of all Visions and key passives
VISIONS_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "wilhelm", "name": "Wilhelm", "thai": "วิลเฮล์ม", "role": "tank",
        "passives": [
            {"id": "wilhelm_bastion", "name": "Bastion", "thai": "กำแพงปราการ (ลดดาเมจทีม 20%)", "ap": 30, "score": 9.0, "role": "tank", "desc": "ลดทอนความเสียหายให้เพื่อนทั้งทีม 20% ขณะเข้าท่า Guard"},
            {"id": "wilhelm_crit_counter", "name": "Critical Counter", "thai": "สวนกลับคริติคอล", "ap": 35, "score": 7.5, "role": "tank", "desc": "สวนกลับด้วยความรุนแรงเมื่อถูกโจมตีติดคริติคอล"},
            {"id": "wilhelm_pdef", "name": "Physical Defense +30%", "thai": "พลังป้องกันกายภาพ +30%", "ap": 50, "score": 8.0, "role": "tank", "desc": "เพิ่มค่าพลังป้องกันกายภาพขึ้น 30%"},
        ]
    },
    {
        "id": "wol", "name": "Warrior of Light", "thai": "นักรบแห่งแสง", "role": "tank",
        "passives": [
            {"id": "wol_phys_def", "name": "Physical Damage Reduction 20%", "thai": "ลดดาเมจกายภาพ 20%", "ap": 35, "score": 8.5, "role": "tank", "desc": "ลดทอนความเสียหายทางกายภาพ 20%"},
            {"id": "wol_stagger_power", "name": "Stagger Power +30%", "thai": "เกจ Stagger +30%", "ap": 45, "score": 8.8, "role": "breaker", "desc": "สะสมเกจเบรคศัตรูเร็วที่สุดในเกม"},
            {"id": "wol_counter", "name": "Physical Counter", "thai": "สวนกลับ 30%", "ap": 25, "score": 7.2, "role": "tank", "desc": "มีโอกาส 30% สวนกลับทันทีเมื่อถูกโจมตี"},
        ]
    },
    {
        "id": "charlotte", "name": "Charlotte", "thai": "ชาร์ลอตต์", "role": "tank",
        "passives": [
            {"id": "charlotte_shell", "name": "Auto-Shell", "thai": "เปิดเทิร์นด้วยเกราะ Shell", "ap": 20, "score": 8.0, "role": "tank", "desc": "รับบัฟ Shell ลดดาเมจเวททันทีเมื่อเริ่มสู้"},
            {"id": "charlotte_protection", "name": "Royal Protection", "thai": "รับดาเมจแทนเพื่อน (Cover)", "ap": 35, "score": 8.5, "role": "tank", "desc": "สละตัวรับการโจมตีอันตรายแทนเพื่อน"},
        ]
    },
    {
        "id": "cecil", "name": "Cecil", "thai": "เซซิล", "role": "tank",
        "passives": [
            {"id": "cecil_pdef", "name": "Physical Defense +20%", "thai": "พลังป้องกันกายภาพ +20%", "ap": 40, "score": 7.8, "role": "tank", "desc": "เพิ่มค่าพลังป้องกันกายภาพ 20%"},
            {"id": "cecil_dark_imm", "name": "Dark Immunity", "thai": "ดูดซับธาตุมืด", "ap": 30, "score": 7.0, "role": "tank", "desc": "ป้องกันและดูดซับการโจมตีธาตุมืดทั้งหมด"},
        ]
    },
    {
        "id": "firion", "name": "Firion", "thai": "ฟิริออน", "role": "phys_dps",
        "passives": [
            {"id": "firion_arms_akimbo", "name": "Arms Akimbo", "thai": "สองมือสองใจ (2 แอคชั่น/เทิร์น)", "ap": 20, "score": 10.0, "role": "phys_dps", "desc": "ทำแอคชั่นได้ 2 ครั้งต่อเทิร์น (คุ้มค่าที่สุดในเกม)"},
            {"id": "firion_blood_weapon", "name": "Blood Weapon", "thai": "ดาบดูดเลือด (Lifesteal 10%)", "ap": 25, "score": 7.8, "role": "phys_dps", "desc": "ดูดเลือด 10% จากความเสียหายกายภาพ"},
        ]
    },
    {
        "id": "squall", "name": "Squall", "thai": "สคอลล์", "role": "phys_dps",
        "passives": [
            {"id": "squall_improvement", "name": "Improvement", "thai": "ยิ่งสู้อารมณ์ยิ่งพุ่ง (ดาเมจ/Stagger +50%)", "ap": 20, "score": 9.8, "role": "phys_dps", "desc": "เพิ่มดาเมจและเกจ Stagger สูงสุด 50% ตามจำนวนแอคชั่น (ซินเนอร์จี้ 100% กับ Arms Akimbo)"},
            {"id": "squall_atk30", "name": "Physical Attack +30%", "thai": "พลังโจมตีกายภาพ +30%", "ap": 60, "score": 8.2, "role": "phys_dps", "desc": "เพิ่มค่า Atk พื้นฐาน 30%"},
        ]
    },
    {
        "id": "cloud", "name": "Cloud", "thai": "คลาวด์", "role": "phys_dps",
        "passives": [
            {"id": "cloud_crit_boost", "name": "Critical Boost", "thai": "ความแรงคริติคอล +35%", "ap": 40, "score": 9.0, "role": "phys_dps", "desc": "คูณความเสียหายคริติคอลขึ้น 35%"},
            {"id": "cloud_crit_rate", "name": "Critical Hit Rate +10%", "thai": "โอกาสคริ +10%", "ap": 25, "score": 7.5, "role": "phys_dps", "desc": "เพิ่มอัตราคริติคอลพื้นฐาน 10%"},
            {"id": "cloud_crit_mp", "name": "Restore MP on Crit", "thai": "ฟื้น MP 3% เมื่อคริ", "ap": 20, "score": 7.6, "role": "phys_dps", "desc": "ฟื้น MP 3% เมื่อโจมตีติดคริติคอล"},
        ]
    },
    {
        "id": "tidus", "name": "Tidus", "thai": "ทีดัส", "role": "breaker",
        "passives": [
            {"id": "tidus_first_strike", "name": "First Strike", "thai": "การันตีเริ่มคนแรกสุด", "ap": 20, "score": 9.9, "role": "breaker", "desc": "รับประกันเริ่มเทิร์นก่อนใครในสนาม"},
            {"id": "tidus_tiptop", "name": "Tip-Top Shape", "thai": "+25% Dmg เมื่อ HP > 80%", "ap": 30, "score": 7.8, "role": "phys_dps", "desc": "เพิ่มพลังโจมตี 25% หาก HP สูง"},
        ]
    },
    {
        "id": "tronn", "name": "Tronn", "thai": "ทรอนน์", "role": "support",
        "passives": [
            {"id": "tronn_half_mp", "name": "Half MP Cost", "thai": "ลดค่าร่าย MP ลงครึ่งหนึ่ง", "ap": 50, "score": 9.8, "role": "magic_dps", "desc": "ลดการใช้ MP ทุกชนิดลง 50% วงจรร่ายเวท/เบิ้ลสกิลไม่สะดุด"},
            {"id": "tronn_stagger_mp", "name": "Restore MP on Stagger", "thai": "ฟื้น MP 5% เมื่อศัตรู Stagger", "ap": 20, "score": 7.8, "role": "breaker", "desc": "ฟื้นฟู 5% MP เมื่อเบรคศัตรูได้"},
            {"id": "tronn_stagger_power", "name": "Stagger Power +20%", "thai": "เกจ Stagger +20%", "ap": 40, "score": 8.2, "role": "breaker", "desc": "สะสมเกจเบรคศัตรูเร็วขึ้น 20%"},
        ]
    },
    {
        "id": "shantotto", "name": "Shantotto", "thai": "ชันโตโตะ", "role": "magic_dps",
        "passives": [
            {"id": "shantotto_aoe", "name": "Area Effect Adept", "thai": "เวทหมู่พลังเต็ม 100% ไม่หารเฉลี่ย", "ap": 40, "score": 9.0, "role": "magic_dps", "desc": "เวทหมู่ได้ความแรงเต็มทุกตัว (ใช้คู่กับ Half MP Cost)"},
            {"id": "shantotto_dark_rite", "name": "Dark Rite", "thai": "พิธีมืด (เวทแรงขึ้นตาม HP ต่ำ)", "ap": 20, "score": 7.6, "role": "magic_dps", "desc": "ยิ่งมี HP ต่ำ พลังเวทจะยิ่งรุนแรงขึ้น"},
        ]
    },
    {
        "id": "terra", "name": "Terra", "thai": "เทอร์ร่า", "role": "magic_dps",
        "passives": [
            {"id": "terra_lb_double", "name": "LB Double Charge", "thai": "เกจ Limit Break เต็มไว 2 เท่า", "ap": 35, "score": 9.0, "role": "support", "desc": "เร่งเกจ Limit Break 200%"},
            {"id": "terra_break_limit", "name": "Break the Limit", "thai": "ดาเมจเวททะลุ 9,999", "ap": 45, "score": 8.8, "role": "magic_dps", "desc": "ปลดล็อคเพดานดาเมจเวทมนตร์"},
        ]
    },
    {
        "id": "bartz", "name": "Bartz", "thai": "บาร์ทซ์", "role": "phys_dps",
        "passives": [
            {"id": "bartz_dual_spellblade", "name": "Dual Spellblade", "thai": "เวทดาบคู่ (Spellblade ฟัน 2 ครั้ง)", "ap": 40, "score": 9.0, "role": "phys_dps", "desc": "สกิล Spellblade ฟันซ้ำอีกครั้ง"},
        ]
    },
    {
        "id": "onion_knight", "name": "Onion Knight", "thai": "ออเนียนไนท์", "role": "support",
        "passives": [
            {"id": "onion_lb_triple", "name": "LB Triple Charge", "thai": "เกจ Limit Break เต็มไว 3 เท่า", "ap": 50, "score": 9.6, "role": "support", "desc": "เร่งเกจ Limit Break ขึ้น 300%"},
        ]
    },
    {
        "id": "ayaka", "name": "Ayaka", "thai": "อายากะ", "role": "healer",
        "passives": [
            {"id": "ayaka_lb_heal", "name": "LB Charge on Heal", "thai": "ฮีลเพื่อนชาร์จ LB +25%", "ap": 20, "score": 9.5, "role": "support", "desc": "ฮีลฟื้นฟูเกจ Limit Break 25% ทันที ใช้แค่ 20 AP"},
            {"id": "ayaka_hand_heals", "name": "The Hand That Heals", "thai": "+50% Dmg & Stagger เมื่อฮีล", "ap": 35, "score": 8.6, "role": "healer", "desc": "ฮีลเพื่อนแล้วตัวเราเองเก่งขึ้น"},
        ]
    },
    {
        "id": "leah", "name": "Leah", "thai": "ลีอาห์", "role": "healer",
        "passives": [
            {"id": "leah_pharmacology", "name": "Pharmacology", "thai": "ไอเทมแรงขึ้น +50%", "ap": 30, "score": 7.5, "role": "healer", "desc": "เพิ่มผลการฟื้นฟูของไอเทมขึ้น 50%"},
        ]
    },
    {
        "id": "clive", "name": "Clive", "thai": "ไคลฟ์", "role": "phys_dps",
        "passives": [
            {"id": "clive_lb_dmg", "name": "Limit Burst Damage +40%", "thai": "ความแรง Limit Break +40%", "ap": 45, "score": 9.0, "role": "phys_dps", "desc": "ทวีคูณดาเมจท่าไม้ตาย 40%"},
        ]
    },
    {
        "id": "amelia", "name": "Amelia", "thai": "อมีเลีย", "role": "breaker",
        "passives": [
            {"id": "amelia_deprotect", "name": "Deprotect Opener", "thai": "เปิดฉากลดเกราะศัตรูทั้งสนาม", "ap": 25, "score": 9.2, "role": "breaker", "desc": "ร่าย Deprotect ใส่ศัตรูทุกตัวทันทีที่เริ่มสู้"},
        ]
    },
    {
        "id": "zidane", "name": "Zidane", "thai": "ซีดาน", "role": "breaker",
        "passives": [
            {"id": "zidane_aggravation", "name": "Aggravation", "thai": "+60% Dmg เมื่อศัตรูมีดีบัฟ", "ap": 25, "score": 9.2, "role": "phys_dps", "desc": "โบนัสดาเมจสูงสุด 60% เมื่อเป้าหมายมีดีบัฟ"},
        ]
    },
    {
        "id": "victoria", "name": "Victoria", "thai": "วิกตอเรีย", "role": "mrp_farm",
        "passives": [
            {"id": "victoria_mrp", "name": "MRP Gain +50%", "thai": "ฟาร์มแต้มวิชั่น MRP +50%", "ap": 30, "score": 10.0, "role": "mrp_farm", "desc": "เร่งการปลดล็อค MR 9 ของวิชั่นทุกตัวเร็วขึ้นเท่าตัว"},
        ]
    }
]

def calculate_max_ap(level: int, max_mr_count: int) -> int:
    # In-Game Verified Formula at Lv.42:
    # Base Character AP = 100
    # Each MR 9 Vision = +16 AP
    # 24 Visions = 100 + (24 * 16) = 484 AP (matches in-game save exactly)
    # 26 Visions = 100 + (26 * 16) = 516 AP
    base_ap = 100
    if level < 42:
        base_ap = int(round(30 + (level * 1.66)))
    return base_ap + (max_mr_count * 16)

def optimize_for_role(role: str, ap_budget: int, base_vis: str = "") -> Dict[str, Any]:
    available = []
    
    # Define role-specific matching
    role_weights = {
        "tank": {"tank": 6.0, "breaker": 1.0, "support": 1.0},
        "phys_dps": {"phys_dps": 6.0, "breaker": 2.0},
        "magic_dps": {"magic_dps": 7.0, "support": 1.5},
        "support": {"support": 6.0, "healer": 3.0, "breaker": 1.5},
        "healer": {"healer": 7.0, "support": 3.0},
        "mrp_farm": {"mrp_farm": 10.0, "breaker": 2.0, "phys_dps": 1.5}
    }

    for v in VISIONS_DATABASE:
        for p in v["passives"]:
            score = p["score"]
            p_role = p["role"]

            # Role filtering/weighting
            weights_map = role_weights.get(role, {})
            if p_role in weights_map:
                score += weights_map[p_role]
            elif role != "all":
                # Heavily down-weight irrelevant roles (e.g. squall improvement in a pure tank build)
                score -= 4.0

            # Must-have key traits
            if role == "mrp_farm" and p["id"] == "victoria_mrp":
                score += 15.0
            if role == "tank" and p["id"] in ["wilhelm_bastion", "wol_phys_def", "charlotte_shell"]:
                score += 5.0
            if role == "healer" and p["id"] in ["ayaka_hand_heals", "ayaka_lb_heal"]:
                score += 6.0
            if role == "magic_dps" and p["id"] in ["tronn_half_mp", "shantotto_aoe", "terra_break_limit"]:
                score += 5.0
            if role == "support" and p["id"] in ["onion_lb_triple", "ayaka_lb_heal", "amelia_deprotect"]:
                score += 5.0
            
            if base_vis and v["id"] == base_vis:
                score += 1.5

            if score > 0:
                available.append({
                    **p,
                    "vision_name": v["name"],
                    "vision_thai": v["thai"],
                    "effective_score": score
                })

    # 0/1 Knapsack DP
    n = len(available)
    dp = [[0.0] * (ap_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = available[i - 1]
        w = item["ap"]
        v = item["effective_score"]
        for cap in range(ap_budget + 1):
            if w <= cap:
                val_with = dp[i - 1][cap - w] + v
                val_without = dp[i - 1][cap]
                dp[i][cap] = max(val_without, val_with)
            else:
                dp[i][cap] = dp[i - 1][cap]

    selected = []
    cap = ap_budget
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            selected.append(available[i - 1])
            cap -= available[i - 1]["ap"]

    selected.reverse()
    total_ap = sum(s["ap"] for s in selected)
    return {
        "selected": selected,
        "total_ap": total_ap,
        "remaining_ap": ap_budget - total_ap,
        "budget": ap_budget
    }

def main():
    parser = argparse.ArgumentParser(description="FF Resonance Character & Role Build Optimizer")
    parser.add_argument("--char", type=str, default="Rain", help="Character Name (Rain, Lasswell, Fina, Lid, Nichol, Archwitch Fina, Jake, Sakura)")
    parser.add_argument("--base_vis", type=str, default="", help="Equipped Base Vision Key (e.g. wilhelm, cloud, shantotto)")
    parser.add_argument("--level", type=int, default=42, help="Character Level (default: 42)")
    parser.add_argument("--max_mr", type=int, default=0, help="Number of Visions with Max MR (MR 9) (default: 0)")
    parser.add_argument("--ap", type=int, default=None, help="Direct Max AP override (if not set, calculated from level and max_mr)")
    parser.add_argument("--role", type=str, default="all", choices=["tank", "phys_dps", "magic_dps", "support", "healer", "mrp_farm", "all"], help="Build Role")
    args = parser.parse_args()

    # Load save_profile.json if exists to sync defaults
    prof_path = os.path.join(os.path.dirname(__file__), "save_profile.json")
    if os.path.exists(prof_path):
        try:
            with open(prof_path, "r", encoding="utf-8") as f:
                prof = json.load(f)
                matched_char = next((c for c in prof.get("characters", []) if c["name"].lower() == args.char.lower()), None)
                if matched_char and args.level == 42:
                    args.level = matched_char["level"]
                if matched_char and not args.base_vis:
                    args.base_vis = matched_char.get("equippedVisionName", "").lower()
                if args.max_mr == 0 and "maxMrCount" in prof:
                    args.max_mr = prof["maxMrCount"]
        except Exception:
            pass

    max_ap = args.ap if args.ap is not None else calculate_max_ap(args.level, args.max_mr)

    print("\n" + "=" * 65)
    print(" ⚡ FINAL FANTASY RESONANCE: CHARACTER & AP BUILD OPTIMIZER ⚡")
    print("=" * 65)
    print(f" ตัวละคร: {args.char} (Lv.{args.level}) | วิชั่นหลัก: {args.base_vis.capitalize() or 'None'}")
    print(f" จำนวน Vision Max MR: {args.max_mr} ตัว | Max AP คำนวณได้: {max_ap} AP")
    print("-" * 65)

    roles_to_run = ["tank", "phys_dps", "magic_dps", "support", "healer", "mrp_farm"] if args.role == "all" else [args.role]

    role_labels = {
        "tank": "🛡️ สายตั้งรับ (Tank / Defense)",
        "phys_dps": "⚔️ สายดาเมจกายภาพ (Physical DPS)",
        "magic_dps": "🔮 สายเวทมนตร์ (Magic / Caster)",
        "support": "💖 สาย Support & ปั๊ม Limit Break",
        "healer": "💚 สายฮีลเลอร์ (Healer / Medic)",
        "mrp_farm": "🌾 สายฟาร์มเร่งเวลวิชั่น (MRP Speed Farm)"
    }

    for r in roles_to_run:
        res = optimize_for_role(r, max_ap, args.base_vis)
        print(f"\n▶ {role_labels.get(r, r)} (ใช้ {res['total_ap']}/{max_ap} AP, เหลือ {res['remaining_ap']} AP):")
        for idx, s in enumerate(res["selected"], 1):
            print(f"   {idx}. [{s['ap']:2d} AP] {s['name']} ({s['thai']}) - จาก {s['vision_name']}")
            print(f"      └ {s['desc']}")

    print("\n" + "=" * 65 + "\n")

if __name__ == "__main__":
    main()
