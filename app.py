import streamlit as st
import google.generativeai as genai

# Streamlit Secrets से Gemini API Key कॉन्फ़िगर करें
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key नहीं मिली। कृपया Streamlit Settings > Secrets में GEMINI_API_KEY डालें।")

# पेज सेटअप
st.set_page_config(page_title="Ruhani Jot AI", page_icon="☬", layout="wide")

# CSS: आउटपुट को सुंदर और पठनीय बनाने के लिए
st.markdown("""
    <style>
    .stCode { background-color: #f0f2f6 !important; border-radius: 10px; }
    .main-header { color: #ff9800; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">☬ Ruhani Jot: Advanced Shabad & Song Creator</p>', unsafe_allow_html=True)

# इनपुट पैनल
with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        category = st.selectbox(
            "श्रेणी (Category) चुनें:",
            ["Devotional", "Kirtan", "Shabad", "Gurbani", "History based"]
        )
        
        song_input = st.text_area(
            "गाने का विवरण या पंक्तियाँ (Description/Lines):", 
            placeholder="जैसे: गुरु साहिब की महिमा या कोई विशेष सिख इतिहास की घटना...",
            height=150
        )

    with col2:
        user_chorus = st.text_input(
            "कोरस (Chorus) - वैकल्पिक:", 
            placeholder="खाली छोड़ने पर AI तुकबंदी के साथ खुद बनाएगा..."
        )
        st.info("""
        **निर्देश:**
        * आउटपुट केवल गुरमुखी (Punjabi) में होगा।
        * 5 बंद (Verses) और 1 कोरस तैयार किया जाएगा।
        * संगीत शैली (Music Style) बोलों के आधार पर चुनी जाएगी।
        """)

# बटन और लॉजिक
if st.button("Generate Complete Song & Style"):
    if not song_input:
        st.warning("कृपया पहले कुछ विवरण या विचार लिखें।")
    else:
        with st.spinner('AI आपकी रूहानी रचना तैयार कर रहा है...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # कोडिंग के अंदर ही आपके द्वारा दिए गए सख्त निर्देश
                system_prompt = f"""
                You are an expert Punjabi devotional lyricist with deep knowledge of Gurbani, Sikh history, and Sikh philosophy.
                Category: {category}

                Write a Sikh devotional song in pure Punjabi (Gurmukhi script only). Do NOT use any English or Hinglish words.

                Requirements:
                1. The song must be based on: {song_input}
                2. Praise Waheguru, Naam Simran, Guru Sahib, and truthful living.
                3. Ensure all lines are respectful and aligned with Sikh teachings (Gurbani & Rehat Maryada).
                4. Proper 'tukhbandi' (rhyming scheme) that naturally matches the chorus.
                5. Structure: 1 Chorus and 5 Verses (Each verse 4 meaningful lines).
                6. Chorus Logic: {f"Use this EXACT chorus: {user_chorus}" if user_chorus else "Create a new spiritually meaningful and rhyming chorus yourself."}
                7. Tone: Peaceful and devotional.
                
                Output Format (Strictly follow this):
                
                [STYLE_START]
                (Provide a music style under 120 chars for Suno.com including Raag, instruments like Dilruba, Tabla, and mood based on the lyrics).
                [STYLE_END]

                [LYRICS_START]
                [Intro]

                [Verse 1]
                (4 lines)

                [Chorus]
                (The main chorus)

                [Verse 2]
                (4 lines)

                [Chorus]

                [Verse 3]
                (4 lines)

                [Chorus]

                [Verse 4]
                (4 lines)

                [Chorus]

                [Verse 5]
                (4 lines)

                [Chorus]

                [Outro]
                [LYRICS_END]
                """

                response = model.generate_content(system_prompt)
                full_text = response.text

                # आउटपुट को पार्स (Parse) करना
                try:
                    music_style = full_text.split("[STYLE_START]")[1].split("[STYLE_END]")[0].strip()
                    lyrics = full_text.split("[LYRICS_START]")[1].split("[LYRICS_END]")[0].strip()
                except:
                    music_style = "Devotional, Raag Based, Tabla, Dilruba, Peaceful"
                    lyrics = full_text

                st.divider()

                # डिस्प्ले और कॉपी सेक्शन
                st.subheader("🎵 Suno Music Style")
                st.code(music_style, language=None)
                st.caption("इसे Suno.com के 'Style' बॉक्स में पेस्ट करें।")

                st.subheader("📝 Suno Lyrics (Full Shabad)")
                st.code(lyrics, language=None)
                st.caption("इसे Suno.com के 'Lyrics' बॉक्स में पेस्ट करें।")

            except Exception as e:
                st.error(f"क्षमा करें, कुछ तकनीकी खराबी आई: {e}")

# फुटर
st.markdown("---")
st.markdown("Created for **@ruhanijot** | Spirituality Meets AI")
