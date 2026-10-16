# The DZIP header hash is checked, and it covers the whole file table — that is why repacks fail

From: `/lm` static reader, 2026-10-16. Source: a Steamless-unpacked COPY of `witcher2.exe` (see
`2026-10-16-lm-reader-steamstub-2-1-unpacked.md`). Scripts in the private `staging` repo,
`witcher-2-vr/unpacked-exe-2026-10-16/` (`dzip_hash_check.py` holds the algorithm).

## What the reader checks

- Two open routines share one small DZIP library inside the exe: `0x0068D430` (no key; used by the plain
  package class, slot 1 of `CDlcPackage`'s vtable at `0x00ABAE22`, and by the base-scripts load) and
  `0x0068D6B0` (takes a key string; used by `CDlcPackage` at `0x00B25CC4`, first with the registry
  `SerialNumber`, then with the literal `NODRM-NODRM-NODRM-NODRM`, and it XOR-decrypts each entry name with
  a key stream) `[inferred-static]`.
- Both read the 32-byte header, require magic `DZIP` and version >= 2, read fileCount and tableOffset,
  read the table, then **recompute a hash over the table and compare it with the header's u64 at +0x18;
  on mismatch they close the archive and return NULL** (`0x0068D5D8`, `0x0068D87D`) `[inferred-static]`.
- The hash (`0x0068E310`): 64-bit FNV-1a style, prime `0x100000001B3`, start `0x00000000FFFFFFFF`; per entry
  in table order: each name byte (signed char, sign-extended), then strlen(name), then the entry's time,
  unpackedSize, offset and packedSize u64s `[verified-numerically 2026-10-16, n=21]` — it reproduces the
  stored hash of all 21 shipped archives in `CookedPC` (base_scripts, pack0, arena, abetterui, every DLC).
- **So per-entry timestamps, offsets and packed sizes all feed the hash.** A repack with fresh FILETIMEs
  and literal-only chunks changes offsets/sizes, so copying the original hash makes it fail: the main
  session's `base_scripts_repack.dzip` computes `0x4715FCE8E8E3A2EF` against a stored `0xDDEFF36ACFD63833`
  `[verified-numerically 2026-10-16, n=1]`. That matches the black screen seen live today; that the
  mismatch is the cause is `[hypothesis]` until a repack with a recomputed hash loads.
- The `unknown` u32 at +0x0C is **never read** by either open routine; the engine's own writer
  (`0x0068E410`) never initialises it, so shipped archives carry leftover stack bytes (several read
  `0x003FF500`) `[inferred-static]`. Any value is fine.
- Chunk decode: `0x0068F3B0` is FastLZ's dispatcher (level = first byte >> 5, plus 1; level 1 and 2 only).
  Our literal-run chunks start with a byte <= 31, i.e. level 1, which is LZF-compatible literal runs
  `[inferred-static]`. The chunk-offset table is read as ceil(unpacked/65536) u32s relative to the file's
  start, with packedSize used as the end of the last chunk — what `dzip_write.py` writes `[inferred-static]`.

## Mount order and overrides (data files)

`0x00B1B1B9`: first `pack0.dzip` … `pack9.dzip` (pack0 without override, pack1+ with), then every other
`*.dzip` and `*.dlc` in `CookedPC` in directory-listing order, each with override on, skipping names
already mounted. File registration (`0x00B1A1FC`) replaces an existing path only when override is on,
so **a later archive wins** (alphabetical on NTFS, so `zzz_` beats `aaa_`) `[inferred-static]`.

## Scripts are compiled at start-up, from fixed archives

`0x00AA69AE` ("Compiling scripts..."): scripts come from a package opened directly on
`CookedPC\base_scripts.dzip`, plus a `scripts.dzip` inside each registered DLC folder (`0x00ABED95`);
compile errors raise "There were errors compiling scripts" `[inferred-static]`. A dev path loads a loose
`scripts\` folder when a flag at `0x01608613` is set (what sets it is unknown). A root-level
`zzz_*.dzip` containing `player.ws` is mounted as DATA, which the script compiler does not appear to read
`[hypothesis]`. **No string `compiledscripts` or `w2scripts` exists in the exe**, so
`compiledscripts.w2scripts` looks unused by this build `[inferred-static]`.

## Suggested next step

Rebuild the repack, then run `dzip_hash_check.py --fix <in> <out>` (or compute the hash in the builder)
and swap it in. If the menu comes back, the hash was the gate.
