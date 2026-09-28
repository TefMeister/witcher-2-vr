"""Unpack a Witcher 2 .dzip archive (e.g. CookedPC/base_scripts.dzip) without the game running.

Layout (community-documented DZIP v2, checked against base_scripts.dzip):
  header: 'DZIP', u32 version (2), u32 fileCount, u32 unknown, u64 tableOffset, u64 hash
  table at tableOffset, per file: u16 nameLen, name (nameLen bytes, NUL-terminated), u64 time,
          u64 unpackedSize, u64 offset, u64 packedSize
  file data at offset: u32 chunk offsets (one per 64 KiB of output, relative to the file's offset;
          the first offset also tells how many there are), then LZF-compressed chunks.
The output is game content: keep it OUT of git.

Usage: python dzip_extract.py base_scripts.dzip OUTDIR [--list]
"""
import struct
import sys
from pathlib import Path

CHUNK = 0x10000


def lzf_decompress(src, out_len):
    out = bytearray()
    i = 0
    n = len(src)
    while i < n and len(out) < out_len:
        ctrl = src[i]
        i += 1
        if ctrl < 32:
            ln = ctrl + 1
            out += src[i:i + ln]
            i += ln
        else:
            ln = ctrl >> 5
            ref = len(out) - ((ctrl & 0x1F) << 8) - 1
            if ln == 7:
                ln += src[i]
                i += 1
            ref -= src[i]
            i += 1
            ln += 2
            for _ in range(ln):
                out.append(out[ref])
                ref += 1
    return bytes(out)


def read_entries(data):
    if data[:4] != b"DZIP":
        raise SystemExit("not a DZIP archive")
    version, count, _unk = struct.unpack_from("<3I", data, 4)
    table = struct.unpack_from("<Q", data, 16)[0]
    p = table
    entries = []
    for _ in range(count):
        nlen = struct.unpack_from("<H", data, p)[0]
        name = data[p + 2:p + 2 + nlen].rstrip(b"\0").decode("latin-1")
        p += 2 + nlen
        _time, size, off, packed = struct.unpack_from("<4Q", data, p)
        p += 32
        entries.append((name, size, off, packed))
    return version, entries


def extract(data, size, off):
    nchunks = (size + CHUNK - 1) // CHUNK
    offs = list(struct.unpack_from(f"<{nchunks}I", data, off)) if nchunks else []
    out = bytearray()
    for k, co in enumerate(offs):
        end = offs[k + 1] if k + 1 < len(offs) else None
        src = data[off + co:off + end] if end else data[off + co:off + co + CHUNK + CHUNK // 8 + 64]
        out += lzf_decompress(src, min(CHUNK, size - len(out)))
    return bytes(out[:size])


def main():
    data = Path(sys.argv[1]).read_bytes()
    version, entries = read_entries(data)
    print(f"DZIP v{version}, {len(entries)} files")
    if "--list" in sys.argv:
        for name, size, _off, _packed in entries:
            print(f"{size:9d}  {name}")
        return
    out = Path(sys.argv[2])
    bad = 0
    for name, size, off, _packed in entries:
        blob = extract(data, size, off)
        if len(blob) != size:
            bad += 1
        dest = out / name.replace("\\", "/")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob)
    print(f"extracted {len(entries)} files, {bad} short")


if __name__ == "__main__":
    main()
