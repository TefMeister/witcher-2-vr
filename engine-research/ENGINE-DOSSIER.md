# Engine Dossier — The Witcher 2: Assassins of Kings (REDengine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M1 (2026-10-16, first `/lm`): runs as shipped, with our d3d9 proxy, in a 1280x720 window; **our own script runs in the game and reads the live camera**, and a **remote console** on TCP 47000 runs exec commands. Static pass done 2026-09-13/14; exe unpacked 2026-10-16. · **VR-readiness verdict:** TBD, but the groundwork is friendlier than the first look suggested — a fixed module base, a **static** D3D9 import, plain-text config files, and a debug console, debug menu and free-camera class all named in the binary.

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
- ⭐ **2026-10-16: the exe unpacks statically.** It carries **SteamStub Variant 2.1 (x86)**; Steamless v3.1.0.5 unpacks a COPY in seconds (`.text` entropy 8.00 → 6.79, entry `0x029262EE` in `.bind` → `0x0066F59D` in `.text`) `[measured 2026-10-16]`. The unpacked copy and the reader's helper scripts live only in the private `staging` repo, `witcher-2-vr/unpacked-exe-2026-10-16/` (exe git-ignored). Every exe question is now `[PD]` work. `.rdata` was never encrypted; `DZIP` is compared as the number `0x50495A44`, which is why the string search missed it.
- Developer console / cvar system present? how opened?: **Answered 2026-10-16, see §9.** ⭐ **`CDebugConsole` is a real class, not a stray string** — and beside it sit **`CGameDebugMenu`** (a separate debug menu the first look had not spotted) and **`CFreeCamera`** `[inferred-static 2026-09-14]`. ⚠️ **How any of them is opened is unknown**; no key binding was found. ⚠️ Debug classes routinely survive into retail builds with their entry points removed, so a class name proves the code was compiled in, not that a player can reach it. Cheapest thing to settle on the first launch.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: The Steam DRM wrapper (`.bind`); no Denuvo or SecuROM string found `[inferred-static 2026-09-13]`. Not tested live. The exe contains the string `DebugConsole`, so a developer console may exist; unchecked.
- Attach workflow that works: not yet tested.
- Injection vector that works: **`bin\d3d9.dll` proxy** (the lanes proxy-gen logging proxy, 32-bit, 23/23 exports); the game calls `Direct3DCreate9`, `DebugSetMute`, `Direct3DShaderValidatorCreate9` through it `[verified-live 2026-10-16, n=3 launches]`. **Script injection:** a replacement `base_scripts.dzip` with a correct table hash (§7a) `[verified-live 2026-10-16, n=1]`.
- **Starting it:** with `bin\steam_appid.txt` = `20920` (Steam running), `witcher2.exe` starts directly: no launcher, no Steam first-run step `[verified-live 2026-10-16, n=4]`. Without it the exe hands itself to Steam, which shows the launcher. Steam's first-run step (DirectX + VC++ installers, an HKLM key) asks for admin rights every launch until allowed; while that prompt is up the game fails with "Direct3D 9 device initialization error!" `[verified-live 2026-10-16, n=1]`.
- **Command-line switches** the exe reads: `-debugdata -texres -width -height -window -assert -log -script -vdb` `[inferred-static 2026-10-16]`. `-script "FreeCamera()"` stores a one-shot exec command meant to run once a world is loaded; live, it gave no free camera `[verified-live 2026-10-16, n=1]` (whether it fired is unknown). `-vdb` is dead.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**:
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from: **script-reachable** (2026-09-28, `/pd`): `base_scripts.dzip` unpacks to
  460 plain-text scripts (`dev-archive/tools/dzip_extract.py`). `CCamera` exposes `GetCameraMatrixWorldSpace()`,
  `GetCameraPosition()`, `SetFov()` / `GetFov()`; `theGame.EnableFreeCamera()` switches an engine free camera
  `[inferred-static 2026-09-28]`. Community script archives already load in this install (`abetterui.dzip`), the
  route the public camera mods use (`/gr` 2026-09-17, `[reported]`). For stereo design, CyberpunkVR's method (a real
  second engine camera, shared per-frame effects) is the prior art to read; its loader does not exist for
  REDengine 1 `[reported]`. Detail: `dev-archive/recon/2026-09-28-scripts-unpacked-free-camera-and-exec-commands/`.
  **2026-10-01 (`/pd`):** `dev-archive/tools/dzip_write.py` writes DZIP v2 (460-file round trip, 0 mismatches
  `[verified-numerically 2026-10-01]`); `build_vrcamprobe.py` builds `zzz_vrcamprobe.dzip`, a 12-line patch of
  `player.ws` that shows the script camera (position, forward, FOV) in the HUD once a second. Unknown until a run:
  whether later archives override scripts, whether `compiledscripts.w2scripts` must go, and what the header's
  unknown/hash fields must hold (the exe is DRM-encrypted on disk). Note
  `modding-notes/2026-10-01-pd-a-script-archive-that-shows-the-camera.md`.
