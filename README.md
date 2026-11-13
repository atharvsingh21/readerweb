# 🎧 ReaderWeb — AI Accessibility Article Reader

ReaderWeb is an assistive web application built to help visually impaired, dyslexic, and auditory learners consume online articles effortlessly. It strips advertisements and webpage clutter, offers a high-contrast low-vision reading mode, and converts clean text into natural human speech using the ElevenLabs API.

## ✨ Key Features
* **Distraction-Free DOM Scraper:** Uses `BeautifulSoup4` to remove navigation bars, scripts, headers, footers, and ads, isolating clean article paragraphs.
* **Low-Vision High-Contrast Mode:** Renders extracted text in an extra-large (`22px`), high-contrast yellow-on-black interface alongside word count and estimated listening duration.
* **Smart Sentence-Boundary Trimming:** Automatically trims text at the nearest sentence-ending punctuation mark so audio never cuts off mid-word.
* **MD5 Hash Audio Caching:** Hashes text and voice selections locally to reuse generated `.mp3` files and prevent duplicate API credit usage.
* **Downloadable Offline Audio:** Allows users to download generated audio clips for offline listening.

## 🛠️ Tech Stack
* **Frontend & UI:** Python, Streamlit
* **Web Scraping:** Requests, BeautifulSoup4
* **AI Voice Synthesis:** ElevenLabs Text-to-Speech API (`eleven_multilingual_v2`)
* **Security & Caching:** `python-dotenv`, `hashlib` (MD5)

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd readerweb
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   Create a `.env` file in the root directory and add your ElevenLabs API key:
   ```text
   ELEVENLABS_API_KEY=your_api_key_here
   ```

5. **Launch the application:**
   ```bash
   streamlit run app.py
   ```
