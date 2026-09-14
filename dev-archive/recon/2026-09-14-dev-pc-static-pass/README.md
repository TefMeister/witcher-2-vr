# 2026-09-14 — The Witcher 2, dev-PC static pass (NO LAUNCH)

**Machine:** dev PC `DESKTOP-V8GTSIR`. Tefa started the download this afternoon after the morning's
check found the folder empty. **Install:** `D:\Program Files (x86)\Steam\steamapps\common\the witcher 2`,
Steam app 20920, fully installed `[inferred-static 2026-09-14]`.

**The game was not launched.** Everything here is PE headers and strings read off disk.

## Files here

| File | What it is |
| --- | --- |
| `pe-imports.txt` | PE header, sections and the full import table |
| `console-and-camera-classes.txt` | the debug-console, debug-menu and camera class names |
| `engine-class-registry.txt` | REDengine's registered class list (~50 KB of `TTypedClass` names) |
| `install-listing.txt` | install root, `bin\` and `bin\config\` |

⚠️ **The game's own `.ini` files are deliberately NOT copied here.** They are original game files, and
the standing rule is that only files we create get committed. Their *setting names* are recorded
below as interface metadata, which is fine; their contents stay on disk.

## ⭐ The headline: a real debug console, a debug menu, and a free camera — all named in the binary

The 2026-09-13 board asked whether `DebugConsole` is a real console. **It is a class, not a stray
string** `[inferred-static 2026-09-14]`:

- **`CDebugConsole`** — the console itself.
- **`CGameDebugMenu`** — a separate debug *menu*, which the earlier note had not spotted.
- **`CFreeCamera`** — ⭐ a free camera class, already in the shipped engine.

⚠️ **How any of the three is opened is unknown**, and no key binding was found. ⚠️ And the standing
caution applies with force here: **debug classes routinely survive into retail builds with their
entry points removed.** A class name proves the code was compiled in; it does not prove a player can
reach it. This is the cheapest thing to settle on the first launch.

## The camera vocabulary is unusually rich

REDengine registers its classes by name, and the camera family is large — `CCamera`,
`CCameraComponent`, `CCameraAreaComponent`, **`CCameraPlanesParameters`** (near/far planes as a named
object), `CCameraFollowingEntity`, `CStaticCamera`, `CFreeCamera`, `CCameraEffectTrigger`, plus whole
sub-families for cutscenes (`CStorySceneEventCamera`, `CStorySceneEventCameraLookAt`,
`CStorySceneEventCustomCamera`, `SSceneCameraShotDescription`), for quests
(`CQuestStaticCameraSwitchBlock`, `CQuestCameraFocusCondition`, …) and for animation
(`CBehaviorGraphCameraControllerNode`, `CBehaviorGraphConstraintNodeCameraLookAt`,
`CBehaviorGraphCameraVerticalDampNode`).

⭐ **Why that is good news rather than just a long list.** A game whose camera is a *named, registered
object* with a separate parameters object is far friendlier than one where the camera is loose
variables in the renderer — and `CFreeCamera` existing means the engine already knows how to let a
camera off its rails. That is the shape head tracking wants.

⚠️ Every one of those is a **name**, recovered from the class registry. Nothing here says what any of
them does, and no code was read.

## Config files ship with the game, in plain text

`bin\config\` contains `User.ini`, `Rendering.ini`, `Community.ini`, `DIMapping.ini` and three
keyboard-layout files `[inferred-static 2026-09-14]`. ⭐ **This is the Alice lesson repeating** — that
project's stereo flag was in a config file the exe never mentioned, and an exe scan had returned a
false negative.

The `[Rendering]` section alone exposes ~30 switches by name: `AllowAntialias`, `AllowBloom`,
`AllowBlur`, `AllowDOF`, `AllowCutsceneDOF`, `AllowScatterDOF`, `AllowMotionBlur`, `AllowSSAO`,
`AllowShafts`, `AllowSharpen`, `AllowVignette`, `AllowRain`, `AllowDecals`, `Fullscreen`, `VSync`,
`UberSampling`, `MeshDistanceScale`, `ShadowQuality`, `ShadowedLights`, `MaxCubeShadowCount/Size`,
`MaxSpotShadowCount/Size`, `TextureDownscale`, `MaxTextureSize`, `TextureMemoryBudget`,
`DanglesLimiter`. `[Engine]` carries **`CustomRenderingSettings`** and `PerformancePlatform`.

⭐ **`Fullscreen` being a plain INI key means windowed mode needs no code patch at all** — the same
result Manhunt reached the hard way. And `CustomRenderingSettings` is worth a look: a flag named
"custom rendering settings" that ships set to 0 is exactly the kind of switch that unlocks a wider
set of options.

⚠️ **No stereo, VR or 3D key appears in the shipped `[Rendering]` section** `[inferred-static 2026-09-14]`.
That is a real negative, but a soft one: the engine may accept keys that are not written by default.

## Binary facts

| | |
| --- | --- |
| `bin\witcher2.exe` | **32-bit**, linked 2013-05-09 `[inferred-static 2026-09-14]` |
| Module base | `0x400000`, ⭐ **ASLR OFF**, NX on — **the base never moves**, so addresses stay valid across runs |
| Sections | usual set plus `.bind` (Steam DRM wrapper, 565 KB) and `PSFD00` (7.8 KB, marked executable) |
| **Renderer** | **Direct3D 9, a real static import**: `d3d9.dll → Direct3DCreate9` |
| Shader helpers | `d3dx9_39.dll`, 15 functions including `D3DXMatrixMultiply`. ⚠️ **`D3DXGetShaderConstantTable` is NOT among them** — unlike Hard Reset and Dead Space 2, so no free route to named shader constants |
| Input | `DINPUT8.dll → DirectInput8Create`, `XINPUT1_3.dll` |
| Audio | FMOD Ex + FMOD Event + **`fmod_event_net.dll`** (FMOD's live network profiler) |
| Other | `w1import.dll` (Witcher 1 save import), `AVIFIL32` (video capture), `dbghelp`, `steam_api.dll` |

⭐ **Two things make this friendlier than the morning's note suggested:** the fixed module base, and a
**static** `d3d9.dll` import — which means a same-named proxy DLL in `bin\` is available as an
injection route without the runtime-resolution uncertainty Tomb Raider and Alan Wake have.

⚠️ The `.bind` Steam wrapper still hides the real start of the program until it unpacks, so
disassembly of the entry path will need a running copy. Ordinary strings and the class registry read
fine off disk, as this pass shows.

## What this does NOT establish

- Nothing has been run.
- No code was disassembled; every claim above is a name, an import, or a config key.
- `CookedPC\` (including the 10.5 GB `pack0.dzip` and the shipped scripts) was **listed, not opened**.
  The scripts are the most interesting unopened thing here, given REDengine is script-driven.
- `PSFD00`'s purpose is still unknown.
