import React, { useState, useRef, useEffect } from 'react';

export default function VoiceStressDetector() {
  const [recording, setRecording] = useState(false);
  const [message, setMessage] = useState('Result will appear here.');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    if (!recording) {
      audioChunksRef.current = [];
    }
  }, [recording]);

  const startRecording = async () => {
    setMessage('Requesting microphone...');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.start();
      setRecording(false);
      setMessage('Recording... Speak now.');

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = processAudio;
    } catch (err) {
      setMessage('Microphone access denied or error: ' + err.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      setMessage('Analyzing recording...');
    }
  };

  const processAudio = async () => {
    const blob = new Blob(audioChunksRef.current);
    const arrayBuffer = await blob.arrayBuffer();
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    const data = audioBuffer.getChannelData(0);

    // Compute average volume (absolute amplitude)
    let sum = 0;
    for (let i = 0; i < data.length; i++) {
      sum += Math.abs(data[i]);
    }
    const avgVolume = sum / data.length;
    
    let stressMessage = '';
    if (avgVolume > 0.1) stressMessage = '😟 You seem stressed. Try taking deep breaths.';
    else if (avgVolume > 0.04) stressMessage = '🙂 A little nervous, but mostly calm.';
    else stressMessage = '😊 You are relaxed and calm!';

    setMessage(`Average Volume: ${avgVolume.toFixed(4)}\n${stressMessage}`);
  };

  return (
    <div style={{ maxWidth: 400, margin: '40px auto', textAlign: 'center', fontFamily: 'Arial' }}>
      <h1>🎤 Voice Stress Detector</h1>
      <button onClick={startRecording} disabled={recording} style={{ padding: '12px 20px', fontSize: 16, marginRight: 10 }}>
        Start Recording
      </button>
      <button onClick={stopRecording} disabled={!recording} style={{ padding: '12px 20px', fontSize: 16 }}>
        Stop Recording
      </button>
      <pre style={{ whiteSpace: 'pre-wrap', marginTop: 30, fontSize: 18 }}>{message}</pre>
    </div>
  );
}
