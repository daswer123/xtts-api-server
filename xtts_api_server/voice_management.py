import math
import re
from pathlib import Path


VOICE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
MIN_XTTS_SAMPLE_SECONDS = 0.33


class InvalidVoiceSampleError(ValueError):
    pass


def filter_valid_voice_samples(
    sample_paths,
    get_duration_seconds,
    min_duration_seconds: float = MIN_XTTS_SAMPLE_SECONDS,
):
    valid_paths = []
    rejected_paths = []

    for sample_path in sample_paths:
        try:
            duration_seconds = float(get_duration_seconds(sample_path))
        except Exception as exc:
            rejected_paths.append((sample_path, f"unreadable WAV ({type(exc).__name__}: {exc})"))
            continue

        if not math.isfinite(duration_seconds) or duration_seconds <= 0:
            rejected_paths.append((sample_path, "empty or invalid WAV duration"))
        elif duration_seconds < min_duration_seconds:
            rejected_paths.append(
                (
                    sample_path,
                    f"duration {duration_seconds:.3f}s is shorter than the XTTS minimum "
                    f"of {min_duration_seconds:.3f}s",
                )
            )
        else:
            valid_paths.append(sample_path)

    return valid_paths, rejected_paths


def normalize_voice_id(value: str) -> str:
    voice_id = str(value or "").strip()
    if voice_id.lower().endswith(".wav"):
        voice_id = voice_id[:-4]
    if "/" in voice_id or "\\" in voice_id or not VOICE_ID_PATTERN.fullmatch(voice_id):
        raise ValueError("Voice ID must use only letters, numbers, dot, dash, or underscore.")
    return voice_id


def flat_voice_path(speaker_folder: str | Path, voice_id: str) -> Path:
    return Path(speaker_folder) / f"{normalize_voice_id(voice_id)}.wav"


def delete_flat_voice(speaker_folder: str | Path, voice_id: str) -> Path | None:
    path = flat_voice_path(speaker_folder, voice_id)
    if not path.is_file():
        return None
    path.unlink()
    return path
