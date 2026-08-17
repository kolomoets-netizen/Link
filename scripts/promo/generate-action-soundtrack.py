#!/usr/bin/env python3
"""
Triumphant action / martial-arts cinematic soundtrack.
Powerful bass drums, African + metallic percussion, cinematic synths.
"""
from __future__ import annotations

import math
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 44100
BPM = 122
BEAT = 60.0 / BPM
BARS = 40  # ~78s
BEATS = BARS * 4
DURATION = BEATS * BEAT


def db(x: float) -> float:
    return 10 ** (x / 20.0)


def soft_clip(x: np.ndarray, drive: float = 1.2) -> np.ndarray:
    return np.tanh(x * drive)


def env_adsr(n: int, a: float, d: float, s: float, r: float) -> np.ndarray:
    a_n, d_n, r_n = max(1, int(a * SR)), max(1, int(d * SR)), max(1, int(r * SR))
    s_n = max(0, n - a_n - d_n - r_n)
    parts = [
        np.linspace(0, 1, a_n, endpoint=False),
        np.linspace(1, s, d_n, endpoint=False),
        np.full(s_n, s),
        np.linspace(s, 0, r_n, endpoint=True),
    ]
    e = np.concatenate(parts)
    if len(e) < n:
        e = np.pad(e, (0, n - len(e)))
    return e[:n]


def place(target: np.ndarray, clip: np.ndarray, at: float, gain: float = 1.0) -> None:
    i = int(at * SR)
    if i < 0 or i >= len(target):
        return
    j = min(len(target), i + len(clip))
    target[i:j] += clip[: j - i] * gain


def bass_drum(sr: int = SR) -> np.ndarray:
    """Powerful cinematic bass drum / taiko-ish boom."""
    n = int(0.55 * sr)
    t = np.arange(n) / sr
    f = 90 * np.exp(-t * 18) + 38
    phase = 2 * math.pi * np.cumsum(f) / sr
    body = np.sin(phase) * np.exp(-t * 5.5)
    sub = np.sin(2 * math.pi * 42 * t) * np.exp(-t * 4.2) * 0.7
    click = np.diff(np.random.randn(n + 1))[:n] * np.exp(-t * 90) * 0.35
    # layered punch
    punch = np.sin(2 * math.pi * 160 * t) * np.exp(-t * 40) * 0.4
    return soft_clip((body + sub + click + punch) * db(-3), 1.4)


def snare_like(sr: int = SR) -> np.ndarray:
    n = int(0.18 * sr)
    t = np.arange(n) / sr
    noise = np.diff(np.random.randn(n + 1))[:n]
    tone = np.sin(2 * math.pi * 180 * t) * np.exp(-t * 25)
    return soft_clip((noise * np.exp(-t * 28) * 0.7 + tone * 0.35) * db(-8))


def djembe(tone: float = 180.0, sr: int = SR) -> np.ndarray:
    """Hand-drum / djembe-ish hit."""
    n = int(0.22 * sr)
    t = np.arange(n) / sr
    f = tone * (1 + 1.2 * np.exp(-t * 40))
    phase = 2 * math.pi * np.cumsum(f) / sr
    skin = np.sin(phase) * np.exp(-t * 14)
    slap = np.diff(np.random.randn(n + 1))[:n] * np.exp(-t * 55) * 0.55
    return soft_clip((skin + slap) * db(-7), 1.25)


def shaker(sr: int = SR) -> np.ndarray:
    n = int(0.07 * sr)
    t = np.arange(n) / sr
    noise = np.diff(np.random.randn(n + 1))[:n]
    # bright grain
    e = np.exp(-t * 55)
    return (noise * e * db(-14)).astype(np.float64)


def metallic_hit(freq: float = 880.0, sr: int = SR) -> np.ndarray:
    """Bright metallic / agogo / anvil-ish percussion."""
    n = int(0.35 * sr)
    t = np.arange(n) / sr
    partials = [1.0, 2.76, 5.4, 8.9]
    amps = [1.0, 0.45, 0.22, 0.12]
    sig = np.zeros(n)
    for p, a in zip(partials, amps):
        sig += a * np.sin(2 * math.pi * freq * p * t) * np.exp(-t * (8 + p * 3))
    noise = np.diff(np.random.randn(n + 1))[:n] * np.exp(-t * 70) * 0.2
    return soft_clip((sig + noise) * db(-10), 1.2)


def tom(freq: float = 120.0, sr: int = SR) -> np.ndarray:
    n = int(0.32 * sr)
    t = np.arange(n) / sr
    f = freq * (1 + 0.8 * np.exp(-t * 25))
    phase = 2 * math.pi * np.cumsum(f) / sr
    return soft_clip(np.sin(phase) * np.exp(-t * 9) * db(-6))