- ⭐ **2026-10-16 (`/lm`): our script reads the live camera.** The `VRCAM` probe (12 lines in `player.ws`, built by
  `dev-archive/tools/build_base_scripts.py`) shows `theCamera.GetCameraMatrixWorldSpace()` and `GetFov()` in the HUD
  once a second. Tutorial start: pos (429.83, 412.67, −6.14), fwd (−0.210, 0.968, −0.135), FOV 53. One mouse sweep
  right: fwd (0.968, 0.210, −0.135), pos moved round Geralt at the same height: an orbit camera, **world Z-up**
  `[verified-live 2026-10-16, n=1]`. `cameraSetFOV(40)` over the remote console zoomed the picture and the probe read
  40 `[verified-live 2026-10-16, n=1]`. Script `Log()` is stubbed in retail (native `0x0092F9F9`), so HUD text is the
  only script output `[inferred-static 2026-10-16]`.
- **Free camera:** `FreeCamera()` (`theGame.EnableFreeCamera(!IsFreeCameraEnabled())`, no cheat gate in the script)
  sent over the remote console replied "handled" but W still walked Geralt and the HUD stayed: no free camera
  `[verified-live 2026-10-16, n=1]`. Whether the native is stubbed is the reader's open question.
- The per-eye override maths (`K_eye = …`):

## 7a. Script archives: the table hash, mount order, where scripts come from (2026-10-16)

- **The DZIP table hash is checked.** Both open routines (`0x0068D430` plain, `0x0068D6B0` keyed, for DLC) recompute
  a hash over the file table and return NULL on a mismatch (`0x0068D5D8`, `0x0068D87D`) `[inferred-static]`. Hash
  (`0x0068E310`): 64-bit FNV-1a style, prime `0x100000001B3`, start `0xFFFFFFFF`; per entry in table order: each name
  byte as a signed char, then strlen(name), then time, unpackedSize, offset, packedSize. It reproduces every shipped
  archive `[verified-numerically 2026-10-16, n=20 on disk]`; `dev-archive/tools/dzip_write.py` now computes it.
- **Live:** a repack of `base_scripts.dzip` with the hash copied from the original (so wrong) gave a black screen
  with an empty HUD instead of the menu, even with every script unchanged; the same repack with the hash recomputed
  loaded normally `[verified-live 2026-10-16, n=1 each]`. So the hash was the gate.
- `unknown` (u32 at +0x0C) is never read; shipped archives hold leftover stack bytes there `[inferred-static]`.
  Literal-only LZF chunks are fine: the decoder is FastLZ (`0x0068F3B0`), level 1 = LZF-compatible `[inferred-static]`.
- **Data mount order** (`0x00B1B1B9`): `pack0`…`pack9`, then every other `*.dzip`/`*.dlc` in `CookedPC` in listing
  order with override on, so **a later archive wins** (`zzz_` beats `aaa_`) `[inferred-static]`.
