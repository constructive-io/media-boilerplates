# ____moduleName____ — agent guide

A library for [Constructive Media](https://github.com/constructive-io/media-engine):
voices to clone, banks of sounds and faces. [`media-library.json`](./media-library.json)
names everything in it. [README.md](./README.md) says how a voice is added.

## Rules

- **Never add a voice without consent.** Every entry under `voices` has a `consent` that
  says whose voice it is (`by`) and by what right it is here (`kind`). Only the person
  who keeps this library can say that. If you were not told, ask; do not fill it in.
- **Never clone a real person from a recording found somewhere.** An interview, a talk or
  a film is not consent.
- **Clips only.** A clip is 15 to 28 seconds. The recording it was cut from goes in
  `originals/`, which is not committed apart from its README. No video, but for a clip of a
  few seconds in `sounds/` that a bank names and a script cuts to with `[video NAME]`.
- **`--by` and `--kind` come from a person.** `media library clip` will not run without
  them, and that is the point. [CONSENT.md](./CONSENT.md) is what to send somebody whose
  voice it is; what they answer is kept outside this repository.
- **The table in the README is written by `media library clip`**, between
  `<!-- voices -->` and `<!-- /voices -->`. Leave the marks in.
- **The words beside a clip are the words in it.** `voices/<persona>/<mood>.txt` is read
  by the speech server along with the sound. Do not tidy it into what should have been
  said.
- **Paths stay inside.** Everything the manifest and the banks name is in this folder,
  by a path from it. Nothing names a path on one machine.
- **Run the check before you say it is done:** `python3 scripts/check.py`, and
  `media library check .` where the engine is installed. Report what the check said, and
  that nobody listened unless somebody did.

## Commands

```sh
python3 scripts/check.py                  # is it a library; needs nothing installed
media library check .                     # the same, and every clip measured
media reference RECORDING                 # how long, how loud, what is wrong with it, where it could be cut
media library clip WHO RECORDING --by "Whose Voice" --kind own           # put a voice in: clean, cut, words, consent, README
media clean RECORDING                     # how noisy a recording is, and what is worth doing about it
media reference RECORDING voices/WHO/MOOD.flac --from S --to S --listen  # cut a clip by hand: end it in the quiet after a sentence
media library add . && media library voices ____moduleName____          # use it here
media say --voice WHO "A few words." out/hello.wav                      # hear a voice
media audition WHO --out out/audition                                   # try it on a set of lines
```
