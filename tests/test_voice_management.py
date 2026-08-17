import tempfile
import unittest
from pathlib import Path

from xtts_api_server.voice_management import (
    MIN_XTTS_SAMPLE_SECONDS,
    delete_flat_voice,
    filter_valid_voice_samples,
    normalize_voice_id,
)


class VoiceManagementTest(unittest.TestCase):
    def test_deletes_flat_uploaded_voice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            voice = Path(temp_dir) / "sample.wav"
            voice.write_bytes(b"wav")

            removed = delete_flat_voice(temp_dir, "sample")

            self.assertEqual(removed, voice)
            self.assertFalse(voice.exists())

    def test_does_not_delete_multi_sample_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            voice_dir = Path(temp_dir) / "sample"
            voice_dir.mkdir()
            (voice_dir / "one.wav").write_bytes(b"wav")

            self.assertIsNone(delete_flat_voice(temp_dir, "sample"))
            self.assertTrue(voice_dir.exists())

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            normalize_voice_id("../sample")

    def test_filters_unreadable_and_too_short_voice_samples(self):
        durations = {
            "valid.wav": 1.0,
            "short.wav": MIN_XTTS_SAMPLE_SECONDS - 0.01,
        }

        def get_duration(sample_path):
            if sample_path == "broken.wav":
                raise RuntimeError("could not decode")
            return durations[sample_path]

        valid, rejected = filter_valid_voice_samples(
            ["valid.wav", "short.wav", "broken.wav"],
            get_duration,
        )

        self.assertEqual(valid, ["valid.wav"])
        self.assertEqual([path for path, _ in rejected], ["short.wav", "broken.wav"])
        self.assertIn("shorter than the XTTS minimum", rejected[0][1])
        self.assertIn("unreadable WAV", rejected[1][1])


if __name__ == "__main__":
    unittest.main()
