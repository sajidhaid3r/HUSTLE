# HUSTLE — MIRAI Internship (2 Months)

This repository is a learning log from a 2-month AI/Python internship. Every script here is written in **Python**, and the UI/frontend layer for all interactive apps is built with **Streamlit**. The core "brains" of the apps come from **Google's Gemini API** (via the `google-genai` SDK) for text/chat generation, and the **Pollinations AI** image endpoint for AI image generation. Environment variables (like the Gemini API key) are managed with **python-dotenv**.

The repo is organized into two kinds of work:
- **Sessions** — small, guided exercises done during each class to learn one new concept at a time (API calls, Streamlit basics, sidebars, chat memory, image generation, etc.)
- **Assignments** — bigger, self-built tasks that combine everything learned in the sessions into a more complete mini-application.

---

## Tech Stack

| Tool / Library | Purpose |
|---|---|
| **Python** | Core programming language for every file in this repo |
| **Streamlit** | Framework used to build all the web UIs (text inputs, buttons, sidebars, chat interface, file downloads, etc.) |
| **google-genai** (`google.genai`) | Official SDK used to call the **Gemini** models (`gemini-2.5-flash`) for text generation and chat |
| **python-dotenv** | Loads the `GEMINI_API_KEY` from a local `.env` file instead of hardcoding it |
| **requests** | Used to call external HTTP APIs (e.g. the Pollinations image-generation endpoint) |
| **Pollinations AI** (`image.pollinations.ai`) | Free text-to-image API used to generate images from a text prompt |

### Setup

```bash
# Install Python packages
pip install streamlit
pip install google-genai
pip install python-dotenv
pip install requests

# Create a .env file in the project root with:
# GEMINI_API_KEY=your_api_key_here

# View Streamlit's own documentation/demo
py -m streamlit hello

# Run any Streamlit app in this repo
py -m streamlit run <filename>.py
```

(These commands are also captured in the [`COMMANDS`](./COMMANDS) file.)

---

## 📘 Sessions

Step-by-step exercises, each one adding a new Streamlit or Gemini concept on top of the last.

### `INTERN.py` — First Gemini API Call
The very first exercise. Connects to the Gemini API using `genai.Client` and sends a single hardcoded prompt ("Explain how the Gemini API works in one sentence") using the `gemini-2.5-flash` model, then prints the response text to the console. No Streamlit UI yet — pure API call to understand the request/response cycle.

### `app.py` — First Streamlit UI
The first Streamlit app in the repo. Displays a title and some text, takes a user's name through `st.text_input`, and shows it back on screen when a button (`st.button`) is clicked. This is the "Hello World" of the UI layer — no AI involved yet, just learning Streamlit's basic input/output/button flow.

### `calculator.py` — Basic Streamlit Logic App
A simple calculator built with Streamlit. Takes two numbers via `st.number_input` and an operator (`+`, `-`, `*`, `/`) via `st.selectbox`, then computes and displays the result when "Calculate" is clicked. Includes a basic check for division by zero. Used to practice Streamlit widgets combined with everyday Python logic/conditionals.

### `Session3.py` — "Multiverse of Chatbots" (Single-turn)
Introduces AI personality role-play. The user picks a personality (e.g. "Virat Kohli", "An angry Ravi Shastri") from a dropdown, types a message, and the app builds a prompt instructing Gemini to respond *as* that personality. Uses `st.spinner` to show a loading state while waiting for the Gemini response, and `dotenv`/`os.getenv` to securely load the API key.

### `Session4.py` — Personality Chat + Sidebar Controls
Builds on Session 3 by moving the personality selector into the **sidebar** (`st.sidebar.selectbox`) and adding an **intensity slider** (`st.sidebar.slider`) so the user can control how strongly the AI plays the chosen personality. This introduces sidebar layout and slider widgets as extra input controls that shape the prompt sent to Gemini.

### `Session5.py` — AI Image Generator
A text-to-image tool. The sidebar lets the user pick an art style (Photorealistic, Cartoon, Anime, Abstract, Fantasy) and set image width/height using sliders. The user's text prompt is combined with the chosen art style and sent to the Pollinations AI image endpoint via `requests.get`. The generated image is displayed with `st.image` and made downloadable with `st.download_button`.

