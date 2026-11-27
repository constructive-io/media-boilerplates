# ____moduleName____

____title____: a tour of a screen, made from a script.
[`tour.conv`](./tour.conv) says the words and where the pointer goes,
[`index.html`](./index.html) holds the screens, and
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
| `pnpm build` | films the tour following that recording |
| `pnpm preview` | opens the tour in your browser with the sound, to scrub through |
| `open index.html` | the tour alone, stepped through with the arrow keys |

This is a package of a media workspace: at the top of the workspace, `pnpm build`
makes every package and `pnpm --filter ____moduleName____ build` this one.

The voice can come from a library instead: `media library add owner/some-voices`,
then `media library voices some-voices`. See
[voice-boilerplates](https://github.com/constructive-io/voice-boilerplates).

## How a tour works

A screen is an element with `data-slide="name"`. A part of it worth pointing at
has `data-step="1"`, `data-step="2"`. When the script says `[slide log step:2]`
the pointer travels to the middle of that part, and the part is ringed while it
is spoken of.

```
[slide log]
NARRATOR: Every boat that comes in gets a line here.
[slide log step:1]
NARRATOR: The newest is at the top.
```

The mark goes on the line **before** the words it belongs with. Other marks:
`[speakers captions]` draws the words as they are said (add `lower-third`,
`waveform` or `faces`), `[pause 0.5]` is half a second of quiet, and
`[video DEMO]` plays a clip full screen, with `DEMO: { file: demo.mp4 }`
declared under `@sounds`.

## Use your own screens

The screens here are a made-up application drawn in HTML, so the template
carries no pictures. For a real one, take a screenshot of each screen at
1920 by 1080, put them in `screens/`, and mark where the pointer goes as a
place on the picture, in hundredths of its width and height:

```html
<section data-slide="log" class="screen">
  <img src="screens/log.png" alt="">
  <i class="spot" data-step="1" data-point="31%,24%"></i>
  <i class="spot" data-step="2" data-point="78%,4%"></i>
</section>
```

A live page works too: build the screen in HTML as this one is, and put
`data-step` on the real buttons and fields.

Colours and type are the variables at the top of the page's `<style>`.
`--stage-accent` is the pointer.

## Before you call it done

- `pnpm check` says `ok`.
- `pnpm build` ends without `need a listen` and without `to look at`. A screen the
  script names and the page does not have is reported there.
- Look at it. Pull a frame out with
  `ffmpeg -ss 12 -i out/____moduleName____.mp4 -frames:v 1 frame.png` and see that the
  pointer is on what is being spoken of.

Nothing under `out/` is committed.
