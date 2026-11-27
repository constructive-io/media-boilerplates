# ____moduleName____

____description____

A library for [Constructive Media](https://github.com/constructive-io/media-engine):
voices to clone, banks of sounds and faces, with one file,
[`media-library.json`](./media-library.json), that says what is here and by
what right. Kept by ____fullName____. Terms: ____license____.

```sh
media library add OWNER/____moduleName____  # or the path to a copy of this folder
media library voices ____moduleName____     # give its voices to the personas on this machine
```

After that a script that names one of its personas, or pulls in one of its
banks with `@include`, renders with what is here.

## What is in it

<!-- voices -->
| Persona | Mood | Whose voice | By what right |
| --- | --- | --- | --- |
| *none yet* | | | |
<!-- /voices -->

`media library clip` writes this table again each time a voice goes in, from
the manifest: leave the two marks where they are. It is what a person reads
before they use a voice.

## Put the first voice in

**1. Record.** [`originals/`](./originals) says how, and has something to read
aloud. Half a minute to a minute of one person, talking the way the voice
should sound, in a quiet room. A phone held a hand away is enough. Recordings
stay in `originals/`, which git passes over.

**2. Put it in.** One command, with whose voice it is and by what right:

```sh
media library clip narrator originals/narrator.wav --by "____fullName____" --kind own --on 2026-01-31
```

It cleans the recording when that helps and does the voice no harm, cuts 15 to
28 seconds where the most talk ends in the quiet after a sentence, writes the
clip to `voices/narrator/neutral.flac` and what was said in it to
`voices/narrator/neutral.txt`, names the voice in `media-library.json` with
its consent, writes the table above, and checks the library. `--by` and
`--kind` are never guessed. For a voice that is not your own, read
[Consent](#consent) first.

**3. Read and listen.** Two things matter more than the rest:

- **The clip ends in the quiet after a whole sentence.** A model that clones
  goes on from where its clip stops. A clip cut in the middle of a word, or a
  breath before the next sentence, is heard at the start of every line said
  with it. Where to cut was chosen by loudness alone, so play the clip:
  `media reference originals/narrator.wav` lists the other places, and
  `--from 41 --to 63` takes one.
- **The words are exactly the sound.** Read the `.txt` against the clip and put
  right any word that was misheard.

**4. Check, and hear it.**

```sh
python3 scripts/check.py                 # needs nothing installed; runs on every push
media library check .                    # the same, and it measures every clip
media library add .
media library voices ____moduleName____
media say --voice narrator "This is the first voice in the library." out/hello.wav
media audition narrator --out out/audition  # a set of lines, and whether the clip bled into them
```

Another mood is another recording: add `--emotion whisper`, and a script asks
for it with `NARRATOR[whisper]: ...`.

### By hand

The same in steps, when you want to choose each one:

```sh
media clean originals/narrator.wav cleaned.wav   # how noisy it is; cleaned only when that is worth doing
media reference originals/narrator.wav           # how long, how loud, and where it could be cut
media reference originals/narrator.wav voices/narrator/neutral.flac --from 3 --to 27 --listen
```

Then name it in `media-library.json`, and in the table above:

```json
"voices": [
  {
    "persona": "narrator",
    "name": "____fullName____",
    "emotion": "neutral",
    "reference": "voices/narrator/neutral.flac",
    "consent": { "by": "____fullName____", "kind": "own", "on": "2026-01-31" }
  }
]
```

## Consent

Every voice says whose it is and by what right it is here. A library with a
voice that does not say is not a library: the check fails.

| `kind` | Means | Also needs |
| --- | --- | --- |
| `own` | the voice of the person who recorded it, named in `by` | |
| `permission` | the person named in `by` said yes to this use | keep what they said, in writing, outside the repository: [CONSENT.md](./CONSENT.md) is something to send them |
| `licensed` | the recording came under a license that allows it | a `note`: which license, and from where |
| `synthetic` | nobody's voice: designed or generated | a `note`: how it was made |

`on` is the day consent was given, written like `2026-01-31`. Do not add a
voice because it would be useful. Add it because its owner said yes, and take
it out the day they say no.

## Sounds and faces

[`banks/`](./banks) holds banks a script pulls in with `@include`,
[`sounds/`](./sounds) the files they play, [`faces/`](./faces) a picture for a
persona. Each folder says how.

## Pin it

A library is used at a commit. On a machine that has added the libraries a
project needs:

```sh
media library lock     # writes media-libraries.json beside the scripts
media library install  # on another machine: the same libraries, at the same commits
```

Tag a commit when the voices in it are ones you would stand behind:
`git tag v0.1.0`, and `"version": "0.1.0"` in the manifest.
