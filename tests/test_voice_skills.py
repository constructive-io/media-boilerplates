"""The two skills about voices say what the library template does."""

import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SKILLS = HERE / ".agents" / "skills"
LIBRARY = HERE / "media" / "library"


class SkillsTest(unittest.TestCase):
    def skill(self, name):
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_each_is_named_for_its_folder_and_says_when_to_use_it(self):
        for name in ("build-a-voice", "voice-library"):
            head = self.skill(name).split("---")[1]
            self.assertIn(f"name: {name}\n", head)
            self.assertRegex(head, r"description: .*Use when")
            self.assertRegex(head, r'version: "\d+\.\d+\.\d+"')

    def test_each_names_the_other_the_engine_and_the_format(self):
        for name, other in (("build-a-voice", "voice-library"), ("voice-library", "build-a-voice")):
            related = self.skill(name).split("## Related skills")[1]
            for wanted in (f"`{other}`", "`constructive-media`", "`conv`"):
                self.assertIn(wanted, related)

    def test_what_they_name_in_a_library_is_in_the_template(self):
        said = self.skill("build-a-voice") + self.skill("voice-library")
        for file in ("originals/README.md", "CONSENT.md", "scripts/check.py", "media-library.json"):
            self.assertIn(file, said)
            self.assertTrue((LIBRARY / file).is_file(), file)
        readme = (LIBRARY / "README.md").read_text(encoding="utf-8")
        self.assertRegex(readme, r"(?s)<!-- voices -->\n\| Persona .*<!-- /voices -->")
        for document in (said, readme, (LIBRARY / "AGENTS.md").read_text(encoding="utf-8"),
                         (LIBRARY / "originals" / "README.md").read_text(encoding="utf-8")):
            self.assertIn("media library clip ", document)
            # Whose voice it is and by what right are on every line that puts one in.
            for line in re.findall(r"^media library clip .*$", document, flags=re.M):
                self.assertIn(" --by ", line)
                self.assertIn(" --kind ", line)

    def test_consent_comes_first_in_both(self):
        for name in ("build-a-voice", "voice-library"):
            self.assertRegex(self.skill(name), r"(?s)\*\*[^*]*(owner said yes|with their yes)[^*]*\*\*")

    def test_the_kinds_of_consent_are_the_checks_own(self):
        import importlib.util
        import sys

        sys.dont_write_bytecode = True     # nothing is left beside the template's script

        spec = importlib.util.spec_from_file_location("check", LIBRARY / "scripts" / "check.py")
        check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(check)
        for kind in check.KINDS:
            self.assertIn(f"`{kind}`", self.skill("voice-library"))


if __name__ == "__main__":
    unittest.main()
