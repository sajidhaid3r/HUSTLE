import os
import json
import io
import urllib.parse
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gtts import gTTS

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Visual Novel Engine", layout="wide")
st.title("📖 Multi-Modal Visual Novel Engine")

# ==========================================
# PHASE 1: DIRECTORS CUT (UI & CACHING)
# ==========================================

# Sidebar Settings
st.sidebar.header("Story Settings")
genre = st.sidebar.selectbox("Story Genre", ["Cyberpunk", "High Fantasy", "Sci-Fi Space Opera", "Cosmic Horror", "Post-Apocalyptic"])
art_style = st.sidebar.selectbox("Art Style", ["Anime / Manga Style", "Digital Concept Art", "Oil Painting", "Pixel Art", "Cinematic Photorealism"])

@st.cache_resource
def get_ai_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found in .env file!")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_ai_client()

# Function to start or reset the story engine
def init_story():
    st.session_state.chat_history = []
    
    # Configure Gemini with a strict JSON system prompt
    system_instruction = f"""
    You are the Game Master for an interactive visual novel game.
    Genre: {genre}
    Art Style: {art_style}

    CRITICAL REQUIREMENT:
    You MUST ALWAYS respond with a SINGLE valid JSON object.
    
    The JSON MUST contain exactly these 3 keys:
    1. "story_text": A compelling 2 to 3 sentence narrative scene.
    2. "image_prompt": A visual description for an image generator. Always include '{art_style}, highly detailed' in the prompt.
    3. "options": A list of 2 to 3 distinct short choice strings for the user's next action.
    """
    
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
            response_mime_type="application/json"
        )
    )
    
    # Generate scene 1
    fetch_next_scene("Begin the story. Introduce the protagonist and setting.")

# ==========================================
# PHASES 2, 4 & 5: JSON PARSING, APIS & ERROR HANDLING
# ==========================================
def fetch_next_scene(user_action):
    # 1. Send message to Gemini and parse JSON
    try:
        response = st.session_state.gemini_chat.send_message(user_action)
        data = json.loads(response.text.strip())
        
        story_text = data.get("story_text", "The story continues...")
        image_prompt = data.get("image_prompt", f"A scene from {genre}")
        options = data.get("options", ["Step forward", "Look around"])
    except Exception as e:
        st.toast("⚠️ Error reading structured story output. Using fallback narrative...")
        story_text = "An unknown phenomenon temporarily blurs your path."
        image_prompt = f"A mysterious scenery in {genre} style"
        options = ["Inspect surroundings", "Proceed with caution"]

    # 2. Visuals: Pollinations AI with graceful failure
    image_bytes = None
    try:
        clean_prompt = urllib.parse.quote(image_prompt)
        url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=576&seed=42&nologo=true"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            image_bytes = res.content
        else:
            st.toast("Image server is busy, skipping visual...")
    except Exception:
        st.toast("Image server network error, skipping visual...")

    # 3. Audio: gTTS with graceful failure
    audio_bytes = None
    try:
        tts = gTTS(text=story_text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_bytes = fp.read()
    except Exception:
        st.toast("Audio narration unavailable for this turn.")

    # Save current scene to chat history
    st.session_state.chat_history.append({
        "story_text": story_text,
        "image": image_bytes,
        "audio": audio_bytes,
        "options": options,
        "user_action": user_action
    })

# Initialize session state if first run
if "chat_history" not in st.session_state:
    init_story()

# Sidebar Reset Button
if st.sidebar.button("🔄 Restart Story", use_container_width=True):
    init_story()
    st.rerun()

# ==========================================
# PHASES 3 & 4: RENDERING & DYNAMIC BUTTONS
# ==========================================

# Render all generated scenes in story history
for idx, scene in enumerate(st.session_state.chat_history):
    st.markdown("---")
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        if scene["image"]:
            st.image(scene["image"], use_container_width=True)
        else:
            st.info("🖼️ [Image Unavailable - Narrative Continues]")
            
    with col2:
        st.subheader(f"Scene {idx + 1}")
        st.write(scene["story_text"])
        
        if scene["audio"]:
            st.audio(scene["audio"], format="audio/mp3")

# Render dynamic choice buttons for the latest scene
if st.session_state.chat_history:
    latest_scene = st.session_state.chat_history[-1]
    
    st.markdown("### 🎯 What do you do next?")
    
    btn_cols = st.columns(len(latest_scene["options"]))
    for i, option in enumerate(latest_scene["options"]):
        with btn_cols[i]:
            # Unique key ensures Streamlit doesn't throw button ID collisions
            btn_key = f"opt_btn_{len(st.session_state.chat_history)}_{i}"
            if st.button(option, key=btn_key, use_container_width=True):
                with st.spinner("Writing the next scene..."):
                    fetch_next_scene(option)
                    st.rerun()

# ==========================================
# DOWNLOAD CHAT HISTORY (LOOPED EXPORT)
# ==========================================
st.sidebar.markdown("---")
if st.session_state.get("chat_history"):
    history_lines = []
    for i, item in enumerate(st.session_state.chat_history):
        history_lines.append(f"--- SCENE {i + 1} ---")
        history_lines.append(f"User Action: {item['user_action']}")
        history_lines.append(f"Story Text: {item['story_text']}\n")
    
    formatted_chat_history = "\n".join(history_lines)

    st.sidebar.download_button(
        label="📥 Download Chat History",
        data=formatted_chat_history,
        file_name="visual_novel_story.txt",
        mime="text/plain",
        use_container_width=True
    )