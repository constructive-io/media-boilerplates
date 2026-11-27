# banks

A bank is a file ending `.sounds` that a script pulls in by name:

```
@include weather
```

It holds only `@sounds` and `@tracks`, written as a script writes them:

```
@sounds
RAIN:    { file: rain.flac, loop: true, track: ambience, level: -8 }
THUNDER: { file: thunder.flac, level: -4 }
```

Save that as `banks/weather.sounds`, and put `rain.flac` and `thunder.flac` in
[`sounds/`](../sounds). A `level:` is in decibels, from -80 to 0. A `file:` is
a name inside `sounds/`, never a path on your machine.
