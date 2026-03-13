if st.button("Generate Complete Song & Style"):
    if song_input:
        with st.spinner('सही मॉडल खोज कर रचना तैयार की जा रही है...'):
            try:
                # 1. उपलब्ध मॉडल्स की लिस्ट चेक करना (Dynamic Selection)
                available_models = [m.name for m in genai.list_models() 
                                   if 'generateContent' in m.supported_generation_methods]
                
                # सबसे नया Flash मॉडल ढूँढना (वरना 1.5-flash को डिफ़ॉल्ट रखना)
                my_model = "models/gemini-1.5-flash" 
                for m in available_models:
                    if "gemini" in m.lower():
                        my_model = m
                        break
                
                # 2. चुने हुए मॉडल को सेट करना
                model = genai.GenerativeModel(my_model)
                
                # आपका वही पुराना सख्त प्रॉम्प्ट (System Instruction)
                system_prompt = f"""
                You are an expert Punjabi devotional lyricist.
                Category: {category}
                Input: {song_input}
                Chorus: {user_chorus if user_chorus else "Create a new rhyming chorus."}
                ... (बाकी सारे 10 नियम यहाँ रहेंगे) ...
                """

                # 3. कंटेंट जनरेट करना
                response = model.generate_content(system_prompt)
                
                # आउटपुट दिखाना
                st.info(f"उपयोग किया गया मॉडल: {my_model}")
                st.code(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
