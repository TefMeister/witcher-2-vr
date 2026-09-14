# Engine Dossier — The Witcher 2: Assassins of Kings (REDengine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, full static pass done (2026-09-13 home, 2026-09-14 dev PC after Tefa downloaded it); the game has **not** been launched. · **VR-readiness verdict:** TBD, but the groundwork is friendlier than the first look suggested — a fixed module base, a **static** D3D9 import, plain-text config files, and a debug console, debug menu and free-camera class all named in the binary.

## 1. Identity
- Game / build / version: The Witcher 2: Assassins of Kings Enhanced Edition, Steam app 20920, fully downloaded. Game exe `bin\witcher2.exe` (linked 2013-05-09, a late patch build); `Launcher.exe` and `bin\Configurator.exe` sit beside it.
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: CD Projekt Red's REDengine, in its first version `[reported]`. Havok and Scaleform strings are present in the exe `[inferred-static 2026-09-13]`. Game logic is script: `CookedPC\base_scripts.dzip` and `compiledscripts.w2scripts` ship with the game.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.): Havok and Scaleform `[inferred-static 2026-09-13]`; audio is **FMOD Ex + FMOD Event**, and notably `fmod_event_net.dll` — FMOD's live network profiler — ships too `[inferred-static 2026-09-14]`. `w1import.dll` handles Witcher 1 save import; `AVIFIL32` is linked for video capture.
- Distinctive file formats / build tags / symbol naming: `.dzip` archives in `CookedPC\` (`pack0.dzip` alone is 10.5 GB, plus one per DLC), `.w2speech` and `.w2strings` language files, `staticShader.cache`. Not yet looked at.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **32-bit** (PE32), `witcher2.exe` 15.7 MB, linked 2013-05-09. Ordinary sections plus `.bind` (the Steam DRM wrapper, 565 KB) and a small `PSFD00` section (7.8 KB, marked executable, purpose still unknown) `[inferred-static 2026-09-13]`. ⭐ **Module base `0x400000`, ASLR OFF — the base never moves** `[inferred-static 2026-09-14]`, so addresses stay valid across runs and sessions.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: **Direct3D 9, confirmed from the import table**: `d3d9.dll → Direct3DCreate9` `[inferred-static 2026-09-14]`. ⭐ A **static** import, so a same-named proxy DLL in `bin\\` is available as an injection route without the runtime-resolution uncertainty Tomb Raider and Alan Wake have. `d3dx9_39.dll` supplies 15 helpers including `D3DXMatrixMultiply`; ⚠️ **`D3DXGetShaderConstantTable` is NOT among them**, unlike Hard Reset and Dead Space 2 — so there is no free route to named shader constants here. Input is `DINPUT8.dll → DirectInput8Create` plus `XINPUT1_3.dll`, both real imports.
- Developer console / cvar system present? how opened?: ⭐ **`CDebugConsole` is a real class, not a stray string** — and beside it sit **`CGameDebugMenu`** (a separate debug menu the first look had not spotted) and **`CFreeCamera`** `[inferred-static 2026-09-14]`. ⚠️ **How any of them is opened is unknown**; no key binding was found. ⚠️ Debug classes routinely survive into retail builds with their entry points removed, so a class name proves the code was compiled in, not that a player can reach it. Cheapest thing to settle on the first launch.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: The Steam DRM wrapper (`.bind`); no Denuvo or SecuROM string found `[inferred-static 2026-09-13]`. Not tested live. The exe contains the string `DebugConsole`, so a developer console may exist; unchecked.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**:
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from:
- The per-eye override maths (`K_eye = …`):

## 7. Constant-buffer fill mechanism
- Map/DISCARD ring / UpdateSubresource / D3D11.1 offset / **persistent map +
  memcpy** (trap):
- Can source contents be read cheaply (captured CPU pointer) or need staging
  read-back?:
- The chosen override patch point and why:

## 8. Pass inventory (by render target)
- Main scene (res/formats):
- Shadow passes (depth-only sizes):
- Post / AA chain (SMAA/TAA/motion vectors; downscale sizes):
- UI / HUD (how it's kept separate):

## 9. cvar / console cheat sheet
| command / cvar | effect | use |
|---|---|---|
| | | |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene (commands used):
- In-process input / camera drive method that worked:
- Frame-capture method; where images land:

## 11. Dead ends & false leads (save future time)
- none yet.

## 9a. Config files ship in plain text, and that is a lead `[inferred-static 2026-09-14]`

`bin\config\` holds `User.ini`, `Rendering.ini`, `Community.ini`, `DIMapping.ini` and three
keyboard-layout files. ⭐ **The Alice lesson repeating** — that project's stereo flag lived in a config
file the exe never mentioned, and an exe scan had returned a false negative.

`[Rendering]` exposes ~30 switches by name: `AllowAntialias`, `AllowBloom`, `AllowBlur`, `AllowDOF`,
`AllowCutsceneDOF`, `AllowScatterDOF`, `AllowMotionBlur`, `AllowSSAO`, `AllowShafts`, `AllowSharpen`,
`AllowVignette`, `AllowRain`, `AllowDecals`, `Fullscreen`, `VSync`, `UberSampling`,
`MeshDistanceScale`, `ShadowQuality`, `ShadowedLights`, `MaxCubeShadowCount`/`Size`,
`MaxSpotShadowCount`/`Size`, `TextureDownscale`, `MaxTextureSize`, `TextureMemoryBudget`,
`DanglesLimiter`. `[Engine]` carries **`CustomRenderingSettings`** and `PerformancePlatform`.

- ⭐ **`Fullscreen` is a plain INI key, so windowed mode needs no code patch at all** — the result
  Manhunt reached the hard way.
- ⭐ **`CustomRenderingSettings` ships at 0** and is worth a look: a switch named "custom rendering
  settings" is exactly the kind that widens the available option set.
- ⚠️ **No stereo, VR or 3D key appears in the shipped `[Rendering]` section.** A real negative, but a
  soft one — the engine may accept keys it does not write by default.

⚠️ The game's own `.ini` files are deliberately **not** copied into this repo: they are original game
files. Setting *names* are interface metadata and are fine to record; contents stay on disk.

## 9b. The camera is a named, registered object `[inferred-static 2026-09-14]`

REDengine registers classes by name, and the camera family is large: `CCamera`, `CCameraComponent`,
`CCameraAreaComponent`, **`CCameraPlanesParameters`** (near/far planes as a named object),
`CCameraFollowingEntity`, `CStaticCamera`, **`CFreeCamera`**, `CCameraEffectTrigger`, plus
sub-families for cutscenes (`CStorySceneEventCamera`, `CStorySceneEventCameraLookAt`,
`CStorySceneEventCustomCamera`, `SSceneCameraShotDescription`), quests
(`CQuestStaticCameraSwitchBlock`, `CQuestCameraFocusCondition`, …) and animation
(`CBehaviorGraphCameraControllerNode`, `CBehaviorGraphConstraintNodeCameraLookAt`,
`CBehaviorGraphCameraVerticalDampNode`).

⭐ A camera that is a **named, registered object with a separate parameters object** is far friendlier
than loose variables in a renderer, and `CFreeCamera` existing means the engine already knows how to
take a camera off its rails. That is the shape head tracking wants.

⚠️ Every one of those is a **name** from the class registry. Nothing here says what any of them does,
and no code was read.

## 12. Open risks toward the North Star
- The Steam DRM wrapper hides the real start of the program until it has unpacked itself, so disassembly of the entry path will have to wait for a running copy. ⚠️ Note this is **not** a general block: ordinary strings, the class registry and the import table all read fine off disk, as the 2026-09-14 pass showed.
- ⭐ **The scripts ship with the game** (`base_scripts.dzip`), and REDengine has a large public modding and research community `[reported]`. Much of this engine may already be explained in public, which is `/gr`'s to collect.
- Cyberpunk 2077's VR work is on a much later REDengine generation `[reported]`, so its lessons may carry over in method more than in detail `[hypothesis]`.
