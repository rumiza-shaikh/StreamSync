import streamlit as st
from pytube import YouTube
import openai
import tempfile
import os

# CONFIG
openai.api_key = st.secrets["openai_api_key"]

# APP TITLE
st.title("🎬 StreamSync: GenAI-Powered Content Navigator")

# VIDEO INPUT
video_input = st.text_input("Paste YouTube URL or upload a file below:")
uploaded_file = st.file_uploader("Or upload a video file (.mp4)", type=["mp4"])

# TRANSCRIPTION PLACEHOLDER (you'd replace this with Whisper API or AssemblyAI in prod)
def fake_transcribe(video_path):
    # Placeholder for actual transcription logic
    return "This is a sample transcript about climate change, emotional appeal, statistics, urgency, and hope."

# CHUNKING & ANALYSIS
def analyze_transcript(transcript):
    prompt = f"""
    Break the following transcript into topic-based segments.
    For each segment, include:
    1. Title
    2. Main topic
    3. Dominant emotion (joy, fear, anger, hope, etc.)
    4. Summary in 1 sentence

    Transcript: {transcript}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response['choices'][0]['message']['content']

# PROCESSING
if video_input or uploaded_file:
    with st.spinner("Processing video..."):
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                video_path = tmp.name
        else:
            yt = YouTube(video_input)
            stream = yt.streams.filter(only_audio=True).first()
            video_path = stream.download(filename='temp_video')

        transcript = fake_transcribe(video_path)
        analysis = analyze_transcript(transcript)

        st.subheader("📑 AI-Generated Video Summary")
        st.markdown(analysis)

        if os.path.exists("temp_video"):
            os.remove("temp_video")

# FOOTER
st.markdown("---")
st.caption("Built with ❤️ by Rumiza Shaikh")
