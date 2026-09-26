from openai import OpenAI
import streamlit as st

# إعدادات الصفحة والتصميم المتناسق مع الهواتف
st.set_page_config(
    page_title="f7ff8 AI Intelligence",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# تخصيص واجهة داكنة فاخرة ومريحة للموبايل
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stChatMessage {
        background-color: #161b22;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# رأس الصفحة والترخيص الرسمي
st.markdown(
    "<h2 style='text-align: center; color: #58a6ff;'>f7ff8 AI System</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #8b949e; font-size: 13px;'>المطور"
    " والمالك الأساسي: <b>أبوجاسم</b> | للإبلاغ عن الأخطاء أو الاستفسار: <a"
    " href='https://t.me/f7ff8' target='_blank' style='color: #58a6ff;"
    " text-decoration: none;'>@f7ff8</a></p>",
    unsafe_allow_html=True,
)

# محاولة جلب المفتاح من الـ Secrets أولاً
api_key = None
try:
  if "OPENROUTER_API_KEY" in st.secrets and st.secrets["OPENROUTER_API_KEY"]:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
  pass

# الشريط الجانبي للإعدادات واختيار النموذج وإدخال المفتاح كبديل آمن
with st.sidebar:
  st.title("إعدادات المنظومة")

  # إذا لم يتم العثور على المفتاح في السكيرتس، نتيحه هنا بكل سهولة
  if not api_key:
    user_input_key = st.text_input(
        "مفتاح التشغيل (API Key):",
        type="password",
        placeholder="sk-or-v1-...",
    )
    if user_input_key:
      api_key = user_input_key
    st.markdown(
        "💡 *الصق مفتاحك هنا ليعمل الموقع فوراً إذا لم تضبط الـ Secrets.*"
    )
  else:
    st.success("✔ تم تحميل المفتاح بنجاح.")

  st.markdown("---")
  selected_display_model = st.selectbox(
      "النموذج النشط", ["f7-f8 slim", "f7-f8 vSuper"]
  )

# ربط الأسماء بالنماذج الفعلية
model_mapping = {
    "f7-f8 slim": "qwen/qwen-2.5-7b-instruct",  # الخفيف والسريع للبرمجة
    "f7-f8 vSuper": "qwen/qwen-2.5-72b-instruct",  # النسخة الكاملة القوية
}
actual_model = model_mapping[selected_display_model]

# تهيئة الذاكرة للمحادثة
if "messages" not in st.session_state:
  st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# استقبال الرسالة من المستخدم
if prompt := st.chat_input("اكتب رسالتك أو استفسارك هنا..."):
  if not api_key:
    st.error(
        "⚠️ يرجى إدخال مفتاح الـ API في الشريط الجانبي (Sidebar) لكي تبدأ المنظومة"
        " بالعمل."
    )
  else:
    # حفظ رسالة المستخدم وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # توليد الرد بشكل فوري وتدفق (Streaming)
    with st.chat_message("assistant"):
      client = OpenAI(
          base_url="https://openrouter.ai/api/v1", api_key=api_key
      )
      message_placeholder = st.empty()
      full_response = ""

      try:
        stream = client.chat.completions.create(
            model=actual_model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            temperature=0.7,
        )

        for chunk in stream:
          if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
      except Exception as e:
        full_response = (
            "⚠️ حدث خطأ في الاتصال بالنموذج. يرجى التحقق من صحة المفتاح."
        )
        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
