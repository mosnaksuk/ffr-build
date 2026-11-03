#!/usr/bin/env python3
"""
Final Fantasy Resonance - Vision & AP Build Optimizer CLI
เครื่องมือค้นหาและจัดพาสซีฟที่คุ้มค่า AP ที่สุดตามวิชั่นที่มีอยู่
"""

import sys
import argparse
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Database of all 26 Visions and their key passives
VISIONS_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "firion",
        "name": "Firion",
        "thai": "ฟิริออน",
        "chapter": 3,
        "passives": [
            {"id": "firion_arms_akimbo", "name": "Arms Akimbo", "thai": "สองมือสองใจ (2 แอคชั่น/เทิร์น)", "ap": 20, "score": 10.0, "role": "phys_dps", "desc": "ทำแอคชั่นได้ 2 ครั้งต่อเทิร์น (คุ้มค่าที่สุดในเกม)"},
            {"id": "firion_blood_weapon", "name": "Blood Weapon", "thai": "ดาบดูดเลือด (Lifesteal 10%)", "ap": 25, "score": 7.5, "role": "phys_dps", "desc": "ดูดเลือด 10% จากความเสียหายกายภาพ"},
            {"id": "firion_arsenal", "name": "Arsenal Adaptability", "thai": "เจาะเกราะ 15%", "ap": 30, "score": 7.0, "role": "phys_dps", "desc": "เพิกเฉยต่อพลังป้องกัน 15%"},
        ]
    },
    {
        "id": "tidus",
        "name": "Tidus",
        "thai": "ทีดัส",
        "chapter": 3,
        "passives": [
            {"id": "tidus_first_strike", "name": "First Strike", "thai": "การันตีเริ่มคนแรกสุด", "ap": 20, "score": 9.8, "role": "breaker", "desc": "รับประกันเริ่มเทิร์นก่อนใครในสนาม"},
            {"id": "tidus_tiptop", "name": "Tip-Top Shape", "thai": "+25% Dmg เมื่อ HP > 80%", "ap": 30, "score": 7.8, "role": "phys_dps", "desc": "เพิ่มพลังโจมตี 25% หาก HP สูง"},
        ]
    },
    {
        "id": "tronn",
        "name": "Tronn",
        "thai": "ทรอนน์",
        "chapter": 1,
        "passives": [
            {"id": "tronn_half_mp", "name": "Half MP Cost", "thai": "ลดค่าร่าย MP ลงครึ่งหนึ่ง", "ap": 50, "score": 9.5, "role": "magic_dps", "desc": "ลดการใช้ MP ทุกชนิดลง 50% วงจรร่ายเวท/เบิ้ลสกิลไม่สะดุด"},
            {"id": "tronn_stagger_mp", "name": "Restore MP on Stagger", "thai": "ฟื้น MP 5% เมื่อศัตรู Stagger", "ap": 20, "score": 7.5, "role": "breaker", "desc": "ฟื้นฟู 5% MP เมื่อเบรคศัตรูได้"},
            {"id": "tronn_stagger_power", "name": "Stagger Power +20%", "thai": "เกจ Stagger +20%", "ap": 40, "score": 8.0, "role": "breaker", "desc": "สะสมเกจเบรคศัตรูเร็วขึ้น 20%"},
        ]
    },
    {
        "id": "squall",
        "name": "Squall",
        "thai": "สคอลล์",
        "chapter": 3,
        "passives": [
            {"id": "squall_improvement", "name": "Improvement", "thai": "ยิ่งสู้อารมณ์ยิ่งพุ่ง (ดาเมจ/Stagger +50%)", "ap": 20, "score": 9.5, "role": "phys_dps", "desc": "เพิ่มดาเมจและเกจ Stagger สูงสุด 50% ตามจำนวนแอคชั่น (ซินเนอร์จี้ 100% กับ Arms Akimbo)"},
            {"id": "squall_atk30", "name": "Physical Attack +30%", "thai": "พลังโจมตีกายภาพ +30%", "ap": 60, "score": 8.2, "role": "phys_dps", "desc": "เพิ่มค่า Atk พื้นฐาน 30%"},
        ]
    },
    {
        "id": "cloud",
        "name": "Cloud Strife",
        "thai": "คลาวด์",
        "chapter": 1,
        "passives": [
            {"id": "cloud_crit_boost", "name": "Critical Boost", "thai": "ความแรงคริติคอล +35%", "ap": 40, "score": 8.8, "role": "phys_dps", "desc": "คูณความเสียหายคริติคอลขึ้น 35%"},
            {"id": "cloud_crit_rate", "name": "Critical Hit Rate +10%", "thai": "โอกาสคริ +10%", "ap": 25, "score": 7.2, "role": "phys_dps", "desc": "เพิ่มอัตราคริติคอลพื้นฐาน 10%"},
            {"id": "cloud_crit_mp", "name": "Restore MP on Crit", "thai": "ฟื้น MP 3% เมื่อคริ", "ap": 20, "score": 7.5, "role": "phys_dps", "desc": "ฟื้น MP 3% เมื่อโจมตีติดคริติคอล"},
        ]
    },
    {
        "id": "terra",
        "name": "Terra",
        "thai": "ทีน่า / เทอร์ร่า",
        "chapter": 1,
        "passives": [
            {"id": "terra_lb_double", "name": "LB Double Charge", "thai": "เกจ Limit Break เต็มไว 2 เท่า", "ap": 35, "score": 8.9, "role": "support", "desc": "เร่งเกจ Limit Break 200%"},
            {"id": "terra_break_limit", "name": "Break the Limit", "thai": "ดาเมจเวททะลุ 9,999", "ap": 45, "score": 8.5, "role": "magic_dps", "desc": "ปลดล็อคเพดานดาเมจเวทมนตร์"},
        ]
    },
    {
        "id": "onion_knight",
        "name": "Onion Knight",
        "thai": "ออเนียนไนท์",
        "chapter": 2,
        "passives": [
            {"id": "onion_lb_triple", "name": "LB Triple Charge", "thai": "เกจ Limit Break เต็มไว 3 เท่า", "ap": 50, "score": 9.3, "role": "support", "desc": "เร่งเกจ Limit Break ขึ้น 300%"},
        ]
    },
    {
        "id": "zidane",
        "name": "Zidane",
        "thai": "ซีดาน",
        "chapter": 2,
        "passives": [
            {"id": "zidane_aggravation", "name": "Aggravation", "thai": "+60% Dmg เมื่อศัตรูมีดีบัฟ", "ap": 25, "score": 9.0, "role": "phys_dps", "desc": "โบนัสดาเมจสูงสุด 60% เมื่อเป้าหมายมีดีบัฟ"},
        ]
    },
    {
        "id": "shantotto",
        "name": "Shantotto",
        "thai": "ชันโตโตะ",
        "chapter": 4,
        "passives": [
            {"id": "shantotto_aoe", "name": "Area Effect Adept", "thai": "เวทหมู่พลังเต็ม 100% ไม่หารเฉลี่ย", "ap": 40, "score": 8.7, "role": "magic_dps", "desc": "เวทหมู่ได้ความแรงเต็มทุกตัว (ใช้คู่กับ Half MP Cost)"},
        ]
    },
    {
        "id": "bartz",
        "name": "Bartz",
        "thai": "บาร์ทซ์",
        "chapter": 5,
        "passives": [
            {"id": "bartz_dual_spellblade", "name": "Dual Spellblade", "thai": "เวทดาบคู่ (Spellblade แสดงผล 2 รอบ)", "ap": 40, "score": 8.9, "role": "phys_dps", "desc": "สกิล Spellblade ฟันซ้ำอีกครั้ง"},
        ]
    },
    {
        "id": "sephiroth",
        "name": "Sephiroth",
        "thai": "เซฟิรอธ",
        "chapter": 5,
        "passives": [
            {"id": "sephiroth_crit_rate", "name": "Critical Hit Rate +20%", "thai": "โอกาสคริ +20%", "ap": 40, "score": 8.4, "role": "phys_dps", "desc": "เพิ่มคริติคอลมหาศาล 20%"},
            {"id": "sephiroth_atk30", "name": "Physical Attack +30%", "thai": "พลังโจมตีกายภาพ +30%", "ap": 60, "score": 8.0, "role": "phys_dps", "desc": "พลังโจมตี +30%"},
        ]
    },
    {
        "id": "victoria",
        "name": "Victoria",
        "thai": "วิกตอเรีย",
        "chapter": 5,
        "passives": [
            {"id": "victoria_mrp", "name": "MRP Gain +50%", "thai": "ฟาร์มแต้มวิชั่น MRP +50%", "ap": 30, "score": 9.9, "role": "mrp_farm", "desc": "เร่งการปลดล็อค MR 9 ของวิชั่นทุกตัวเร็วขึ้นเท่าตัว"},
        ]
    },
    {
        "id": "ayaka",
        "name": "Ayaka",
        "thai": "อายากะ",
        "chapter": 7,
        "passives": [
            {"id": "ayaka_lb_heal", "name": "LB Charge on Heal", "thai": "ฮีลเพื่อนชาร์จ LB +25%", "ap": 20, "score": 9.4, "role": "support", "desc": "ฮีลฟื้นฟูเกจ Limit Break 25% ทันที ใช้แค่ 20 AP"},
            {"id": "ayaka_hand_heals", "name": "The Hand That Heals", "thai": "+50% Dmg & Stagger เมื่อฮีล", "ap": 35, "score": 8.5, "role": "support", "desc": "ฮีลเพื่อนแล้วตัวเราเองเก่งขึ้น"},
        ]
    },
    {
        "id": "wol",
        "name": "Warrior of Light",
        "thai": "นักรบแห่งแสง",
        "chapter": 1,
        "passives": [
            {"id": "wol_stagger_power", "name": "Stagger Power +30%", "thai": "เกจ Stagger +30%", "ap": 45, "score": 8.6, "role": "breaker", "desc": "สะสมเกจเบรคศัตรูเร็วที่สุดในเกม"},
            {"id": "wol_phys_def", "name": "Physical Damage Reduction 20%", "thai": "ลดดาเมจกายภาพ 20%", "ap": 35, "score": 7.7, "role": "tank", "desc": "ลดทอนความเสียหายทางกายภาพ 20%"},
        ]
    },
    {
        "id": "wilhelm",
        "name": "Wilhelm",
        "thai": "วิลเฮล์ม",
        "chapter": 5,
        "passives": [
            {"id": "wilhelm_bastion", "name": "Bastion", "thai": "ลดดาเมจทั้งทีม 20%", "ap": 30, "score": 8.5, "role": "tank", "desc": "ลดทอนความเสียหายให้ทีมทั้งปาร์ตี้ 20% ตอน Guard"},
        ]
    },
    {
        "id": "charlotte",
        "name": "Charlotte",
        "thai": "ชาร์ลอตต์",
        "chapter": 7,
        "passives": [
            {"id": "charlotte_shell", "name": "Auto-Shell", "thai": "เปิดเทิร์นด้วยเกราะ Shell", "ap": 20, "score": 7.8, "role": "tank", "desc": "รับบัฟ Shell ลดดาเมจเวททันทีเมื่อเริ่มสู้"},
            {"id": "charlotte_protection", "name": "Royal Protection", "thai": "รับดาเมจแทนเพื่อน (Cover)", "ap": 35, "score": 8.3, "role": "tank", "desc": "สละตัวรับการโจมตีอันตรายแทนเพื่อน"},
        ]
    },
    {
        "id": "clive",
        "name": "Clive",
        "thai": "ไคลฟ์",
        "chapter": 5,
        "passives": [
            {"id": "clive_lb_dmg", "name": "Limit Burst Damage +40%", "thai": "ความแรง Limit Break +40%", "ap": 45, "score": 8.7, "role": "phys_dps", "desc": "ทวีคูณดาเมจท่าไม้ตาย 40%"},
        ]
    },
    {
        "id": "amelia",
        "name": "Amelia",
        "thai": "อมีเลีย",
        "chapter": 6,
        "passives": [
            {"id": "amelia_deprotect", "name": "Deprotect Opener", "thai": "เปิดฉากลดเกราะศัตรูทั้งสนาม", "ap": 25, "score": 8.9, "role": "breaker", "desc": "ร่าย Deprotect ใส่ศัตรูทุกตัวทันทีที่เริ่มสู้"},
        ]
    }
]

