# 2026-09-14 — The Witcher 2 is NOT usable on the dev PC yet

**Machine:** dev PC `DESKTOP-V8GTSIR`. **No launch, no analysis** — this is an install check, and it
came back negative.

## What was found

`D:\Program Files (x86)\Steam\steamapps\common\the witcher 2\` **exists and is completely empty**
`[inferred-static 2026-09-14]`.

Steam's own record explains why: `appmanifest_20920.acf` reads `StateFlags=1026` with
`BytesDownloaded=0` of `BytesToDownload=17108201264`. **The download is queued or paused and not one
byte of the 17.1 GB has arrived.** Partial state files are sitting in `steamapps\downloading\20920\`.

## What that means for this project

The 2026-09-13 `[PD]` row — *"finish the first static look: imports, whether `DebugConsole` is a real
console and how it opens, what the shipped scripts say about the camera"* — **cannot run on this
machine.** There is no binary to read.

⚠️ **This is the Burnout Paradise lesson repeating, and it is worth naming.** That project stalled
because a folder existed while the game did not. The folder here exists too. **Checking for the
folder is not checking for the game; check for the executable, or check Steam's own state flag.**

## What would change it

The user starts (or resumes) the Steam download for app 20920 on this PC. Nothing else is blocked in
the meantime — the home PC has the game fully installed and can run that `[PD]` row today.
