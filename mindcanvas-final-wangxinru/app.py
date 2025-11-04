import streamlit as st
import plotly.express as px
import random
import requests

st.set_page_config(page_title="MindCanvas — DreamWeaver Edition", page_icon="🌌", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #b8c6ff 0%, #e8e9ff 50%, #d5d9f6 100%);
    color: #101018;
    font-family: "Inter", sans-serif;
}
.stApp {
    background: radial-gradient(circle at 50% 20%, rgba(180,180,255,0.3), rgba(200,220,255,0.1));
}
h1, h2, h3 {
    font-family: "Inter", sans-serif;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.title("🌌 MindCanvas • DreamWeaver Edition")
st.markdown("A synesthetic space where dreams meet data — Created by **Wang Xinru**")

# ---------------- INPUT ----------------
keyword = st.text_input("Enter a dream keyword (e.g. ocean, flying, city, forest):", "dream")

# ---------------- EMOTION ANALYZER ----------------
st.header("🧠 Emotion Analyzer")
emo_labels = ["Joy", "Curiosity", "Peace", "Wonder", "Sadness", "Fear"]
emo_scores = [round(random.uniform(0.1, 1.0), 2) for _ in emo_labels]
fig = px.bar(x=emo_labels, y=emo_scores, color=emo_labels, title="Simulated Emotion Distribution")
st.plotly_chart(fig, use_container_width=True)
st.caption("✨ Local mode: showing simulated emotional spectrum.")

# ---------------- VISUAL MOOD BOARD ----------------
st.header("🖼️ Visual Mood Board")

try:
    unsplash_url = f"https://source.unsplash.com/800x600/?{keyword},art,dream"
    st.image(unsplash_url, caption=f"keyword: {keyword}")
except Exception as e:
    st.warning(f"Image failed to load: {e}")

# ---------------- SOUNDSCAPE ----------------
st.header("🎵 Soundscape")

sound_choices = [
    "https://cdn.pixabay.com/download/audio/2021/08/08/audio_720b7cc77f.mp3?filename=ambient-piano-11111.mp3",
    "https://cdn.pixabay.com/download/audio/2022/03/15/audio_1b1b4e4a90.mp3?filename=dreamy-ambient-piano-110054.mp3",
    "https://cdn.pixabay.com/download/audio/2021/09/14/audio_19f2bfa05b.mp3?filename=dreamy-ambient-1135.mp3"
]
st.audio(random.choice(sound_choices))
st.caption("🎧 Ambient dream sound loaded locally")

# ---------------- MOOD QUOTE ----------------
st.header("💬 Mood Quote")
quotes = [
    ("Dreams are the whispers of the soul.", "Unknown"),
    ("In dreams, we touch the infinite.", "Anaïs Nin"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("A single dream is more powerful than a thousand realities.", "J.R.R. Tolkien"),
    ("Hold fast to dreams, for if dreams die, life is a broken-winged bird.", "Langston Hughes")
]
quote, author = random.choice(quotes)
st.markdown(f"_{quote}_ — **{author}**")

# ---------------- AI REFLECTION ----------------
st.header("🪞 AI Reflection")
reflections = [
    f"✨ In the realm of {keyword}, emotions bloom like constellations in the sky.",
    f"✨ Every {keyword} drifts between memory and imagination, a bridge of unseen colors.",
    f"✨ To dream of {keyword} is to remember what it means to feel alive.",
    f"✨ {keyword.capitalize()} becomes a mirror — reflecting both longing and peace.",
    f"✨ Beneath the {keyword}, silence hums with the rhythm of forgotten dreams."
]
st.write(random.choice(reflections))

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Created by Wang Xinru — MindCanvas Final Edition 🌙")
