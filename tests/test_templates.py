"""What the templates promise whoever scaffolds from them. Standard library only."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLANK = re.compile(r"____([A-Za-z_][A-Za-z0-9_]*?)____")
#: What the tool that scaffolds fills in itself, by the kind of template.
FILLED = {"workspace": {"name", "workspaceName"}, "module": {"moduleName", "packageIdentifier"}}
#: Never copied into what is made.
OWN = {".boilerplate.json", ".boilerplate.js", ".boilerplates.json"}
#: Asked for the LICENSE file that is written, whether or not a file has the blank.
ALWAYS_USED = {"license"}


def templates():
    return sorted(path.parent for path in ROOT.rglob(".boilerplate.json") if "node_modules" not in path.parts)


def read(folder):
    return json.loads((folder / ".boilerplate.json").read_text(encoding="utf-8"))


def files(folder):
    return [path for path in sorted(folder.rglob("*")) if path.is_file() and path.name not in OWN]


def blanks(folder):
    found = set()
    for path in files(folder):
        found.update(BLANK.findall(str(path.relative_to(folder))))
        found.update(BLANK.findall(path.read_text(encoding="utf-8")))
    return found


def filled(text):
    return BLANK.sub("harbour", text)


class TemplatesTest(unittest.TestCase):
    def test_there_is_a_workspace_and_a_module(self):
        root = json.loads((ROOT / ".boilerplates.json").read_text(encoding="utf-8"))
        kinds = {folder.name: read(folder)["type"] for folder in templates()}
        self.assertEqual(kinds, {"workspace": "workspace", "module": "module"})
        self.assertEqual({folder.parent for folder in templates()}, {ROOT / root["dir"]})

    def test_what_only_the_engine_reads_names_templates_that_are_there(self):
        root = json.loads((ROOT / ".boilerplates.json").read_text(encoding="utf-8"))
        within = ROOT / root["dir"]
        for other, name in root["aliases"].items():
            self.assertTrue((within / name / ".boilerplate.json").is_file(), f"`{other}` means {name}, which is not there")
            self.assertFalse((within / other).exists(), f"`{other}` is another name and a folder both")
        first = root["first"]
        self.assertEqual(read(within / first["template"])["type"], "module")
        self.assertRegex(first["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_every_blank_is_asked_about_and_every_question_is_used(self):
        for folder in templates():
            described = read(folder)
            asked = [BLANK.fullmatch(question["name"]).group(1) for question in described["questions"]]
            self.assertEqual(len(asked), len(set(asked)), f"{folder.name} asks something twice")
            used = blanks(folder)
            automatic = FILLED[described["type"]]
            self.assertEqual(used - automatic - set(asked), set(), f"{folder.name} has a blank nothing asks about")
            self.assertEqual(set(asked) - used - ALWAYS_USED, set(), f"{folder.name} asks what nothing uses")
            self.assertEqual(set(asked) & automatic, set(), f"{folder.name} asks what the tool fills in")

    def test_a_question_says_what_it_asks_and_can_be_left_alone(self):
        for folder in templates():
            for question in read(folder)["questions"]:
                self.assertTrue(question.get("message", "").strip(), f"{folder.name}: {question['name']} has no message")
                # Scaffolded with nobody to ask, every question still has an answer.
                self.assertTrue({"default", "defaultFrom", "setFrom"} & set(question),
                                f"{folder.name}: {question['name']} has no default")

    def test_a_module_says_which_workspace_it_goes_into(self):
        for folder in templates():
            described = read(folder)
            if described["type"] == "module":
                # Left out, pgpm takes it to need a pgpm workspace, and refuses a media one.
                self.assertEqual(described.get("requiresWorkspace"), "pnpm")
            self.assertNotIn("skills", described, "skills are installed from repositories a reader may not have")

    def test_what_is_made_is_what_it_should_be(self):
        for folder in templates():
            package = json.loads(filled((folder / "package.json").read_text(encoding="utf-8")))
            self.assertIn("lint", package["scripts"])
            self.assertIn("build", package["scripts"])
            self.assertFalse((folder / "Makefile").exists(), "a package's commands are its scripts")
            for name in ("README.md", "AGENTS.md", ".motd"):
                self.assertTrue((folder / name).is_file(), f"{folder.name} has no {name}")

    def test_the_workspace_is_a_pnpm_workspace_as_constructive_makes_one(self):
        folder = ROOT / "media" / "workspace"
        package = json.loads(filled((folder / "package.json").read_text(encoding="utf-8")))
        self.assertIs(package["private"], True)
        for script in ("lint", "check", "build", "clean"):
            self.assertIn("pnpm -r", package["scripts"][script])
        # One thing is said at a time: two builds at once would fight over one speech server.
        self.assertIn("--workspace-concurrency=1", package["scripts"]["build"])
        workspace = (folder / "pnpm-workspace.yaml").read_text(encoding="utf-8")
        self.assertIn("- 'packages/*'", workspace)
        self.assertIn("minimumReleaseAge:", workspace)
        self.assertIn("**/out/", (folder / ".gitignore").read_text(encoding="utf-8").split())
        self.assertIn("pnpm lint", (folder / ".github/workflows/ci.yml").read_text(encoding="utf-8"))

    def test_the_deck_names_no_voice_and_holds_nothing_rendered(self):
        folder = ROOT / "media" / "module"
        script = (folder / "talk.conv").read_text(encoding="utf-8")
        self.assertIn("persona: narrator", script)
        for word in ("@include", "voice:", "backend:"):
            self.assertNotIn(word, script)
        page = (folder / "index.html").read_text(encoding="utf-8")
        self.assertIn("stage.js", page)
        self.assertFalse((folder / "stage.js").exists(), "the engine hands the page its stage")
        kept = {path.suffix for path in files(ROOT) if ".git" not in path.parts and "node_modules" not in path.parts}
        self.assertEqual(kept & {".wav", ".flac", ".mp3", ".mp4", ".mov", ".png", ".jpg", ".safetensors"}, set())

    def test_the_page_of_the_deck_has_what_its_script_names(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("follows", ROOT / "scripts" / "follows.py")
        follows = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(follows)
        folder = ROOT / "media" / "module"
        self.assertEqual(follows.follows((folder / "talk.conv").read_text(encoding="utf-8"),
                                         (folder / "index.html").read_text(encoding="utf-8")), [])

    def test_the_readme_lists_every_template_and_the_skill_is_where_it_says(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for folder in templates():
            self.assertIn(f"(./{folder.relative_to(ROOT)})", readme)
        self.assertTrue((ROOT / ".agents/skills/media-workspace/SKILL.md").is_file())
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(".agents/skills/media-workspace/SKILL.md", guide)


if __name__ == "__main__":
    unittest.main()
