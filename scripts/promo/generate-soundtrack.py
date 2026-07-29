#!/usr/bin/env python3
"""
Procedural Apple-keynote-style corporate soundtrack.
Finger snaps on beats, short risers into snaps, 808 bass, soft kick, shimmer pads.
"""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

import numpy as np

SR = 44100
BPM = 130
BEAT = 60.0 / BPM
DURATION_BARS = 32  # ~59s at 130 BPM (4/4)
BARS = DURATION_BARS
BEATS = BARS * 4
DURATION = BEATS * BEAT


def db(x: float) -> float:
    return 10 ** (x / 20.0)


def env_adsr(n: int, a: float, d: float, s: float, r: float, sr: int = SR) -> np.ndarray:
    a_n = max(1, int(a * sr))
    d_n = max(1, int(d * sr))
    r_n = max(1, int(r * sr))
    s_n = max(0, n - a_n - d_n - r_n)
    attack = np.linspace(0, 1, a_n, endpoint=False)
    decay = np.linspace(1, s, d_n, endpoint=False)
    sustain = np.full(s_n, s)
    release = np.linspace(s, 0, r_n, endpoint=True)
    e = np.concatenate([attack, decay, sustain, release])
    if len(e) < n:
        e = np.pad(e, (0, n - len(e)))
    return e[:n]


def soft_clip(x: np.ndarray, drive: float = 1.1) -> np.ndarray:
    return np.tanh(x * drive)


def lowpass(x: np.ndarray, cutoff: float, sr: int = SR) -> np.ndarray:
    """Fast one-pole LPF (vectorized recurrence via numba-free loop on C-level via numpy)."""
    if len(x) == 0:
        return x
    x = np.ascontiguousarray(x, dtype=np.float64)
    alpha = 1.0 - math.exp(-2.0 * math.pi * cutoff / sr)
    y = np.empty_like(x)
    acc = 0.0
    # Local bindings for speed
    xa = x
    ya = y
    a = alpha
    for i in range(len(xa)):
        acc += a * (xa[i] - acc)
        ya[i] = acc
    return ya


def highpass(x: np.ndarray, cutoff: float, sr: int = SR) -> np.ndarray:
    return x - lowpass(x, cutoff, sr)


def finger_snap(sr: int = SR) -> np.ndarray:
    """Crisp finger-snap: short noise burst + mid click."""
    n = int(0.09 * sr)
    t = np.arange(n) / sr
    noise = np.random.randn(n)
    noise = highpass(noise, 1800)
    noise = lowpass(noise, 9000)
    click = np.sin(2 * math.pi * 1800 * t) * np.exp(-t * 180)
    body = np.sin(2 * math.pi * 420 * t) * np.exp(-t * 70)
    e = np.exp(-t * 95)
    e[: int(0.001 * sr)] *= np.linspace(0, 1, int(0.001 * sr))
    snap = (noise * e * 0.85 + click * 0.55 + body * 0.25)
    # tiny pre-transient
    pre = int(0.002 * sr)
    out = np.zeros(n + pre)
    out[pre:] = snap
    out[:pre] = np.linspace(0, snap[0] * 0.3, pre)
    return soft_clip(out * db(-2))


def kick(sr: int = SR) -> np.ndarray:
    n = int(0.28 * sr)
    t = np.arange(n) / sr
    # pitch sweep 120 -> 42 Hz
    phase = 2 * math.pi * (120 * np.exp(-t * 28) + 42) * t / (1 + t * 8)
    # better: integrate instantaneous freq
    f0 = 120 * np.exp(-t * 35) + 40
    phase = 2 * math.pi * np.cumsum(f0) / sr
    tone = np.sin(phase) * np.exp(-t * 9)
    click = highpass(np.random.randn(n), 2000) * np.exp(-t * 120) * 0.15
    return soft_clip((tone + click) * db(-8))


def bass_808(sr: int = SR, freq: float = 49.0) -> np.ndarray:
    """Round pulsating 808-style sine with pitch drop."""
    n = int(0.55 * sr)
    t = np.arange(n) / sr
    f = freq * (1 + 0.55 * np.exp(-t * 22))
    phase = 2 * math.pi * np.cumsum(f) / sr
    tone = np.sin(phase)
    # slight harmonics for body
    tone += 0.18 * np.sin(2 * phase) * np.exp(-t * 8)
    e = env_adsr(n, 0.004, 0.12, 0.55, 0.28)
    # soft saturation
    return soft_clip(tone * e * db(-6), 1.3)


def riser(length: float = 0.18, sr: int = SR) -> np.ndarray:
    """Short white-noise / reverse-cymbal whoosh into the snap."""
    n = int(length * sr)
    t = np.arange(n) / sr
    noise = np.random.randn(n)
    # rising bandpass feel via increasing HP cutoff simulation
    noise = highpass(noise, 400)
    noise = lowpass(noise, 12000)
    # amplitude crescendo
    amp = (t / length) ** 1.6
    # slight upward pitch illusion via FM of noise envelope
    shimmer = np.sin(2 * math.pi * (900 + 2400 * (t / length)) * t) * 0.12 * amp
    out = (noise * amp * 0.55 + shimmer) * db(-10)
    # fade tip so it ducks under snap
    out[-int(0.008 * sr) :] *= np.linspace(1, 0.15, int(0.008 * sr))
    return out


