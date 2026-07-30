#!/usr/bin/env python3
"""
Cinematic corporate trap @ 110 BPM for istock.link promo.
Heavy 808s, sharp snares, crisp hi-hats, motivational brass, electronic pulses.
Structure: lean intro → build → hard drop main → outro.
"""
from __future__ import annotations

import math
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 44100
BPM = 110
BEAT = 60.0 / BPM
# ~48s ≈ script length (22 bars * 4 beats ≈ 48s)
BARS = 22
BEATS = BARS * 4
DURATION = BEATS * BEAT


def db(x: float) -> float:
    return 10 ** (x / 20.0)


def soft_clip(x: np.ndarray, drive: float = 1.25) -> np.ndarray:
    return np.tanh(x * drive)


def env_adsr(n: int, a: float, d: float, s: float, r: float) -> np.ndarray:
    a_n, d_n, r_n = max(1, int(a * SR)), max(1, int(d * SR)), max(1, int(r * SR))
    s_n = max(0, n - a_n - d_n - r_n)
    e = np.concatenate(
        [
            np.linspace(0, 1, a_n, endpoint=False),
            np.linspace(1, s, d_n, endpoint=False),
            np.full(s_n, s),
            np.linspace(s, 0, r_n, endpoint=True),
        ]
    )
    if len(e) < n:
        e = np.pad(e, (0, n - len(e)))
    return e[:n]


def place(target: np.ndarray, clip: np.ndarray, at: float, gain: float = 1.0) -> None:
    i = int(at * SR)
    if i < 0 or i >= len(target):
        return
    j = min(len(target), i + len(clip))
    target[i:j] += clip[: j - i] * gain


