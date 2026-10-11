import os
import io
import json
import requests
import streamlit as st

# ==========================================
# ฟังก์ชันโหลดค่าจากไฟล์ .env (แบบไม่ต้องพึ่งพาไลบรารีภายนอก)
# ==========================================
def load_env_file(filepath=".env"):
    """โหลดค่า API Key จากไฟล์ .env หากมีอยู่"""
    env_vars = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        env_vars[key.strip()] = val.strip().strip('"').strip("'")
        except Exception:
            pass
    return env_vars

# โหลดค่าเบื้องต้น
local_env = load_env_file()
DEFAULT_API_KEY = os.environ.get("AIFORTHAI_API_KEY", local_env.get("AIFORTHAI_API_KEY", ""))

# ==========================================
# การตั้งค่าหน้าเว็บ Streamlit
# ==========================================
st.set_page_config(
    page_title="AIForThai Web Studio",
    page_icon="🇹🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0d324d 0%, #7f5a83 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .main-header p {
        color: #e0e0e0;
        margin: 6px 0 0 0;
        font-size: 1rem;
    }
    .token-chip {
        display: inline-block;
        background: #f0f2f6;
        color: #1e293b;
        border: 1px solid #cbd5e1;
        padding: 4px 10px;
        margin: 4px;
        border-radius: 16px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .sentiment-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .sentiment-pos {
        background-color: #e6f4ea;
        border: 1px solid #34a853;
        color: #137333;
    }
    .sentiment-neg {
        background-color: #fce8e6;
        border: 1px solid #ea4335;
        color: #c5221f;
    }
    .sentiment-neu {
        background-color: #e8f0fe;
        border: 1px solid #4285f4;
        color: #1a73e8;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Sidebar: จัดการการเชื่อมต่อและ API Key
# ==========================================
with st.sidebar:
    st.image("https://aiforthai.in.th/assets/img/logo.png", width=180)
    st.title("⚙️ ตั้งค่าระบบ")
    
    api_key_input = st.text_input(
        "AIForThai API Key:",
        value=DEFAULT_API_KEY,
        type="password",
        help="คีย์เข้าถึงบริการ AIForThai รับได้จากเว็บไซต์ aiforthai.in.th",
        placeholder="กรอก API Key ของคุณที่นี่..."
    )
    
    # บันทึกหรือดึง API Key จาก session state
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("🟢 มี API Key พร้อมใช้งาน")
    else:
        st.session_state["api_key"] = ""
        st.warning("⚠️ กรุณาระบุ API Key ก่อนเริ่มใช้งาน")
        
    st.markdown("---")
    st.markdown("### 📌 วิธีขอรับ API Key")
    st.markdown("""
    1. เข้าไปที่ [aiforthai.in.th](https://aiforthai.in.th/)
    2. สมัครสมาชิก / ล็อกอิน
    3. ไปที่เมนู **บัญชีผู้ใช้** หรือ **Dashboard**
    4. คัดลอก **API Key** มาวางที่ช่องด้านบน
    """)
    
    st.markdown("---")
    st.caption("🇹🇭 พัฒนาโดยใช้ Streamlit & แพลตฟอร์ม AIForThai (NECTEC)")

api_key = st.session_state.get("api_key", "")

# Header
st.markdown("""
<div class="main-header">
    <h1>🇹🇭 AIForThai Web Application</h1>
    <p>แพลตฟอร์มทดสอบและใช้งานโมเดลปัญญาประดิษฐ์สัญชาติไทย โดย NECTEC</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.info("💡 **เริ่มต้นใช้งาน:** โปรดกรอก **AIForThai API Key** ในแถบเมนูด้านซ้ายเพื่อเริ่มส่งคำขอไปยังโมเดล AI")

# ฟังก์ชันตัวช่วยในการเรียก API
def call_aiforthai_api(url, method="GET", params=None, data=None, files=None, headers=None, timeout=30):
    """ฟังก์ชันมาตรฐานสำหรับเชื่อมต่อ API ของ AIForThai"""
    if not api_key:
        return None, "กรุณาระบุ API Key ในแถบด้านซ้ายก่อนใช้งาน"
    
    req_headers = {"Apikey": api_key}
    if headers:
        req_headers.update(headers)
        
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=req_headers, params=params, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, headers=req_headers, data=data, json=params if not data else None, files=files, timeout=timeout)
        else:
            return None, f"Method {method} ไม่รองรับ"
            
        return response, None
    except requests.exceptions.Timeout:
        return None, "การเชื่อมต่อไปยัง API หมดเวลา (Timeout) โปรดลองใหม่อีกครั้ง"
    except requests.exceptions.RequestException as e:
        return None, f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}"

# ==========================================
# Tabs เมนูการทำงานของ AI
# ==========================================
tab_sentiment, tab_tlex, tab_ner, tab_vaja, tab_custom = st.tabs([
    "💬 วิเคราะห์อารมณ์ (S-Sense)",
    "✂️ ตัดคำภาษาไทย (TLex+)",
    "🏷️ ระบุชื่อเฉพาะ (T-NER)",
    "🔊 เสียงพูดภาษาไทย (Vaja)",
    "⚡ ทดสอบ API อื่นๆ"
])

# ----------------------------------------------------
# 1. วิเคราะห์อารมณ์ความรู้สึก (S-Sense Sentiment Analysis)
# ----------------------------------------------------
with tab_sentiment:
    st.subheader("💬 S-Sense: วิเคราะห์อารมณ์ความรู้สึกจากข้อความ")
    st.write("จำแนกข้อความภาษาไทยว่าเป็น **บวก (Positive)**, **ลบ (Negative)** หรือ **เป็นกลาง (Neutral)**")
    
    col_input, col_preset = st.columns([3, 1])
    with col_preset:
        st.write("**ตัวอย่างข้อความ:**")
        if st.button("👍 เชิงบวก (ประทับใจ)", key="btn_pos"):
            st.session_state["sentiment_text"] = "อาหารร้านนี้อร่อยมาก บรรยากาศดี พนักงานบริการรวดเร็วและสุภาพ ประทับใจสุดๆ"
        if st.button("👎 เชิงลบ (ผิดหวัง)", key="btn_neg"):
            st.session_state["sentiment_text"] = "รออาหารนานมาก พนักงานพูดจาไม่ดี รสชาติแย่ ไม่คุ้มค่ากับราคาเลย"
        if st.button("😐 เป็นกลาง (ทั่วไป)", key="btn_neu"):
            st.session_state["sentiment_text"] = "ร้านเปิดให้บริการทุกวันตั้งแต่เวลา 10:00 น. ถึง 21:00 น."
            
    with col_input:
        default_val = st.session_state.get("sentiment_text", "อาหารร้านนี้อร่อยมาก บริการดีเลิศ ประทับใจมากๆ เลยครับ")
        user_text = st.text_area("ข้อความภาษาไทยที่ต้องการวิเคราะห์:", value=default_val, height=120, key="txt_sentiment")
        
        btn_analyze = st.button("🚀 วิเคราะห์ความรู้สึก", type="primary", key="btn_analyze_sentiment")

    if btn_analyze:
        if not user_text.strip():
            st.warning("กรุณากรอกข้อความที่ต้องการวิเคราะห์")
        else:
            with st.spinner("กำลังส่งข้อความไปวิเคราะห์ที่ AIForThai S-Sense..."):
                url = "https://api.aiforthai.in.th/ssense"
                response, err = call_aiforthai_api(url, method="GET", params={"text": user_text})
                
                if err:
                    st.error(f"❌ {err}")
                elif response.status_code != 200:
                    st.error(f"❌ API Error ({response.status_code}): {response.text}")
                else:
                    try:
                        res_json = response.json()
                        sentiment_data = res_json.get("sentiment", {})
                        
                        polarity = str(sentiment_data.get("polarity", "")).lower()
                        score = sentiment_data.get("score", 0.0)
                        
                        # แสดงผลลัพธ์
                        col_r1, col_r2, col_r3 = st.columns(3)
                        with col_r1:
                            if polarity == "positive":
                                card_html = '<div class="sentiment-card sentiment-pos"><h2>😊 เชิงบวก (Positive)</h2><p>ข้อความแสดงความรู้สึกในแง่ดี ชื่นชม พอใจ</p></div>'
                            elif polarity == "negative":
                                card_html = '<div class="sentiment-card sentiment-neg"><h2>😡 เชิงลบ (Negative)</h2><p>ข้อความแสดงความรู้สึกไม่พอใจ ตำหนิ ผิดหวัง</p></div>'
                            else:
                                card_html = '<div class="sentiment-card sentiment-neu"><h2>😐 เป็นกลาง (Neutral)</h2><p>ข้อความบอกเล่าทั่วไป ไม่แสดงอารมณ์ชัดเจน</p></div>'
                            st.markdown(card_html, unsafe_allow_html=True)

                        with col_r2:
                            st.metric("คะแนนความรู้สึก (Sentiment Score)", f"{score}")
                        with col_r3:
                            st.metric("HTTP Status", f"{response.status_code} OK")

                        # คำเชิงบวก / เชิงลบที่ตรวจพบ
                        pos_words = res_json.get("preprocess", {}).get("positive", [])
                        neg_words = res_json.get("preprocess", {}).get("negative", [])
                        
                        if pos_words or neg_words:
                            st.write("---")
                            st.write("#### 🔍 คำที่ส่งผลต่ออารมณ์:")
                            c_w1, c_w2 = st.columns(2)
                            with c_w1:
                                if pos_words:
                                    st.success(f"**คำเชิงบวกที่พบ:** {', '.join(pos_words)}")
                                else:
                                    st.info("ไม่พบคำเชิงบวกเด่นชัด")
                            with c_w2:
                                if neg_words:
                                    st.error(f"**คำเชิงลบที่พบ:** {', '.join(neg_words)}")
                                else:
                                    st.info("ไม่พบคำเชิงลบเด่นชัด")

                        with st.expander("📄 ดูผลลัพธ์ JSON ฉบับเต็ม"):
                            st.json(res_json)
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
                        st.text(response.text)

# ----------------------------------------------------
# 2. ตัดคำภาษาไทย (TLex+)
# ----------------------------------------------------
with tab_tlex:
    st.subheader("✂️ TLex+: บริการตัดคำและประมวลผลคำภาษาไทย")
    st.write("แยกคำในประโยคภาษาไทยที่ไม่มีการเว้นวรรค พร้อมนับจำนวนคำและแสดงการจัดกลุ่มคำ")
    
    tlex_input = st.text_area(
        "ข้อความที่ต้องการตัดคำ:",
        value="ยินดีต้อนรับสู่การพัฒนาโมเดลปัญญาประดิษฐ์ภาษาไทยสำหรับแอปพลิเคชันยุคใหม่",
        height=100,
        key="txt_tlex"
    )
    
    if st.button("🚀 ตัดคำ (Tokenize)", type="primary", key="btn_run_tlex"):
        if not tlex_input.strip():
            st.warning("กรุณากรอกข้อความ")
        else:
            with st.spinner("กำลังตัดคำด้วย TLex+..."):
                url = "https://api.aiforthai.in.th/tlexplus"
                response, err = call_aiforthai_api(url, method="GET", params={"text": tlex_input})
                
                if err:
                    st.error(f"❌ {err}")
                elif response.status_code != 200:
                    st.error(f"❌ API Error ({response.status_code}): {response.text}")
                else:
                    try:
                        res_json = response.json()
                        words = []
                        if isinstance(res_json, list):
                            words = res_json
                        elif isinstance(res_json, dict):
                            words = res_json.get("words", res_json.get("tokens", []))
                            if not words and "tokenizer" in res_json:
                                words = res_json["tokenizer"].get("words", [])
                            if not words and "output" in res_json:
                                words = res_json["output"].split("|")
                        
                        if not words and isinstance(res_json, str):
                            words = res_json.split("|")

                        st.write("---")
                        st.write("#### 📊 ผลการตัดคำ:")
                        
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric("จำนวนคำทั้งหมด (Total Words)", len(words))
                        with col_m2:
                            st.metric("จำนวนคำที่ไม่ซ้ำ (Unique Words)", len(set(words)))

                        st.write("**คำที่แยกได้ (Token Chips):**")
                        chips_html = "".join([f'<span class="token-chip">{w}</span>' for w in words if w.strip()])
                        st.markdown(chips_html, unsafe_allow_html=True)
                        
                        st.write("---")
                        st.text_input("รูปแบบคั่นด้วยเครื่องหมาย | (Pipe Separated):", value="|".join(words))

                        with st.expander("📄 ดูผลลัพธ์ JSON ฉบับเต็ม"):
                            st.json(res_json)
                    except Exception as e:
                        st.error(f"การแปลงผลลัพธ์ขัดข้อง: {e}")
                        st.text(response.text)

# ----------------------------------------------------
# 3. ระบุชื่อเฉพาะ (T-NER)
# ----------------------------------------------------
with tab_ner:
    st.subheader("🏷️ T-NER: จำแนกหน่วยชื่อเฉพาะภาษาไทย (Named Entity Recognition)")
    st.write("ระบุเอนทิตีสำคัญในข้อความ เช่น บุคคล (Person), สถานที่ (Location), องค์กร (Organization), วันที่ (Date)")
    
    ner_sample = "นายสมศักดิ์ เดินทางไปประชุมที่สำนักงาน กสทช. ถนนพหลโยธิน กรุงเทพมหานคร เมื่อวันที่ 12 สิงหาคม 2568"
    ner_input = st.text_area("ข้อความสำหรับระบุเอนทิตี:", value=ner_sample, height=100, key="txt_ner")
    
    if st.button("🚀 สกัดเอนทิตี (Extract Entities)", type="primary", key="btn_run_ner"):
        if not ner_input.strip():
            st.warning("กรุณาระบุข้อความ")
        else:
            with st.spinner("กำลังประมวลผล T-NER..."):
                url = "https://api.aiforthai.in.th/tner"
                response, err = call_aiforthai_api(url, method="GET", params={"text": ner_input})
                
                if err:
                    st.error(f"❌ {err}")
                elif response.status_code != 200:
                    st.error(f"❌ API Error ({response.status_code}): {response.text}")
                else:
                    try:
                        res_json = response.json()
                        st.write("---")
                        st.write("#### 🎯 ผลการวิเคราะห์เอนทิตี:")
                        
                        with st.expander("📄 ดูผลลัพธ์ JSON ฉบับเต็ม", expanded=True):
                            st.json(res_json)
                    except Exception as e:
                        st.error(f"การแปลงผลลัพธ์ขัดข้อง: {e}")
                        st.text(response.text)

# ----------------------------------------------------
# 4. แปลงข้อความเป็นเสียงพูด (Vaja Text-to-Speech)
# ----------------------------------------------------
with tab_vaja:
    st.subheader("🔊 Vaja (วาจา): สังเคราะห์เสียงพูดภาษาไทย")
    st.write("แปลงข้อความตัวหนังสือให้ออกมาเป็นไฟล์เสียงพูดภาษาไทย (.wav) คุณภาพสูง")
    
    vaja_text = st.text_area(
        "ข้อความที่ต้องการให้ออกเสียง:",
        value="สวัสดีครับ ยินดีต้อนรับสู่ระบบปัญญาประดิษฐ์เพื่อคนไทย AI for Thai ขอให้มีความสุขกับการเขียนโปรแกรมครับ",
        height=100,
        key="txt_vaja"
    )
    
    if st.button("🎙️ สร้างเสียงพูด (Synthesize Audio)", type="primary", key="btn_run_vaja"):
        if not vaja_text.strip():
            st.warning("กรุณากรอกข้อความที่ต้องการให้แปลงเป็นเสียง")
        else:
            with st.spinner("กำลังสังเคราะห์เสียงด้วย Vaja..."):
                url = "https://api.aiforthai.in.th/vaja"
                response, err = call_aiforthai_api(
                    url, 
                    method="POST", 
                    params={"text": vaja_text}
                )
                
                if err:
                    st.error(f"❌ {err}")
                elif response.status_code != 200:
                    st.error(f"❌ API Error ({response.status_code}): {response.text}")
                else:
                    try:
                        res_json = response.json()
                        audio_url = res_json.get("audio_url", "")
                        
                        if audio_url:
                            # ดึงไฟล์เสียงจาก audio_url
                            audio_res = requests.get(audio_url)
                            if audio_res.status_code == 200:
                                st.success("✅ สังเคราะห์เสียงพูดสำเร็จ!")
                                st.audio(audio_res.content, format="audio/wav")
                                
                                st.download_button(
                                    label="⬇️ ดาวน์โหลดไฟล์เสียง (.wav)",
                                    data=audio_res.content,
                                    file_name="speech_output.wav",
                                    mime="audio/wav"
                                )
                            else:
                                st.error("ไม่สามารถโหลดไฟล์เสียงจาก URL ได้")
                        else:
                            st.warning("ไม่พบ audio_url ในผลลัพธ์:")
                            st.json(res_json)
                    except Exception:
                        # กรณี API คืนไฟล์เสียงตรงๆ (Binary)
                        st.success("✅ สังเคราะห์เสียงพูดสำเร็จ!")
                        st.audio(response.content, format="audio/wav")
# ----------------------------------------------------
# 5. ทดสอบ API อื่นๆ ของ AIForThai (Custom API Explorer)
# ----------------------------------------------------
with tab_custom:
    st.subheader("⚡ Custom API Explorer: ทดสอบ API ใดก็ได้ของ AIForThai")
    st.write("ทดสอบ API ตัวอื่นๆ เช่น OCR, Speech-to-text, Machine Translation, หรือโมเดลใหม่ๆ ในแดชบอร์ดของคุณ")
    
    col_ep, col_m = st.columns([4, 1])
    with col_ep:
        custom_endpoint = st.text_input(
            "API Endpoint URL:",
            value="https://api.aiforthai.in.th/ssense",
            help="ระบุ URL ของ API ที่ต้องการเรียกใช้งาน"
        )
    with col_m:
        custom_method = st.selectbox("HTTP Method:", ["GET", "POST"])
        
    st.write("**พารามิเตอร์ (Parameters / Form Data / Body):**")
    custom_params_type = st.radio("ชนิดของข้อมูลที่ส่ง:", ["URL Parameters (Query string)", "Form Data (POST Data)", "Raw JSON"], horizontal=True)
    
    custom_input_val = st.text_area(
        "ระบุข้อมูล (JSON หรือ Key=Value):",
        value='{"text": "ทดสอบระบบ AI สำหรับคนไทย"}',
        height=100
    )
    
    if st.button("🚀 ส่งคำขอ (Send Request)", key="btn_send_custom"):
        if not custom_endpoint.strip():
            st.warning("กรุณาระบุ Endpoint URL")
        else:
            with st.spinner("กำลังส่งคำขอไปยัง API..."):
                params = None
                data = None
                
                try:
                    if custom_params_type == "Raw JSON":
                        params = json.loads(custom_input_val)
                    elif custom_params_type == "URL Parameters (Query string)":
                        try:
                            params = json.loads(custom_input_val)
                        except Exception:
                            params = dict(item.split("=") for item in custom_input_val.split("&") if "=" in item)
                    else:
                        try:
                            data = json.loads(custom_input_val)
                        except Exception:
                            data = dict(item.split("=") for item in custom_input_val.split("&") if "=" in item)
                except Exception as parse_err:
                    st.error(f"รูปแบบข้อมูลผิดพลาด: {parse_err}")
                    params = None
                    data = None

                response, err = call_aiforthai_api(
                    custom_endpoint,
                    method=custom_method,
                    params=params if custom_method == "GET" else None,
                    data=data if custom_method == "POST" else None
                )
                
                if err:
                    st.error(f"❌ {err}")
                else:
                    st.write("---")
                    st.write(f"**HTTP Status:** `{response.status_code}` | **Time:** `{response.elapsed.total_seconds():.2f}s`")
                    try:
                        st.json(response.json())
                    except Exception:
                        st.text(response.text)