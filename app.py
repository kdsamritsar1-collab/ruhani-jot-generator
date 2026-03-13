import streamlit as st

# पेज सेटअप
st.set_page_config(page_title="Ruhani Jot AI", page_icon="🎵")

st.title("🎵 Ruhani Jot: Suno AI Automator")
st.markdown("गाने के बोल डालें और AI आधारित संगीत शैली प्राप्त करें।")

# इनपुट फील्ड्स
song_text = st.text_area("यहाँ गाने की पंक्तियाँ लिखें:", height=150)
chorus_text = st.text_input("कोरस (Optional):")

if st.button("Generate Style & Format"):
    if song_text:
        # लॉजिक: शब्दों के आधार पर स्टाइल तय करना
        style = "Devotional, Soulful, Indian Classical, Raag Bhairavi, Soft Tabla" # Default
        
        if any(word in song_text for word in ["दर्शन", "शांति", "सिमरन", "नाम"]):
            style = "Male Vocals, Raag Darbari, Meditative, Sarangi, Soft Tabla, 70 BPM"
        elif any(word in song_text for word in ["फतेह", "खालसा", "सिंह", "जीत"]):
            style = "High Energy, Power Percussion, Nagada, Dhol, Cinematic, Folk Fusion"
        elif any(word in song_text for word in ["रूह", "मौला", "नूर", "साहब"]):
            style = "Sufi Rock, Rabab, Harmonium, Deep Vocals, Ambient, 90 BPM"

        # आउटपुट दिखाना
        st.subheader("📋 Music Style")
        st.code(style)
        
        full_lyrics = f"[Intro]\n\n[Verse]\n{song_text}\n\n"
        if chorus_text:
            full_lyrics += f"[Chorus]\n{chorus_text}\n\n"
        full_lyrics += "[Outro]\n[End]"
        
        st.subheader("📋 Lyrics Format")
        st.code(full_lyrics)
    else:
        st.error("कृपया पहले गाने के बोल डालें।")