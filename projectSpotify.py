import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyaudio
import wave
import speech_recognition as sr

# Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="your_client_id",
                                               client_secret="your_client_secret",
                                               redirect_uri="your_redirect_uri",
                                               scope="user-read-playback-state,user-modify-playback-state"))

# Play the track (requires playback on a device, e.g., Spotify desktop or web app)
track_uri = "spotify:track:your_track_uri"
sp.start_playback(uris=[track_uri])

# Capture the audio (e.g., using pyaudio)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 60  # Example: record for 60 seconds
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Transcribe the audio
recognizer = sr.Recognizer()
with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
    audio = recognizer.record(source)
    transcript = recognizer.recognize_google(audio)

# Save transcript to a file
with open("transcript.txt", "w") as file:
    file.write(transcript)

print("Transcript saved.")