def shimmer_pad(n: int, sr: int = SR, root: float = 261.63) -> np.ndarray:
    """Bright shimmering pad bed — no melody, soft major texture."""
    t = np.arange(n) / sr
    freqs = [root, root * 5 / 4, root * 3 / 2, root * 2, root * 3]
    sig = np.zeros(n, dtype=np.float64)
    for i, f in enumerate(freqs):
        det = 1 + (i - 2) * 0.0012
        amp = db(-28 - i * 1.5)
        trem = 0.85 + 0.15 * np.sin(2 * math.pi * (0.07 + i * 0.03) * t + i)
        # gentle 2nd harmonic for shimmer without harshness
        phase = 2 * math.pi * f * det * t
        sig += (np.sin(phase) + 0.08 * np.sin(2 * phase)) * amp * trem
    # airy high texture (short-block filtered to avoid slow full-buffer LPF)
    rng = np.random.default_rng(3)
    air = rng.standard_normal(n) * db(-36)
    # crude HP via difference
    air = np.diff(air, prepend=air[0])
    air *= 0.5 + 0.5 * np.sin(2 * math.pi * 0.05 * t)
    sig = sig + air
    beat_n = int(BEAT * sr)
    for b in range(0, BEATS, 4):
        start = b * beat_n
        end = min(n, start + 4 * beat_n)
        if start >= n:
            break
        L = end - start
        swell = 0.7 + 0.3 * np.sin(np.linspace(0, math.pi, L))
        sig[start:end] *= swell
    return sig


def place(target: np.ndarray, clip: np.ndarray, at: float, gain: float = 1.0) -> None:
    i = int(at * SR)
    if i >= len(target) or i < 0:
        return
    j = min(len(target), i + len(clip))
    target[i:j] += clip[: j - i] * gain


def render() -> np.ndarray:
    n = int(DURATION * SR)
    mix = np.zeros(n)
    pad = shimmer_pad(n)
    mix += pad

    snap = finger_snap()
    k = kick()
    b808 = bass_808(freq=46.25)  # ~F#1-ish round
    b808_alt = bass_808(freq=41.2)  # E1 variation every other bar

    for beat in range(BEATS):
        t0 = beat * BEAT
        # short riser leading into each beat/snap
        r = riser(length=0.16 if beat % 4 == 0 else 0.12)
        place(mix, r, t0 - len(r) / SR + 0.004, gain=1.0 if beat % 4 == 0 else 0.7)
        # finger snap on every beat (downbeat louder)
        snap_gain = 1.15 if beat % 4 == 0 else 0.92
        place(mix, snap, t0, gain=snap_gain)
        # soft kick — stronger on 1 and 3
        if beat % 2 == 0:
            place(mix, k, t0, gain=0.85 if beat % 4 == 0 else 0.55)
        # 808 pulse every beat, slightly longer on downbeats
        bass = b808 if (beat // 4) % 2 == 0 else b808_alt
        place(mix, bass, t0, gain=0.95 if beat % 4 == 0 else 0.72)

    # subtle electronic texture ticks (very quiet)
    rng = np.random.default_rng(7)
    for beat in range(0, BEATS, 2):
        t0 = beat * BEAT + BEAT * 0.5
        tick_n = int(0.02 * SR)
        tick = highpass(rng.standard_normal(tick_n), 5000) * np.linspace(1, 0, tick_n) * db(-28)
        place(mix, tick, t0, gain=1.0)

    # soft master bus
    mix = soft_clip(mix * 0.95, 1.05)
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * db(-1.5)

    # fade in/out
    fade = int(0.02 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    return mix.astype(np.float32)


def write_wav(path: Path, audio: np.ndarray, sr: int = SR) -> None:
    pcm = np.clip(audio * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main() -> None:
    np.random.seed(42)
    print(f"Rendering {DURATION:.1f}s @ {BPM} BPM…")
    audio = render()
    # stereo widen slightly
    left = audio
    right = np.concatenate([np.zeros(int(0.008 * SR)), audio[: -int(0.008 * SR)]])
    # rebalance
    stereo = np.stack([left * 0.98 + right * 0.02, right * 0.98 + left * 0.02], axis=1)
    peak = np.max(np.abs(stereo)) + 1e-9
    stereo = (stereo / peak * db(-1.0)).astype(np.float32)

    out_dir = Path("/workspace/docs/assets/audio")
    art_dir = Path("/opt/cursor/artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)
    art_dir.mkdir(parents=True, exist_ok=True)

    wav_path = out_dir / "istocklink-corporate-keynote.wav"
    # write stereo wav
    pcm = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("WAV:", wav_path)

    # mp3 via ffmpeg
    mp3_path = out_dir / "istocklink-corporate-keynote.mp3"
    import subprocess

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(wav_path),
            "-codec:a",
            "libmp3lame",
            "-qscale:a",
            "2",
            str(mp3_path),
        ],
        check=True,
        capture_output=True,
    )
    for dest in (art_dir / "istocklink-corporate-keynote.mp3", art_dir / "istocklink-corporate-keynote.wav"):
        src = mp3_path if dest.suffix == ".mp3" else wav_path
        dest.write_bytes(src.read_bytes())
    print("MP3:", mp3_path)


if __name__ == "__main__":
    main()
