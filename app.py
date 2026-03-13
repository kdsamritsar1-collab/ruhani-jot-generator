import streamlit as st
import google.generativeai as genai

# 1. API Key कॉन्फ़िगरेशन
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key not found. Please add GEMINI_API_KEY in Streamlit Secrets.")

# 2. पेज सेटअप
st.set_page_config(page_title="Ruhani Jot AI Dashboard", page_icon="☬", layout="wide")

st.markdown('<h1 style="color: #ff9800;">☬ Ruhani Jot: Ultimate Content Creator</h1>', unsafe_allow_html=True)

# 3. इनपुट पैनल
col1, col2 = st.columns([1, 1])

with col1:
    category = st.selectbox(
        "Select Category:",
        ["Devotional", "Kirtan", "Shabad", "Gurbani", "History based"]
    )
    song_input = st.text_area("Song Idea / Short Description:", placeholder="e.g., The spiritual power of Sarovar...", height=150)

with col2:
    user_chorus = st.text_input("Chorus (Optional):", placeholder="Leave blank for AI to generate...")
    translate_desc = st.checkbox("Include Punjabi Translation of Video Description", value=True)
    st.info("Output: Style & SEO in English | Lyrics in Gurmukhi.")

# 4. मुख्य लॉजिक
if st.button("Generate All Assets"):
    if not song_input:
        st.warning("Please enter a description or idea.")
    else:
        with st.spinner('Crafting global SEO and spiritual lyrics...'):
            try:
                # उपलब्ध मॉडल ढूँढना (Auto-Detect Logic)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                my_model = "models/gemini-1.5-flash"
                for m in available_models:
                    if "gemini" in m.lower():
                        my_model = m
                        break
                
                model = genai.GenerativeModel(my_model)

                # उन्नत प्रॉम्प्ट
                system_prompt = f"""
                You are an expert Punjabi Devotional Lyricist and YouTube SEO Manager.
                Input Idea: {song_input}
                Category: {category}
                Chorus: {f"Use this exactly: {user_chorus}" if user_chorus else "Create a new spiritually deep chorus."}

                TASK 1: Write a Shabad/Song in pure GURMUKHI script (5 Verses + 1 Chorus).
                TASK 2: Suggest a Suno.com Music Style in ENGLISH (under 120 chars).
                TASK 3: Provide YouTube SEO Metadata in ENGLISH:
                - 3 Viral Titles.
                - Professional Video Description (integrating keywords).
                - 15 Trending Tags/Keywords.
                - 5 Popular Hashtags.
                TASK 4: {f"Translate the Video Description into pure GURMUKHI Punjabi as well." if translate_desc else ""}
                TASK 5: Provide a high-quality ENGLISH Image Prompt for an AI Thumbnail.

                Strictly format the output using these markers: [STYLE], [LYRICS], [SEO], [PUNJABI_DESC], [THUMBNAIL].
                """

                response = model.generate_content(system_prompt)
                full_text = response.text

                # डेटा को विभाजित (Parse) करना
                try:
                    style_part = full_text.split("[STYLE]")[1].split("[LYRICS]")[0].strip()
                    lyrics_part = full_text.split("[LYRICS]")[1].split("[SEO]")[0].strip()
                    seo_part = full_text.split("[SEO]")[1].split("[PUNJABI_DESC]")[0].strip()
                    
                    if translate_desc:
                        punjabi_desc = full_text.split("[PUNJABI_DESC]")[1].split("[THUMBNAIL]")[0].strip()
                    else:
                        punjabi_desc = "Translation not requested."
                        
                    thumbnail_part = full_text.split("[THUMBNAIL]")[1].strip()

                    # टैब सिस्टम
                    tab1, tab2, tab3, tab4 = st.tabs(["🎵 Music & Lyrics", "📈 YouTube SEO", "ੴ Punjabi Desc", "🎨 Thumbnail"])

                    with tab1:
                        st.subheader("Suno Style (English)")
                        st.code(style_part)
                        st.subheader("Lyrics (Gurmukhi)")
                        st.code(lyrics_part)
                    
                    with tab2:
                        st.subheader("YouTube SEO (English)")
                        st.code(seo_part)
                    
                    with tab3:
                        st.subheader("Punjabi Video Description")
                        if translate_desc:
                            st.code(punjabi_desc)
                        else:
                            st.write("Enable the checkbox to generate Punjabi description.")
                    
                    with tab4:
                        st.subheader("AI Thumbnail Image Prompt")
                        st.code(thumbnail_part)
                
                except Exception as parse_error:
                    st.code(full_text) # Fallback if parsing fails

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Developed for **@ruhanijot** | Amritsar | 2026 SEO Optimized")
