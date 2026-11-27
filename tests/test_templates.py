"""What the templates promise whoever scaffolds from them. Standard library only."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLANK = re.compile(r"____([A-Za-z_][A-Za-z0-9_]*?)____")
#: What the tool that scaffolds fills in itself, by the kind of template.
FILLED = {"workspace": {"name", "workspaceName"}, "module": {"moduleName", "packageIdentifier"},
          "generic": {"moduleName", "packageIdentifier"}}
#: Never copied into what is made.
OWN = {".boilerplate.json", ".boilerplate.js", ".boilerplates.json"}
#: Asked for the LICENSE file that is written, whether or not a file has the blank.
ALWAYS_USED = {"license"}
#: Every template, and what `.boilerplate.json` calls its kind. One with a script is a package of a workspace.
#: A library is neither: it is a repository of its own, made wherever it is asked for.
TEMPLATES = {"workspace": "workspace", "module": "module", "animation": "module", "walkthrough": "module",
             "document": "module", "library": "generic"}
#: What is a repository of its own, with no `package.json`.
APART = {"library"}
#: The script each one that has a script is made from.
SCRIPTS = {"module": "talk.conv", "animation": "scene.conv", "walkthrough": "tour.conv", "document": "reading.conv"}
#: The skills this repository holds.
SKILLS = ("media-workspace", "narrated-video", "narrated-document", "voice-library", "build-a-voice")
#: Where a template's skills come from, and the ones kept elsewhere: the engine's, and the format's.
HERE = "constructive-io/media-engine-boilerplates"
ELSEWHERE = {"constructive-io/media-engine": {"constructive-media"}, "constructive-io/conversation-format": {"conv"}}
#: The skill a template cannot be worked in without.
NEEDS = {"workspace": {"media-workspace", "narrated-video", "narrated-document"}, "module": {"narrated-video"},
         "walkthrough": {"narrated-video"}, "animation": {"narrated-video"}, "document": {"narrated-document"},
         "library": {"voice-library", "build-a-voice"}}


def templates():
    return sorted(path.parent for path in ROOT.rglob(".boilerplate.json") if "node_modules" not in path.parts)


def read(folder):
    return json.loads((folder / ".boilerplate.json").read_text(encoding="utf-8"))


def files(folder):
    return [path for path in sorted(folder.rglob("*"))
            if path.is_file() and path.name not in OWN and "__pycache__" not in path.parts]


def blanks(folder):
    found = set()
    for path in files(folder):
        found.update(BLANK.findall(str(path.relative_to(folder))))
        found.update(BLANK.findall(path.read_text(encoding="utf-8")))
    return found


def filled(text):
    return BLANK.sub("harbour", text)


class TemplatesTest(unittest.TestCase):
    def test_there_is_a_workspace_and_what_goes_in_one(self):
        root = json.loads((ROOT / ".boilerplates.json").read_text(encoding="utf-8"))
        kinds = {folder.name: read(folder)["type"] for folder in templates()}
        self.assertEqual(kinds, TEMPLATES)
        self.assertEqual(set(SCRIPTS), {name for name, kind in TEMPLATES.items() if kind == "module"})
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
            if folder.name in APART:
                # Left out, both tools would look for a workspace to put it in.
                self.assertIs(described.get("requiresWorkspace"), False)

    def test_a_template_names_the_skills_that_go_with_it(self):
        """`pgpm init` and `media init` copy these into `.agents/skills/` of what is made."""
        for folder in templates():
            wanted = read(folder).get("skills")
            self.assertIsInstance(wanted, list, f"{folder.name} names no skills")
            named = set()
            for one in wanted:
                self.assertEqual(set(one), {"source", "skills"}, folder.name)
                # owner/name: every reader can fetch it, and both tools read it the same way.
                self.assertRegex(one["source"], r"^constructive-io/[a-z-]+$", folder.name)
                for skill in one["skills"]:
                    self.assertNotIn(skill, named, f"{folder.name} names {skill} twice")
                    named.add(skill)
                    if one["source"] == HERE:
                        self.assertTrue((ROOT / ".agents/skills" / skill / "SKILL.md").is_file(),
                                        f"{folder.name} names {skill}, which is not a skill of this repository")
                    else:
                        self.assertIn(skill, ELSEWHERE.get(one["source"], ()), f"{folder.name}: {one['source']}")
            self.assertLessEqual(NEEDS[folder.name], named, folder.name)
            self.assertLessEqual({"constructive-media", "conv"}, named, f"{folder.name}: the engine's skill and the format's")
        every = {skill for folder in templates() for one in read(folder)["skills"] for skill in one["skills"]}
        self.assertLessEqual(set(SKILLS), every, "a skill of this repository comes with no template")

    def test_what_is_made_is_what_it_should_be(self):
        for folder in templates():
            for name in ("README.md", "AGENTS.md", ".motd"):
                self.assertTrue((folder / name).is_file(), f"{folder.name} has no {name}")
            if folder.name in APART:
                self.assertFalse((folder / "package.json").exists(), f"{folder.name} is not a package")
                continue
            package = json.loads(filled((folder / "package.json").read_text(encoding="utf-8")))
            self.assertIn("lint", package["scripts"])
            self.assertIn("build", package["scripts"])
            self.assertFalse((folder / "Makefile").exists(), "a package's commands are its scripts")
            if folder.name in SCRIPTS:
                # The workspace ignores what is rendered, and runs these in every package.
                self.assertFalse((folder / ".gitignore").exists(), f"{folder.name}: the workspace ignores out/")
                self.assertEqual(package["scripts"]["lint"], f"conv check {SCRIPTS[folder.name]}")
                self.assertEqual(package["scripts"]["check"], f"media conv {SCRIPTS[folder.name]}")
                for script in ("say", "film", "preview", "stills", "clean"):
                    self.assertIn(script, package["scripts"], f"{folder.name} has no {script}")
                self.assertIs(package["private"], True)

    def test_a_command_a_template_names_is_one_it_has(self):
        for name in SCRIPTS:
            folder = ROOT / "media" / name
            scripts = json.loads(filled((folder / "package.json").read_text(encoding="utf-8")))["scripts"]
            for path in files(folder):
                if path.name == "package.json":
                    continue
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"\bmake (check|sound|preview|pdf)\b|`make`|Makefile", text),
                                  f"{path.relative_to(ROOT)} speaks of make")
                for said in re.findall(r"`pnpm ([a-z]+)`", text):
                    self.assertIn(said, scripts, f"{path.relative_to(ROOT)} names `pnpm {said}`")

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
        self.assertIn("pnpm lint", (ROOT / "media/workspace/.github/workflows/ci.yml").read_text(encoding="utf-8"))

    def test_a_template_names_no_voice_and_holds_nothing_rendered(self):
        for name, called in SCRIPTS.items():
            folder = ROOT / "media" / name
            self.assertEqual([path.name for path in folder.glob("*.conv")], [called])
            script = (folder / called).read_text(encoding="utf-8")
            self.assertIn("persona: narrator", script, name)
            for word in ("@include", "voice:", "backend:"):
                self.assertNotIn(word, script, name)
            page = (folder / "index.html").read_text(encoding="utf-8")
            self.assertIn("stage.js", page, name)
            self.assertFalse((folder / "stage.js").exists(), "the engine hands the page its stage")
        kept = {path.suffix for path in files(ROOT) if ".git" not in path.parts and "node_modules" not in path.parts}
        self.assertEqual(kept & {".wav", ".flac", ".mp3", ".mp4", ".mov", ".png", ".jpg", ".safetensors"}, set())

    def test_every_page_has_what_its_script_names(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("follows", ROOT / "scripts" / "follows.py")
        follows = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(follows)
        for name, called in SCRIPTS.items():
            folder = ROOT / "media" / name
            self.assertEqual(follows.follows((folder / called).read_text(encoding="utf-8"),
                                             (folder / "index.html").read_text(encoding="utf-8")), [], name)

    def test_the_readme_lists_every_template_and_the_skills_are_where_it_says(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for folder in templates():
            self.assertIn(f"(./{folder.relative_to(ROOT)})", readme)
        guide = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for skill in SKILLS:
            written = ROOT / ".agents/skills" / skill / "SKILL.md"
            self.assertTrue(written.is_file(), skill)
            self.assertIn(f"name: {skill}\n", written.read_text(encoding="utf-8"))
            self.assertIn(f".agents/skills/{skill}/SKILL.md", guide)
            self.assertIn(f"--skill {skill}", readme)

    def test_a_skill_starts_a_thing_the_way_this_repository_does(self):
        for skill in SKILLS:
            text = (ROOT / ".agents/skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"\bmake (check|sound|preview|pdf)\b|`make`|Makefile", text), skill)
            for old in ("video-boilerplates", "document-boilerplates", "voice-boilerplates"):
                self.assertNotIn(old, text, f"{skill} sends a reader to a repository that was folded into this one")
            for name in re.findall(r"media init ([a-z]+) ", text):
                self.assertIn(name, set(TEMPLATES) | {"deck", "voices"}, f"{skill} starts from `{name}`")
            for name in re.findall(r"--template ([a-z]+)", text):
                self.assertIn(name, TEMPLATES, f"{skill} starts from `{name}`")


if __name__ == "__main__":
    unittest.main()