def make_808(freq: float = 49.0, dur: float = 0.7) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1.0 + 2.2 * np.exp(-t * 28))
    phase = 2 * math.pi * np.cumsum(f) / SR
    tone = np.sin(phase)
    tone += 0.2 * np.sin(2 * phase) * np.exp(-t * 10)
    e = np.exp(-t * 3.8)
    e[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return soft_clip(tone * e * db(-2), 1.55)


def make_kick() -> np.ndarray:
    n = int(0.28 * SR)
    t = np.arange(n) / SR
    f = 140 * np.exp(-t * 32) + 48
    phase = 2 * math.pi * np.cumsum(f) / SR
    body = np.sin(phase) * np.exp(-t * 10)
    click = np.diff(np.random.randn(n + 1))[:n] * np.exp(-t * 120) * 0.25
    return soft_clip((body + click) * db(-6), 1.3)


def make_snare() -> np.ndarray:
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    noise = np.diff(np.random.randn(n + 1))[:n]
    tone = np.sin(2 * math.pi * 200 * t) * np.exp(-t * 30)
    return soft_clip((noise * np.exp(-t * 32) * 0.85 + tone * 0.35) * db(-5), 1.2)


def make_clap() -> np.ndarray:
    n = int(0.2 * SR)
    out = np.zeros(n)
    for delay, g in [(0, 1.0), (0.012, 0.7), (0.024, 0.45), (0.038, 0.25)]:
        sn = make_snare()
        place(out, sn, delay, g)
    return soft_clip(out * db(-3), 1.15)


def make_hat(open_: bool = False) -> np.ndarray:
    n = int((0.06 if not open_ else 0.14) * SR)
    t = np.arange(n) / SR
    noise = np.diff(np.random.randn(n + 1))[:n]
    # bright metallic
    tone = np.sin(2 * math.pi * 7500 * t) * np.exp(-t * (80 if not open_ else 28))
    e = np.exp(-t * (70 if not open_ else 22))
    return (noise * e * 0.7 + tone * 0.35) * db(-16 if not open_ else -14)


def make_tick() -> np.ndarray:
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    noise = np.diff(np.random.randn(n + 1))[:n] * np.exp(-t * 100)
    return noise * db(-18)


def brass_hit(freqs: list[float], dur: float = 0.4) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for f in freqs:
        for h, a in [(1, 1.0), (2, 0.35), (3, 0.22), (4, 0.1)]:
            sig += a * np.sin(2 * math.pi * f * h * t) / len(freqs)
    e = env_adsr(n, 0.008, 0.07, 0.5, 0.2)
    return soft_clip(sig * e * db(-9), 1.35)


def pulse_bass(freq: float, dur: float = 0.4) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    # modern electronic pulse
    sq = np.sign(np.sin(2 * math.pi * freq * t))
    sine = np.sin(2 * math.pi * freq * t)
    sig = 0.35 * sq + 0.65 * sine
    e = env_adsr(n, 0.005, 0.05, 0.4, 0.2)
    return soft_clip(sig * e * db(-10), 1.2)


def riser(length: float = 1.0) -> np.ndarray:
    n = int(length * SR)
    t = np.arange(n) / SR
    noise = np.diff(np.random.randn(n + 1))[:n]
    amp = (t / length) ** 1.5
    sweep = np.sin(2 * math.pi * (120 + 2200 * (t / length)) * t) * amp * 0.3
    return (noise * amp * 0.5 + sweep) * db(-11)


def stab_synth(freq: float, dur: float = 0.22) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.sin(2 * math.pi * freq * t) + 0.4 * np.sin(2 * math.pi * freq * 2 * t)
    e = env_adsr(n, 0.003, 0.04, 0.3, 0.12)
    return soft_clip(sig * e * db(-11))


def low_brass_swell(n: int) -> np.ndarray:
    t = np.arange(n) / SR
    # C minor motivational bed
    freqs = [65.41, 77.78, 98.00, 130.81]  # C2 Eb2 G2 C3
    sig = np.zeros(n)
    for i, f in enumerate(freqs):
        trem = 0.75 + 0.25 * np.sin(2 * math.pi * (0.05 + i * 0.02) * t)
        sig += np.sin(2 * math.pi * f * t) * db(-24 - i) * trem
    return sig


def section(beat: int) -> str:
    """intro 0-4 bars, build 4-8, drop 8-18, outro 18-22"""
    bar = beat // 4
    if bar < 4:
        return "intro"
    if bar < 8:
        return "build"
    if bar < 18:
        return "drop"
    return "outro"


def render() -> np.ndarray:
    np.random.seed(21)
    n = int(DURATION * SR)
    mix = np.zeros(n)
    mix += low_brass_swell(n)

    kick = make_kick()
    sn808 = make_808(46.25, 0.75)  # F#
    sn808_c = make_808(41.2, 0.75)  # E
    sn808_g = make_808(49.0, 0.7)  # G
    snare = make_snare()
    clap = make_clap()
    hat_c = make_hat(False)
    hat_o = make_hat(True)
    tick = make_tick()

    # Brass chords (C minor / Eb motivational)
    brass_c = brass_hit([130.81, 155.56, 196.00, 261.63], 0.45)  # C Eb G C
    brass_f = brass_hit([174.61, 220.00, 261.63], 0.4)  # F A C
    brass_ab = brass_hit([207.65, 261.63, 311.13], 0.4)  # Ab C Eb

    for beat in range(BEATS):
        t0 = beat * BEAT
        bar = beat // 4
        b = beat % 4
        sec = section(beat)

        # --- Intro: lean ticking + low brass already in bed ---
        if sec == "intro":
            place(mix, tick, t0, 0.9)
            place(mix, tick, t0 + BEAT * 0.5, 0.55)
            if b == 0:
                place(mix, kick, t0, 0.55)
            if b == 0 and bar % 2 == 0:
                place(mix, brass_c, t0, 0.45)

        # --- Build: claps + rising energy ---
        elif sec == "build":
            place(mix, kick, t0, 0.85 if b % 2 == 0 else 0.0)
            if b in (1, 3):
                place(mix, clap, t0, 0.9)
            # hats 8ths
            place(mix, hat_c, t0, 0.7)
            place(mix, hat_c, t0 + BEAT * 0.5, 0.5)
            if b == 0:
                place(mix, sn808_c, t0, 0.7)
            if b == 0 and bar == 7:
                r = riser(BEAT * 4)
                place(mix, r, t0, 1.2)
            if b == 0:
                place(mix, brass_f if bar % 2 else brass_c, t0, 0.65)
            # rising stab sequence last build bar
            if bar == 7:
                place(mix, stab_synth(261.63 * (1 + b * 0.25)), t0 + BEAT * 0.25, 0.8)

        # --- Drop: swagger 808 + bright stabs ---
        elif sec == "drop":
            # punchy 808 on every downbeat + syncopation
            if b == 0:
                bass = sn808 if (bar % 4) in (0, 1) else (sn808_g if bar % 4 == 2 else sn808_c)
                place(mix, bass, t0, 1.25)
            if b == 2:
                place(mix, sn808_c, t0, 0.85)
            if b == 3 and bar % 2 == 1:
                place(mix, sn808, t0 + BEAT * 0.5, 0.55)

            place(mix, kick, t0 if b % 2 == 0 else t0, 0.35 if b % 2 == 0 else 0.0)

            # sharp snare accents
            if b in (1, 3):
                place(mix, snare, t0, 1.05 if b == 1 else 0.85)
                if bar % 2 == 0 and b == 1:
                    place(mix, clap, t0 + 0.01, 0.6)

            # crisp hi-hat trap rolls
            for k in range(4):
                g = 0.75 if k in (0, 2) else 0.4
                place(mix, hat_c, t0 + BEAT * k / 4, g)
            if b == 3:
                place(mix, hat_o, t0 + BEAT * 0.5, 0.7)

            # motivational brass + bright stabs on phrase hits
            if b == 0:
                chord = brass_c if bar % 4 in (0, 1) else (brass_ab if bar % 4 == 2 else brass_f)
                place(mix, chord, t0, 0.95)
            if b == 2:
                place(mix, stab_synth(392.00), t0, 0.9)
                place(mix, stab_synth(523.25), t0 + 0.04, 0.7)
            # electronic pulse under
            if b % 2 == 0:
                place(mix, pulse_bass(65.41 if b == 0 else 82.41, 0.35), t0, 0.75)

        # --- Outro ---
        else:
            if b == 0:
                place(mix, sn808_c, t0, 0.8)
                place(mix, brass_c, t0, 0.7)
            if b in (1, 3):
                place(mix, snare, t0, 0.55)
            place(mix, hat_c, t0, 0.4)
            if bar == BARS - 1 and b == 0:
                place(mix, brass_c, t0, 1.1)
                place(mix, sn808, t0, 1.0)

    mix = soft_clip(mix * 0.88, 1.2)
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * db(-1.0)
    fade_in = int(0.03 * SR)
    fade_out = int(0.6 * SR)
    mix[:fade_in] *= np.linspace(0, 1, fade_in)
    mix[-fade_out:] *= np.linspace(1, 0, fade_out)
    return mix.astype(np.float32)


def write_stereo(path: Path, mono: np.ndarray) -> None:
    delay = int(0.01 * SR)
    left = mono
    right = np.concatenate([np.zeros(delay), mono[:-delay]])
    stereo = np.stack([left * 0.97 + right * 0.03, right * 0.97 + left * 0.03], axis=1)
    peak = np.max(np.abs(stereo)) + 1e-9
    stereo = (stereo / peak * db(-0.8)).astype(np.float32)
    pcm = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main() -> None:
    print(f"Rendering corporate trap {DURATION:.1f}s @ {BPM} BPM…")
    audio = render()
    out = Path("/workspace/docs/assets/audio")
    art = Path("/opt/cursor/artifacts")
    out.mkdir(parents=True, exist_ok=True)
    art.mkdir(parents=True, exist_ok=True)
    wav = out / "istocklink-corporate-trap-110.wav"
    mp3 = out / "istocklink-corporate-trap-110.mp3"
    write_stereo(wav, audio)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-qscale:a", "2", str(mp3)],
        check=True,
        capture_output=True,
    )
    (art / mp3.name).write_bytes(mp3.read_bytes())
    (art / wav.name).write_bytes(wav.read_bytes())
    print("MP3:", mp3)
    print("WAV:", wav)


if __name__ == "__main__":
    main()
