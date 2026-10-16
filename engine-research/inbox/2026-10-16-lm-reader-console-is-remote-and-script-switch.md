# The retail "debug console" has no keyboard path; a `-script` switch runs one exec command after load

From: `/lm` static reader, 2026-10-16, on the Steamless-unpacked copy. Supersedes: dossier §9 row
"opening the console" (the `IK_Tilde=(GameKey="CHEAT_Console")` idea).

- **`CHEAT_Console` is not an input action.** It is value 0 of the script enum `ECheats`
  (`CHEAT_Console, CHEAT_FreeCamera, CHEAT_DebugPages, CHEAT_InstantKill, CHEAT_Teleport,
  CHEAT_MovementOnPhysics, CHEAT_TimeScaling`, registered at `0x004127EE`). Shipped key names are all
  `GI_*` `[inferred-static]`. Binding a key to `CHEAT_Console` should do nothing `[hypothesis]`.
- **`theGame.IsCheatEnabled()` is stubbed: its native (`0x00AA75D3`) always returns false**
  `[inferred-static]`.
- **`CDebugConsole` is an on-screen log plus a REMOTE command receiver**, not a typed console. RTTI bases:
  `IDebugChannelReciever` + `IOutputDevice`. Built unconditionally at start-up (`0x00AC9952`, global
  `0x0160C6F0`). Its packet handler (`0x00AA353D`) runs a command when a debug-channel packet named
  `ConsoleCommand` arrives; it shows `Warning`/`Error`/`Script` log lines. Its command-line-history
  routines (`0x00AA33DF`, `0x00AA341A`) have no callers `[inferred-static]`.
- **`CGameDebugMenu` (an `IViewportHook`) is never built**: its vtable `0x00E76B44` is referenced only by
  its own destructor `[inferred-static]`. The script hooks `DebugMenuEntriesGet/EntrySelect` in
  `game/debug.ws` are not named anywhere in the exe.
- **No `DBGConsoleOn` or similar ini key exists in the exe** (searched ASCII and UTF-16) `[inferred-static]`.
- ⭐ **Command line switches** parsed at `0x00AC92FD`: `-debugdata`, `-texres`, `-width`, `-height`,
  `-window`, `-assert`, `-log`, `-script`, `-vdb` `[inferred-static]`.
  - **`-script "<Cmd>()"`** stores the next argument (`0x01612274`) and, if it contains `(` and `)`, arms a
    one-shot flag. Once a world is loaded and the game is active, `0x00B1FF61` runs it ONCE through the
    same executor the console uses (`0x00ABBE18`: splits on space ( ) , and calls a script function whose
    exec/flag bit is set). So `witcher2.exe -script "FreeCamera()"` should toggle the free camera after a
    save loads, with no console `[hypothesis]` — the cheapest live test.
  - `-vdb` only sets a byte nothing reads (dead in retail) `[inferred-static]`.
- The other route for commands is the network debug channel (see
  `2026-10-16-lm-reader-debug-channel-ports-47000-47001.md`).
