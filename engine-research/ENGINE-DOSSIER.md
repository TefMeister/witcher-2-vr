# Engine Dossier — The Witcher 2: Assassins of Kings (REDengine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, first static look (2026-09-13); the game has not been launched yet. · **VR-readiness verdict:** TBD. Nothing seen so far rules it out.

## 1. Identity
- Game / build / version: The Witcher 2: Assassins of Kings Enhanced Edition, Steam app 20920, fully downloaded. Game exe `bin\witcher2.exe` (linked 2013-05-09, a late patch build); `Launcher.exe` and `bin\Configurator.exe` sit beside it.
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: CD Projekt Red's REDengine, in its first version `[reported]`. Havok and Scaleform strings are present in the exe `[inferred-static 2026-09-13]`. Game logic is script: `CookedPC\base_scripts.dzip` and `compiledscripts.w2scripts` ship with the game.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.):
- Distinctive file formats / build tags / symbol naming: `.dzip` archives in `CookedPC\` (`pack0.dzip` alone is 10.5 GB, plus one per DLC), `.w2speech` and `.w2strings` language files, `staticShader.cache`. Not yet looked at.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **32-bit** (PE32), `witcher2.exe` 15.7 MB, linked 2013-05-09. Ordinary sections plus `.bind` (the Steam DRM wrapper's section) and a small `PSFD00` section of unknown purpose `[inferred-static 2026-09-13]`.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: Direct3D 9: `d3d9.dll` and `d3dx9_39.dll` are named in the exe `[inferred-static 2026-09-13]`. XInput 1.3, DirectInput 8 and NVAPI strings are also present.
- Developer console / cvar system present? how opened?: not yet investigated.

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

## 12. Open risks toward the North Star
- The Steam DRM wrapper hides the real start of the program until it has unpacked itself, so some static reading may have to wait for a running copy.
- ⭐ **The scripts ship with the game** (`base_scripts.dzip`), and REDengine has a large public modding and research community `[reported]`. Much of this engine may already be explained in public, which is `/gr`'s to collect.
- Cyberpunk 2077's VR work is on a much later REDengine generation `[reported]`, so its lessons may carry over in method more than in detail `[hypothesis]`.
