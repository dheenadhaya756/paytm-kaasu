"""Original ambient score for the Kaasu film, synthesised from scratch (no samples, no copyright).
Soft detuned pad following Am - F - C - G, a slow arpeggio, and a Soundbox-style chime at key moments."""
import os, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
LEN = float(os.environ.get("LEN", "122"))
t = np.arange(int(SR * LEN)) / SR
out = np.zeros_like(t)
N = lambda name: {"A2": 110.0, "C3": 130.81, "E3": 164.81, "F2": 87.31, "A3": 220.0, "G2": 98.0, "B2": 123.47, "D3": 146.83, "C4": 261.63, "E4": 329.63, "G3": 196.0, "A4": 440.0, "F3": 174.61, "D4": 293.66, "B3": 246.94, "G4": 392.0, "E5": 659.25, "B4": 493.88}[name]
chords = [["A2", "C3", "E3", "A3"], ["F2", "A3", "C4", "F3"], ["C3", "E3", "G3", "C4"], ["G2", "B2", "D3", "G3"]]
bar = float(os.environ.get("BAR", "7.6"))  # seconds per chord
def env(start, dur, a=2.5, r=3.0):
    e = np.zeros_like(t); s, en = int(start * SR), int(min(LEN, start + dur + r) * SR)
    x = t[s:en] - start
    e[s:en] = np.clip(x / a, 0, 1) * np.where(x > dur, np.clip(1 - (x - dur) / r, 0, 1), 1)
    return e
k = 0; s = 0.0
while s < LEN:
    ch = chords[k % 4]; e = env(s, bar, 2.8, 3.2)
    for n in ch:
        f = N(n)
        for det in (-0.6, 0.0, 0.7):
            out += e * 0.045 * np.sin(2 * np.pi * (f + det) * t) * (1 + 0.15 * np.sin(2 * np.pi * 0.2 * t))
    # slow arpeggio, one octave up, very soft
    for j, n in enumerate(ch):
        st = s + 1.2 + j * 1.6
        if st < LEN:
            pe = np.exp(-np.clip(t - st, 0, None) * 2.2) * (t >= st)
            out += pe * 0.03 * np.sin(2 * np.pi * N(n) * 4 * t)
    s += bar; k += 1
def chime(at, gain=0.22):
    global out
    for f, dl in ((1318.5, 0.0), (1975.5, 0.14)):
        st = at + dl; pe = np.exp(-np.clip(t - st, 0, None) * 4.0) * (t >= st)
        out += pe * gain * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t))
for at in [float(x) for x in os.environ.get("CHIMES", "1.0,112.2").split(",")]:  # "money received" at the open, "Pongal stock paid" at the close
    chime(at)
# gentle low-pass via moving average, fade in/out, normalise
out = np.convolve(out, np.ones(6) / 6, mode="same")
fade = np.minimum(1, np.minimum(t / 2.5, (LEN - t) / 4.0)); out *= fade
out = out / np.max(np.abs(out)) * 0.6
pcm = (out * 32767).astype(np.int16)
os.makedirs(os.path.join(ROOT, "video"), exist_ok=True)
with wave.open(os.path.join(ROOT, "video", os.environ.get("OUT", "music.wav")), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("music.wav", LEN, "s")
