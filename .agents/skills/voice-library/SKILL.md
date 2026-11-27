---
name: voice-library
description: Make and use a voice library for Constructive Media — a repository of clips voices are cloned from, banks of sounds and faces, with consent written down for every voice. Use when asked to "make a voice library", "start a voice repo", "record my voice for cloning", "add a voice to the library", "cut a reference clip", "share voices between machines", "add a sound bank", "pin the voices a project uses", or when a script's persona has no voice and one should come from a repository.
compatibility: Constructive Media (`media`) or pgpm (npm) to start a library; Python 3.9+ for its check; Constructive Media (`media`) to cut clips, hear voices and add the library
metadata:
  author: constructive-io
  version: "0.4.0"
---

# Voice libraries

A `.conv` script names a persona. A **library** says whose voice that is. It is
a folder, most often a git repository, holding:

```
media-library.json           what is here, and for every voice, whose it is
voices/narrator/neutral.flac a clip to clone from: 15 to 28 seconds, one person, one mood
voices/narrator/neutral.txt  the words said in it, exactly
banks/weather.sounds         a bank a script pulls in with @include
sounds/rain.flac             the files banks play
faces/narrator.png           a picture for a persona
```

The engine, [Constructive Media](https://github.com/constructive-io/media-engine),
holds no voices and the format does not change for them. Libraries are where
they live.

## The rule that comes first

**Only add a voice whose owner said yes.** Their own voice, recorded by them;
or a voice they gave permission for; or a recording under a license that
allows it; or a voice that is nobody's. An interview, a talk, a film or a clip
found online is none of these. If you were not told whose voice a recording is
and that they agreed, ask the person you are working for. Never fill in
`consent` yourself.

## Start a library

```sh
media init library my-voices --no-tty
cd my-voices
python3 scripts/check.py
```

The name is the library's: lower case, joined by hyphens. It is made where you
are, as a folder of its own: a library is a repository, not a package of a
workspace. Add `--description "..."`, `--fullName "..."` and `--license "..."`
to answer the other questions; with `--no-tty` the ones left out take their
defaults.

Without the engine, the same comes from pgpm:

```sh
npm install -g pgpm
pgpm init --repo constructive-io/media-engine-boilerplates --template library --moduleName my-voices --no-tty
```

## Add a voice

**1. Get a recording**, from the person, of forty seconds to a minute of talk
in a quiet room. The library's `originals/README.md` says how to record and
has something to read aloud. Recordings stay in `originals/`, which is not
committed.

**2. Put it in**, saying whose voice it is and by what right:

```sh
media reference originals/narrator.wav      # how long, how loud, what is wrong with it, where it could be cut
media library clip narrator originals/narrator.wav --by "Ada Marsh" --kind own --on 2026-01-31
```

`media library clip` cleans the recording when that helps, cuts 15 to 28
seconds where the most talk ends in the quiet after a sentence (or where
`--from` and `--to` say), writes `voices/narrator/neutral.flac` and its words
beside it, names the voice in `media-library.json` with its consent, writes
the table in the README and checks the library. `--emotion whisper` is another
mood of the same persona. `--said "…"` gives the words; without it a
transcriber writes them.

`--by` and `--kind` come from the person you are working for, every time. For
`permission`, the library's `CONSENT.md` is what to send the voice's owner;
their answer is kept outside the repository.

**3. Read the words against the sound.** `voices/narrator/neutral.txt` is given
to the speech model along with the clip: a misheard word there is a misspoken
word in everything cloned from it. If you cannot hear the clip yourself, say
so and leave the reading to a person.

**4. Check it and hear it:**

```sh
python3 scripts/check.py
media library check .
media library add .
media library voices my-voices
media say --voice narrator "This is the first voice in the library." out/hello.wav
media audition narrator --out out/audition
```

`media audition` says a set of lines and reports any that came back with the
clip's own words in them. When a voice fails it, or sounds wrong, the skill
`build-a-voice` in this repository goes through why.

### What a voice is, in the manifest

`media library clip` writes this. By hand it is:

```json
{
  "persona": "narrator",
  "name": "Ada Marsh",
  "emotion": "neutral",
  "reference": "voices/narrator/neutral.flac",
  "consent": { "by": "Ada Marsh", "kind": "own", "on": "2026-01-31" }
}
```

| Field | Is |
| --- | --- |
| `persona` | who a script's character speaks as: lower case, hyphens |
| `emotion` | the mood this clip is for. `neutral` unless said. One clip for each mood |
| `reference` | the clip, by its path from the library's folder |
| `said` | the clip's words, when there is no `.txt` beside it |
| `profile` | instead of a clip: the name a speech server knows one of its own voices by |
| `seed` | a whole number that fixes the take |
| `consent.by` | whose voice it is |
| `consent.kind` | `own`, `permission`, `licensed` or `synthetic` |
| `consent.note` | needed for `licensed` (which license, from where) and `synthetic` (how it was made) |
| `consent.on` | the day it was given, as `2026-01-31` |

## Sounds and faces

A bank is `banks/NAME.sounds`, holding `@sounds` and `@tracks` as a script
writes them. Each `file:` is a path from the library's `sounds/` folder, and
`level:` is in decibels, from -80 to 0:

```
@sounds
RAIN: { file: rain.flac, loop: true, track: ambience, level: -8 }
```

A face is a square picture named under `"faces"`: `{ "narrator": "faces/narrator.png" }`.

## Use a library somewhere else

```sh
media library add owner/my-voices  # GitHub, any git address, or a folder
media library list
media library voices my-voices     # voices already kept on this machine are left alone; --replace to take the library's
media library update my-voices     # move to its newest commit
media library lock                 # write media-libraries.json beside the scripts
media library install              # another machine: the same libraries at the same commits
```

A script's own bank beside it wins over a library's bank of the same name.

## Before you say it is done

- `python3 scripts/check.py` says `ok`, and `media library check .` does where the
  engine is installed. Pass on any `note:` lines.
- Every voice has consent that a person gave you, not that you inferred.
- Nothing from `originals/` but its README is committed, and no clip is longer than half a minute.
- Say what was checked. The check reads the manifest and measures the clips;
  it does not tell you a voice sounds like its owner. Only a listener does.

## Related skills

| Skill | Where | For |
| --- | --- | --- |
| `build-a-voice` | here | from a recording to a voice that passes its audition, and what to do when one does not |
| `constructive-media` | [media-engine](https://github.com/constructive-io/media-engine) | the engine: rendering scripts, voices, filming |
| `conv` | [conversation-format](https://github.com/constructive-io/conversation-format) | writing and checking `.conv` scripts |
| `media-workspace`, `narrated-video`, `narrated-document` | here | the projects that speak with a library's voices |
