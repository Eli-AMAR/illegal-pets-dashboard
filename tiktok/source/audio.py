"""Synthesize a lo-fi hip-hop bed for a TikTok video. No samples, pure numpy.
Usage: python3 audio.py <dur_seconds> <seed> <transpose_semitones> <bpm> <out.wav>
"""
import sys
import wave

import numpy as np

SR = 44100


def env_exp(n, rate):
    t = np.arange(n) / SR
    return np.exp(-t * rate)


def kick(rate=9.0, dur=0.42, f0=115.0, f1=46.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sweep = f1 + (f0 - f1) * np.exp(-t * 28)
    phase = 2 * np.pi * np.cumsum(sweep) / SR
    body = np.sin(phase) * env_exp(n, rate)
    click = np.random.default_rng(1).standard_normal(n) * env_exp(n, 220) * 0.25
    return (body + click) * 0.95


def snare(rng):
    n = int(0.28 * SR)
    noise = rng.standard_normal(n)
    noise = np.diff(noise, prepend=0)  # brighten
    body = np.sin(2 * np.pi * 187 * np.arange(n) / SR) * env_exp(n, 30) * 0.5
    return (noise * env_exp(n, 22) * 0.45 + body) * 0.8


def hat(rng, open_=False):
    n = int((0.30 if open_ else 0.07) * SR)
    noise = rng.standard_normal(n)
    noise = np.diff(np.diff(noise, prepend=0), prepend=0)  # crispy highpass
    return noise * env_exp(n, 18 if open_ else 90) * 0.22


def tone(freq, dur, attack=0.008, decay=2.2, harm=0.14, detune=0.0015):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for d in (1 - detune, 1.0, 1 + detune):
        y += np.sin(2 * np.pi * freq * d * t)
    y += harm * np.sin(2 * np.pi * freq * 2 * t)
    a = np.minimum(1.0, t / max(attack, 1e-4))
    return y / 3 * a * np.exp(-t * decay)


def add(buf, pos, sig, gain=1.0):
    i = int(pos * SR)
    if i >= len(buf):
        return
    seg = sig[: len(buf) - i]
    buf[i:i + len(seg)] += seg * gain


def note(semitone_from_a2):
    return 110.0 * 2 ** (semitone_from_a2 / 12.0)


def build(dur, seed, transpose, bpm):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    beat = 60.0 / bpm
    bar = 4 * beat
    nbars = int(np.ceil(dur / bar)) + 1

    drums = np.zeros(n)
    bass = np.zeros(n)
    keys = np.zeros(n)

    # Am - F - C - G progression (roots relative to A2), chords as triads.
    prog = [
        (0, [0, 3, 7]),      # Am
        (-4, [0, 4, 7]),     # F
        (3, [0, 4, 7]),      # C
        (-2, [0, 4, 7]),     # G
    ]

    kick_sig = kick()
    kick_times_per_bar = [0.0, 1.75, 2.5] if seed % 2 == 0 else [0.0, 1.5, 2.75]
    kick_positions = []

    for b in range(nbars):
        t0 = b * bar
        root, triad = prog[b % 4]
        root += transpose

        for kt in kick_times_per_bar:
            add(drums, t0 + kt * beat, kick_sig, 0.9)
            kick_positions.append(t0 + kt * beat)
        for st in (1.0, 3.0):
            add(drums, t0 + st * beat, snare(rng), 0.85)
        for e in range(8):
            vel = (0.9, 0.45, 0.7, 0.4)[e % 4] * (0.85 + 0.3 * rng.random())
            add(drums, t0 + e * 0.5 * beat, hat(rng), vel)
        if b % 2 == 1:
            add(drums, t0 + 3.5 * beat, hat(rng, open_=True), 0.5)

        # Bass: root with a syncopated push (kept >=110Hz so phone speakers carry it)
        f = note(root)
        add(bass, t0, tone(f, beat * 2.2, decay=1.4, harm=0.45), 0.8)
        add(bass, t0 + 2.5 * beat, tone(f, beat * 1.4, decay=1.8, harm=0.45), 0.55)

        # Keys: soft chord stab on 1 and the 'and' of 3, octave-doubled for presence
        for st, g in ((0.0, 0.85), (2.5, 0.55)):
            for semi in triad:
                f2 = note(root + semi) * 2
                add(keys, t0 + st * beat, tone(f2, beat * 2.0, attack=0.02, decay=1.6, harm=0.35), g / len(triad))
                add(keys, t0 + st * beat, tone(f2 * 2, beat * 1.6, attack=0.02, decay=2.2), 0.35 * g / len(triad))

    # Sidechain duck of bass+keys after each kick
    duck = np.ones(n)
    t_axis = np.arange(int(0.30 * SR)) / SR
    duck_shape = 1 - 0.5 * np.exp(-t_axis * 14)
    for kp in kick_positions:
        i = int(kp * SR)
        seg = duck_shape[: max(0, n - i)]
        if len(seg):
            duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], seg)

    mix = drums * 0.9 + (bass * 0.8 + keys * 0.8) * duck
    mix = np.tanh(mix * 1.25)

    # Gentle fades
    fin = int(0.06 * SR)
    mix[:fin] *= np.linspace(0, 1, fin)
    fout = int(0.9 * SR)
    mix[-fout:] *= np.linspace(1, 0, fout)

    mix = mix / np.max(np.abs(mix)) * 0.72

    # Subtle stereo width: right channel slightly delayed copy of hats/keys content
    delay = int(0.0006 * SR)
    right = np.copy(mix)
    right[delay:] = right[delay:] * 0.4 + mix[:-delay] * 0.6
    stereo = np.stack([mix, right], axis=1)
    return (stereo * 32767).astype(np.int16)


def main():
    dur = float(sys.argv[1]); seed = int(sys.argv[2])
    transpose = int(sys.argv[3]); bpm = float(sys.argv[4]); out = sys.argv[5]
    data = build(dur, seed, transpose, bpm)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())
    print(f"wrote {out}: {dur:.1f}s @ {bpm:.0f}bpm, transpose {transpose:+d}")


if __name__ == '__main__':
    main()
