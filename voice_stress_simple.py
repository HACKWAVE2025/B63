import streamlit as st
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

st.set_page_config(page_title="Voice Stress Detector (Single Code Prototype)", page_icon="🎤")
st.title("🎤 Voice Stress Detector (Simple Prototype)")

st.write("Click **Record** then speak for a few seconds. Click **Stop** to see the stress result.")

duration = st.slider("Recording duration (seconds):", 2, 5, 3)

if "recording" not in st.session_state:
    st.session_state.recording = False

def start_recording():
    st.session_state.recording = True
    st.session_state.audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
    st.info("Recording... Speak now!")

def stop_recording():
    if st.session_state.recording:
        sd.stop()
        st.session_state.recording = False
        st.success("Recording stopped.")
        # Save temp file (optional if you want playback or saving)
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        write(temp_file.name, 44100, st.session_state.audio)
        # Analyze volume
        avg_volume = np.mean(np.abs(st.session_state.audio))
        # Determine stress
        if avg_volume > 0.06:
            message = "😟 You seem stressed. Try taking a deep breath."
        elif avg_volume > 0.03:
            message = "🙂 You seem a little nervous, but mostly calm."
        else:
            message = "😊 You seem relaxed and calm!"
        st.write(f"**Average Volume:** {avg_volume:.4f}")
        st.write(f"**Assessment:** {message}")

col1, col2 = st.columns(2)
with col1:
    if not st.session_state.recording:
        if st.button("Record"):
            start_recording()

with col2:
    if st.session_state.recording:
        if st.button("Stop"):
            stop_recording()
