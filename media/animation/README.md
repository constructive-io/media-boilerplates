# ____moduleName____

____title____: a short film whose pictures are a page, made from a script.
[`scene.conv`](./scene.conv) says the words and which scene it is,
[`index.html`](./index.html) draws every picture, and
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
| `pnpm build` | films the page following that recording |
| `pnpm preview` | opens the page in your browser with the sound, to scrub through |
| `pnpm stills` | after `pnpm say`: a picture of every beat in `out/stills/`, in seconds, to look at before filming |

This is a package of a media workspace: at the top of the workspace, `pnpm build`
makes every package and `pnpm --filter ____moduleName____ build` this one.

The voice can come from a library instead: `media library add owner/some-voices`,
then `media library voices some-voices`. See
[voice-boilerplates](https://github.com/constructive-io/voice-boilerplates).

## How the page knows where the script is

The page has no slides. The script still says `[slide lamp]`, and the player
hands that to the page three ways:

| The page gets | When | For |
| --- | --- | --- |
| `<body data-stage-slide="lamp" data-stage-step="0">` | as the script reaches the mark | rules: `body[data-stage-slide="lamp"] #sky { fill: … }`, with a `transition` |
| a `stage:change` event, with `{ slide, step, line, clip, show }` | on every change | anything rules cannot do |
| `window.stage.t`, `window.stage.level()`, `window.stage.timeline` | every frame | drawing: seconds into the recording, how loud the voice is from 0 to 1, and when every mark falls |

The loudness is also the CSS variable `--stage-level`, so a rule can breathe
with the voice: `transform: scale(calc(1 + var(--stage-level) * 0.2))`.

**Draw from `t` alone, never from a count of frames or from what was drawn
before.** The film is the page recorded as it plays, so it has to come out the
same every time, and a preview has to scrub both ways.

The picture here is an SVG. A `<canvas>`, WebGL, or a library that draws from a
time you give it all work the same way: read `window.stage.t` in
`requestAnimationFrame`.

## Change it

- **The words and the scenes**: `scene.conv`. A mark goes on the line before the
  words it belongs with. `[speakers captions]` draws the words as they are said;
  `[speakers off]` draws nothing over your picture.
- **What a scene looks like**: the rules under `body[data-stage-slide="…"]` in the
  page's `<style>`.
- **What moves**: the `draw` function at the bottom of the page.

Sound under the voice is declared in the script, before the `---`, and played by
a mark. The file sits beside the script:

```
@sounds
SEA: { file: sea.flac, loop: true, track: ambience, level: -18 }
---
[SEA]
```

## Before you call it done

- `pnpm check` says `ok`.
- `pnpm build` ends without `need a listen`.
- Look at it. Pull frames out with
  `ffmpeg -ss 6 -i out/____moduleName____.mp4 -frames:v 1 frame.png`: one from each scene.

Nothing under `out/` is committed.
