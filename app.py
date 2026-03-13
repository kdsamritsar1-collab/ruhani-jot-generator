import streamlit as st
import google.generativeai as genai

# 1. API Key कॉन्फ़िगरेशन (Secrets से)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key नहीं मिली। कृपया Streamlit Settings > Secrets में GEMINI_API_KEY डालें।")

# 2. पेज सेटअप और स्टाइलिंग
st.set_page_config(page_title="Ruhani Jot AI", page_icon="☬", layout="wide")

st.markdown("""
    <style>
    .stCode { background-color: #f9f9f9 !important; border: 1px solid #ddd; border-radius: 8px; }
    h1 { color: #ff9800; }
    </style>
    """, unsafe_allow_html=True)

st.title("☬ Ruhani Jot: Auto-Model Shabad Creator")

# 3. इनपुट पैनल
col1, col2 = st.columns([1, 1])

with col1:
    category = st.selectbox(
        "श्रेणी (Category) चुनें:",
        ["Devotional", "Kirtan", "Shabad", "Gurbani", "History based"]
    )
    song_input = st.text_area("गाने का विचार या संक्षिप्त विवरण लिखें:", placeholder="जैसे: अमृत वेले का महत्व...", height=150)

with col2:
    user_chorus = st.text_input("कोरस (Chorus) - वैकल्पिक:", placeholder="खाली छोड़ें यदि AI से बनवाना हो...")
    st.info("यह सिस्टम आपके अकाउंट में उपलब्ध सबसे सटीक और तेज़ Gemini मॉडल को ऑटो-डिटेक्ट करेगा।")

# 4. मुख्य लॉजिक (Auto-Model Detect)
if st.button("Generate Shabad & Suno Style"):
    if not song_input:
        st.warning("कृपया विवरण या कुछ पंक्तियाँ दर्ज करें।")
    else:
        with st.spinner('उपलब्ध मॉडल की जांच और रचना की तैयारी हो रही है...'):
            try:
                # उपलब्ध मॉडल्स की लिस्ट प्राप्त करना
                available_models = [m.name for m in genai.list_models() 
                                   if 'generateContent' in m.supported_generation_methods]
                
                # ऑटो-डिटेक्ट: सबसे नया 'gemini' मॉडल चुनें
                my_model = "models/gemini-1.5-flash" # डिफ़ॉल्ट
                for m in available_models:
                    if "gemini" in m.lower():
                        my_model = m
                        break
                
                # मॉडल लोड करना
                model = genai.GenerativeModel(my_model)

                # कोडिंग में दिए गए सख्त निर्देश (Strict Instructions)
                system_prompt = f"""
                You are an expert Punjabi devotional lyricist with deep knowledge of Gurbani, Sikh history, and Sikh philosophy.
                Category: {category}
                Write a Sikh devotional song in pure Punjabi (Gurmukhi script only). Do NOT use English or Hinglish.

                Requirements:
                1. Based on: {song_input}
                2. Praise Waheguru, Naam Simran, and Guru Sahib.
                3. Structure: 1 Chorus and 5 Verses (Each 4 lines).
                4. Proper 'tukhbandi' (rhyming) matching the chorus.
                5. Chorus Logic: {f"Use this exact chorus: {user_chorus}" if user_chorus else "Create a new spiritually deep chorus yourself."}
                
                Output Format:
                [STYLE_START]
                (Detailed music style under 120 chars for Suno.com including Raag, Instruments, and Mood)
                [STYLE_END]

                [LYRICS_START]
                [Intro]
                [Verse 1]
                [Chorus]
                [Verse 2]
                [Chorus]
                [Verse 3]
                [Chorus]
                [Verse 4]
                [Chorus]
                [Verse 5]
                [Chorus]
                [Outro]
                [LYRICS_END]
                """

                # एआई से रिस्पॉन्स लेना
                response = model.generate_content(system_prompt)
                full_text = response.text

                # परिणाम दिखाना
                st.divider()
                st.success(f"मॉडल सक्रिय: {my_model}")

                if "[STYLE_START]" in full_text and "[LYRICS_START]" in full_text:
                    style_part = full_text.split("[STYLE_START]")[1].split("[STYLE_END]")[0].strip()
                    lyrics_part = full_text.split("[LYRICS_START]")[1].split("[LYRICS_END]")[0].strip()
                    
                    st.subheader("🎵 Suno Music Style")
                    st.code(style_part)
                    
                    st.subheader("📝 Suno Lyrics (Gurmukhi)")
                    st.code(lyrics_part)
                else:
                    st.code(full_text)

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Created for **@ruhanijot** | Amritsar, Punjab")
