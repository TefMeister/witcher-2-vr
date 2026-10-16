# witcher2.exe carries SteamStub Variant 2.1, and a COPY unpacks statically with Steamless

From: `/lm` static reader, 2026-10-16. Answers the dossier §12 risk and the board row that said the console
search "needs the game running".

- A copy of `bin\witcher2.exe` (sha256 `cb9fbc9c…a55fe8`, identical to the installed file) was run through
  Steamless v3.1.0.5 CLI (release zip sha256 `e3e2d22e…2dc4f5`, the same build Alice used). It reported
  **SteamStub Variant 2.1 (x86)** and unpacked in seconds, no launch `[measured 2026-10-16]`.
  (Alice's exe was Variant 3.1; this one is older.)
- Before → after `[measured 2026-10-16]`: `.text` entropy 8.00 → **6.79**; 16-byte `int3` padding runs
  0 → 70; `.bind` removed; entry point `0x029262EE` (in `.bind`) → **`0x0066F59D`** (in `.text`).
  Other sections unchanged; base `0x400000`, no ASLR.
- The unpacked copy lives only on this PC (git-ignored) in the private `staging` repo folder
  `witcher-2-vr/unpacked-exe-2026-10-16/`, beside the small Python helpers used to read it. Never commit it.
- Every exe-side DZIP question and the console question are now `[PD]` work.
- Correction to the 2026-10-01 note: `.rdata` was never encrypted (entropy 5.05 packed and unpacked); the
  string `DZIP` was "missing" because the code compares it as the number `0x50495A44`.