def epic_pad(n: int, sr: int = SR) -> np.ndarray:
    """Cinematic sweeping pads — triumphant minor/major lift."""
    t = np.arange(n) / sr
    # D minor / F major epic: D F A C + rising fifths
    roots = [146.83, 174.61, 220.00, 261.63, 293.66]  # D3 F3 A3 C4 D4
    sig = np.zeros(n)
    for i, f in enumerate(roots):
        trem = 0.8 + 0.2 * np.sin(2 * math.pi * (0.04 + i * 0.015) * t)
        phase = 2 * math.pi * f * (1 + 0.001 * i) * t
        sig += np.sin(phase) * db(-22 - i) * trem
        sig += 0.15 * np.sin(2 * phase) * db(-26 - i) * trem
    # slow filter-ish swell every 8 bars via amplitude
    bar_n = int(8 * BEAT * 4 * sr)  # 8 bars
    for start in range(0, n, bar_n):
        end = min(n, start + bar_n)
        L = end - start
        swell = 0.65 + 0.35 * np.sin(np.linspace(0, math.pi, L)) ** 1.2
        sig[start:end] *= swell
    return sig


def brass_stab(freq: float, dur: float = 0.35) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    # brass-ish: saw approx via odd harmonics
    sig = np.zeros(n)
    for h, a in [(1, 1.0), (2, 0.4), (3, 0.28), (4, 0.12), (5, 0.1)]:
        sig += a * np.sin(2 * math.pi * freq * h * t)
    e = env_adsr(n, 0.01, 0.08, 0.55, 0.18)
    return soft_clip(sig * e * db(-12), 1.3)


def lead_pluck(freq: float, dur: float) -> np.ndarray:
    n = max(2, int(dur * SR))
    t = np.arange(n) / SR
    sig = (
        np.sin(2 * math.pi * freq * t)
        + 0.35 * np.sin(2 * math.pi * freq * 2.01 * t)
        + 0.12 * np.sin(2 * math.pi * freq * 3 * t) * np.exp(-t * 8)
    )
    e = env_adsr(n, 0.005, 0.06, 0.35, max(0.1, dur * 0.4))
    return soft_clip(sig * e * db(-9))


def riser(length: float = 0.5) -> np.ndarray:
    n = int(length * SR)
    t = np.arange(n) / SR
    noise = np.diff(np.random.randn(n + 1))[:n]
    amp = (t / length) ** 1.4
    whoosh = noise * amp
    sweep = np.sin(2 * math.pi * (200 + 1800 * (t / length)) * t) * amp * 0.25
    return (whoosh * 0.45 + sweep) * db(-12)


def melody_notes():
    # Triumphant D-minor / F-major lift motifs (Hz)
    D4, E4, F4, G4, A4, Bb4, C5 = 293.66, 329.63, 349.23, 392.00, 440.00, 466.16, 523.25
    D5, E5, F5, G5, A5 = 587.33, 659.25, 698.46, 783.99, 880.00
    phrase_a = [
        (D5, 1), (F5, 1), (A5, 1), (G5, 1),
        (F5, 2), (D5, 1), (E5, 1),
        (F5, 1), (A5, 1), (C5, 1), (D5, 1),
        (A4, 2), (None, 1), (D5, 1),
    ]
    phrase_b = [
        (F5, 1), (G5, 1), (A5, 1.5), (G5, 0.5),
        (F5, 1), (E5, 1), (D5, 2),
        (A5, 1), (G5, 1), (F5, 1), (D5, 1),
        (F5, 2), (None, 0.5), (A4, 1.5),
    ]
    return phrase_a + phrase_b


