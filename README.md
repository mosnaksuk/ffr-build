# Final Fantasy Resonance - Vision & AP Build Optimizer

เครื่องมือแนะนำและคำนวณบิลด์การจัดพาสซีฟของวิชั่น (Visions) ในเกม **Final Fantasy Resonance** เพื่อให้เกิดความคุ้มค่าของค่า **AP (Ability Points)** สูงสุด และสร้าง Synergy ของสกิลที่ทรงพลังที่สุด

---

## 🌟 ฟีเจอร์หลัก (Features)

1. **Owned Vision Selector**: เลือกระบุวิชั่นที่มีอยู่ในไอดีของคุณจากทั้งหมด 26 ตัว (พร้อมระบบกรองช่วง Chapter 1-2, Chapter 3-4 หรือครบทุกตัว)
2. **AP Budget Optimizer**: ระบุจำนวน AP สูงสุดของตัวละคร (เช่น 50, 100, 120, 150, 200 AP) ระบบจะใช้อัลกอริทึม **0/1 Knapsack Dynamic Programming** คำนวณหาเซ็ตสกิลที่สร้างผลลัพธ์และ Synergy สูงสุดโดยไม่เกินงบ AP
3. **สายการเล่นที่รองรับ (Build Archetypes)**:
   - ⚔️ **Physical DPS & Multi-Action**: สายโจมตีกายภาพเบิ้ลเทิร์น (Arms Akimbo + Improvement + Crit Boost)
   - 🔮 **Magic Nuke & Infinite MP**: สายมหาเวทล้างสนาม (Half MP Cost + Area Effect Adept + Break the Limit)
   - 🛡️ **Sentinel Defense**: สายแทงก์อมตะป้องกันทีม (Bastion + Auto-Shell + Physical Redux)
   - ⚡ **Stagger Breaker & Turn Rush**: สายเบรคไวออกตัวก่อน (First Strike + Stagger Power + Aggravation)
   - 💖 **Support & LB Battery**: สายปั๊มเกจ Limit Break (LB Triple Charge + LB Charge on Heal + Clive LB Boost)
   - 🌾 **MRP Speed Farm**: สายเร่งฟาร์มเลเวลวิชั่น (MRP Gain +50% + First Strike + Arms Akimbo)
4. **Interactive Sandbox**: ทดลองปรับแต่ง ถอด-ใส่ สกิลเองได้แบบเรียลไทม์ พร้อมเกจบอก AP ที่ใช้และคงเหลือ
5. **Preset Meta Builds**: เทมเพลตบิลด์ยอดนิยมระดับ Meta ที่ชุมชนผู้เล่นแนะนำ สามารถคลิกโหลดได้ทันที

---

## 🚀 วิธีการใช้งาน

### 1. เปิดผ่านเว็บเบราว์เซอร์ (Web Interface)
ดับเบิ้ลคลิกเปิดไฟล์ `index.html` บนเบราว์เซอร์ใดก็ได้ (Chrome, Edge, Firefox) หรือรันผ่าน Local Server:
```bash
# ด้วย Python
python -m http.server 8080
# จากนั้นเปิด http://localhost:8080 ในเบราว์เซอร์
```

### 2. ใช้งานผ่าน Command Line (CLI Python)
มีสคริปต์ `optimizer.py` ให้ใช้งานใน Terminal:
```bash
# คำนวณบิลด์สายกายภาพ ด้วยงบ 100 AP
python optimizer.py --ap 100 --role phys_dps

# คำนวณบิลด์สายเวท ด้วยงบ 90 AP โดยระบุวิชั่นที่มีอยู่
python optimizer.py --ap 90 --role magic_dps --owned tronn shantotto terra bartz

# ดูคำสั่งทั้งหมด
python optimizer.py --help
```

---

## 📊 ตารางพาสซีฟระดับเทพ (God-Tier AP Value)

| สกิล (Passive) | วิชั่นต้นทาง | เงื่อนไขปลด | ค่า AP | ความคุ้มค่า / ผลลัพธ์ |
| :--- | :--- | :---: | :---: | :--- |
| **Arms Akimbo** | Firion | MR 9 | **20 AP** | **SSS-Tier**: ทำ 2 แอคชั่นใน 1 เทิร์น (คุ้มค่า AP ที่สุดในเกม) |
| **First Strike** | Tidus | MR 3 | **20 AP** | **SSS-Tier**: การันตีได้ออกตัวเป็นคนแรกสุดของการต่อสู้ |
| **Improvement** | Squall | MR 1 | **20 AP** | **SSS-Tier**: เพิ่มดาเมจและเกจ Stagger สูงสุด +50% ตามจำนวนแอคชั่น |
| **Half MP Cost** | Tronn | MR 9 | **50 AP** | **SSS-Tier**: ลดการใช้ MP ทุกชนิดลง 50% ทำให้คอมโบไม่สะดุด |
| **LB Triple Charge** | Onion Knight | MR 9 | **50 AP** | **SSS-Tier**: เร่งอัตราการเก็บเกจ Limit Break ไวขึ้น 300% |
| **LB Charge on Heal** | Ayaka | MR 9 | **20 AP** | **SSS-Tier**: ฮีลเพื่อนแล้วชาร์จเกจ Limit Break ของตัวเอง 25% |
| **MRP Gain +50%** | Victoria | MR 7 | **30 AP** | **SSS-Tier**: เร่งฟาร์มแต้มวิชั่น MRP หลังจบการต่อสู้ขึ้น 50% |
| **Aggravation** | Zidane | MR 7 | **25 AP** | **S-Tier**: โบนัสดาเมจสูงสุด 60% เมื่อเป้าหมายมีดีบัฟ |
| **Critical Boost** | Cloud Strife | MR 7 | **40 AP** | **S-Tier**: เพิ่มตัวคูณความเสียหายคริติคอล 35% |
