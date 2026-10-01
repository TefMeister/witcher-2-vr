"""Pack a folder into a Witcher 2 .dzip archive (DZIP v2), the reverse of dzip_extract.py. No game needed.

Layout written (as dzip_extract.py reads it, community-documented DZIP v2):
  header: 'DZIP', u32 version 2, u32 fileCount, u32 unknown, u64 tableOffset, u64 hash
  file data: per file, u32 chunk offsets (one per 64 KiB of output, relative to the file's start), then LZF chunks
  table: per file u16 nameLen, name + NUL, u64 time, u64 unpackedSize, u64 offset, u64 packedSize

The chunks are LZF streams made only of literal runs (control bytes 0..31): valid LZF that any LZF decoder reads,
just not smaller. Simple and impossible to get subtly wrong; script archives are tiny anyway.

⚠️ NOT KNOWN (2026-10-01): what the header's `unknown` u32 and the u64 `hash` must hold. Real archives carry
values with no formula found; the exe that reads them is encrypted on disk (Steam DRM), so the check cannot be read
statically. Both are written as 0 unless --unknown / --hash are given. The first flat run that loads our archive
answers whether the game cares.

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


def build(src, unknown=0, hash_=0):
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
    header = b"DZIP" + struct.pack("<3I", 2, len(entries), unknown) + struct.pack("<2Q", header_len + len(body), hash_)
    return bytes(header + body + table), entries


def main():
    args = sys.argv[1:]
    src, out = args[0], args[1]
    unknown = int(args[args.index("--unknown") + 1], 0) if "--unknown" in args else 0
    hash_ = int(args[args.index("--hash") + 1], 0) if "--hash" in args else 0
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
