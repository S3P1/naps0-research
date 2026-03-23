"""
prep_donateacry.py — DonateACry corpus preprocessing for Naps0 research.

Source: https://github.com/gveres/donateacry-corpus
License: MIT

Converts raw DonateACry audio files to the normalized format used in
Naps0 training. Applies:
  - Resampling to 16 kHz
  - Mono conversion
  - RMS normalization to target level
  - Label mapping to Naps0 taxonomy (4 classes)

DonateACry label mapping:
  hungry    → hunger
  belly_pain → pain
  discomfort → discomfort
  tired     → tired
  burping   → EXCLUDED (acoustically ambiguous, not in Naps0 taxonomy)

Usage:
    python prep_donateacry.py --input_dir /path/to/donateacry \
                              --output_dir /path/to/processed \
                              --sample_rate 16000
"""

import argparse
import os
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from tqdm import tqdm

# ── Configuration ─────────────────────────────────────────────────────────────

LABEL_MAP = {
    "hungry":      "hunger",
    "belly_pain":  "pain",
    "discomfort":  "discomfort",
    "tired":       "tired",
    "burping":     None,   # excluded
}

RMS_TARGET   = 0.05
SAMPLE_RATE  = 16000
MIN_DURATION = 1.0   # seconds — clips shorter than this are skipped


# ── Helpers ───────────────────────────────────────────────────────────────────

def rms_normalize(audio: np.ndarray, target: float = RMS_TARGET) -> np.ndarray:
    rms = np.sqrt(np.mean(audio ** 2))
    if rms < 1e-8:
        return audio
    return audio * (target / rms)


def process_file(src_path: Path, dst_path: Path) -> bool:
    """Load, resample, normalize and save a single audio file."""
    try:
        audio, sr = librosa.load(src_path, sr=SAMPLE_RATE, mono=True)
    except Exception as e:
        print(f"  [SKIP] {src_path.name}: load error — {e}")
        return False

    if len(audio) / SAMPLE_RATE < MIN_DURATION:
        print(f"  [SKIP] {src_path.name}: too short ({len(audio)/SAMPLE_RATE:.2f}s)")
        return False

    audio = rms_normalize(audio)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(dst_path), audio, SAMPLE_RATE, subtype="PCM_16")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main(input_dir: str, output_dir: str) -> None:
    input_root  = Path(input_dir)
    output_root = Path(output_dir)

    stats = {label: {"ok": 0, "skip": 0} for label in LABEL_MAP.values() if label}
    stats["excluded"] = {"ok": 0, "skip": 0}

    for src_label, dst_label in LABEL_MAP.items():
        src_folder = input_root / src_label
        if not src_folder.exists():
            print(f"[WARN] folder not found: {src_folder}")
            continue

        audio_files = list(src_folder.glob("*.wav")) + list(src_folder.glob("*.mp3"))

        if dst_label is None:
            print(f"  Excluding {len(audio_files)} clips from '{src_label}'")
            stats["excluded"]["skip"] += len(audio_files)
            continue

        print(f"Processing '{src_label}' → '{dst_label}' ({len(audio_files)} files)…")
        dst_folder = output_root / dst_label

        for src_file in tqdm(audio_files, leave=False):
            dst_file = dst_folder / src_file.name
            ok = process_file(src_file, dst_file)
            if ok:
                stats[dst_label]["ok"] += 1
            else:
                stats[dst_label]["skip"] += 1

    print("\n── Summary ──────────────────────────────────")
    for label, counts in stats.items():
        print(f"  {label:12s}  ok={counts['ok']:4d}  skip={counts['skip']:4d}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess DonateACry corpus for Naps0.")
    parser.add_argument("--input_dir",  required=True, help="Path to raw DonateACry folder")
    parser.add_argument("--output_dir", required=True, help="Destination for processed WAV files")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
