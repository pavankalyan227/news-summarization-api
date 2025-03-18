import streamlit as st
import requests

st.title("📰 News Summarization & Hindi TTS")

company = st.text_input("Enter a company name")

if st.button("Fetch News"):
    response = requests.get(f"http://127.0.0.1:8000/news/{company}")
    if response.status_code == 200:
        data = response.json()
        st.write("### Extracted News Articles")
        for article in data["Articles"]:
            st.write(f"**{article['Title']}**")
            st.write(f"📜 {article['Summary']}")
            st.write(f"🟢 Sentiment: **{article['Sentiment']}**")
            st.write("---")
    else:
        st.error("Failed to fetch news!")

if st.button("Generate Hindi Speech"):
    response = requests.get(f"http://127.0.0.1:8000/tts/{company}")
    if response.status_code == 200:
        audio_path = response.json()["audio_path"]
        if audio_path:
            st.audio(audio_path)
        else:
            st.error("No speech generated!")
    else:
        st.error("Failed to generate TTS!")
