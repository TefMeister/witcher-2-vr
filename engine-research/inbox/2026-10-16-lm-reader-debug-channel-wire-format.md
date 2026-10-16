# The debug channel's wire format: how to send a console command to the running game

From: `/lm` static reader, 2026-10-16, on the Steamless-unpacked copy. Follows
`2026-10-16-lm-reader-debug-channel-ports-47000-47001.md`. **Nothing here has been sent to a game yet.**
Client: private `staging` repo, `witcher-2-vr/debug-channel/w2console.py` (has `--dry-run`).

## Format `[inferred-static]` for every line

- **Ports:** TCP 47000 carries requests and replies; TCP 47001 only pushes broadcasts. Both bound on all
  interfaces. **No handshake**: the accept path (`0x00B0CB41`) sends nothing.
- **Framing, both directions:** u32 payload length, little-endian (raw, no `htonl`), then the payload
  (send `0x00B0C5E3`, receive `0x00B0C790`). Receive is non-blocking, once per engine frame, from the main
  loop (`0x00AA6D28`). A 4-byte header split across two TCP segments would be misread, so send each
  message in one call.
- **String:** u32 character count (little-endian, NUL not counted), then UTF-16LE characters
  (`0x00B0C82A` read, `0x00B0C8C6` write).
- **Request payload:** string packet name, then that receiver's fields. The server makes a CName from the
  name and offers the packet to each registered `IDebugChannelReciever` until one returns true
  (`0x00B19BB2`). `CDebugConsole` (`0x00AA353D`) takes **`ConsoleCommand`**, reads one more string, and
  runs it through the console executor (`0x00ABBE18`).
- **Example**, `cameraSetFOV(90)`: `44 00 00 00 | 0e 00 00 00 "ConsoleCommand" (UTF-16) | 10 00 00 00
  "cameraSetFOV(90)" (UTF-16)`, 72 bytes in all.
- **Reply on 47000, always:** u32 length + payload whose first byte is `01` if some receiver took the
  packet, `00` if none did. The console adds nothing more, so `01` does not prove the command worked.
- **Broadcasts on 47001:** `CDebugConsole` forwards lines from the engine's Warning, Error and Script log
  channels as [string kind "Warning"/"Error"/"Log"][string text] (`0x00AA364E` → `0x00B19A94`).
  ⚠️ **The script-side `Log()` is stubbed in retail** (native `0x0092F9F9` reads its argument and
  discards it), so script `Log()` calls produce nothing there, and the `VRCAM` probe's `Log()` line is a
  no-op too; its HUD text is the only output.

## Command syntax `[inferred-static]`

The executor splits on space, `(`, `)` and `,`. The first token must name a global script function marked
`exec`; the brackets are optional for functions with no arguments (`FreeCamera` and `FreeCamera()` both
parse). Arguments go in order, comma-separated. String arguments cannot contain spaces. How enum
arguments are written (by name, such as `CS_Interior`, or by number) is not checked `[hypothesis]`.

## Commands worth sending for a camera test (from the unpacked scripts)

| command | what the script does | file |
|---|---|---|
| `FreeCamera()` | toggles the engine free camera (`theGame.EnableFreeCamera(!IsFreeCameraEnabled())`) | game/debug.ws |
| `cameraSetFOV(90)` / `camFov(90)` | `theCamera.SetFov(f)`, a float | game/debug.ws, engine/camera.ws |
| `ActivePause()` | toggles active pause | game/debug.ws |
| `SetTimeScale(0.2)`, `SlowTime()`, `NormalTime()` | game time scale | game/debug.ws, brix.ws |
| `GodMode()` / `Immortal()` | player cannot die during long tests | game/debug.ws |
| `camResetRotation()`, `camResetRotationNow()` | recentres the gameplay camera | engine/camera.ws |
| `camSetCameraState(CS_Interior)` | camera behaviour state; enum syntax unverified | engine/camera.ws |
| `CameraInterior()` / `CameraExploration()` / `CameraWide()` | raise camera behaviour events | game/debug.ws |
| `camLookAtStatic(x, y, duration, actTime)` | points the camera at screen-space x, y | engine/camera.ws |
| `hide_hud()` / `show_hud()`, `HideGui()` / `ShowGui()` | clean screenshots | game/debug.ws |
| `TeleportTest2()` | lifts the player 100 m up with physics off (the only teleport-type exec found) | game/bosses/zagnica/brix.ws |

No exec function teleports the player to arbitrary coordinates. `CameraInfo` and `CameraTestInfo` only
`Log()`, which is stubbed, so they print nothing.

## Live test plan (FLAT)

At the menu, `netstat -ano | findstr 4700`; then from a loaded save,
`w2console.py "cameraSetFOV(40)" --log 3` and watch the picture zoom; the reply should be `01`.
