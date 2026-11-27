# ____moduleName____ — agent guide

A document that is read aloud. [`index.html`](./index.html) is the document,
[`reading.conv`](./reading.conv) is what the voice says, and
[Constructive Media](https://github.com/constructive-io/constructive-media) (`me`) prints
the one and films it following the other. [README.md](./README.md) says what each mark
and attribute does.

## Rules

- **The document is the page.** Write it to be read on its own: the PDF has no voice.
- **The script decides where the page is.** A move is a mark in `reading.conv`, on the
  line before the words it goes with. Do not time anything in the page.
- **Every `[slide NAME]` in the script is a `data-slide="NAME"` in the page**, and
  every `step:N` a `data-step="N"` inside it.
- **Do not copy `stage.js` or `stage.css` in.** The engine hands them to the page.
- **Nothing rendered is committed.** `out/` is ignored.
- **Another one is `me init document NAME`** at the top of the workspace, not a copy of this
  folder.
- **A voice is a person's.** `narrator` speaks with whatever voice this machine was
  given for it. Do not clone anybody who has not said yes.

## Before you say it is done

```sh
pnpm check      # the script is a script
pnpm pdf        # printed: out/____moduleName____.pdf
pnpm build      # said and filmed: out/____moduleName____.mp4
```

`pnpm build` must end with no `need a listen` and no `to look at`. Then open the PDF, and look
at frames of the film (`ffmpeg -ss 12 -i out/____moduleName____.mp4 -frames:v 1 frame.png`)
before saying it is right, and say what you looked at. The engine checks every spoken
line by listening back to it; nobody has heard it until a person has.
