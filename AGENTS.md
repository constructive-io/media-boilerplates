# media-boilerplates — agent guide

What `me init` starts a project from: a pnpm workspace, and a narrated deck that goes in
one. The templates are in the pgpm boilerplate format, so `pgpm init --repo` reads them
too. See [README.md](./README.md).

## Rules that are specific to this repository

- **Both tools, the same files.** `me init` and `pgpm init --repo` must write the same
  tree from these templates. `scripts/verify.sh` compares them. Anything only the engine
  reads goes in `.boilerplates.json` (`aliases`, `first`), which pgpm passes over.
- **Constructive's pnpm conventions.** A workspace has `pnpm-workspace.yaml` with
  `packages/*`, a private root `package.json` whose scripts are `pnpm -r run …`, and CI on
  `pnpm/action-setup`. A module is a package: its commands are `package.json` scripts,
  never a Makefile.
- **No media here.** No audio, no video, no pictures of people. A template's screens are
  drawn in HTML and SVG. Everything rendered goes to `out/`, which is ignored.
- **Nothing personal or local.** No real people, products, project names, machine paths
  or credentials in templates, tests, docs or commit messages. Examples use made-up names.
- **Every template speaks as the persona `narrator`.** A template names no voice and adds
  no library: whose voice `narrator` is belongs to the machine.
- **A template never copies `stage.js` or `stage.css` in.** The engine hands them to the
  page. A template only loads them.
- **Blanks** are `____name____` words. `name` and `workspaceName` (a workspace) and
  `moduleName` and `packageIdentifier` (a module) are filled by the tool. Any other needs
  a question in that template's `.boilerplate.json`, and a question nothing uses is
  removed. `tests/test_templates.py` holds both.
- **A new template** is a folder under `media/` with a `.boilerplate.json`, a row in the
  README's table, and a line in `scripts/verify.sh`.
- **MIT.** Nothing copied in under another license.

## Before you say it is done

```sh
python3 -m unittest discover -s tests
bash scripts/verify.sh
```

Both run in CI. `scripts/verify.sh` needs `pgpm` (`npm install -g pgpm`), node and pnpm.
With `me` installed it also scaffolds with `me init` and compares the two trees.

CI cannot film. After changing a page or a script, film it yourself and look:

```sh
bash scripts/verify.sh /tmp/made
cd /tmp/made/pgpm/harbour-talks && pnpm install && pnpm build
ffmpeg -ss 10 -i packages/first-talk/out/first-talk.mp4 -frames:v 1 frame.png
```

Say which frames you looked at. A film nobody looked at is not checked.

## The media-workspace skill

How a project is started and worked in is a skill in this repo:
`.agents/skills/media-workspace/SKILL.md`.

```sh
npx skills add https://github.com/constructive-io/media-boilerplates --skill media-workspace
```
