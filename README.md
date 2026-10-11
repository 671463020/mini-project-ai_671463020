# 🇹🇭 AIForThai Web Studio

เว็บแอปพลิเคชันปัญญาประดิษฐ์ (AI Web App) ที่เชื่อมต่อกับบริการ **AI for Thai** (แพลตฟอร์ม AI สัญชาติไทยโดย NECTEC) พัฒนาด้วย Python และ Streamlit

---

## 🚀 ฟีเจอร์ที่รองรับ

1. **💬 วิเคราะห์อารมณ์ความรู้สึก (S-Sense Sentiment Analysis)**
   - วิเคราะห์ข้อความว่าเป็น เชิงบวก (Positive), เชิงลบ (Negative) หรือ เป็นกลาง (Neutral)
   - แสดงคะแนน Sentiment Score และไฮไลท์คำที่ส่งผลต่ออารมณ์
2. **✂️ ตัดคำภาษาไทย (TLex+ Word Tokenization)**
   - แยกคำในประโยคภาษาไทยที่เขียนติดกัน
   - นับจำนวนคำทั้งหมดและคำที่ไม่ซ้ำ แสดงผลแบบ Token Chips สวยงาม
3. **🏷️ ระบุชื่อเฉพาะภาษาไทย (T-NER - Named Entity Recognition)**
   - จำแนกบุคคล (Person), องค์กร (Organization), สถานที่ (Location), วันที่ (Date)
4. **🔊 แปลงข้อความเป็นเสียงพูด (Vaja Text-to-Speech)**
   - สังเคราะห์เสียงพูดภาษาไทยจากตัวอักษร
   - เล่นไฟล์เสียง (.wav) ผ่านหน้าเว็บได้ทันที พร้อมปุ่มดาวน์โหลด
5. **⚡ Custom API Explorer**
   - รองรับการทดสอบ API อื่นๆ ของ AIForThai (เช่น OCR, Translation, ฯลฯ) ผ่าน HTTP GET/POST

---

## 🛠️ วิธีการติดตั้งและรันโปรเจกต์

### 1. ติดตั้งไลบรารีที่จำเป็น
```bash
pip install -r requirements.txt
```

### 2. ตั้งค่า API Key (เลือกวิธีใดวิธีหนึ่ง)
- **วิธีที่ 1:** กรอก API Key ผ่านช่องกรอกบน Sidebar หน้าเว็บโดยตรง
- **วิธีที่ 2:** สร้างไฟล์ `.env` ในโฟลเดอร์โปรเจกต์:
  ```bash
  copy .env.example .env
  ```
  จากนั้นเปิดไฟล์ `.env` แล้วระบุคีย์ของคุณ:
  ```env
  AIFORTHAI_API_KEY=your_actual_api_key_here
  ```

> 💡 **วิธีขอรับ API Key:**
> 1. สมัครสมาชิกที่ [https://aiforthai.in.th](https://aiforthai.in.th)
> 2. ล็อกอินเข้าสู่ระบบ แล้วไปที่เมนู **บัญชีผู้ใช้** เพื่อคัดลอก **API Key**

### 3. รันเว็บแอปพลิเคชัน
```bash
streamlit run app.py
```
เมื่อรันคำสั่ง ระบบจะเปิดหน้าเว็บที่เบราว์เซอร์อัตโนมัติ (ปกติจะอยู่ที่ `http://localhost:8501`)
