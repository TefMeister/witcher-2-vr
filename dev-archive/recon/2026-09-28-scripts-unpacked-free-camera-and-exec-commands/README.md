# 2026-09-28 — /pd: the scripts are plain text, and they already carry a free camera and 403 console commands

Dev PC, `/pd`, no game launched, nothing run. Game at `D:\Program Files (x86)\Steam\steamapps\common\the witcher 2`.

## Unpacked

`CookedPC\base_scripts.dzip` unpacked with our own reader, `dev-archive/tools/dzip_extract.py` (DZIP v2: file table at
the end, LZF-compressed 64 KiB chunks). **460 files, 0 short, all plain WitcherScript source** with comments
`[inferred-static 2026-09-28]`. The unpacked scripts are game content and stay out of git.

## The camera, as the scripts see it

`engine/camera.ws` (`CCamera`), `engine/game.ws` (`theGame`) and `game/debug.ws` `[inferred-static 2026-09-28]`:

| script call | what it offers VR |
| --- | --- |
| `theGame.EnableFreeCamera( flag )` / `IsFreeCameraEnabled()` | an engine free camera, switchable from script |
| `theCamera.GetCameraMatrixWorldSpace() : Matrix`, `GetCameraPosition()`, `GetCameraDirection()` | the live camera pose, readable from script |
| `theCamera.SetFov( fov )` / `GetFov()` | the field of view, settable from script |
| `TeleportCamera( pos, rot )` (minigames), `AttachCameraBehavior( name )`, `RaiseEvent( 'Camera_Interior' )` … | camera placement and behaviour switching |
| `GetActiveSceneCamera()`, `PlayCutscene( …, cameraNum )`, static cameras | cutscene and fixed cameras are separate objects |

**403 `exec function`s** (console commands) across the scripts, among them `FreeCamera` (toggle), `cameraSetFOV`,
`camFov`, `CameraInfo`, `CameraInterior` / `CameraExploration` / `CameraWide`, `camLookAt*`, `camSetCameraState`,
`GodMode`. `game/debug.ws` also has a debug menu whose item 7 toggles the free camera and item 8 teleports the player
to it.

## The console

`witcher2.exe` carries `CDebugConsole` and `CGameDebugMenu` (RTTI), the action names `CHEAT_Console` and
`CHEAT_DebugPages`, and `ConsoleCommand` `[inferred-static 2026-09-28]`. Key bindings live in
`bin\config\Input_QWERTY.ini` as `IK_<key>=(GameKey="<action>",Value=1)`; **no key is bound to `CHEAT_Console`**.
Binding one is the cheapest console test `[hypothesis]`: `IK_Tilde=(GameKey="CHEAT_Console",Value=1)`.

## Windowed

`bin\config\User.ini` → `[Rendering] Fullscreen=1`. Setting `Fullscreen=0` is the likely window route `[hypothesis]`
(the resolution keys are not in that file).

## Also worth knowing

`CookedPC` already holds community archives beside the game's own (`abetterui.dzip`, for one), so extra script
archives load in this install `[inferred-static 2026-09-28]`. That is the route the public camera mods use
(`/gr` note, 2026-09-17).

## NOT established

- Whether `CHEAT_Console` responds to a binding in the shipping exe.
- What `EnableFreeCamera` looks like in play, and whether the camera matrix it reports is the rendered one.
- Anything about the GPU side (dossier §6 first half).
