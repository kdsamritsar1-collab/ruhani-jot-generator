import streamlit as st
import google.generativeai as genai

# Streamlit Secrets से API Key कॉन्फ़िगर करें
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key नहीं मिली। कृपया Streamlit Settings > Secrets में GEMINI_API_KEY डालें।")

# पेज सेटअप
st.set_page_config(page_title="Ruhani Jot AI", page_icon="☬", layout="wide")

st.markdown("""
    <style>
    .stCode { background-color: #f0f2f6 !important; border-radius: 10px; }
    .main-header { color: #ff9800; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">☬ Ruhani Jot: Advanced Shabad Creator (Auto-Model)</p>', unsafe_allow_html=True)

# इनपुट सेक्शन
col1, col2 = st.columns([1, 1])
with col1:
    category = st.selectbox("श्रेणी (Category) चुनें:", ["Devotional", "Kirtan", "Shabad", "Gurbani", "History based"])
    song_input = st.text_area("गाने का विवरण/पंक्तियाँ:", placeholder="जैसे: अमृत वेले की महिमा...", height=150)

with col2:
    user_chorus = st.text_input("कोरस (Chorus) - वैकल्पिक:", placeholder="खाली छोड़ने पर AI खुद बनाएगा...")
    st.info("यह सिस्टम खुद सबसे तेज़ उपलब्ध Gemini मॉडल को ढूँढकर रचना तैयार करेगा।")

# बटन लॉजिक
if st.button("Generate Complete Song & Style"):
    if not song_input:
        st.warning("कृपया विवरण दर्ज करें।")
    else:
        with st.spinner('सही मॉडल खोज कर रचना तैयार की जा रही है...'):
            try:
                # 1. डायनामिक मॉडल सिलेक्शन (जो चालू होगा उसे पकड़ेगा)
                available_models = [m.name for m in genai.list_models() 
                                   if 'generateContent' in m.supported_generation_methods]
                
                # सबसे नया gemini मॉडल चुनें (1.5-flash को प्राथमिकता)
                my_model = "models/gemini-1.5-flash"
                for m in available_models:
                    if "gemini" in m.lower() and "flash" in m.lower():
                        my_model = m
                        break
                
                model = genai.GenerativeModel(my_model)

                # 2. आपका सख्त इंस्ट्रक्शन प्रॉम्प्ट
                system_prompt = f"""
                You are an expert Punjabi devotional lyricist with deep knowledge of Gurbani and Sikh history.
                Category: {category}
                Write a Sikh devotional song in pure Punjabi (Gurmukhi script only). No English/Hinglish.

                Requirements:
                - Based on: {song_input}
                - Structure: 1 Chorus and 5 Verses (Each 4 lines).
                - Proper tukhbandi (rhyming).
                - Chorus: {f"Use this EXACTLY: {user_chorus}" if user_chorus else "Create a new deep rhyming chorus yourself."}
                
                Output Format:
                [STYLE_START]
                (Detailed music style under 120 chars for Suno.com)
                [STYLE_END]

                [LYRICS_START]
                [Intro]
                [Verse 1]
                [Chorus]
                ... (Full structure up to Verse 5) ...
                [Outro]
                [LYRICS_END]
                """

                # 3. कंटेंट जनरेट करना
                response = model.generate_content(system_prompt)
                full_text = response.text

                # 4. आउटपुट दिखाना
                st.divider()
                st.success(f"सफलतापूर्वक {my_model} मॉडल का उपयोग किया गया।")

                # डेटा को अलग-अलग करना
                try:
                    music_style = full_text.split("[STYLE_START]")[1].split("[STYLE_END]")[0].strip()
                    lyrics = full_text.split("[LYRICS_START]")[1].split("[LYRICS_END]")[0].strip()
                    
                    st.subheader("🎵 Suno Music Style")
                    st.code(music_style)
                    
                    st.subheader("📝 Suno Lyrics (Gurmukhi)")
                    st.code(lyrics)
                except:
                    st.code(full_text) # अगर फॉर्मेटिंग में कुछ अलग हुआ तो पूरा दिखाएगा

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Created for **@ruhanijot**")
