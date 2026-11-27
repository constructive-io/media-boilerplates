# ____moduleName____

____title____: a document that is read aloud.
[`index.html`](./index.html) is the document, [`reading.conv`](./reading.conv)
is what the voice says about it, and
[Constructive Media](https://github.com/constructive-io/constructive-media)
makes two things from them: a PDF, and a video of the document being read,
scrolling to wherever the voice is.

```sh
pnpm pdf                                                    # out/____moduleName____.pdf
media voice narrator <a voice your speech server has> --new  # once: whose voice `narrator` is
pnpm build                                                  # out/____moduleName____.mp4
```

| Command | Does |
| --- | --- |
| `pnpm pdf` | prints the document: `out/____moduleName____.pdf`. Needs no voice |
| `pnpm lint` | reads the script and says what is wrong with it. Needs only Node |
| `pnpm check` | the same with the engine, which also knows this machine's voices and libraries |
| `pnpm say` | says the script: `out/____moduleName____.flac`, and a manifest of when everything fell |
| `pnpm build` | films the document following that recording |
| `pnpm preview` | opens the document in your browser with the sound, to scrub through |
| `open index.html` | the document alone |

This is a package of a media workspace: at the top of the workspace, `pnpm build`
makes every package and `pnpm --filter ____moduleName____ build` this one.

The voice can come from a library instead: `media library add owner/some-voices`,
then `media library voices some-voices`. See
[voice-boilerplates](https://github.com/constructive-io/voice-boilerplates).

## Write the document

It is one page of HTML. A section is an element with `data-slide="name"`. A
part of a section worth pointing at, such as a row, a paragraph or an item, has
`data-step="1"`, `data-step="2"`.

```html
<section data-slide="costs">
  <h2>What it costs</h2>
  <p data-step="1">Oil, forty litres a month.</p>
  <p data-step="2">Wicks, two a year.</p>
</section>
```

The look on a screen and in the film is the `<style>` at the top; the look on
paper is the `@media print` part of it. Colours and type are variables.

## Write what is said

Everything after `---` in `reading.conv` is the reading. A mark in square
brackets goes on the line **before** the words it belongs with:

| Mark | Does |
| --- | --- |
| `[slide costs]` | scrolls to the section `costs`, and dims the others |
| `[slide costs step:2]` | lights up its second part, and brings it to the middle |
| `[speakers lower-third captions]` | what is drawn of whoever speaks, from here on: any of `faces`, `lower-third`, `waveform`, `captions` |
| `[speakers off]` | draws nothing of them |
| `[pause 0.5]` | half a second of quiet |

The voice need not read every word. A reading that says what each section is
for, and leaves the detail to the page, is easier to listen to than the page
read out. If you do want it word for word, put each paragraph on a line of its
own.

After changing one line, `media say reading.conv out/____moduleName____.flac --only 4`
says only line 4 again and keeps the rest.

## Before you call it done

- `pnpm pdf`, and open it. Check where the pages break.
- `pnpm check` says `ok`.
- `pnpm build` ends without `need a listen` and without `to look at`. A section the
  script names and the page does not have is reported there.
- Look at the film. Pull a frame out with
  `ffmpeg -ss 12 -i out/____moduleName____.mp4 -frames:v 1 frame.png` and see that the
  section on screen is the one being spoken of.

Nothing under `out/` is committed.
