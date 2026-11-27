"""The check that a page has what a script names. Standard library only."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("follows", ROOT / "scripts" / "follows.py")
follows = importlib.util.module_from_spec(spec)
spec.loader.exec_module(follows)

PAGE = """
<body data-stage="deck">
<section data-slide="title"><h1>The log</h1></section>
<section data-slide="log">
  <input data-step="2"><img src="a.png">
  <ol><li data-step="1">One</li></ol>
</section>
<section data-slide="close"><p data-step="1">Done</p></section>
</body>
"""


class FollowsTest(unittest.TestCase):
    def missing(self, script, page=PAGE):
        return follows.follows(script, page)

    def test_a_script_the_page_follows(self):
        self.assertEqual(self.missing("[slide title]\nA: Hello.\n[slide log step:2]\nA: There.\n[slide close step:1]\n"), [])

    def test_a_slide_the_page_does_not_have(self):
        self.assertEqual(self.missing("A: Hello.\n[slide pricing]\n"), ["line 2: the page has no slide called `pricing`"])

    def test_a_step_belongs_to_its_own_slide(self):
        self.assertEqual(self.missing("[slide title step:1]\n"), ["line 1: the slide `title` has no step 1"])
        self.assertEqual(self.missing("[slide close step:2]\n"), ["line 1: the slide `close` has no step 2"])
        self.assertEqual(self.missing("[slide log step:0]\n"), [])

    def test_only_marks_are_read(self):
        self.assertEqual(self.missing("# [slide gone]\nA: She said [slide gone] aloud.\n[speakers captions]\n"), [])

    def test_a_page_that_draws_itself_speaks_of_its_scenes(self):
        page = '<style>body[data-stage-slide="dusk"] #sky { fill: navy; }</style><body data-stage="plain"><svg></svg>'
        self.assertEqual(self.missing("[slide dusk]\n", page), [])
        self.assertEqual(self.missing("[slide dawn step:1]\n", page),
                         ["line 1: the page says nothing of a scene called `dawn`"])

    def test_every_template_follows_its_script(self):
        found = 0
        for told in sorted(ROOT.glob("media/*/.boilerplate.json")):
            if not list(told.parent.glob("*.conv")):
                continue                                    # a workspace has no script of its own
            scripts = list(told.parent.glob("*.conv"))
            self.assertEqual(len(scripts), 1, told.parent.name)
            page = (told.parent / "index.html").read_text(encoding="utf-8")
            self.assertEqual(follows.follows(scripts[0].read_text(encoding="utf-8"), page), [], told.parent.name)
            self.assertIn('<script src="stage.js" defer></script>', page)
            self.assertFalse((told.parent / "stage.js").exists(), "the engine hands stage.js over")
            found += 1
        self.assertGreaterEqual(found, 1)

    def test_no_template_holds_media(self):
        media = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".gif"}
        held = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*")
                if path.is_file() and ".git" not in path.parts and path.suffix.lower() in media]
        self.assertEqual(held, [])


if __name__ == "__main__":
    unittest.main()
