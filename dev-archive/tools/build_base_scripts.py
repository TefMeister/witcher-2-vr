"""Build a replacement CookedPC\\base_scripts.dzip from YOUR installed one, with our script patches applied.

Why a full replacement (2026-10-16, /lm): the game compiles its scripts at start-up from base_scripts.dzip only
(plus a scripts.dzip inside each DLC folder) [inferred-static]; a separate zzz_*.dzip holding player.ws had no effect
[verified-live 2026-10-16, n=1]. The archive's table hash must be right or the game refuses it and shows a black
screen with an empty HUD instead of the menu [verified-live 2026-10-16, n=1]; dzip_write.table_hash computes it.

Every script is copied in the original order; only the patched ones change. Patches today: the camera readout
from build_vrcamprobe.py (VRCAM line in the HUD once a second).

The output is game content: install it, never commit it. Back up the original first.

Usage: python build_base_scripts.py "<game>\\CookedPC\\base_scripts.dzip" OUT.dzip [--nopatch]
       Point it at an ORIGINAL archive (your backup), not one this tool already wrote.
       --nopatch repacks every script unchanged (the control run).
"""
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dzip_extract as rd      # noqa: E402
import dzip_write as wr        # noqa: E402
import build_vrcamprobe as bp  # noqa: E402

HEADER_LEN = 32


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    nopatch = "--nopatch" in sys.argv
    data = src.read_bytes()
    _version, entries = rd.read_entries(data)
    if not nopatch and bp.TAG in rd.extract(data, *[(s, o) for n, s, o, _ in entries
                                                     if n.lower() == bp.SCRIPT.lower()][0]).decode("latin-1"):
        raise SystemExit("this archive is already patched - point at the original backup")
    body = bytearray()
    new_entries = []
    patched = 0
    for name, size, off, _packed in entries:
        content = rd.extract(data, size, off)
        if name.lower() == bp.SCRIPT.lower() and not nopatch:
            content = bp.patch(content.decode("latin-1")).encode("latin-1")
            patched += 1
        blob = wr.pack_file(content)
        new_entries.append((name, len(content), HEADER_LEN + len(body), len(blob)))
        body += blob
    if not nopatch and patched != 1:
        raise SystemExit(f"{bp.SCRIPT} patched {patched} times, expected once - nothing written")
    now = int(time.time() * 10_000_000) + wr.FILETIME_EPOCH
    table = bytearray()
    for name, size, off, packed in new_entries:
        raw = name.encode("latin-1") + b"\0"
        table += struct.pack("<H", len(raw)) + raw + struct.pack("<4Q", now, size, off, packed)
    hash_ = wr.table_hash(new_entries, now)
    header = b"DZIP" + struct.pack("<3I", 2, len(new_entries), 0) + struct.pack("<2Q", HEADER_LEN + len(body), hash_)
    blob = bytes(header + body + table)
    out.write_bytes(blob)
    # read back: same names in the same order, every file identical to what went in
    _v, back = rd.read_entries(blob)
    bad = sum(1 for (n1, s1, o1, _), (n2, s2, o2, _) in zip(entries, back)
              if n1 != n2 or (rd.extract(blob, s2, o2) != rd.extract(data, s1, o1)
                              and not (n1.lower() == bp.SCRIPT.lower() and not nopatch)))
    print(f"wrote {out}: {len(back)} files, {patched} patched, {bad} unexpected differences, hash {hash_:#018x}")
    sys.exit(1 if bad or len(back) != len(entries) else 0)


if __name__ == "__main__":
    main()
