import streamlit as st
import requests
import plotly.express as px

# ----- PAGE CONFIG -----
st.set_page_config(page_title="MindCanvas — DreamWeaver Edition", page_icon="🧠", layout="wide")

# ----- STYLE -----
st.markdown('''
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
''', unsafe_allow_html=True)

st.title("🌌 MindCanvas • DreamWeaver Edition")
st.markdown("A synesthetic space where dreams meet data — Created by **Wang Xinru**")

# ----- Load API Keys -----
NINJAS_KEY = st.secrets.get("ninjas_key")
HF_TOKEN = st.secrets.get("hf_token")
PIXABAY_KEY = st.secrets.get("pixabay_key")

# ----- Input -----
keyword = st.text_input("Enter a dream keyword (e.g. ocean, flying, city, forest):", "dream")

# ----- Emotion Analyzer -----
st.header("🧠 Emotion Analyzer")
if HF_TOKEN:
    try:
        resp = requests.post(
            "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": f"I had a dream about {keyword}. It made me feel emotional and inspired."},
            timeout=15
        )
        data = resp.json()
        # Fix inconsistent structure
        emotions = []
        if isinstance(data, list):
            if isinstance(data[0], list):
                emotions = data[0]
            elif isinstance(data[0], dict):
                emotions = data
        if emotions:
            df = {item["label"]: item["score"] for item in emotions}
            fig = px.bar(
                x=list(df.keys()),
                y=list(df.values()),
                title="Emotion Distribution",
                color=list(df.keys()),
                labels={"x": "Emotion", "y": "Confidence"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No emotion data returned.")
    except Exception as e:
        st.warning(f"Emotion API error: {e}")
else:
    st.info("请在 secrets 中设置 HuggingFace token。")

# ----- Visual Mood Board -----
st.header("🖼️ Visual Mood Board")
if PIXABAY_KEY:
    try:
        img_url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={keyword}&image_type=photo&per_page=3"
        r = requests.get(img_url, timeout=10)
        if r.headers.get("Content-Type", "").startswith("application/json"):
            data = r.json()
            if data.get("hits"):
                st.image(data["hits"][0]["webformatURL"], caption=f"keyword: {keyword}")
            else:
                st.warning("未找到相关图片。")
        else:
            st.warning("Pixabay 图像接口暂时不可用。")
    except Exception as e:
        st.error(f"Pixabay 图像错误: {e}")
else:
    st.info("请在 secrets 中设置 Pixabay key。")

# ----- Soundscape -----
st.header("🎵 Soundscape")
if PIXABAY_KEY:
    try:
        sound_url = f"https://pixabay.com/api/audio/?key={PIXABAY_KEY}&q={keyword}&per_page=3"
        r = requests.get(sound_url, timeout=10)
        if r.headers.get("Content-Type", "").startswith("application/json"):
            data = r.json()
            if data.get("hits"):
                audio = data["hits"][0].get("audio") or data["hits"][0].get("previewURL")
                if audio:
                    st.audio(audio)
                else:
                    st.warning("找到音效但无有效音频链接。")
            else:
                st.warning("未找到相关音效。")
        else:
            st.warning("Pixabay 返回的不是 JSON（可能服务器繁忙）。")
    except Exception as e:
        st.error(f"音效模块错误: {e}")
else:
    st.info("请在 secrets 中设置 Pixabay key。")

# ----- Mood Quote -----
st.header("💬 Mood Quote")
if NINJAS_KEY:
    try:
        url = "https://api.api-ninjas.com/v1/quotes?category=dreams"
        headers = {"X-Api-Key": NINJAS_KEY}
        res = requests.get(url, headers=headers, timeout=10)
        if res.headers.get("Content-Type", "").startswith("application/json"):
            quotes = res.json()
            if isinstance(quotes, list) and quotes:
                q = quotes[0]
                st.markdown(f"_{q['quote']}_ — **{q['author']}**")
            else:
                st.warning("未获得引用。")
        else:
            st.warning("API Ninjas 返回的不是 JSON。")
    except Exception as e:
        st.error(f"Quote API 错误: {e}")
else:
    st.info("请在 secrets 中设置 API Ninjas key。")

# ----- AI Reflection -----
st.header("🪞 AI Reflection")
if HF_TOKEN:
    try:
        payload = {"inputs": f"Write a short poetic reflection about {keyword} and human emotions in two sentences."}
        url = "https://api-inference.huggingface.co/models/gpt2-medium"
        r = requests.post(url, headers={"Authorization": f"Bearer {HF_TOKEN}"}, json=payload, timeout=20)
        result = r.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            text = result[0]["generated_text"]
            st.write(text[:400])
        else:
            st.write("✨ The dream fades into silence... (no reflection generated)")
    except Exception as e:
        st.warning(f"HuggingFace 反思模块错误: {e}")
else:
    st.info("请在 secrets 中设置 HuggingFace token。")

# ----- Footer -----
st.markdown("---")
st.caption("Created by Wang Xinru — MindCanvas Final Edition 🌙")