- **Scripts come only from `CookedPC\base_scripts.dzip`** plus a `scripts.dzip` inside each DLC folder (`0x00AA69AE`,
  `0x00ABED95`), compiled at every start `[inferred-static]`. A loose `zzz_*.dzip` holding `player.ws` did nothing live
  (it also had a wrong hash, so that test proves little). No string `compiledscripts`/`w2scripts` exists in the exe,
  and the game ran normally with `compiledscripts.w2scripts` set aside and did not rebuild it: the file looks unused
  `[verified-live 2026-10-16, n=1]`.

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
| `FreeCamera` | toggles the engine free camera (`game/debug.ws`) | camera exploration; VR base |
| `cameraSetFOV <f>`, `camFov <f>` | sets the field of view | FOV tests |
| `CameraInterior` / `CameraExploration` / `CameraWide` | switch camera behaviour | |
| 400 more `exec function`s | all listed in the unpacked scripts | |
| ~~opening the console by key~~ | **[disproved 2026-10-16]** `IK_Tilde`/`IK_NumPad0` → `CHEAT_Console`, `IK_NumPad1` → `CHEAT_DebugPages`: nothing opened while W moved Geralt (n=1 per key). `CHEAT_Console` is an `ECheats` enum value, not an input action; `IsCheatEnabled` (`0x00AA75D3`) always returns false; `CDebugConsole` has no typing path; `CGameDebugMenu` is never built; no `DBGConsoleOn` key exists `[inferred-static 2026-10-16]` | — |
| ⭐ **remote console** | the engine's debug channel listens on **TCP 47000** (requests + replies) and **47001** (log broadcasts), all interfaces, on every launch `[verified-live 2026-10-16, n=1]`. Packet: u32 LE length, then UTF-16LE strings each as u32 count + chars: `"ConsoleCommand"`, then the command line; reply byte `01` = handled `[verified-live 2026-10-16, n=1]`. Client: private `staging/witcher-2-vr/debug-channel/w2console.py "cameraSetFOV(40)"`. ⚠️ Reachable from the LAN while the game runs | camera tests, scripted setups |
| exec syntax | split on space ( ) , ; first token a script `exec function`; brackets optional with no arguments; arguments cannot contain spaces `[inferred-static]` | |
| windowed | `Documents\Witcher 2\Config\User.ini` `[Rendering] Fullscreen=0`, `[Viewport] Width=1280` `Height=720` (the `bin\config` copy is only the first-start template) `[verified-live 2026-10-16, n=3]` | the window rule |
| music off | same file, `[Sound] MusicVolume=0` `[verified-live 2026-10-16]` | the music rule |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene: direct start (§4), Esc x4 past the films, NEW GAME → NEW GAME → **Space** on the tutorial
  question → ~60 s → Tab x2: Geralt on a jetty, controllable. The tutorial cannot be saved. Full route and controls:
  `ai-game-control-profiles/routes/the-witcher-2/KNOWN.md`.
- Input: scancode SendInput; menus by arrow keys (synthetic mouse clicks are ignored in the menus); hold keys
  (sliders, W); relative mouse SendInput turns the camera. Commands: the remote console (§9).
- Frame capture: Menu-o-matiC `look` on the 1280x720 window.
- **Five automation capabilities (2026-10-16):** self-launch ✅, menu→gameplay ✅, commands ✅ (remote console),
  character + camera ✅ (W, mouse), self-close ✅ (main menu QUIT).

## 11. Dead ends & false leads (save future time)
- Binding keys to `CHEAT_Console` / `CHEAT_DebugPages` (2026-10-16): does nothing; the console is remote-only (§9).
- A separate `zzz_*.dzip` to override a script (2026-10-16): scripts are only read from `base_scripts.dzip` (§7a).
- Copying the original DZIP hash into a repack (2026-10-16): the hash covers the table, so it must be recomputed (§7a).

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
- **Screen effects to switch off in VR** (the standing rule; flat play untouched): `AllowBlur`, `AllowDOF`,
  `AllowCutsceneDOF`, `AllowScatterDOF`, `AllowMotionBlur`, `AllowVignette`, probably `AllowSharpen` — all plain keys
  in the live `Documents\Witcher 2\Config\User.ini` `[inferred-static]`; none flipped and checked by eye yet.
  `AllowRain` and `AllowShafts` are world effects and stay. Low-health tint, damage flashes and screen blood are
  not covered by these keys `[hypothesis]`; still to find.
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
- ~~The Steam DRM wrapper hides the real start of the program~~ **Resolved 2026-10-16:** a copy unpacks statically (§3). ⚠️ Note this is **not** a general block: ordinary strings, the class registry and the import table all read fine off disk, as the 2026-09-14 pass showed.
- ⭐ **The scripts ship with the game** (`base_scripts.dzip`), and REDengine has a large public modding and research community `[reported]`. Much of this engine may already be explained in public, which is `/gr`'s to collect.
- Cyberpunk 2077's VR work is on a much later REDengine generation `[reported]`, so its lessons may carry over in method more than in detail `[hypothesis]`.

## Inbox folds, 2026-09-29

**The editor could drive the game camera over the network (`/gr` 2026-09-29).** A Witcher 2 graphics programmer's 2014 post says the engine carried a network command protocol (on the script debugger's connection) through which the editor set the camera's position, rotation, near/far and FOV `[reported]`; retail survival unknown. Cheap static check: Winsock `bind`/`listen`/`accept` imports and listener strings near the script-debugger code; none means retire the lead `[hypothesis]`. Topic: `external-research/topics/2026-09-29-witcher-2-had-a-network-camera-link-to-its-editor.md`.

