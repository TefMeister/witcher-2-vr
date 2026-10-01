# 2026-10-01 (`/pd`, dev PC): a script archive that shows the camera once a second

**The game was not launched, and nothing here has been run inside it. Nothing was installed.**

## What was built (`dev-archive/tools/`)

- **`dzip_write.py`**, the reverse of our reader: packs a folder into a DZIP v2 archive. Chunks are LZF made of
  literal runs only (valid LZF, no compression), so the format cannot be subtly wrong. **Round trip of all 460 game
  scripts through writer and reader: 0 mismatches** `[verified-numerically 2026-10-01, n=460 files]`.
- **`build_vrcamprobe.py`**: reads `game\player\player.ws` from the player's own `base_scripts.dzip`, adds 12 lines
  at two anchors that must each occur exactly once (a repeating 1 s timer started in `CPlayer.OnSpawned` after
  `m_isSpawned = true;`, and the timer itself before `clearHudTextFieldTimer`), and packs it as
  `zzz_vrcamprobe.dzip`. The timer reads `theCamera.GetCameraMatrixWorldSpace()` and `GetFov()` and writes
  `VRCAM pos … fwd … fov …` to the script log **and** to the HUD's centre text, so a screenshot shows it even if a
  shipping build drops `Log()`. The game's script is never committed; only the recipe is.

## Not known, and what answers it

- **Does the game load a script from a later archive?** The only community archive installed here
  (`abetterui.dzip`) carries interface files, no scripts, so it proves nothing for scripts.
- **Must `CookedPC\compiledscripts.w2scripts` (1.9 MB) be set aside** so the scripts are recompiled?
- **What the DZIP header's `unknown` u32 and u64 `hash` must hold.** Real archives carry values with no formula
  found; the exe that checks them is encrypted on disk by the Steam DRM wrapper (not even the string `DZIP` is
  visible), so this cannot be read statically. We write 0.

The flat run answers all three: if `VRCAM` text appears in the HUD, the archive loaded and the scripts compiled.

## Why it is not installed

Witcher 2 has never been started on this PC. The first-launch rule is: runs as shipped → runs with our file →
windowed, before anything else. The archive goes in after that first plain launch.
