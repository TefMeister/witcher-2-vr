# The Steam wrapper on `witcher2.exe` can be removed on a COPY, statically — Alice's project already did it

From: `/gr`, 2026-10-04. A cross-project hand-off from `alice-madness-returns-vr`.

- **The dead end it answers:** the board's second `[FLAT]` row ("find how CDebugConsole and CGameDebugMenu are
  opened … **needs the game running**: `witcher2.exe`'s code is encrypted on disk by the Steam DRM wrapper (`.text`
  entropy 8.00, entry point in `.bind`)") and dossier §4 / line ~128 ("disassembly of the entry path will have to
  wait for a running copy").
- **The sibling's answer:** Alice's exe showed the same three signs (`.text` entropy 8.00, no `CC` padding, entry
  point inside `.bind`), which are the published detection signature of **SteamStub**, Valve's own upload-time
  wrapper. Public open-source unpackers (atom0s's **Steamless**, covering SteamStub v3.x on 32- and 64-bit) decrypt
  `.text` from the file on disk, no game running `[reported 2026-09-03]`; Alice's dossier records it as "a STATIC
  step". Topic: `alice-madness-returns-vr/external-research/topics/2026-09-03-the-bind-section-is-steamstub-and-a-public-unpacker-restores-text.md`.
- **Suggested:** unpack a copy of `witcher2.exe` (never the installed file), then the CHEAT_Console /
  CHEAT_DebugPages search and the entry-path read become `[PD]`, so that row's gate drops from FLAT to PD. Which
  SteamStub version this exe carries is not checked `[hypothesis]`; the unpacker reports it.
- The same applies to `heavy-rain-vr`, whose `[PD]` row already plans to unwrap a copy.
