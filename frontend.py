import streamlit as st
import requests

st.title("🎤 Voice Stress & Depression Detector")
st.write("Upload or record your voice to analyze stress levels.")

uploaded_file = st.file_uploader("Upload your voice sample (WAV file)", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Analyze"):
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post("http://127.0.0.1:5000/analyze", files=files)
            result = response.json()

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Stress Level: {result['stress_level']}")
                st.write(f"Pitch: {result['pitch']:.2f}")
                st.write(f"Energy: {result['energy']:.4f}")
        except Exception as e:
            st.error(f"Connection error: {e}")
