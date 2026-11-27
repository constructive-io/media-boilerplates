# Asking for a voice

For a voice that is not your own, its owner says yes **in writing** before a
clip of it is committed. This is something to send them. Keep what comes back
somewhere outside this repository, and write the day they agreed in the
manifest as `consent.on`.

It is a plain note between two people, not legal advice. For anything that
will be sold, or a voice people would know, have a lawyer write the agreement.

---

**To:** the person whose voice it is

I would like to make a copy of your voice that a computer can speak with.

**What I will do.** Keep a recording of you of about half a minute, and the
words you say in it, in a library called `____moduleName____`. Software
(Constructive Media) uses that clip to say new lines in a voice that sounds
like yours.

**What it will be used for.**
*(say it plainly: narration for these videos, a character in this project,
for this long)*

**Who can get at it.**
*(only me / the people working on this project / anybody: the library is public)*

**What it will not be used for.** Anything you have not agreed to here. Not to
pass as you, to say things as if you had said them, or to deceive anybody
about who is speaking.

**You can change your mind.** Tell me, and I take the clip out of the library
and stop making new lines with it. What was already published I will take down
where I can, and tell you where I cannot.

**Your name, as it should be written beside the voice:**

**Do you agree?** *(a reply that says yes, with the date, is enough)*

---

When they have said yes:

```sh
media library clip PERSONA originals/RECORDING --by "Their Name" --kind permission --on 2026-01-31
```
