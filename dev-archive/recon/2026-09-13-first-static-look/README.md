# First static look (2026-09-13)

Read from the installed Steam copy on the home PC, without launching the game. Every claim
below is `[inferred-static 2026-09-13]` unless tagged otherwise: it comes from reading file headers
and strings, not from running anything.

- **Install:** `the witcher 2`, 19 GB.
- **Identity:** The Witcher 2: Assassins of Kings Enhanced Edition, Steam app 20920, fully downloaded. Game exe `bin\witcher2.exe` (linked 2013-05-09, a late patch build); `Launcher.exe` and `bin\Configurator.exe` sit beside it.
- **Engine:** CD Projekt Red's REDengine, in its first version `[reported]`. Havok and Scaleform strings are present in the exe `[inferred-static 2026-09-13]`. Game logic is script: `CookedPC\base_scripts.dzip` and `compiledscripts.w2scripts` ship with the game.
- **Binary:** **32-bit** (PE32), `witcher2.exe` 15.7 MB, linked 2013-05-09. Ordinary sections plus `.bind` (the Steam DRM wrapper's section) and a small `PSFD00` section of unknown purpose `[inferred-static 2026-09-13]`.
- **Renderer:** Direct3D 9: `d3d9.dll` and `d3dx9_39.dll` are named in the exe `[inferred-static 2026-09-13]`. XInput 1.3, DirectInput 8 and NVAPI strings are also present.
- **Protection:** The Steam DRM wrapper (`.bind`); no Denuvo or SecuROM string found `[inferred-static 2026-09-13]`. Not tested live. The exe contains the string `DebugConsole`, so a developer console may exist; unchecked.
- **Other files:** `.dzip` archives in `CookedPC\` (`pack0.dzip` alone is 10.5 GB, plus one per DLC), `.w2speech` and `.w2strings` language files, `staticShader.cache`. Not yet looked at.

## Method

PE headers read with a short script: machine type, link timestamp, section names and sizes.
Then a case-insensitive search of each binary for renderer DLL names (`d3d9`, `d3d11`, `d3d12`,
`dxgi`, `vulkan-1`, `opengl32`), protection markers (`denuvo`, `securom`, `.bind`) and middleware
names. A string match shows a name is present in the file, not that the code path is used.

## Risks noted

- The Steam DRM wrapper hides the real start of the program until it has unpacked itself, so some static reading may have to wait for a running copy.
- ⭐ **The scripts ship with the game** (`base_scripts.dzip`), and REDengine has a large public modding and research community `[reported]`. Much of this engine may already be explained in public, which is `/gr`'s to collect.
- Cyberpunk 2077's VR work is on a much later REDengine generation `[reported]`, so its lessons may carry over in method more than in detail `[hypothesis]`.
