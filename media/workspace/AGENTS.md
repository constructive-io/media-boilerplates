# ____repoName____ — agent guide

A pnpm workspace of things made from scripts. Each folder under `packages/` has a
`.conv` script, a page of HTML and a `package.json` whose scripts call
[Constructive Media](https://github.com/constructive-io/media-engine) (`media`).
[README.md](./README.md) has the commands; each package's README says what its marks and
attributes do.

## Rules

- **A new package is `media init deck NAME`**, run at the top of the workspace, or
  `walkthrough`, `animation` or `document` in place of `deck`. Do not copy a package by
  hand: a copy keeps the old name in its scripts.
- **The script decides what is on the screen.** A change on the screen is a mark in the
  script, on the line before the words it goes with. A page times nothing itself.
- **A script names personas, never voices.** A voice is given to a persona on a machine
  (`media voice`) or comes from a library (`media library`). Do not clone anybody who has not
  said yes.
- **Libraries are pinned.** After adding or updating one, run `media library lock` at the top
  of the workspace and commit `media-libraries.json`.
- **Nothing rendered is committed.** No sound, no film, no frames: `out/` is ignored.
- **One thing is said at a time.** `pnpm build` goes through the packages one by one. Do
  not start two builds at once on one machine.

## Before you say it is done

```sh
pnpm lint                       # every script is a script
pnpm --filter NAME build        # said and filmed: packages/NAME/out/NAME.mp4
```

A build must end with no `need a listen` and no `to look at`. Then look at frames of the
film (`ffmpeg -ss 12 -i packages/NAME/out/NAME.mp4 -frames:v 1 frame.png`) before saying it
is right, and say what you looked at. The engine checks every spoken line by listening
back to it; nobody has heard it until a person has.

## Skills

How the work is done is written down in `.agents/skills/`, put there when this workspace
was made: `media-workspace`, `narrated-video`, `narrated-document`, `conv` and
`constructive-media`. Read the one for what you were asked to do before you start. If the
folder is not there, or to bring a skill up to date:

```sh
npx skills add https://github.com/constructive-io/media-engine --skill constructive-media
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill media-workspace
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill narrated-video
npx skills add https://github.com/constructive-io/media-engine-boilerplates --skill narrated-document
npx skills add https://github.com/constructive-io/conversation-format --skill conv
```
