import streamlit as st
import google.generativeai as genai

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="Universal AI Assistant", page_icon="🤖", layout="wide")

# 2. साइडबार (सेटिंग्स मेन्यू)
with st.sidebar:
    st.header("⚙️ सेटिंग्स (Settings)")
    api_key = st.text_input("अपनी Gemini API Key डालें:", type="password", help="Google AI Studio से API Key प्राप्त करें")
    selected_model = st.selectbox(
        "AI मॉडल चुनें:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
    )
    st.markdown("---")
    st.markdown("**निर्देश:**\n1. अपनी API Key दर्ज करें।\n2. मॉडल चुनें।\n3. चैट बॉक्स में सवाल पूछना शुरू करें।")

# 3. मुख्य इंटरफेस
st.title("🌐 Universal AI Chatbot")
st.caption("ब्राउज़र के अंदर चलने वाला आपका व्यक्तिगत AI सहायक")

# चैट हिस्ट्री सेशन स्टेट
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट स्क्रीन पर दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# यूजर इनपुट और AI रिस्पॉन्स
if prompt := st.chat_input("दुनिया का कोई भी सवाल पूछें..."):
    if not api_key:
        st.warning("⚠️ कृपया पहले साइडबार (Settings) में अपनी API Key दर्ज करें!")
    else:
        # यूजर का मैसेज सेव और डिस्प्ले करें
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI का रिस्पॉन्स जेनरेट करें
        with st.chat_message("assistant"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(selected_model)
                
                with st.spinner("सोच रहा हूँ..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

