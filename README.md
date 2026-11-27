# media-boilerplates

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" alt="Constructive" />
</p>

<p align="center" width="100%">
  <a href="https://github.com/constructive-io/media-boilerplates/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/constructive-io/media-boilerplates/actions/workflows/ci.yml/badge.svg" alt="CI status" />
  </a>
  <a href="https://github.com/constructive-io/media-boilerplates/blob/main/LICENSE"><img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license" /></a>
</p>

<p align="center" width="100%">
  Start a media project in one command: a workspace of talks that are written, not recorded.
</p>

```sh
me init workspace harbour-talks
cd harbour-talks
pnpm install
pnpm lint         # every script is a script
pnpm build        # packages/first-talk/out/first-talk.mp4
```

That is a pnpm workspace with one deck in it. A deck is two files: a script in
the [`.conv` format](https://github.com/constructive-io/conversation-format)
that says the words and when the slides change, and a page of plain HTML that
holds the slides. [Constructive Media](https://github.com/constructive-io/constructive-media)
(`me`) says the script in a voice, checks every line by listening back to it,
and films the page as it follows the recording.

Another deck, in a workspace you already have:

```sh
me init deck quarterly-review --title "The quarter in ten minutes"
```

It lands in `packages/quarterly-review`. Any pnpm workspace will do: the deck
is a package with a `package.json`, and brings nothing else with it.

## Templates

| Template | Is | Lands |
| --- | --- | --- |
| [`workspace`](./media/workspace) | a pnpm workspace: `packages/*`, the script checker, CI that reads every script | in a new folder named for it, or the empty folder you are in if it has that name |
| [`module`](./media/module), also called `deck` | a narrated deck as a package: a script, a page, and `pnpm build` | in `packages/NAME` from the top of a pnpm workspace, or `./NAME` anywhere else |

`me init workspace NAME` makes the workspace and its first deck together.
`--bare` makes the workspace alone. `me init --list` says what each template
asks, and every question is also a flag: `--title`, `--fullName`, `--role`,
`--license`.

## With pgpm, without the engine

These are [pgpm](https://github.com/constructive-io/constructive) boilerplates,
in the same format as the ones `pgpm init` uses, so the engine is not needed to
start from them:

```sh
npm install -g pgpm
pgpm init workspace --repo constructive-io/media-boilerplates --name harbour-talks
cd harbour-talks
pgpm init --repo constructive-io/media-boilerplates --moduleName first-talk
```

Both tools write the same files in the same places. `me init` reads this
repository with Python's standard library alone, and adds two things pgpm does
not look at, both in [`.boilerplates.json`](./.boilerplates.json): other names
for a template (`deck`), and what a new workspace starts with.

## What you need to build

`pnpm lint` needs only Node. `pnpm build` needs
[Constructive Media](https://github.com/constructive-io/constructive-media) set
up, with a speech server, Chrome or Chromium, and a voice for the persona
`narrator`:

```sh
me voice narrator <a voice your speech server has> --new
```

or a voice from a library, started with
[voice-boilerplates](https://github.com/constructive-io/voice-boilerplates).

## Your own boilerplates

A boilerplate repository is folders. One with a `.boilerplate.json` is a
template, a word between four underscores (`____title____`) is a blank, and
every blank is a question:

```json
{
  "type": "module",
  "requiresWorkspace": "pnpm",
  "questions": [
    { "name": "____title____", "message": "The title on the first screen", "default": "A short talk", "required": true }
  ]
}
```

Point either tool at yours:

```sh
me init poster launch-night --repo your-org/your-boilerplates
export CONSTRUCTIVE_MEDIA_BOILERPLATES=your-org/your-boilerplates     # or for every me init
```

## Working on the templates

```sh
python3 -m unittest discover -s tests     # every blank has a question, every slide a script names is in the page
bash scripts/verify.sh                    # scaffolds with pgpm, and with me when it is installed, and compares
```

`scripts/verify.sh FOLDER` keeps what it scaffolded, to run `pnpm build` in.
Filming is not part of CI: it takes the engine and a voice.

## Related

- [constructive-media](https://github.com/constructive-io/constructive-media): the engine that says a script and films a page, and `me init`.
- [conversation-format](https://github.com/constructive-io/conversation-format): the `.conv` format the scripts are written in.
- [video-boilerplates](https://github.com/constructive-io/video-boilerplates): a walkthrough of an application, an animation, a deck on its own.
- [document-boilerplates](https://github.com/constructive-io/document-boilerplates): a document that is read aloud.
- [voice-boilerplates](https://github.com/constructive-io/voice-boilerplates): a library of voices, sounds and faces.
- [constructive](https://github.com/constructive-io/constructive): pgpm, whose `init` these templates are written for.

## License

[MIT](./LICENSE)
