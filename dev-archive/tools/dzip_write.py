"""Pack a folder into a Witcher 2 .dzip archive (DZIP v2), the reverse of dzip_extract.py. No game needed.

Layout written (as dzip_extract.py reads it, community-documented DZIP v2):
  header: 'DZIP', u32 version 2, u32 fileCount, u32 unknown, u64 tableOffset, u64 hash
  file data: per file, u32 chunk offsets (one per 64 KiB of output, relative to the file's start), then LZF chunks
  table: per file u16 nameLen, name + NUL, u64 time, u64 unpackedSize, u64 offset, u64 packedSize

The chunks are LZF streams made only of literal runs (control bytes 0..31): valid LZF that any LZF decoder reads,
just not smaller. Simple and impossible to get subtly wrong; script archives are tiny anyway.

THE HASH IS CHECKED (2026-10-16, /lm): the game recomputes a hash over the file table and refuses the archive on a
mismatch (a repack with a copied hash gave a black screen instead of the menu; the same repack with the hash
recomputed loaded). The hash: 64-bit FNV-1a style, prime 0x100000001B3, start 0xFFFFFFFF; per table entry, in
order: each name byte as a signed char, then strlen(name), then time, unpackedSize, offset, packedSize
[verified-numerically 2026-10-16, n=21 shipped archives]. build() computes it unless --hash is given.
The `unknown` u32 is never read by the game [inferred-static]; 0 is fine.

Usage: python dzip_write.py SRC_FOLDER OUT.dzip [--unknown 0xNN] [--hash 0xNN] [--check]
       (paths inside the archive use backslashes, relative to SRC_FOLDER, e.g. game\\player\\player.ws)
       --check re-reads the result with dzip_extract.py's reader and compares every file byte for byte.
"""
import struct
import sys
import time
from pathlib import Path

CHUNK = 0x10000          # output bytes per chunk, as the reader expects
LITERAL_MAX = 32         # an LZF literal run carries 1..32 bytes (control byte = length - 1)
FILETIME_EPOCH = 116444736000000000   # 1601-01-01 to 1970-01-01 in 100 ns units
HASH_PRIME = 0x100000001B3
HASH_START = 0x00000000FFFFFFFF
MASK64 = (1 << 64) - 1


def lzf_literals(block):
    out = bytearray()
    for i in range(0, len(block), LITERAL_MAX):
        run = block[i:i + LITERAL_MAX]
        out.append(len(run) - 1)
        out += run
    return bytes(out)


def pack_file(data):
    """Chunk-offset table + LZF chunks for one file; offsets are relative to the file's own start."""
    chunks = [lzf_literals(data[i:i + CHUNK]) for i in range(0, len(data), CHUNK)]
    table_len = 4 * len(chunks)
    offs, pos = [], table_len
    for c in chunks:
        offs.append(pos)
        pos += len(c)
    return struct.pack(f"<{len(offs)}I", *offs) + b"".join(chunks)


def table_hash(entries, now_or_times):
    """The hash the game checks: over every table entry, in table order (see the docstring)."""
    h = HASH_START
    times = now_or_times if isinstance(now_or_times, list) else [now_or_times] * len(entries)
    for (name, size, off, packed), t in zip(entries, times):
        raw = name.encode("latin-1")
        for v in [b - 256 if b >= 128 else b for b in raw] + [len(raw), t, size, off, packed]:
            h = ((h ^ (v & MASK64)) * HASH_PRIME) & MASK64
    return h


def build(src, unknown=0, hash_=None):
    files = sorted(p for p in Path(src).rglob("*") if p.is_file())
    now = int(time.time() * 10_000_000) + FILETIME_EPOCH
    header_len = 4 + 4 * 3 + 8 * 2
    body = bytearray()
    entries = []
    for p in files:
        data = p.read_bytes()
        blob = pack_file(data)
        entries.append((str(p.relative_to(src)).replace("/", "\\"), len(data), header_len + len(body), len(blob)))
        body += blob
    table = bytearray()
    for name, size, off, packed in entries:
        raw = name.encode("latin-1") + b"\0"
        table += struct.pack("<H", len(raw)) + raw + struct.pack("<4Q", now, size, off, packed)
    if hash_ is None:
        hash_ = table_hash(entries, now)
    header = b"DZIP" + struct.pack("<3I", 2, len(entries), unknown) + struct.pack("<2Q", header_len + len(body), hash_)
    return bytes(header + body + table), entries


def main():
    args = sys.argv[1:]
    src, out = args[0], args[1]
    unknown = int(args[args.index("--unknown") + 1], 0) if "--unknown" in args else 0
    hash_ = int(args[args.index("--hash") + 1], 0) if "--hash" in args else None
    blob, entries = build(src, unknown, hash_)
    Path(out).write_bytes(blob)
    print(f"wrote {out}: {len(entries)} file(s), {len(blob)} bytes")
    if "--check" in args:
        sys.path.insert(0, str(Path(__file__).parent))
        import dzip_extract as rd
        version, got = rd.read_entries(blob)
        bad = 0
        for (name, size, off, _packed), (ename, _s, _o, _p) in zip(got, entries):
            original = (Path(src) / ename.replace("\\", "/")).read_bytes()
            if name != ename or rd.extract(blob, size, off) != original:
                bad += 1
                print(f"MISMATCH {name}")
        print(f"check: DZIP v{version}, {len(got)} file(s) read back, {bad} mismatch(es)")
        sys.exit(1 if bad or len(got) != len(entries) else 0)


if __name__ == "__main__":
    main()
