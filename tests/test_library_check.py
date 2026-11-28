"""The library template's check: what it passes, and what it refuses.

Standard library only. Nothing here is a recording: a clip is a few made-up
bytes in a temporary folder, which is all the check looks at.
"""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "media" / "library" / "scripts" / "check.py"

sys.dont_write_bytecode = True     # nothing is left beside the template's script
spec = importlib.util.spec_from_file_location("check", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def library(folder: Path, **changes) -> Path:
    """A whole library of made-up things: a cloned voice, a server's voice, a bank, a face."""
    for name in ("voices/ada", "banks", "sounds", "faces"):
        (folder / name).mkdir(parents=True, exist_ok=True)
    (folder / "voices/ada/neutral.flac").write_bytes(b"not really a recording")
    (folder / "voices/ada/neutral.txt").write_text("The lamp was lit at dusk.\n")
    (folder / "banks/weather.sounds").write_text(
        "# what the weather does\n@sounds\nRAIN: { file: rain.flac, loop: true, track: ambience, level: -8 }\n")
    (folder / "sounds/rain.flac").write_bytes(b"not really rain")
    (folder / "faces/ada.png").write_bytes(b"not really a picture")
    manifest = {
        "library": "lighthouse",
        "version": "0.1.0",
        "voices": [
            {"persona": "ada", "name": "Ada Marsh", "reference": "voices/ada/neutral.flac",
             "consent": {"by": "Ada Marsh", "kind": "own", "on": "2026-01-31"}},
            {"persona": "ben", "profile": "a-voice-of-the-servers",
             "consent": {"by": "nobody", "kind": "synthetic", "note": "one of the speech server's own voices"}},
        ],
        "banks": ["banks"],
        "sounds": ["sounds"],
        "faces": {"ada": "faces/ada.png"},
    }
    manifest.update(changes)
    (folder / "media-library.json").write_text(json.dumps(manifest, indent=2))
    return folder


class CheckTest(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.folder = Path(scratch.name) / "lighthouse"
        self.folder.mkdir()

    def problems(self, **changes):
        return check.check(library(self.folder, **changes))[2]

    def voice(self, **changes):
        voice = {"persona": "ada", "reference": "voices/ada/neutral.flac",
                 "consent": {"by": "Ada Marsh", "kind": "own"}}
        voice.update(changes)
        return {"voices": [{key: value for key, value in voice.items() if value is not None}]}

    def test_a_whole_library_passes(self):
        name, voices, problems, notes = check.check(library(self.folder))
        self.assertEqual((name, voices, problems, notes), ("lighthouse", 2, [], []))

    def test_an_empty_one_passes_and_says_it_is_empty(self):
        (self.folder / "banks").mkdir()
        (self.folder / "media-library.json").write_text(json.dumps(
            {"library": "lighthouse", "voices": [], "banks": ["banks"], "sounds": [], "faces": {}}))
        name, voices, problems, notes = check.check(self.folder)
        self.assertEqual((name, voices, problems), ("lighthouse", 0, []))
        self.assertEqual(notes, ["it holds no voices, no banks and no faces yet"])

    def test_a_folder_that_is_not_one_says_so(self):
        self.assertIn("is not a library", check.check(self.folder)[2][0])
        (self.folder / "media-library.json").write_text("{ not json")
        self.assertIn("cannot be read as JSON", check.check(self.folder)[2][0])
        (self.folder / "media-library.json").write_text("[]")
        self.assertIn("should hold an object", check.check(self.folder)[2][0])

    def test_its_name_is_lower_case_with_hyphens(self):
        self.assertIn('"library" is the library\'s name', self.problems(library="The Lighthouse")[0])

    def test_a_voice_with_no_consent_is_refused(self):
        (problem,) = self.problems(**self.voice(consent=None))
        self.assertIn('ada/neutral: it has no "consent"', problem)

    def test_consent_says_who_and_what_kind(self):
        self.assertIn('who gave it, as "by"', self.problems(**self.voice(consent={"kind": "own"}))[0])
        self.assertIn('"kind" of its consent', self.problems(**self.voice(consent={"by": "Ada Marsh"}))[0])
        self.assertIn('"kind" of its consent',
                      self.problems(**self.voice(consent={"by": "Ada Marsh", "kind": "found online"}))[0])
        self.assertIn("written like 2026-11-26",
                      self.problems(**self.voice(consent={"by": "Ada Marsh", "kind": "own", "on": "last week"}))[0])

    def test_a_licensed_or_designed_voice_says_more(self):
        self.assertIn("which license", self.problems(**self.voice(consent={"by": "A reader", "kind": "licensed"}))[0])
        self.assertIn("how the voice was made",
                      self.problems(**self.voice(consent={"by": "nobody", "kind": "synthetic"}))[0])
        self.assertEqual(self.problems(**self.voice(
            consent={"by": "A reader", "kind": "licensed", "note": "CC0, from a public reading"})), [])

    def test_a_clip_is_there_is_a_sound_and_has_its_words(self):
        self.assertIn("is not there", self.problems(**self.voice(reference="voices/ada/warm.flac"))[0])
        self.assertIn("not a kind of sound file", self.problems(**self.voice(reference="voices/ada/neutral.txt"))[0])
        library(self.folder)
        (self.folder / "voices/ada/neutral.txt").unlink()
        (problem,) = check.check(self.folder)[2]
        self.assertIn("the words said in its clip are not written down", problem)
        self.assertEqual(self.problems(**self.voice(said="The lamp was lit at dusk.")), [])

    def test_a_voice_is_a_clip_or_a_servers_voice(self):
        self.assertIn('a "reference", a clip to clone from, or a "profile"', self.problems(**self.voice(reference=None))[0])
        self.assertEqual(self.problems(**self.voice(reference=None, profile="a-voice-of-the-servers")), [])

    def test_a_persona_has_one_voice_for_a_mood(self):
        twice = self.voice()["voices"] * 2
        self.assertIn("ada/neutral is there twice", self.problems(voices=twice)[0])
        other = [twice[0], dict(twice[0], emotion="whisper")]
        self.assertEqual(self.problems(voices=other), [])

    def test_nothing_it_names_is_outside_it(self):
        (self.folder.parent / "elsewhere.flac").write_bytes(b"x")
        self.assertIn("outside the library", self.problems(**self.voice(reference="../elsewhere.flac"))[0])
        self.assertIn("outside the library", self.problems(**self.voice(reference="/tmp/elsewhere.flac"))[0])
        self.assertIn("outside the library", self.problems(faces={"ada": "../face.png"})[0])
        self.assertIn("outside the library", self.problems(banks=[".."])[0])

    def test_a_bank_plays_only_what_the_library_holds(self):
        library(self.folder)
        (self.folder / "banks/weather.sounds").write_text('@sounds\nTHUNDER: { file: "thunder.flac" }\n')
        self.assertIn("bank `weather`: it plays `thunder.flac`, which is not in", check.check(self.folder)[2][0])
        (self.folder / "banks/weather.sounds").write_text("@sounds\nRAIN: { file: /Users/somebody/rain.flac }\n")
        self.assertIn("a path only this machine has", check.check(self.folder)[2][0])
        (self.folder / "banks/weather.sounds").write_text("@sounds\n# RAIN: { file: gone.flac }\nRAIN: { prompt: rain }\n")
        self.assertEqual(check.check(self.folder)[2], [])

    def test_a_face_is_a_picture_that_is_there(self):
        self.assertIn("is not there", self.problems(faces={"ada": "faces/gone.png"})[0])
        self.assertIn("should be a picture", self.problems(faces={"ada": "voices/ada/neutral.txt"})[0])

    def test_what_was_left_in_by_mistake_is_noted(self):
        library(self.folder)
        (self.folder / "session.wav").write_bytes(b"the whole recording")
        (self.folder / "session.mov").write_bytes(b"and the camera's")
        for kept in ("originals", "out"):                      # where recordings and renders are meant to be
            (self.folder / kept).mkdir()
            (self.folder / kept / "session.wav").write_bytes(b"the whole recording")
        (self.folder / "voices/ada/neutral.flac").write_bytes(b"x" * (check.CLIP_BYTES + 1))
        _, _, problems, notes = check.check(self.folder)
        self.assertEqual(problems, [])
        self.assertEqual(len(notes), 3)
        self.assertTrue(any("`session.wav` is a recording that no voice and no bank names" in note for note in notes))
        self.assertTrue(any("`session.mov` is footage" in note for note in notes))
        self.assertTrue(any("its clip is 6 MB" in note for note in notes))

    def test_a_short_video_among_the_sounds_is_a_clip_to_cut_to(self):
        library(self.folder)
        (self.folder / "banks/titles.sounds").write_text("@sounds\nOPENING: { file: opening.mp4 }\n")
        (self.folder / "sounds/opening.mp4").write_bytes(b"not really a title")
        _, _, problems, notes = check.check(self.folder)
        self.assertEqual(problems, [])
        self.assertEqual(notes, [])
        (self.folder / "faces/opening.mp4").write_bytes(b"not really a title")
        self.assertIn("`faces/opening.mp4` is footage", check.check(self.folder)[3][0])

    def test_what_it_does_not_know_is_noted_not_refused(self):
        _, _, problems, notes = check.check(library(self.folder, colour="blue"))
        self.assertEqual(problems, [])
        self.assertEqual(notes, ['"colour" is not something a library says; it is ignored'])

    def test_as_a_command_it_says_ok_or_fails(self):
        library(self.folder)
        ran = subprocess.run([sys.executable, str(SCRIPT), str(self.folder)], capture_output=True, text=True)
        self.assertEqual((ran.returncode, ran.stdout.strip()), (0, "ok: lighthouse, 2 voice(s)"))
        library(self.folder, **self.voice(consent=None))
        ran = subprocess.run([sys.executable, str(SCRIPT), str(self.folder)], capture_output=True, text=True)
        self.assertEqual(ran.returncode, 1)
        self.assertIn("1 problem(s): this is not a library yet", ran.stderr)


if __name__ == "__main__":
    unittest.main()
