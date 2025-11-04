import streamlit as st
import requests
import plotly.express as px
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
    </style>
''', unsafe_allow_html=True)

st.title("🌌 MindCanvas • DreamWeaver Edition")
st.markdown("A synesthetic space where dreams meet data — Created by **Wang Xinru**")

# ----- Load API keys -----
NINJAS_KEY = st.secrets.get("ninjas_key")
HF_TOKEN = st.secrets.get("hf_token")
PIXABAY_KEY = st.secrets.get("pixabay_key")

# ----- Input Section -----
keyword = st.text_input("Enter a dream keyword (e.g. ocean, flying, city, forest):", "dream")

# ----- Emotion Analyzer (HuggingFace) -----
st.header("🧠 Emotion Analyzer")
if HF_TOKEN:
    try:
        resp = requests.post(
            "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": keyword},
            timeout=10
        )
        data = resp.json()[0] if isinstance(resp.json(), list) else []
        if data:
            df = {item["label"]: item["score"] for item in data}
            fig = px.bar(x=list(df.keys()), y=list(df.values()), title="Emotion Distribution", color=list(df.keys()))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No emotion data returned.")
    except Exception as e:
        st.warning(f"Emotion API error: {e}")
else:
    st.info("请在 secrets 中设置 HuggingFace token。")

# ----- Visual Mood Board (Pixabay Image) -----
st.header("🖼️ Visual Mood Board")
if PIXABAY_KEY:
    try:
        img_url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={keyword}&image_type=photo&per_page=3"
        r = requests.get(img_url).json()
        if r.get("hits"):
            st.image(r["hits"][0]["webformatURL"], caption=f"keyword: {keyword}")
        else:
            st.warning("未找到相关图片。")
    except Exception as e:
        st.error(f"Pixabay 图像错误: {e}")
else:
    st.info("请在 secrets 中设置 Pixabay key。")

# ----- Soundscape (Pixabay Audio) -----
st.header("🎵 Soundscape")
if PIXABAY_KEY:
    try:
        sound_url = f"https://pixabay.com/api/audio/?key={PIXABAY_KEY}&q={keyword}&per_page=3"
        r = requests.get(sound_url).json()
        if r.get("hits"):
            audio = r["hits"][0]["audio"]
            st.audio(audio)
        else:
            st.warning("未找到相关音效。")
    except Exception as e:
        st.error(f"音效模块错误: {e}")
else:
    st.info("请在 secrets 中设置 Pixabay key。")

# ----- Mood Quote (API Ninjas) -----
st.header("💬 Mood Quote")
if NINJAS_KEY:
    try:
        url = f"https://api.api-ninjas.com/v1/quotes?category=inspirational"
        headers = {"X-Api-Key": NINJAS_KEY}
        res = requests.get(url, headers=headers, timeout=10).json()
        if isinstance(res, list) and res:
            st.markdown(f"_{res[0]['quote']}_ — **{res[0]['author']}**")
        else:
            st.warning("未获得引用。")
    except Exception as e:
        st.error(f"Quote API 错误: {e}")
else:
    st.info("请在 secrets 中设置 API Ninjas key。")

# ----- AI Reflection (HuggingFace Text Generation) -----
st.header("🪞 AI Reflection")
if HF_TOKEN:
    try:
        payload = {"inputs": f"Write a poetic reflection about {keyword} and human emotion."}
        r = requests.post("https://api-inference.huggingface.co/models/gpt2",
                          headers={"Authorization": f"Bearer {HF_TOKEN}"},
                          json=payload,
                          timeout=10)
        result = r.json()
        text = result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else "No reflection generated."
        st.write(text[:400])
    except Exception as e:
        st.warning(f"HuggingFace 反思模块错误: {e}")
else:
    st.info("请在 secrets 中设置 HuggingFace token。")

st.markdown("---")
st.caption("Created by Wang Xinru — MindCanvas Final Edition")
