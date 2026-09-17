# The Witcher 2: readable scripts, official REDkit, camera mods, and an unconfirmed console route

**Status:** 🆕 new · **Priority:** high — it bears directly on both `[PD]` rows on the board (open
`base_scripts.dzip`; find how `CDebugConsole` opens).

## What was found

1. **The script archive opens with a public tool.** **Gibbed RED Tools** (Nexus mod 768) unpack and
   repack `.dzip` archives, `base_scripts.dzip` included; mod-merging guides use exactly that workflow
   `[reported]`. So the board row "see whether the shipped scripts are readable" has a known route.
2. **CD PROJEKT RED's own REDkit exists for this game** `[reported]`: an official toolset with the
   Witcher Script Studio (an IDE with script debugging and profiling) and a command-line tool to cook
   and uncook game files. Its wiki is online at redkitwiki.cdprojektred.com.
3. **The camera is already moved by script mods.** **Enhanced Camera** (Nexus 724) repositions the
   camera, and **First Person Camera (FPC)** (Nexus 1128), a preset on JackBaldy's original, puts it in
   first person, with known bugs in fist fights, resets after cutscenes, and doors `[reported]`. Guides
   describe these as edits inside `base_scripts.dzip` `[reported]`. That is good evidence that camera
   placement is script-reachable in this engine `[hypothesis]`, which matters for head tracking.
4. **Console: no Witcher 2 method found.** The Witcher 3 opens its debug console with
   `DBGConsoleOn=true` under `[General]` in `bin\config\base\general.ini`, documented on CD PROJEKT
   RED's own Witcher 3 REDkit wiki `[reported]`. Whether any similar key exists for The Witcher 2 is
   **unknown**; it is a cheap thing to try, but a different engine generation `[hypothesis]`. A
   GameFAQs thread about the Witcher 2 console returned HTTP 403 to the automated fetch, so that is
   **not** a negative.

## Why it matters here

The dossier found `CDebugConsole`, `CGameDebugMenu` and `CFreeCamera` as real classes, but not how
to open them. Script-level camera control plus official script tooling could make head tracking a
script job before any native hooking.

## Next steps

- `[PD]`: unpack `base_scripts.dzip` with Gibbed RED Tools and search the scripts for the camera
  classes the dossier names, and for any console or debug-menu toggle.
- `[FLAT]`, cheap: try a `DBGConsoleOn`-style key in the game's `bin\config\` ini files, alongside the
  board's `CustomRenderingSettings=1` test.
- Read the FPC mod page's description online to learn which script values it changes. Do not
  download it to look inside.

## Sources

- https://www.nexusmods.com/witcher2/mods/768
- https://witcher-games.fandom.com/wiki/Extracting_The_Witcher_2_files
- https://redkitwiki.cdprojektred.com/redkit.htm
- https://www.nexusmods.com/witcher2/mods/724
- https://www.nexusmods.com/witcher2/mods/1128
- https://cdprojektred.atlassian.net/wiki/spaces/W3REDkit/pages/36208717/WS+Enable+debug+console+in-game
