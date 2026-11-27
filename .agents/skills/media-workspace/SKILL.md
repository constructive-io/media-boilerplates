---
name: media-workspace
description: Start and work in a media project made with Constructive Media — a pnpm workspace whose packages are narrated decks, walkthroughs, animations and documents, each a `.conv` script and a page. Use when asked to "start a media project", "set up a media workspace", "make a new deck", "add a deck to this repo", "add a talk", "media init", "scaffold a narrated deck", "start a presentation that reads itself", or when a repository has `packages/*/*.conv` and something in it needs to be made, changed or built.
compatibility: Constructive Media (`media`) or pgpm (npm) to scaffold; Node and pnpm to lint; the engine with a speech server and Chrome or Chromium to build; ffmpeg to pull frames out
metadata:
  author: constructive-io
  version: "0.2.0"
---

# Media workspace

A media project is a pnpm workspace. Each package is something made from a
script:

```
harbour-talks/
  package.json            pnpm lint, pnpm build: every package, one at a time
  pnpm-workspace.yaml     packages/*
  media-libraries.json    which voice libraries, at which commit (once one is added)
  packages/
    first-talk/
      talk.conv           the words, who says them, and when the screen changes
      index.html          the slides
      package.json        lint, check, say, film, build, preview, clean
      out/                the sound and the film. Ignored, never committed
```

[Constructive Media](https://github.com/constructive-io/constructive-media)
(`media`) says a script in a voice, checks each line by listening back to it, and
films the page following the recording.

## Start

| The request | Run |
| --- | --- |
| a new project | `media init workspace NAME` — the workspace and a first deck |
| a new project, nothing in it | `media init workspace NAME --bare` |
| another deck, in a workspace | `media init deck NAME --title "…"` at the top of the workspace: it lands in `packages/NAME` |
| a tour of an application's screens, with a pointer | `media init walkthrough NAME` |
| pictures the page draws, moving with the voice | `media init animation NAME` |
| a document read aloud, and printed as a PDF | `media init document NAME` |
| any of them in a pnpm workspace that is not a media one | the same. Each is a package and brings nothing else |
| the engine is not installed | `pgpm init workspace --repo constructive-io/media-boilerplates --name NAME`, then inside it `pgpm init --repo constructive-io/media-boilerplates --moduleName NAME` for a deck. Add `--template walkthrough`, `animation` or `document` for the others |

Every question a template asks is a flag, and `media init --list` shows them:
`--title`, `--fullName` (who is speaking), `--role` (under their name),
`--license`. With nobody at the keyboard add `--no-tty`: defaults are taken and
a question with no default is an error that names its flag.

`media init` never writes into a folder that has something in it. It says so and
stops. Do not copy an existing package to make a new one: the copy keeps the
old name in its scripts.

## Work

```sh
pnpm install                    # once: the script checker
pnpm lint                       # every script is a script. Needs only Node
pnpm --filter first-talk build  # say it and film it: packages/first-talk/out/first-talk.mp4
pnpm build                      # every package, one at a time
```

Inside a package, `pnpm preview` plays the page in a browser with the sound, to
scrub through before filming, and `pnpm say` re-says only lines whose words
changed.

To change a package, change its two files. What a mark in the script does
(`[slide NAME step:N]`, `[speakers lower-third captions]`, `[pause 0.5]`) and
what an attribute in the page does (`data-slide`, `data-step`, `data-enter`) is
in the package's own README, and in two skills beside this one:
[narrated-video](../narrated-video/SKILL.md) for a deck, a walkthrough or an
animation, and [narrated-document](../narrated-document/SKILL.md) for a
document, which also has `pnpm pdf`.
A slide the script names and the page lacks is refused before anything is said.

## Voices

A script names a persona (`narrator`), never a voice. Before the first build
the persona needs one:

```sh
media voices                                # what this machine has
media voice narrator <a voice the speech server has> --new
```

or from a library:

```sh
media library search
media library add owner/some-voices
media library voices some-voices
media library lock                          # writes media-libraries.json: commit it
```

`pnpm libraries` on another machine adds what `media-libraries.json` lists, at
the same commits. A voice is cloned only from somebody who has said yes, and a
library says so for each voice it holds.

A script with `@include NAME` for a bank that comes from a library fails
`pnpm lint`: `conv` looks for `banks/NAME.sounds` beside the script and knows
nothing of this machine's libraries. In that package set `lint` to
`media conv talk.conv`, and say that CI can no longer read that script.

## Done means looked at

- `pnpm lint` passes.
- The build ends with no `need a listen:` and no `left out, having no file:`.
- Frames were pulled and looked at, the first picture and the last slide
  among them: `ffmpeg -ss 12 -i out/NAME.mp4 -frames:v 1 frame.png`.
- Say which frames you looked at, and that nobody has heard the sound until a
  person has.
- Nothing under `out/` is committed.

## Related

- [constructive-media](https://github.com/constructive-io/constructive-media): the engine and its own skill.
- [conversation-format](https://github.com/constructive-io/conversation-format): the `.conv` format and the `conv` skill.
- [voice-boilerplates](https://github.com/constructive-io/voice-boilerplates): start a library of voices.
