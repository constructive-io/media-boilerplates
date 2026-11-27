# voices

One folder for each persona, and in it one clip for each mood:

```
voices/narrator/neutral.flac     the clip a speech server clones from
voices/narrator/neutral.txt      the words said in it, exactly
voices/narrator/whisper.flac
voices/narrator/whisper.txt
```

A clip is 15 to 28 seconds of one person in one mood, with nothing else to be
heard. `media reference` cuts one from a longer recording and writes its words
beside it; the [README](../README.md) walks through it.

What a clip was cut from does not belong here. Keep it in `originals/`, which
git is told to pass over, or somewhere else altogether.