def render() -> np.ndarray:
    np.random.seed(11)
    n = int(DURATION * SR)
    mix = np.zeros(n)

    # Pads bed
    mix += epic_pad(n)

    bd = bass_drum()
    sn = snare_like()
    dj_low = djembe(140)
    dj_mid = djembe(210)
    dj_hi = djembe(320)
    sh = shaker()
    metal_hi = metallic_hit(980)
    metal_lo = metallic_hit(620)
    tom_lo = tom(95)
    tom_hi = tom(150)

    # Percussion + drums pattern
    for beat in range(BEATS):
        t0 = beat * BEAT
        bar = beat // 4
        b = beat % 4

        # Powerful bass drum — four-on-floor-ish but cinematic accents
        if b in (0, 2) or (bar % 4 == 3 and b == 3):
            place(mix, bd, t0, gain=1.25 if b == 0 else 0.95)
        if b == 0 and bar % 2 == 0:
            # double boom on phrase starts
            place(mix, bd, t0 + 0.08, gain=0.45)

        # Snare / clap backbeat
        if b in (1, 3):
            place(mix, sn, t0, gain=0.85 if b == 1 else 0.7)

        # African polyrhythm — 3+3+2 feel over 4
        # hits on 0, 0.75, 1.5, 2.25, 3.0 within bar… map via sixteenth-ish
        if b == 0:
            place(mix, dj_low, t0, 1.0)
            place(mix, dj_mid, t0 + BEAT * 0.75, 0.85)
        if b == 1:
            place(mix, dj_hi, t0 + BEAT * 0.5, 0.75)
        if b == 2:
            place(mix, dj_mid, t0, 0.9)
            place(mix, dj_low, t0 + BEAT * 0.75, 0.7)
        if b == 3:
            place(mix, dj_hi, t0 + BEAT * 0.25, 0.8)
            place(mix, dj_mid, t0 + BEAT * 0.75, 0.65)

        # Shakers 16th energy
        for k in range(4):
            place(mix, sh, t0 + BEAT * k / 4, gain=0.55 if k % 2 == 0 else 0.35)

        # Metallic percussion — lively accents
        if b == 0 and bar % 2 == 0:
            place(mix, metal_hi, t0 + BEAT * 0.5, 0.9)
        if b == 2:
            place(mix, metal_lo, t0 + BEAT * 0.5, 0.75)
        if b == 3 and bar % 4 == 3:
            place(mix, metal_hi, t0, 1.05)
            place(mix, metal_lo, t0 + BEAT * 0.5, 0.8)

        # Tom fills every 4th bar
        if bar % 4 == 3 and b == 2:
            place(mix, tom_hi, t0, 0.9)
            place(mix, tom_lo, t0 + BEAT * 0.5, 1.0)
            place(mix, tom_hi, t0 + BEAT * 0.75, 0.7)

        # Riser into downbeats of even 4-bar sections
        if b == 0 and bar % 4 == 0 and bar > 0:
            r = riser(0.55)
            place(mix, r, t0 - len(r) / SR, 1.1)

    # Brass / synth stabs — triumphant hits
    stab_freqs = [146.83, 174.61, 220.00, 293.66]  # D F A D
    for bar in range(0, BARS, 2):
        t0 = bar * 4 * BEAT
        for i, f in enumerate(stab_freqs):
            place(mix, brass_stab(f, 0.4), t0 + i * 0.03, gain=0.85)
        # answering stab on beat 3 of bar
        place(mix, brass_stab(220.00, 0.28), t0 + 2 * BEAT, 0.7)
        place(mix, brass_stab(293.66, 0.28), t0 + 2 * BEAT + 0.04, 0.7)

    # Melodic heroic lead
    phrase = melody_notes()
    t_beat = 8.0  # enter after 2 bars
    end_beat = BEATS - 8
    while t_beat < end_beat:
        for note, dur in phrase:
            if t_beat >= end_beat:
                break
            if note is not None:
                place(mix, lead_pluck(note, dur * BEAT * 0.9), t_beat * BEAT, 1.15)
                # octave power on long notes
                if dur >= 1.5:
                    place(mix, lead_pluck(note * 0.5, dur * BEAT * 0.9), t_beat * BEAT, 0.45)
            t_beat += dur

    # Sub drone pulse for battle weight
    t = np.arange(n) / SR
    drone = np.sin(2 * math.pi * 36.71 * t) * db(-22)  # D1
    drone *= 0.7 + 0.3 * np.sin(2 * math.pi * (BPM / 60) * t)
    mix += drone

    mix = soft_clip(mix * 0.85, 1.15)
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * db(-1.2)
    fade_in = int(0.05 * SR)
    fade_out = int(0.8 * SR)
    mix[:fade_in] *= np.linspace(0, 1, fade_in)
    mix[-fade_out:] *= np.linspace(1, 0, fade_out)
    return mix.astype(np.float32)


def write_stereo(path: Path, mono: np.ndarray) -> None:
    # wider stereo: delay + slight EQ difference via phase
    delay = int(0.012 * SR)
    left = mono
    right = np.concatenate([np.zeros(delay), mono[:-delay]]) if delay < len(mono) else mono
    stereo = np.stack([left * 0.96 + right * 0.04, right * 0.96 + left * 0.04], axis=1)
    peak = np.max(np.abs(stereo)) + 1e-9
    stereo = (stereo / peak * db(-1.0)).astype(np.float32)
    pcm = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main() -> None:
    print(f"Rendering action track {DURATION:.1f}s @ {BPM} BPM…")
    audio = render()
    out_dir = Path("/workspace/docs/assets/audio")
    art = Path("/opt/cursor/artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)
    art.mkdir(parents=True, exist_ok=True)

    wav = out_dir / "istocklink-triumphant-action.wav"
    mp3 = out_dir / "istocklink-triumphant-action.mp3"
    write_stereo(wav, audio)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-qscale:a", "2", str(mp3)],
        check=True,
        capture_output=True,
    )
    (art / mp3.name).write_bytes(mp3.read_bytes())
    (art / wav.name).write_bytes(wav.read_bytes())
    print("WAV:", wav)
    print("MP3:", mp3)


if __name__ == "__main__":
    main()
