# ____moduleName____

____title____: a talk with slides, made from a script.
[`talk.conv`](./talk.conv) says the words and when the slides change,
[`index.html`](./index.html) holds the slides, and
[Constructive Media](https://github.com/constructive-io/constructive-media)
says the one and films the other.

```sh
media voice narrator <a voice your speech server has> --new  # once: whose voice `narrator` is
pnpm build                                                  # out/____moduleName____.mp4
```

| Command | Does |
| --- | --- |
| `pnpm lint` | reads the script and says what is wrong with it. Needs only Node |
| `pnpm check` | the same with the engine, which also knows this machine's voices and libraries |
| `pnpm say` | says the script: `out/____moduleName____.flac`, and a manifest of when everything fell |
| `pnpm build` | says it, then films the deck following that recording |
| `pnpm preview` | opens the deck in your browser with the sound, to scrub through |
| `open index.html` | the deck alone, stepped through with the arrow keys |

This is a package of a media workspace: at the top of the workspace, `pnpm build`
makes every package and `pnpm --filter ____moduleName____ build` this one.

The voice can come from a library instead: `media library add owner/some-voices`,
then `media library voices some-voices`. See
[voice-boilerplates](https://github.com/constructive-io/voice-boilerplates).

## Change the words

Everything after `---` in `talk.conv` is the talk. A line is `NARRATOR:` and
what is said. A mark in square brackets goes on the line **before** the words
it belongs with:

| Mark | Does |
| --- | --- |
| `[slide how]` | shows the slide the page calls `how` |
| `[slide how step:2]` | reveals its steps up to 2 |
| `[speakers lower-third captions]` | what is drawn of whoever speaks, from here on: any of `faces`, `lower-third`, `waveform`, `captions` |
| `[speakers off]` | draws nothing of them |
| `[pause 0.5]` | half a second of quiet |
| `[video DEMO]` | plays the clip `DEMO` full screen, with its sound |

A second speaker is a second line under `@characters`, with a persona of its
own. A clip is declared under `@sounds`, before the `---`:

```
@sounds
DEMO: { file: demo.mp4 }
```

After changing one line, `media say talk.conv out/____moduleName____.flac --only 4`
says only line 4 again and keeps the rest.

## Change the slides

A slide is any element with `data-slide="name"`. Inside it, anything with
`data-step="1"`, `data-step="2"` waits until the script reaches that step.

```html
<section data-slide="pricing">
  <h2>Two plans</h2>
  <p data-step="1">One for a keeper</p>
  <p data-step="2">One for a harbour</p>
</section>
```

The frame is 1920 by 1080 and scaled to fit, so sizes in `px` and `em` come out
the same in the film as on your screen. Colours and type are the variables at
the top of the page's `<style>`. The player adds the classes `is-current` to
the slide on screen, `is-shown` to a step once reached and `is-now` to the one
being spoken of, for rules of your own.

A step for every spoken line reads best: put `[slide pricing step:2]` before
the line that speaks of it, so that what is being said is what just arrived.

## Make things move

`data-enter` says how a thing arrives, on a step or on anything else in a
slide:

```html
<h2 data-enter="wipe">Two plans</h2>
<p data-step="1" data-enter="left">One for a keeper</p>
<p data-step="2" data-enter="left" style="--stage-delay: 0.3s">One for a harbour</p>
<line data-step="2" data-enter="draw" x1="0" y1="0" x2="400" y2="0"/>
```

| `data-enter` | It |
| --- | --- |
| `rise` | comes up into place. What a step does when nothing is said |
| `fade` | only fades in |
| `left`, `right` | slides in from that side |
| `grow`, `pop` | grows from its middle; `pop` overshoots a little |
| `wipe` | is uncovered from left to right |
| `draw` | is drawn along its length: an SVG line, path or shape |

`--stage-delay` holds a thing back, so that several arrive one after another,
and `--stage-time` is how long it takes. A thing with no `data-step` arrives
when its slide does.

What a page draws for itself, a chart filling or a clock running down, is
drawn in the `<script>` at the bottom of the page from
`window.stage.since('moves', 2)`: the seconds since the script reached that
step, and `null` before it. Draw from that and nothing else, never from a
timer of the page's own, and the film, the preview and a second filming all
come out the same.

With two speakers, `body[data-stage-speaker="grace"] { --stage-accent: … }`
gives each a colour while they talk. The engine names whoever speaks first at
the bottom left of the frame, so keep that corner clear on a slide where
somebody new begins.

Everything a page can do is in
[the engine's guide to the stage](https://github.com/constructive-io/constructive-media/blob/main/docs/STAGE.md).

## Before you call it done

- `pnpm check` says `ok`.
- `pnpm build` ends without `need a listen` and without `to look at`. A slide the
  script names and the page does not have is reported there.
- Look at it. Pull a frame out with
  `ffmpeg -ss 12 -i out/____moduleName____.mp4 -frames:v 1 frame.png`, or watch it.

Nothing under `out/` is committed.
