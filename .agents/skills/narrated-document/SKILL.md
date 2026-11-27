---
name: narrated-document
description: Make a document that is also read aloud with Constructive Media — one HTML page that prints as a PDF and is filmed scrolling to wherever a voice is. Use when asked to "narrate this document", "make a video of this report", "read this doc aloud", "turn this write-up into a video", "make a narrated report", "make a PDF and a video of the same thing", "record a walkthrough of this document", or when a report, memo or write-up should reach people who would rather listen than read.
compatibility: Constructive Media (`media`) or pgpm (npm) to start from the template; Node and pnpm to lint; the engine with Chrome or Chromium to print, and a speech server to say and film; ffmpeg to pull frames out
metadata:
  author: constructive-io
  version: "0.2.0"
---

# Narrated documents

One page of HTML is the document. A script beside it is what a voice says about
it. [Constructive Media](https://github.com/constructive-io/media-engine)
makes two things from them:

```
index.html      the document           ->  media print  ->  a PDF
reading.conv    what the voice says    ->  media say, media film  ->  a video of the page being read
```

In the video the page scrolls to the section being spoken of, the others dim,
and the part named is lit up. Nothing is recorded by hand.

## Start

A document is a package of a pnpm workspace, started at the top of one:

```sh
media init workspace harbour-papers --bare    # once, when there is no workspace yet
cd harbour-papers && pnpm install
media init document my-report --title "How the log is kept" --fullName "Ada Marsh" --role "Keeper"
cd packages/my-report
pnpm pdf      # works at once, with no voice
```

Without the engine, the same files come from
`pgpm init --repo constructive-io/media-engine-boilerplates --template document --moduleName my-report`.
The workspace itself is the `media-workspace` skill's subject.

## Write the document first

It should read on its own: the PDF has no voice.

```html
<body data-stage="document">
<article>
  <section data-slide="costs">
    <h2>What it costs</h2>
    <p data-step="1">Oil, forty litres a month.</p>
    <p data-step="2">Wicks, two a year.</p>
  </section>
</article>
</body>
```

- A **section** is an element with `data-slide="name"`. Name every section the
  voice will stop at.
- A **part** worth pointing at has `data-step="1"`, `data-step="2"`, counted
  within its section: a paragraph, a row of a table, an item of a list.
- The look is the page's `<style>`: variables for colour and type, and an
  `@media print` part for paper, with the page size in `@page`.

Turning an existing document into one of these is mostly adding those two
attributes. Keep its words.

## Then write the reading

```
@characters
NARRATOR: { persona: narrator, name: Ada Marsh, title: Keeper }
---
[speakers lower-third captions]
[slide title]
NARRATOR: This is a short report on how the log is kept.
[speakers captions]
[slide costs]
NARRATOR: Most of the cost is oil.
[slide costs step:1]
NARRATOR: Forty litres of it a month.
```

| Mark | Does |
| --- | --- |
| `[slide NAME]` | scrolls to the section `NAME` and dims the others |
| `[slide NAME step:N]` | lights up part N of it and brings it to the middle |
| `[speakers …]` | what is drawn of whoever speaks from here on: any of `faces`, `lower-third`, `waveform`, `captions`; `off` |
| `[pause 0.5]` | half a second of quiet |

**A mark goes on the line before the words it belongs with.**

Do not read the page out. Say what each section is for and what a listener
should take from it, in sentences made for the ear, and let the page hold the
figures. A good reading is a third of the length of the page. When word-for-word
is what was asked for, put one paragraph on a line and a `step` on each.

## Make it

```sh
pnpm check                                                 # media conv reading.conv: needs no voice
pnpm pdf                                                   # media print . out/my-report.pdf
media voice narrator <a voice the speech server has> --new  # once, if `narrator` has no voice
pnpm build                                                 # media say, then media film: out/my-report.mp4
pnpm preview                                               # the page with the sound, in a browser
```

After changing a few lines of the reading, say only those again:

```sh
media say reading.conv out/my-report.flac --only 4,7
media film out/my-report.flac out/my-report.mp4 --page .
```

## Before you say it is done

1. `pnpm check` says `ok`.
2. Open the PDF. Look at where the pages break: a heading alone at the foot of a
   page wants `break-after: avoid`, a table cut in two wants `break-inside: avoid`.
3. `pnpm build` ended with no `need a listen:` line and no `to look at`. The second is
   where a section the script names and the page lacks is reported.
4. **Look at frames**, one from every section, at times taken from
   `out/my-report.manifest.json`:

   ```sh
   ffmpeg -ss 12.5 -i out/my-report.mp4 -frames:v 1 frame.png
   ```

   The section on screen is the one being spoken of, the lit part is the one
   named, and the captions can be read.
5. Say what was checked and what was not. The engine listened to every line; no
   person has heard it until one has.

## What goes wrong

| What you see | Do |
| --- | --- |
| `'narrator' has no voice to speak in` | `media voice narrator <a voice> --new`, or add a library |
| `no Chrome or Chromium was found` | install one, or name it in `CONSTRUCTIVE_MEDIA_MODEL_BROWSER` |
| `the page has no slide called …` | the script and the page disagree on a section's name |
| the page does not move in the film | the body lacks `data-stage="document"`, or the sections lack `data-slide` |
| the last section cannot reach the top | that is the end of the page: the player leaves room below it unless the page's own `padding` took it away |
| the PDF is dark, or has captions in it | the page overrides the player's print rules: keep its colours out of `@media print` |

## Related

- The workspace a document is a package of: `npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill media-workspace`
- Decks, walkthroughs and animations: `npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill narrated-video`
- The engine's own skill: `npx skills add https://github.com/constructive-io/media-engine --skill constructive-media`
- The format's skill, for writing scripts: `npx skills add https://github.com/constructive-io/conversation-format --skill conv`
- Voices: [voice-library](../voice-library/SKILL.md), and [build-a-voice](../build-a-voice/SKILL.md) for making one from a recording
