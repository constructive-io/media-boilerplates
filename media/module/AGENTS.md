# ____moduleName____ — agent guide

A talk with slides, made from a script. [`talk.conv`](./talk.conv) is the script, [`index.html`](./index.html) the page, and
[Constructive Media](https://github.com/constructive-io/constructive-media) (`me`) says
the one and films the other. [README.md](./README.md) says what each mark and attribute
does.

## Rules

- **The script decides what is on the screen.** A change on the screen is a mark in
  `talk.conv`, on the line before the words it goes with. Do not time anything in the page:
  no `setTimeout`, no counting frames. What the page draws for itself is drawn from
  `window.stage.since(SLIDE, STEP)`, the seconds since the script got there.
- **A step for every spoken line.** What is being said is what just arrived. A slide
  that sits still under four lines is a slide with three steps missing.
- **How a thing arrives is `data-enter`**, not an animation of your own: `rise`, `fade`,
  `left`, `right`, `grow`, `pop`, `wipe`, `draw`, with `--stage-delay` and `--stage-time`.
- **Keep the bottom left clear where somebody first speaks.** The engine names them there.
- **Every `[slide NAME]` in the script is a `data-slide="NAME"` in the page**, and
  every `step:N` a `data-step="N"` inside it.
- **Do not copy `stage.js` or `stage.css` in.** The engine hands them to the page.
- **Nothing rendered is committed.** `out/` is ignored.
- **Another deck is `me init deck NAME`** at the top of the workspace, not a copy of this
  folder.
- **A voice is a person's.** `narrator` speaks with whatever voice this machine was
  given for it. Do not clone anybody who has not said yes.

## Before you say it is done

```sh
pnpm check      # the script is a script
pnpm build      # said and filmed: out/____moduleName____.mp4
```

`pnpm build` must end with no `need a listen` and no `to look at`. Then look at frames of
the film (`ffmpeg -ss 12 -i out/____moduleName____.mp4 -frames:v 1 frame.png`) before
saying it is right, and say what you looked at. The engine checks every spoken line by
listening back to it; nobody has heard it until a person has.
