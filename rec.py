################################################################
import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from hmmlearn import hmm
import librosa
import time
import joblib
import subprocess
import sys

###################################################################

def record_voice(filename, duration=3, fs=16000):
    print("Recording...NOW!!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, audio)
    print(f"Saved: {filename}")


def extract_features(filename):
    y, sr = librosa.load(filename, sr=None)

    # Trim silence
    y_trimmed, _ = librosa.effects.trim(y)

    # Normalize volume
    y_normalized = librosa.util.normalize(y_trimmed)

    # Extract MFCCs
    mfcc = librosa.feature.mfcc(y=y_normalized, sr=sr, n_mfcc=13)

    # Return full time-series MFCC for HMM
    return mfcc.T  # shape: (n_frames, 13)


def train_hmm(samples):
    lengths = [len(s) for s in samples]
    X = np.concatenate(samples)
    model = hmm.GaussianHMM(n_components=11, covariance_type='diag', n_iter=1000)
    model.fit(X, lengths)
    joblib.dump(model, "voice_model.pkl")
    return model


def score_sample(model, filename):
    features = extract_features(filename)
    return model.score(features)  # higher = more likely to be you


def monitor_bob(process, stop_callback):
    for line in process.stdout:
        print("Bob:", line.strip())
        if "EXIT_SIGNAL" in line:
            print("User said goodbye.")
            stop_callback()
            break
        
def shutdown(proc):
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("Bob/Flask shutdown complete.")
###################################################################

files = ["a.wav", "b.wav", "c.wav", "d.wav", "e.wav", "f.wav", "g.wav", "h.wav", "i.wav", "j.wav", "k.wav"]
samples = [extract_features(f) for f in files]
#model = train_hmm(samples)
#print("trained")
model = joblib.load("voice_model.pkl")

###################################################################

 


while True:
    print("test_now")
    # Step 4: Record a test sample
    record_voice("test.wav")

    # Step 5: Score the test
    score = score_sample(model, "test.wav")
    print("Score:", score)

    threshold = -7000
    
    # Step 6: Decide pass/fail
    if score > threshold:  # Adjust threshold as needed
        print("🔓 Access Granted")
        bob_proc = subprocess.Popen(
            ["/home/leddy/bob/bin/python3.11", "/home/leddy/bob/gui_bob7_4_3.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True
        )

        # Monitor Bob output and wait for 'goodbye'
        t = threading.Thread(target=monitor_bob, args=(bob_proc, shutdown), daemon=True)
        t.start()
        t.join()

    else:
        print("🔒 Access Denied")
    time.sleep(1)
    
print("closed")

################################################################spacebarspacebarhtop 