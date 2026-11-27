---
name: narrated-video
description: Make a narrated video from a script and a page with Constructive Media — a deck that presents itself, a walkthrough of an application with a pointer, or an animation drawn by the page. Use when asked to "make a narrated deck", "turn this deck into a video", "make a video of this talk", "make a walkthrough video", "make a product tour", "make an explainer video", "animate this to a voiceover", "add narration to these slides", or when a `.conv` script has `[slide …]` marks and needs a page to follow it.
compatibility: Constructive Media (`media`) or pgpm (npm) to start from a template; Node and pnpm to lint; the engine with a speech server and Chrome or Chromium to say and film; ffmpeg to pull frames out
metadata:
  author: constructive-io
  version: "0.3.0"
---

# Narrated video

A video here is never recorded by hand. Two files make it:

```
talk.conv     the words, who says them, and when the screen changes
index.html    what is on the screen
```

[Constructive Media](https://github.com/constructive-io/media-engine) says
the script (`media say`), which writes the sound and a manifest of when every line
and every mark fell. Then it films the page following that manifest (`media film`).
To change the video, change a file and make it again.

## Pick a template

| The request | Template | Script |
| --- | --- | --- |
| a talk, a pitch, a lesson with slides | `deck` (the folder is `module`) | `talk.conv` |
| a tour of an application's screens, a how-to | `walkthrough` | `tour.conv` |
| pictures that move with the voice, an explainer with one scene | `animation` | `scene.conv` |
| a document read aloud, also wanted as a PDF | `document`: see the `narrated-document` skill | `reading.conv` |

Each is a package of a pnpm workspace, started at the top of one:

```sh
media init workspace harbour-talks --bare     # once, when there is no workspace yet
cd harbour-talks && pnpm install
media init deck my-talk --title "What we learned" --fullName "Ada Marsh" --role "Keeper"
cd packages/my-talk
```

The name is the folder and the name of the film. `media init walkthrough NAME` and
`media init animation NAME` are the other two. Asked from a keyboard, `media init`
asks for whatever was not given; `--no-tty` takes the defaults. Without the
engine, the same files come from
`pgpm init --repo constructive-io/media-engine-boilerplates --template walkthrough --moduleName NAME`
(leave `--template` out for a deck). The workspace itself is the
`media-workspace` skill's subject.

## Write the script

Everything before `---` declares; everything after is said, in order.

```
@characters
NARRATOR: { persona: narrator, name: Ada Marsh, title: Keeper }
---
[speakers lower-third captions]
[slide title]
NARRATOR: Hello.
[slide how step:1]
NARRATOR: A script says the words.
```

| Mark | Does |
| --- | --- |
| `[slide NAME]` | shows the slide, screen or scene the page calls `NAME` |
| `[slide NAME step:N]` | reveals that slide's steps up to N; in a walkthrough, sends the pointer to step N |
| `[speakers …]` | what is drawn of whoever speaks from here on: any of `faces`, `lower-third`, `waveform`, `captions`; `all`; `off` |
| `[video CLIP]` | plays a clip full screen with its sound; `CLIP: { file: demo.mp4 }` is declared under `@sounds` |
| `[pause 0.5]` | half a second of quiet |

**A mark goes on the line before the words it belongs with.** It lands at the
moment those words start.

**Sounds** come from a bank: one of the script's own under `@sounds`, or a
library's, pulled in by name at the top of the script. Each bank is its own
line (`@include foley` does not bring `interface` with it):

```conv
@include foley
@include interface
---
[slide door]
[DOOR]
[pause 1.5]
NARRATOR: Somebody is home.
```

A sound and then a pause is a beat with nobody talking: the sound plays in the
quiet, and a mark before them lands when the quiet starts, so the page can move
while the sound is heard. A script that includes a library's bank is checked
with `pnpm check` (the engine knows the libraries on this machine); `pnpm lint`
alone cannot find it.

Write for the ear. One thought to a line, a line to a step. Spell out what a
voice would stumble on: "version two", not "v2". A second speaker is a second
line under `@characters` with a persona of its own.

`pnpm check` (which is `media conv talk.conv`) reads the script and reports every
problem at once. It needs no voice, so run it after every edit. `pnpm lint` is
the same with `conv` alone, which is what CI has.

## Make the page

A slide is any element with `data-slide="NAME"`. A step inside it has
`data-step="1"`, `data-step="2"`. The page loads two files the engine hands it:

```html
<link rel="stylesheet" href="stage.css">
<script src="stage.js" defer></script>
<body data-stage="deck">
  <section data-slide="how">
    <h2>Three things make it</h2>
    <li data-step="1">A script says the words</li>
  </section>
</body>
```

| `<body data-stage="…">` | Is |
| --- | --- |
| `deck` | one slide at a time in a frame of 1920 by 1080 |
| `walkthrough` | a deck with a pointer that goes to the step being spoken of, or to its `data-point="x%,y%"` |
| `plain` | no slides: the page draws its own picture |
| `document` | one page that scrolls to where the voice is |

The player adds `is-current` to the slide on screen, `is-shown` to a step once
reached and `is-now` to the one being spoken of. Its own rules give way to any
rule the page writes. Colours and type are variables: `--stage-bg`,
`--stage-ink`, `--stage-dim`, `--stage-accent`, `--stage-font`.

**Make it move.** A deck that only swaps slides is a slideshow. Three things
make it a film, and the `deck` template shows all three:

1. **A step for every spoken line.** Put `[slide how step:2]` before the line
   that speaks of it. A slide that sits still under four lines has three steps
   missing.
2. **`data-enter` on what arrives**: `rise` (when nothing is said), `fade`,
   `left`, `right`, `grow`, `pop`, `wipe`, or `draw` for an SVG line or shape.
   `style="--stage-delay: 0.3s"` holds one back so several arrive in turn;
   `--stage-time` is how long it takes. With no `data-step` it arrives with
   its slide.
3. **What the page draws for itself is drawn from the script's clock**, never
   from a timer or a count of frames:

```js
(function draw() {
  var stage = window.stage;
  if (stage) {
    var since = stage.since('pricing', 2);   // seconds since `[slide pricing step:2]`, or null before it
    var ends = stage.when('close');          // when the script reaches a mark, or null
    var loud = stage.level();                // the voice, from 0 to 1
    // set attributes from those, and from nothing that was drawn before
  }
  requestAnimationFrame(draw);
})();
```

`body[data-stage-speaker="grace"]` is whoever spoke last, for a colour each.
The engine names whoever speaks first at the bottom left of the frame: keep
that corner clear on a slide where somebody new begins.

The scene's name is also on the body, as `data-stage-slide="NAME"`, for rules
with a `transition`, and every change is a `stage:change` event on `document`.

An existing deck made some other way can be filmed too, if each of its slides
can carry `data-slide` and it loads the two files. Do not rebuild a deck that
only needs marking.

## Say it and film it

```sh
media voice narrator <a voice the speech server has> --new  # once, if `narrator` has no voice
pnpm build                                                 # media say, then media film: out/my-talk.mp4
pnpm preview                                               # the page with the sound, in a browser, to scrub
pnpm stills                                                # after `pnpm say`: a picture of every beat, in out/stills/
```

Look before you film. `media still` draws the page at any moment of the
recording in a few seconds, where a film takes as long as the sound runs:
`media still out/my-talk.flac out/stills --page . --at how:2 --at 48.5` for
chosen moments (a slide, a slide and step, or seconds), `--sheet` for all of
them on one page.

`media voices` lists who has a voice. A voice can come from a library:
`media library add owner/some-voices`, then `media library voices some-voices`.

After changing a few lines, say only those again and keep the rest:

```sh
media say talk.conv out/my-talk.flac --only 4,7
media film out/my-talk.flac out/my-talk.mp4 --page .
```

## Before you say it is done

1. `pnpm check` says `ok`.
2. `pnpm build` ended with no `need a listen:` line. A line listed there did not pass
   the listening check: say it again with `--only`, or reword it.
3. `pnpm build` ended with no `to look at`. That is where a slide the script names and
   the page lacks is reported.
4. **Look at every beat.** `pnpm stills`, and read the sheets in `out/stills/`.
   Check that the slide is the one being spoken of, that nothing runs off the
   frame, that the captions do not cover what matters, and in a walkthrough that
   the pointer is on the thing named.
5. Say what was checked and what was not. The engine listened to every line; no
   person has heard it until one has.

## What goes wrong

| What you see | Do |
| --- | --- |
| `'narrator' has no voice to speak in` | `media voice narrator <a voice> --new`, or add a library |
| `no Chrome or Chromium was found` | install one, or name it in `CONSTRUCTIVE_MEDIA_MODEL_BROWSER` |
| `the page has no slide called …` | the script and the page disagree on a name: fix whichever is wrong |
| a step shows before the script reaches it | a rule of the page's own sets its `opacity`; the player's rules give way to the page's. Scope yours to `.is-shown` |
| the pointer sits in a corner | the step is `display: none` or has no size: give it a `data-point="x%,y%"` |
| a caption covers the content | move the content up, or `[speakers off]` for that slide |
| the film differs from one build to the next | something on the page keeps its own clock: draw from `window.stage.t` |

## Related

- The workspace these are packages of: `npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill media-workspace`
- A document read aloud: `npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill narrated-document`
- The engine's own skill: `npx skills add https://github.com/constructive-io/media-engine --skill constructive-media`
- The format's skill, for writing scripts: `npx skills add https://github.com/constructive-io/conversation-format --skill conv`
- Voices: [voice-library](../voice-library/SKILL.md) for a library of them, and
  [build-a-voice](../build-a-voice/SKILL.md) for making one from a recording
