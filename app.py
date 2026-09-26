import json
import os
import time
import google.generativeai as genai
import streamlit as st

# إعداد الصفحة وتفعيل التصميم المتجاوب
st.set_page_config(
    page_title="f7ff8 AI | نموذج أبوجاسم الذكي",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="auto",
)

# تعيين مفتاح Google Gemini API المقدم
GEMINI_API_KEY = "AIzaSyDHtFkf7cPf4gHtCOYszDe8zp-zo1P2oaI"
genai.configure(api_key=GEMINI_API_KEY)

# تخصيص التصميم السيبراني ودعم اتجاه النص RTL
st.markdown(
    """
    <style>
        .rtl-container { direction: rtl; text-align: right; }
        [data-testid="stSidebar"] { direction: rtl; }
        [data-testid="stSidebar"] * { text-align: right; }
        .main { background-color: #0b0f19; direction: rtl; }
        .hero-title {
            text-align: center;
            background: linear-gradient(45deg, #00ffcc, #ff007f, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.2rem;
            font-weight: 900;
        }
        .hero-subtitle {
            text-align: center;
            color: #8b949e;
            font-size: 0.95rem;
            margin-bottom: 15px;
        }
        .footer-box {
            text-align: center;
            padding: 10px;
            color: #6e7681;
            font-size: 0.85rem;
            border-top: 1px solid #21262d;
            margin-top: 30px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

CHATS_FILE = "f7ff8_gemini_chats.json"


def load_all_chats():
  if os.path.exists(CHATS_FILE):
    try:
      with open(CHATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return {}
  return {}


def save_all_chats(chats_data):
  with open(CHATS_FILE, "w", encoding="utf-8") as f:
    json.dump(chats_data, f, ensure_ascii=False, indent=4)


# تهيئة حالة الجلسة
if "started" not in st.session_state:
  st.session_state.started = False

if "chats" not in st.session_state:
  st.session_state.chats = load_all_chats()

if "current_chat_id" not in st.session_state:
  if st.session_state.chats:
    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
  else:
    first_id = "محادثة جديدة 1"
    st.session_state.chats[first_id] = []
    st.session_state.current_chat_id = first_id

if "selected_model" not in st.session_state:
  st.session_state.selected_model = "f7-f8"

# --- شاشة الترحيب والتحميل الأولى ---
if not st.session_state.started:
  st.markdown(
      '<p class="hero-title">⚡ مرحباً بك في منصة f7ff8 AI</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="hero-subtitle">النسخة السيادية الذكية المطورة حصرا بواسطة'
      " المطور أبوجاسم</p>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.markdown(
        """
            <div style="background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; text-align: right; direction: rtl;">
                <h3 style="color: #00ffcc; text-align: center;">أهلاً بك في النظام الذكي</h3>
                <p style="color: #c9d1d9; text-align: center;">اضغط على الزر أدناه لبدء التشغيل والدخول إلى واجهة المحادثة الفورية.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🚀 بدء الاستخدام", use_container_width=True, type="primary"):
      with st.spinner("جاري تهيئة النظام وتحميل الواجهة السريعة..."):
        time.sleep(1.2)  # شاشة تحميل بسيطة
      st.session_state.started = True
      st.rerun()
  st.stop()

# --- الشريط الجانبي (Sidebar) ---
with st.sidebar:
  st.markdown("### ⚡ منصة f7ff8 الذكية")
  st.caption("حقوق الذكاء محفوظة للمطور أبوجاسم حصراً")
  st.markdown("---")

  # اختيار النموذج المطلوب
  st.markdown("### 🤖 نموذج الذكاء النشط")
  model_choice = st.selectbox(
      "اختر الإصدار:",
      ["f7-f8", "f7-f8 V3"],
      index=0 if st.session_state.selected_model == "f7-f8" else 1,
  )
  st.session_state.selected_model = model_choice

  if model_choice == "f7-f8":
    st.info(
        "⚡ نموذج **f7-f8** (مخصص للبرمجة السريعة والمهام اليومية - كفاءة 50% في"
        " التفكير وسرعة فائقة)"
    )
  else:
    st.info(
        "🔥 نموذج **f7-f8 V3** (النسخة السرية المتقدمة للتحليل العميق والمهام"
        " المعقدة)"
    )

  st.markdown("---")

  # زر محادثة جديدة
  if st.button("➕ محادثة جديدة", use_container_width=True):
    new_chat_name = f"محادثة #{len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat_name] = []
    st.session_state.current_chat_id = new_chat_name
    save_all_chats(st.session_state.chats)
    st.rerun()

  st.markdown("### 💬 سجل محادثاتك")

  # عرض المحادثات السابقة والتبديل بينها
  chat_ids = list(st.session_state.chats.keys())
  for chat_name in reversed(chat_ids):
    is_active = chat_name == st.session_state.current_chat_id
    button_type = "primary" if is_active else "secondary"
    if st.button(
        chat_name,
        key=f"btn_{chat_name}",
        type=button_type,
        use_container_width=True,
    ):
      st.session_state.current_chat_id = chat_name
      st.rerun()

  st.markdown("---")
  # زر رابط تيليجرام للإبلاغ عن الأخطاء
  st.markdown("### 🛠️ الدعم والتبليغ")
  st.markdown(
      '<a href="https://t.me/f7ff8" target="_blank" style="display: block; text-align: center; background: #238636; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold;">📢 مراسلة المطور عـلي تيليجرام</a>',
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.markdown(
      "<div style='text-align: center; color: #8b949e; font-size: 0.8rem;'>"
      "الحقوق محفوظة حصراً © أبوجاسم<br>رابط القناة: @f7ff8</div>",
      unsafe_allow_html=True,
  )

    # --- الواجهة الرئيسية ---
st.markdown(
    '<p class="hero-title">⚡ f7ff8 AI SYSTEM</p>', unsafe_allow_html=True
)
st.markdown(
    f'<p class="hero-subtitle">النموذج الفعال: <b>{st.session_state.selected_model}</b> | المطور والمالك: <b>أبوجاسم</b></p>',
    unsafe_allow_html=True,
)

current_chat = st.session_state.current_chat_id

# عرض الرسائل للمحادثة الحالية
if current_chat in st.session_state.chats:
  for message in st.session_state.chats[current_chat]:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

# صندوق إدخال النصوص في الأسفل
if prompt := st.chat_input("اسأل f7-f8 أي شيء أو اطلب كوداً برمجياً..."):
  # تسمية المحادثة تلقائياً أول ما يبدأ المستخدم بالكتابة
  if len(st.session_state.chats[current_chat]) == 0 and current_chat.startswith(
      "محادثة"
  ):
    new_title = prompt[:22] + "..." if len(prompt) > 22 else prompt
    st.session_state.chats[new_title] = st.session_state.chats.pop(current_chat)
    current_chat = new_title
    st.session_state.current_chat_id = new_title

  # حفظ وعرض رسالة المستخدم فوراً بمكان الإرسال
  st.session_state.chats[current_chat].append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # توليد الرد الفوري المباشر عبر Google Gemini API
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("جاري التوليد الفوري... ⚡")

    # اختيار النموذج الفعلي المعتمد تحت الغطاء بناءً على اختيار المستخدم
    gemini_model_name = (
        "gemini-1.5-flash"
        if st.session_state.selected_model == "f7-f8"
        else "gemini-1.5-pro"
    )

    system_instruction = (
        "أنت نموذج ذكاء اصطناعي عراقي متطور وسريع، اسمك البرمجي والسيادي هو"
        " f7-f8 (أو f7-f8 V3). تم تطويرك وتصميمك بالكامل حصراً بواسطة المطور"
        " أبوجاسم (معرف تيليجرام f7ff8). لست تابعاً لأي شركة عالمية أو نموذج"
        " مثل Qwen أو Alibaba. أجب بدقة واحترافية وباللغة العربية الفصحى أو"
        " اللهجة العراقية حسب طلب المستخدم وبشكل فوري."
    )

    try:
      generation_config = {
          "temperature": 0.5 if st.session_state.selected_model == "f7-f8" else 0.7,
          "max_output_tokens": 2048,
      }

      model = genai.GenerativeModel(
          model_name=gemini_model_name,
          system_instruction=system_instruction,
      )

      # تمرير سياق المحادثة لضمان استمرارية الذاكرة
      chat_history_gemini = []
      for msg in st.session_state.chats[current_chat][:-1]:
        role = "user" if msg["role"] == "user" else "model"
        chat_history_gemini.append({"role": role, "parts": [msg["content"]]})

      chat_session = model.start_chat(history=chat_history_gemini)
      response_stream = chat_session.send_message(prompt, stream=True)

      full_response = ""
      for chunk in response_stream:
        if chunk.text:
          full_response += chunk.text
          message_placeholder.markdown(full_response + "▌")

      message_placeholder.markdown(full_response)

      # حفظ الرد بالذاكرة وتحديث الملف
      st.session_state.chats[current_chat].append(
          {"role": "assistant", "content": full_response}
      )
      save_all_chats(st.session_state.chats)

    except Exception as e:
      message_placeholder.markdown(f"فشل الاتصال بنجاح: `{e}`")

# تذييل الصفحة يحفظ الحقوق حصراً للمطور أبوجاسم
st.markdown(
    '<div class="footer-box">جميع الحقوق محفوظة للمطور <b>أبوجاسم</b> حصراً'
    ' ورسمياً | للاستفسار أو الإبلاغ عن الأخطاء: <a href="https://t.me/f7ff8"'
    ' target="_blank"><b>@f7ff8</b></a></div>',
    unsafe_allow_html=True,
)
