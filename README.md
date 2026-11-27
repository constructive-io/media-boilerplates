# media-engine-boilerplates

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" alt="Constructive" />
</p>

<p align="center" width="100%">
  <a href="https://github.com/constructive-io/media-engine-boilerplates/actions/workflows/ci.yml">
    <img height="20" src="https://github.com/constructive-io/media-engine-boilerplates/actions/workflows/ci.yml/badge.svg" alt="CI status" />
  </a>
  <a href="https://github.com/constructive-io/media-engine-boilerplates/blob/main/LICENSE"><img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license" /></a>
</p>

<p align="center" width="100%">
  Start a media project in one command: a workspace of talks, tours, films and documents that are written, not recorded.
</p>

```sh
media init workspace harbour-talks
cd harbour-talks
pnpm install
pnpm lint         # every script is a script
pnpm build        # packages/first-talk/out/first-talk.mp4
```

That is a pnpm workspace with one deck in it. A deck is two files: a script in
the [`.conv` format](https://github.com/constructive-io/conversation-format)
that says the words and when the slides change, and a page of plain HTML that
holds the slides. [Constructive Media](https://github.com/constructive-io/media-engine)
(`media`) says the script in a voice, checks every line by listening back to it,
and films the page as it follows the recording.

Something else, in a workspace you already have:

```sh
media init deck quarterly-review --title "The quarter in ten minutes"
media init walkthrough first-day --title "Your first day in the log"
media init animation how-it-works
media init document annual-report
```

Each lands in `packages/NAME`. Any pnpm workspace will do: what is made is a
package with a `package.json`, and brings nothing else with it.

And whose voice a script is said in, which is a repository of its own:

```sh
media init library my-voices
cd my-voices
media library clip narrator originals/narrator.wav --by "Ada Marsh" --kind own
media audition narrator
```

A library holds the clips voices are cloned from, banks of sounds and faces,
and one file that says what is in it and, for every voice, whose it is and by
what right it is there. The template has no voices in it.

## Templates

| Template | Is | Lands |
| --- | --- | --- |
| [`workspace`](./media/workspace) | a pnpm workspace: `packages/*`, the script checker, CI that reads every script | in a new folder named for it, or the empty folder you are in if it has that name |
| [`module`](./media/module), also called `deck` | a narrated deck: slides that reveal as they are spoken of | in `packages/NAME` from the top of a pnpm workspace, or `./NAME` anywhere else |
| [`walkthrough`](./media/walkthrough) | a tour of an application's screens, with a pointer that goes to what is being spoken of | the same |
| [`animation`](./media/animation) | a film whose pictures the page draws for itself, moving with the voice | the same |
| [`document`](./media/document) | a document read aloud, scrolling to where the voice is, and the same page as a PDF | the same |
| [`library`](./media/library), also called `voices` | a library of voices, banks of sounds and faces, with consent written down for every voice | in `./NAME`, wherever you are: it is a repository of its own, not a package |

Every one but the workspace and the library is a package: a `.conv` script, a
page of HTML, and a `package.json` whose scripts are `lint`, `check`, `say`,
`film`, `stills`, `build`, `preview` and `clean`. The document has `pdf` as
well. The library has a check of its own, `python3 scripts/check.py`, which
runs on every push.

`media init workspace NAME` makes the workspace and its first deck together.
`--bare` makes the workspace alone. `media init --list` says what each template
asks, and every question is also a flag: `--title`, `--fullName`, `--role`,
`--license`.

## With pgpm, without the engine

These are [pgpm](https://github.com/constructive-io/constructive) boilerplates,
in the same format as the ones `pgpm init` uses, so the engine is not needed to
start from them:

```sh
npm install -g pgpm
pgpm init workspace --repo constructive-io/media-engine-boilerplates --name harbour-talks
cd harbour-talks
pgpm init --repo constructive-io/media-engine-boilerplates --moduleName first-talk
pgpm init --repo constructive-io/media-engine-boilerplates --template walkthrough --moduleName first-day
pgpm init --repo constructive-io/media-engine-boilerplates --template library --moduleName my-voices
```

Both tools write the same files in the same places. `media init` reads this
repository with Python's standard library alone, and adds two things pgpm does
not look at, both in [`.boilerplates.json`](./.boilerplates.json): other names
for a template (`deck`, `voices`), and what a new workspace starts with.

## What you need to build

`pnpm lint` needs only Node. `pnpm build` needs
[Constructive Media](https://github.com/constructive-io/media-engine) set
up, with a speech server, Chrome or Chromium, and a voice for the persona
`narrator`:

```sh
media voice narrator <a voice your speech server has> --new
```

or a voice from a library, started with `media init library NAME`.

## The one rule about voices

**A voice is a person's.** Every voice in a library says whose it is and by
what right it is there: their own, by their permission, under a license, or
nobody's because it was designed. A library with a voice that does not say
fails its check, and the engine will not add it. Do not record, clone or
publish a voice whose owner has not said yes.

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
media init poster launch-night --repo your-org/your-boilerplates
export CONSTRUCTIVE_MEDIA_BOILERPLATES=your-org/your-boilerplates     # or for every media init
```

## Working on the templates

```sh
python3 -m unittest discover -s tests     # every blank has a question, every slide a script names is in the page,
                                          # and the library's check refuses what it should
bash scripts/verify.sh                    # scaffolds with pgpm, and with media when it is installed, and compares
```

`scripts/verify.sh FOLDER` keeps what it scaffolded, to run `pnpm build` in.
Filming is not part of CI: it takes the engine and a voice.

## Skills

Five skills say how the work is done, for an agent that is asked to do it. A project
started from a template gets the ones that go with it, in `.agents/skills/` at the top of
the workspace, with the engine's own (`constructive-media`) and the format's (`conv`): both
`media init` and `pgpm init` copy them, from the `skills` each template names in its
`.boilerplate.json`. `media init --no-skills` leaves them out. To add one by hand:

```sh
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill media-workspace      # start a project, add to it, build it
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill narrated-video       # write a deck, a walkthrough or an animation
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill narrated-document    # write a document that is read aloud
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill voice-library        # make and use a library of voices, sounds and faces
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill build-a-voice        # from a recording to a voice that passes its audition
```

## Related

- [media-engine](https://github.com/constructive-io/media-engine): the engine that says a script and films a page, and `media init`.
- [conversation-format](https://github.com/constructive-io/conversation-format): the `.conv` format the scripts are written in.
- [constructive](https://github.com/constructive-io/constructive): pgpm, whose `init` these templates are written for.

## License

[MIT](./LICENSE)