### `Session6.py` — AI Chat With History (Persistent Conversation)
The most advanced session exercise. Uses `st.session_state` to store chat history across interactions and `@st.cache_resource` to avoid re-creating the Gemini client on every rerun. Instead of a one-off `generate_content` call, it uses `client.chats.create(...)` to start a persistent Gemini **chat session**, so the AI remembers earlier turns in the conversation. Displays the full conversation using `st.chat_message`/`st.chat_input`, and adds a `st.download_button` to export the entire chat history as a `.txt` file.

---

## 📗 Assignments

Larger, self-directed builds that combine the concepts learned across sessions.

### `assignment2.py` — AI Multiverse Chat App
A more polished version of the personality chatbot. Sets a custom page title/icon with `st.set_page_config`, offers a longer list of selectable personalities (Common Indian Man, Crazy Salman Khan Fan, Motivational Coach, Software Engineer, Stand-up Comedian, etc.), and maintains full chat history using `st.session_state`. Adds a **"Clear Chat"** button in the sidebar to reset the conversation, and wraps the Gemini API call in a `try/except` block for basic error handling so the app doesn't crash if the request fails.

### `Assignment3.py` — Multiverse Chatbot (Memory Vault Edition)
Similar in spirit to `assignment2.py` but refactored: personality options ("Helpful Assistant", "Funny Friend", "Strict Teacher", "Motivational Coach") live in the sidebar, and chat history is referred to as a "Memory Vault" stored in `st.session_state.messages`. Uses `st.chat_input`/`st.chat_message` for a native chat-style interface, and builds a dynamic system prompt that tells Gemini which personality to adopt before generating each reply.

### `4a.py` — Single-Shot AI Image Generator (Script)
A plain Python script (no Streamlit UI) that sends one hardcoded, descriptive text prompt to the Pollinations image API using `requests.get`, then saves the returned image bytes to disk as `GOAT.png`. Used to test and understand the image-generation API directly before wrapping it in a Streamlit interface.

### `Assignment4/code.py` — Full-Featured AI Image Generator App
The most complete assignment in the repo. A polished Streamlit app for AI image generation that includes:
- Sidebar controls for image **width/height** (`st.number_input`) and a **"Magic Enhance"** checkbox that appends quality-boosting keywords (e.g. "masterpiece, 8k resolution, highly detailed") to the prompt
- A **"Surprise Me!"** button that picks a random prompt from a predefined list instead of requiring user input
- Proper URL encoding of prompts with `urllib.parse.quote`
- Error handling with automatic **retry logic** — if generation fails with Magic Enhance on, it retries with the original, unenhanced prompt
- Saving the generated image to disk via `pathlib.Path`, displaying it with `st.image`, and offering it as a download with `st.download_button`

The `Assignment4/Video` file contains links to a Google Drive demo video and a LinkedIn post showcasing this project in action.

### `COMMANDS` — Reference Notes
Not a Python file — a plain text cheat-sheet of terminal commands used throughout the internship (installing `google-genai`, installing `streamlit`, running the Streamlit docs, and running a Streamlit app).

---

## Project Structure

```
HUSTLE/
├── app.py                 # Session: first Streamlit UI
├── calculator.py          # Session: basic Streamlit calculator
├── Session3.py            # Session: personality chatbot (single-turn)
├── Session4.py            # Session: personality chatbot + sidebar/slider
├── Session5.py            # Session: AI image generator
├── Session6.py            # Session: AI chat with memory/history
├── INTERN.py              # Session: first raw Gemini API call
├── assignment2.py         # Assignment: AI Multiverse chat app
├── Assignment3.py         # Assignment: Multiverse chatbot (memory vault)
├── 4a.py                  # Assignment: single-shot image generator script
├── Assignment4/
│   ├── code.py            # Assignment: full-featured AI image generator app
│   └── Video               # Demo video / LinkedIn post links
├── COMMANDS                # Terminal command reference notes
└── README.md
```
