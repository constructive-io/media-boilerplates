# ____repoName____

A media workspace: talks, tours and films that are written, not recorded.
Every folder under [`packages/`](./packages) is one of them, with a script that
says the words and a page that holds what is on the screen.
[Constructive Media](https://github.com/constructive-io/media-engine)
(`media`) says the one and films the other.

```sh
pnpm install      # the script checker, and nothing else
pnpm lint         # every script is a script. Needs no voice
pnpm build        # say and film everything: packages/*/out/*.mp4
```

| Command | Does |
| --- | --- |
| `pnpm lint` | reads every script with [`conv`](https://github.com/constructive-io/conversation-format) and says what is wrong. Needs only Node |
| `pnpm check` | the same with the engine, which also knows this machine's voices and libraries |
| `pnpm build` | says and films every package, one at a time. A line already said is kept |
| `pnpm clean` | throws away everything rendered |
| `pnpm --filter NAME build` | one package only |

`pnpm build` needs [Constructive Media](https://github.com/constructive-io/media-engine)
set up, with a speech server, Chrome or Chromium, and a voice for each persona
the scripts name.

## Add something

```sh
media init deck quarterly-review --title "The quarter in ten minutes"
```

It lands in `packages/quarterly-review`, with a script, a page and a README
that says what to change.

| `media init …` | Makes |
| --- | --- |
| `deck NAME` | a talk with slides that reveal as they are spoken of |
| `walkthrough NAME` | a tour of an application's screens, with a pointer |
| `animation NAME` | a film whose pictures the page draws, moving with the voice |
| `document NAME` | a document read aloud, and the same page as a PDF |

Without the engine, the same templates come from
`pgpm init --repo constructive-io/media-engine-boilerplates --moduleName quarterly-review`,
with `--template walkthrough`, `animation` or `document` for the other three.

## Voices and sounds

A script names a persona, never a voice. Whose voice a persona is belongs to
this machine:

```sh
media voice narrator <a voice your speech server has> --new
```

or to a library, which is a repository of voices, sounds and faces:

```sh
media library search                  # what the indexes list
media library add owner/some-voices
media library voices some-voices      # give its voices to the personas here
media library lock                    # media-libraries.json: which libraries, at which commit
```

Commit `media-libraries.json`. On another machine `pnpm libraries` adds the
same libraries at the same commits.

A script that takes sounds from a library (`@include some-bank`) is one `conv`
cannot check alone, since only the engine knows this machine's libraries. In
that package, make `lint` the same as `check`: `media conv talk.conv`.

## What is kept and what is not

Scripts, pages and `media-libraries.json` are committed. Nothing rendered is:
sound and film land in each package's `out/`, which is ignored, and are made
again from the script.
