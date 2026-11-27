# media-engine-boilerplates — agent guide

What `media init` starts a project from: a pnpm workspace, and what goes in one — a narrated
deck, a walkthrough, an animation, a document that is read aloud — and a library of voices,
which is a repository of its own. The templates are in
the pgpm boilerplate format, so `pgpm init --repo` reads them
too. See [README.md](./README.md).

## Rules that are specific to this repository

- **Both tools, the same files.** `media init` and `pgpm init --repo` must write the same
  tree from these templates. `scripts/verify.sh` compares them. Anything only the engine
  reads goes in `.boilerplates.json` (`aliases`, `first`), which pgpm passes over.
- **Constructive's pnpm conventions.** A workspace has `pnpm-workspace.yaml` with
  `packages/*`, a private root `package.json` whose scripts are `pnpm -r run …`, and CI on
  `pnpm/action-setup`. A module is a package: its commands are `package.json` scripts,
  never a Makefile.
- **No media here, and no voices, ever.** No audio, no video, no pictures of people, no
  model weights. A template's screens are drawn in HTML and SVG. Everything rendered goes
  to `out/`, which is ignored. A test that needs a clip writes a few made-up bytes into a
  temporary folder.
- **Consent is not optional.** Do not weaken the consent rule in
  `media/library/scripts/check.py`, and do not ship the library template with a voice
  already in it.
- **`media/library/scripts/check.py` is standard library only**, for Python 3.9 and later.
  It says what the engine's `media library check` says, apart from measuring the clips.
  When the engine's rules for a library change, change this with them.
- **Nothing personal or local.** No real people, products, project names, machine paths
  or credentials in templates, tests, docs or commit messages. Examples use made-up names.
- **Every template with a script speaks as the persona `narrator`.** A template names no voice and adds
  no library: whose voice `narrator` is belongs to the machine.
- **A template never copies `stage.js` or `stage.css` in.** The engine hands them to the
  page. A template only loads them.
- **Blanks** are `____name____` words. `name` and `workspaceName` (a workspace) and
  `moduleName` and `packageIdentifier` (a module, and the library) are filled by the tool. Any other needs
  a question in that template's `.boilerplate.json`, and a question nothing uses is
  removed. `tests/test_templates.py` holds both.
- **A new template** is a folder under `media/` with a `.boilerplate.json`, a row in the
  README's table, a line in `TEMPLATES` and `SCRIPTS` of `tests/test_templates.py`, and a
  line in `kinds` of `scripts/verify.sh`. One with a script is a `module` that needs a
  `pnpm` workspace, with the same script names as the others. The `library` is the one
  that is not: it is `generic`, needs no workspace (`"requiresWorkspace": false`), and has
  no `package.json`.
- **This is the one place for templates.** A deck, a walkthrough, an animation, a
  document and a library of voices were once in repositories of their own. They are all
  here now.
- **MIT.** Nothing copied in under another license.

## Before you say it is done

```sh
python3 -m unittest discover -s tests
bash scripts/verify.sh
```

Both run in CI. `scripts/verify.sh` needs `pgpm` (`npm install -g pgpm`), node and pnpm.
With `media` installed it also scaffolds with `media init` and compares the two trees.

CI cannot film. After changing a page or a script, film it yourself and look:

```sh
bash scripts/verify.sh /tmp/made
cd /tmp/made/pgpm/harbour-talks && pnpm install && pnpm --filter harbour-tour build
ffmpeg -ss 10 -i packages/harbour-tour/out/harbour-tour.mp4 -frames:v 1 frame.png
```

Say which frames you looked at. A film nobody looked at is not checked.

## The skills

Five skills live here, and a template that changes takes its skill with it:

| Skill | Says how to |
| --- | --- |
| `.agents/skills/media-workspace/SKILL.md` | start a project, add to it and build it |
| `.agents/skills/narrated-video/SKILL.md` | write a deck, a walkthrough or an animation |
| `.agents/skills/narrated-document/SKILL.md` | write a document that is read aloud and printed |
| `.agents/skills/voice-library/SKILL.md` | make and use a library: the manifest, consent, banks, faces, pinning |
| `.agents/skills/build-a-voice/SKILL.md` | get from a recording to a voice that passes its audition, and mend one that does not |

```sh
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill media-workspace
```

Each template names the skills that go with it, as `skills` in its `.boilerplate.json`, and
`media init` and `pgpm init` copy them into `.agents/skills/` of the workspace that is made.
A new skill is added to the templates it is for; `tests/test_templates.py` says so when one
is in no template, or a template names one that is not there.

`tests/test_voice_skills.py` holds the two about voices to the library template: a file or a
mark a skill names is in it. When a command of the engine's changes, change the skills with it.
