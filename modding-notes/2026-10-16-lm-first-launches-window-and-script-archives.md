# 2026-10-16 (`/lm`, dev PC): first launches, the window, and why our script archives do nothing yet

First live session on this game. Everything below was seen once (n=1) unless it says otherwise.

## The first-game checklist: done

1. **Runs as shipped**: launched through Steam, the game's launcher appeared, "Launch game" reached the main menu
   `[verified-live 2026-10-16, n=1]`.
2. **Runs with our file**: the shared logging proxy as `bin\d3d9.dll` (32-bit, 23 of 23 exports, staging
   `proxy-d3d9/`). The game called `Direct3DCreate9`, `DebugSetMute` and `Direct3DShaderValidatorCreate9` through it
   and reached the menu `[verified-live 2026-10-16, n=3 launches]`. It stays installed.
3. **Windowed**: `Documents\Witcher 2\Config\User.ini` `[Rendering] Fullscreen=0`, `[Viewport] Width=1280`,
   `Height=720` gives a 1280x720 client area with the desktop untouched `[measured 2026-10-16]`. The copy in
   `bin\config\` is only the template the game copies on its first start.
- **Music off**: Options > Sound and Music, slider held to 0; saved as `[Sound] MusicVolume=0` in the same file.

## Starting it

- **Direct start works** with `bin\steam_appid.txt` holding `20920` (Steam running): no launcher, and no Steam
  first-run step. Without the file the exe hands itself back to Steam, which opens the launcher
  `[verified-live 2026-10-16, n=4]`. The file stays installed.
- Steam's first-run step for this game (DirectX and Visual C++ installers, an HKLM key) needs administrator rights
  and asks every launch until allowed. While the prompt is up the game fails with "Direct3D 9 device initialization
  error!" `[verified-live 2026-10-16, n=1]`; the direct start avoids the step altogether.
- No save is needed for tests: New Game, then accept the tutorial with **Space**, gives a controllable Geralt in
  about a minute. The tutorial cannot be saved. Route detail: `ai-game-control-profiles/routes/the-witcher-2/KNOWN.md`.

## The debug console: not reachable by key binding

`IK_Tilde` and `IK_NumPad0` bound to `CHEAT_Console`, `IK_NumPad1` to `CHEAT_DebugPages` in the live
`Input_QWERTY.ini`: nothing opened, at the main menu or in play, while W did move Geralt in the same run
`[verified-live 2026-10-16, n=1 per key]`. The bindings were taken out again. Most likely the actions are gated off
in the retail build `[hypothesis]`; the unpacked exe should say how.

## Script archives: the game rejects archives our writer makes

| Test | What happened |
| --- | --- |
| `zzz_vrcamprobe.dzip` (one patched `player.ws`) added | menu and tutorial normal, no `VRCAM` text |
| same, with `compiledscripts.w2scripts` set aside | same; the game runs fine without that file and does not rebuild it |
| plus `aaa_vrcamprobe.dzip` (same content, sorts first) | same |
| **full replacement `base_scripts.dzip`, our 12 lines added** | intro plays, then a black screen with an empty HUD instead of the menu |
| **full replacement `base_scripts.dzip`, every script UNCHANGED** (the control) | **the same black screen** |

So the 12 lines are not the cause: **the game reads `base_scripts.dzip` and refuses anything our writer packs**
`[verified-live 2026-10-16, n=1 each]`. Our writer copies the header's `unknown` and `hash` from the original,
stores data as LZF literal runs only, sorts nothing (original order kept) and writes a fresh timestamp. The
likeliest culprit is the `hash` (or `unknown`) being a checksum of the content `[hypothesis]`; the LZF-literal style
is the second candidate. **This also means the single-file archive tests prove nothing about load order**: those
archives were probably refused too.

The two test archives were removed and `compiledscripts.w2scripts` put back (hash-checked).

## Later the same session: the hash was the gate, and our script runs

The reader unpacked a copy of the exe (SteamStub 2.1, Steamless) and found that the game recomputes a hash over each
archive's file table and refuses the archive on a mismatch; the formula reproduces every shipped archive
(dossier §7a). With the hash recomputed:

- the patched `base_scripts.dzip` loads, the menu is normal, and **the `VRCAM` line shows in the HUD** in the tutorial
  `[verified-live 2026-10-16, n=1]`: pos (429.83, 412.67, −6.14), fwd (−0.210, 0.968, −0.135), FOV 53;
- **it tracks the camera**: one mouse sweep right turned fwd to (0.968, 0.210, −0.135) and moved the camera round
  Geralt at the same height, an orbit camera in a Z-up world `[verified-live 2026-10-16, n=1]`.

## A remote console, with no exe patch

The engine listens on TCP 47000/47001 for its debug channel on every launch `[verified-live 2026-10-16, n=1]`. A
`ConsoleCommand` packet runs any script `exec function`. The reader worked out the wire format and wrote
`staging/witcher-2-vr/debug-channel/w2console.py`. Live: `cameraSetFOV(40)` → reply `01`, the picture zoomed and the
probe read FOV 40 `[verified-live 2026-10-16, n=1]`. ⚠️ The ports listen on all interfaces while the game runs.

- `FreeCamera()` over the console: reply `01`, but no free camera (W still walked Geralt) `[verified-live 2026-10-16,
  n=1]`. `-script "FreeCamera()"` on the command line: also no free camera, n=1. Open question for the reader:
  whether the native is stubbed in retail.

## The camera can be steered from outside the game

The engine's own free camera is switched off in retail (its native does nothing). The gameplay camera, though, can
be turned to an exact angle: `camResetRotationTo(angle, 0)` over the remote console pointed it north at 0, west at
90, south at 180 and east at 270, read off the `VRCAM` line `[verified-live 2026-10-16, n=1 per angle]`. Streams of
these commands at 30 and 60 per second were all handled with 2–9 ms replies and ended on the right angle
(`staging/witcher-2-vr/debug-channel/yaw_sweep.py`), recorded as `yaw-sweep_2026-10-16_18-31-58.mp4`. That is the
first head-turn route; whether it looks smooth needs a human eye.

## Screen effects for VR

`AllowBlur`, `AllowDOF`, `AllowCutsceneDOF`, `AllowScatterDOF`, `AllowMotionBlur`, `AllowVignette`, `AllowSharpen` set
to 0 in the live `User.ini`: at the same tutorial spot the dark corners and the soft distant trees were gone
`[verified-live 2026-10-16, n=1, by eye]`. Put back for flat play afterwards.

## Not recorded

Only the first two launches (started through Steam) were recorded by the automatic recorder; the later direct
starts were not, so the console and archive tests have no video. The steering sweep was recorded by hand.

## Installed now (dev PC)

- `bin\d3d9.dll`: the logging proxy, sha256 `2dc123ec...`, writes `bin\witcher2_proxy_log.txt`.
- `bin\steam_appid.txt`: `20920`.
- `CookedPC\base_scripts.dzip`: **ours**, the VRCAM build (`dev-archive/tools/build_base_scripts.py` from the
  original). The original is backed up outside the repo; rebuild with the tool, never commit the output.
- Live config: window 1280x720, music 0.
