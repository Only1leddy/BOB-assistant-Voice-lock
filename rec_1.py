###################################################################

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from hmmlearn import hmm
import librosa

###################################################################

def record_voice(filename, duration=3, fs=16000):
    print("Recording...NOW!!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, audio)
    print(f"Saved: {filename}")


def make_3_recs():
    for name in ["a.wav", "b.wav", "c.wav", "d.wav", "e.wav", "f.wav", "g.wav", "h.wav", "i.wav", "j.wav", "k.wav"]:
        print(f"Recording {name}...")
        record_voice(name)
        
###################################################################
        
go = input("do you want to rewite voice lock files? Y/?")

if go == "y" or go == "yes":
    print("ok we start")
    make_3_recs()
else:    
    print("no then, ok thanks goodbuy")

###################################################################    