import os
import hashlib
import requests
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")

st.set_page_config(page_title="ReaderWeb - AI Accessibility Reader", page_icon="🎧")
st.title("🎧 ReaderWeb: Accessibility Article Reader")
st.write("Paste any article URL below to strip ads, enable low-vision reading, and listen to a natural AI voice.")

os.makedirs("audio_cache", exist_ok=True)

DEFAULT_VOICES = {
    "Sarah (Soft & Clear)": "EXAVITQu4vr4xnSDxMaL",
    "George (Warm & Narrative)": "JBFqnCBsd6RMkjVDRZzb",
    "Charlie (Natural & Casual)": "IKne3meq5aSn9XLyUdCD",
    "Laura (Upbeat & Friendly)": "FGY2WhTYpPnrIDTdsKH5",
    "Liam (Articulate & Calm)": "TX3LPaxmHKxFdv7VOQHJ",
}

with st.sidebar:
    st.header("Accessibility & Voice Settings")
    if not API_KEY:
        st.error("API Key missing! Add ELEVENLABS_API_KEY to your .env file.")
    else:
        st.success("API Key loaded from .env ✅")

    low_vision_mode = st.toggle("👁️ Low-Vision High-Contrast Mode", value=True)
    selected_voice_name = st.selectbox("Choose a Voice", list(DEFAULT_VOICES.keys()))
    selected_voice_id = DEFAULT_VOICES[selected_voice_name]
    char_limit = st.slider("Max Characters per Audio (Saves Credits)", 150, 2000, 500)

def extract_clean_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
        
    paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 40]
    return "\n\n".join(paragraphs)

def trim_to_complete_sentence(text, limit):
    if len(text) <= limit:
        return text
    snippet = text[:limit]
    # Find the last sentence-ending punctuation mark
    last_end = max(snippet.rfind("."), snippet.rfind("!"), snippet.rfind("?"))
    if last_end > limit * 0.4:
        return snippet[:last_end + 1]
    return snippet

with st.form("reader_form"):
    url_input = st.text_input("Enter Article URL:", placeholder="https://wikipedia.org")
    submitted = st.form_submit_button("Convert to Audio")

if submitted:
    if not url_input:
        st.warning("Please enter a URL first.")
    elif not API_KEY:
        st.error("Please add ELEVENLABS_API_KEY to your .env file.")
    else:
        with st.spinner("Extracting clean article text..."):
            try:
                clean_text = extract_clean_text(url_input)
                if not clean_text:
                    st.error("Could not find readable paragraphs on this page.")
                    st.stop()
                
                trimmed_text = trim_to_complete_sentence(clean_text, char_limit)
                word_count = len(trimmed_text.split())
                est_seconds = max(1, round((word_count / 150) * 60))

                st.subheader("Extracted Reader View")
                col1, col2, col3 = st.columns(3)
                col1.metric("Characters", len(trimmed_text))
                col2.metric("Words", word_count)
                col3.metric("Est. Audio Length", f"~{est_seconds} sec")

                # Render High-Contrast Low-Vision Box or Standard Reader View
                if low_vision_mode:
                    st.markdown(
                        f"""
                        <div style="background-color: #000000; color: #FFE81F; padding: 24px; 
                        border-radius: 10px; font-size: 22px; line-height: 1.7; 
                        font-family: Arial, sans-serif; border: 2px solid #FFE81F;">
                        {trimmed_text.replace(chr(10), '<br>')}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.text_area("Cleaned Text", trimmed_text, height=220)

                st.write("")
                text_hash = hashlib.md5((trimmed_text + selected_voice_id).encode()).hexdigest()
                audio_path = f"audio_cache/{text_hash}.mp3"

                if os.path.exists(audio_path):
                    st.success("Loaded from local cache! (0 API credits used)")
                else:
                    with st.spinner("Generating AI voice via ElevenLabs..."):
                        client = ElevenLabs(api_key=API_KEY)
                        audio_generator = client.text_to_speech.convert(
                            text=trimmed_text,
                            voice_id=selected_voice_id,
                            model_id="eleven_multilingual_v2",
                            output_format="mp3_44100_128",
                        )
                        with open(audio_path, "wb") as f:
                            for chunk in audio_generator:
                                f.write(chunk)
                        st.success("Audio generated and cached locally!")

                st.audio(audio_path, format="audio/mp3")
                with open(audio_path, "rb") as file:
                    st.download_button("Download MP3", data=file, file_name="readerweb_article.mp3", mime="audio/mp3")

            except Exception as e:
                st.error(f"Error: {e}")
