---
name: build-a-voice
description: Build a cloned voice for Constructive Media from a recording of a person, and make it a good one — recording, cleaning, choosing where to cut, the clip's words, moods, auditioning, and mending a voice that says words it was not given, rushes, hisses or sounds like somebody else. Use when asked to "make a voice from this recording", "clone my voice", "train a voice", "the voice says extra words", "the voice sounds wrong / noisy / too fast", "add a whisper / angry version of the voice", "which part of the recording should I use", or when `media audition` fails.
compatibility: Constructive Media (`media`) with ffmpeg; a speech server, or on a Mac `pip install mlx-audio` and CONSTRUCTIVE_MEDIA_ADAPTER_SPEECH=mlx; a transcriber for --listen and auditions
metadata:
  author: constructive-io
  version: "0.1.1"
---

# Build a voice

A voice here is not trained. It is **cloned at the moment of speaking** from
one short clip and the words said in it: the speech model hears the clip,
reads its words, and goes on in the same voice with the line it was given. So
the whole craft is the clip. A good one takes ten minutes; a bad one costs
takes on every line the voice ever says.

Where the voice is kept (a library, its manifest, consent) is the skill
`voice-library`, beside this one. **A voice is only built for its owner, or
with their yes.** Ask whose voice a recording is before you touch it.

## The short way

```sh
media reference originals/ada.wav        # what is wrong with it, and where it could be cut
media library clip ada originals/ada.wav --by "Ada Marsh" --kind own --on 2026-01-31
media library add . && media library voices my-voices
media audition ada --out out/audition    # eight lines, one take each, listened back to
```

Eight of eight, or seven, and a person who has listened and says it is them:
done. Anything less, read on.

## What makes a clip good

| | Wants to be | Because |
| --- | --- | --- |
| Length | 15 to 28 seconds | under 12 there is too little voice to copy; past 30 most models stop listening |
| Who | one person | a second voice, even a laugh off to the side, is averaged in |
| Mood | one, and the one you want | the model copies the mood with the voice. A clip that builds to a shout shouts |
| Room | quiet and soft | hiss, hum and echo are copied as faithfully as the person |
| Pauses | none over a second or so | a long pause is copied as a long pause, in every line |
| The end | the quiet after a whole, plain sentence | **the model goes on from where the clip stops** |
| The words | exactly what is heard | they are the model's map of the clip |

The last two are where nearly every bad voice comes from.

## Step by step

**1. The recording.** Forty seconds to a minute, so there is somewhere to
choose from. The library's `originals/README.md` has how to record and a
passage to read. If you are given a long recording (an hour of somebody
talking), it is fine: step 3 finds the places.

**2. Is it clean?**

```sh
media clean originals/ada.wav               # measures; writes nothing
media clean originals/ada.wav cleaned.wav   # does what is worth doing, and says what it cost the voice
```

Rumble and mains hum are taken off with filters, which no voice minds. Hiss
needs a denoiser, which takes a little of the voice too: the command says how
much, and leaves the recording alone when cleaning would cost more than it
gains. A recording with music or other people under it is not mended by any of
this. Ask for another.

**3. Where to cut.**

```sh
media reference originals/ada.wav
#   where it could be cut, the likeliest first:
#     --from 12.9 --to 37.8    24.9 seconds, 24 of them talk, its longest pause 0.5, ending in 1.0 of quiet
```

Each place begins where a phrase begins and ends in a quiet long enough to
follow a sentence. They are found **by loudness alone**. The engine cannot
tell that the stretch is one person, or one mood, or that the quiet is the end
of a sentence and not a thought held in the middle of one. A person listens,
or you read the transcript: if the heard words stop on "and the", choose
another.

**4. Cut it, with its words.**

```sh
media library clip ada originals/ada.wav --by "Ada Marsh" --kind own --from 12.9 --to 37.8
# or, outside a library:
media reference originals/ada.wav voices/ada/neutral.flac --from 12.9 --to 37.8 --listen
```

Open `voices/ada/neutral.txt` and read it against the clip. Put right what was
misheard: names, numbers, anything said twice. Do not tidy it. If she said
"um, the the lantern", the words are "um, the the lantern". `--tighten`
shortens pauses over 0.8 seconds when the speaker is a slow one.

**5. Audition.**

```sh
media audition ada --out out/audition
media audition ada --lines my-lines.txt     # lines like the ones the voice will really say
```

Each line is said once, with no second try, and listened back to. The report
says which came out as written and whether any began with the end of the clip.
Then somebody plays two or three of the takes: the check hears words, not
likeness.

## When a voice is wrong

| What you hear | Why | Do |
| --- | --- | --- |
| A line starts with words that are not in the script | the clip ends mid-sentence, or its `.txt` is missing the last words of the sound | move `--to` back to the quiet after the sentence before; make the `.txt` exactly the sound |
| The same stray word at the start of many lines | that word is the next thing said after the clip stops | cut 0.2 to 0.5 seconds earlier, or choose another place |
| Lines come out rushed, or run together | the clip is fast, or was tightened too far | choose a slower stretch; do not `--tighten` under 0.5 |
| Long gaps in the middle of lines | a long pause in the clip | `--tighten`, or another stretch |
| Hiss, hum or a room on every line | it is in the clip | `media clean`, or record again somewhere soft and quiet |
| It sounds like somebody, but not them | too short, or two people, or a put-on voice in the clip | a longer stretch (20 seconds and up) of them talking plainly |
| Every line sounds excited, or sad | the clip's mood | a clip in the mood you want. Make the other a second mood |
| Fine on short lines, wanders on long ones | models drift over long lines | write shorter lines in the script; nothing is wrong with the voice |
| Numbers and names said wrong | the script, not the voice | write them as they are said: "nineteen eighty-four", "Shiv-awn" |
| One line in ten is bad, differently each time | chance | the engine listens to every line of a render and takes it again; a `seed` in the manifest fixes a take you liked |

Change one thing, audition again, and compare the count. A voice that passes
eight of eight on one stretch and five on another is telling you about the
stretches.

## Moods

Another mood is another clip of the same person, recorded in that mood:

```sh
media library clip ada originals/ada-quiet.wav --by "Ada Marsh" --kind own --emotion whisper
media audition ada --emotion whisper
```

A script asks for it with `ADA[whisper]: ...`. Do not try to get a whisper out
of a neutral clip with stage directions; record one. Three moods a person
really uses are worth more than ten they acted.

## What you cannot tell them

Say plainly which of these happened: the audition passed (words were right);
somebody listened (it sounds like them). The first without the second is a
voice nobody has heard. And say whose voice it is and that they agreed. If
you do not know, the voice is not finished.

## Related skills

| Skill | Where | For |
| --- | --- | --- |
| `voice-library` | here | the library a voice is kept in: manifest, consent, banks, faces, pinning |
| `constructive-media` | [media-engine](https://github.com/constructive-io/media-engine) | the engine: rendering scripts, filming, every command above in full ([docs/VOICES.md](https://github.com/constructive-io/media-engine/blob/main/docs/VOICES.md)) |
| `conv` | [conversation-format](https://github.com/constructive-io/conversation-format) | the scripts a voice speaks: characters, moods, pauses, sounds |