def optimize_build(owned_visions: List[str], ap_budget: int, role: str) -> Dict[str, Any]:
    available_passives = []
    for v in VISIONS_DATABASE:
        if v["id"] in owned_visions or not owned_visions:  # if empty, assume all
            for p in v["passives"]:
                item = p.copy()
                item["vision_name"] = v["name"]
                available_passives.append(item)

    if not available_passives:
        return {"selected": [], "total_ap": 0, "remaining_ap": ap_budget, "ap_budget": ap_budget}

    # Calculate weighted efficiency
    for p in available_passives:
        weight = p["score"]
        if role == "all":
            pass
        elif role == p["role"]:
            weight += 3.0
        elif p["score"] >= 9.5:
            weight += 1.5
        p["effective_score"] = weight

    # 0/1 Knapsack Dynamic Programming for global optimum
    n = len(available_passives)
    dp = [[0.0] * (ap_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = available_passives[i - 1]
        w = item["ap"]
        v = item["effective_score"]
        for cap in range(ap_budget + 1):
            if w <= cap:
                val_with = dp[i - 1][cap - w] + v
                val_without = dp[i - 1][cap]
                dp[i][cap] = max(val_without, val_with)
            else:
                dp[i][cap] = dp[i - 1][cap]

    # Backtrack to find chosen items
    selected = []
    cap = ap_budget
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            item = available_passives[i - 1]
            selected.append(item)
            cap -= item["ap"]

    selected.reverse()
    total_ap = sum(s["ap"] for s in selected)
    remaining_ap = ap_budget - total_ap

    return {
        "selected": selected,
        "total_ap": total_ap,
        "remaining_ap": remaining_ap,
        "ap_budget": ap_budget
    }

def main():
    parser = argparse.ArgumentParser(description="FF Resonance Vision & AP Build Optimizer")
    parser.add_argument("--ap", type=int, default=100, help="Character AP Budget Limit (default: 100)")
    parser.add_argument("--role", type=str, default="phys_dps", choices=["phys_dps", "magic_dps", "breaker", "tank", "support", "mrp_farm", "all"], help="Build Archetype")
    parser.add_argument("--owned", nargs="*", default=[], help="List of owned Vision IDs (e.g., firion tidus squall cloud tronn). Omit to assume all.")
    args = parser.parse_args()

    result = optimize_build(args.owned, args.ap, args.role)

    print("\n" + "="*60)
    print(" ⚡ FINAL FANTASY RESONANCE: VISION & AP BUILD OPTIMIZER ⚡")
    print("="*60)
    print(f" เป้าหมายสายการเล่น: {args.role}")
    print(f" AP ที่ใช้: {result['total_ap']} / {result['ap_budget']} AP (เหลือ {result['remaining_ap']} AP)")
    print("-" * 60)
    print(" รายการพาสซีฟและสกิลที่แนะนำให้ติดตั้ง:")
    for idx, s in enumerate(result["selected"], 1):
        print(f"  {idx}. [{s['ap']:2d} AP] {s['name']} ({s['thai']}) - จาก {s['vision_name']}")
        print(f"     └ {s['desc']}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
