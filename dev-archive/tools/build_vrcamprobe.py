"""Build zzz_vrcamprobe.dzip: the player script with a once-a-second camera readout, from YOUR installed game.

What it adds to game\\player\\player.ws (two insertions, nothing removed):
  1. in CPlayer.OnSpawned, right after `m_isSpawned = true;`: start a repeating 1 s timer;
  2. before `timer function clearHudTextFieldTimer`: the timer, which reads theCamera.GetCameraMatrixWorldSpace()
     and GetFov(), and writes "VRCAM pos <x y z w> fwd <x y z w> fov <deg>" to the script log AND to the HUD's own
     centre text (theHud.m_hud.setCSText), so a screenshot shows it even if the shipping build drops Log().
The game's script is read from CookedPC\\base_scripts.dzip and never committed; only this recipe is. Each anchor
must occur exactly once or nothing is built.

⚠️ NOT KNOWN: whether the game loads a script that a later archive overrides (the one community archive installed
here, abetterui.dzip, carries no scripts), whether CookedPC\\compiledscripts.w2scripts must be removed first so the
scripts are recompiled, and what the DZIP header's unknown/hash fields must hold (dzip_write.py). The first flat run
answers all three.

Usage: python build_vrcamprobe.py "<game>\\CookedPC" OUT_FOLDER     -> OUT_FOLDER\\zzz_vrcamprobe.dzip
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dzip_extract as rd   # noqa: E402
import dzip_write as wr     # noqa: E402

SCRIPT = "game\\player\\player.ws"
ARCHIVE_NAME = "zzz_vrcamprobe.dzip"      # sorts after every shipped archive
TIMER_PERIOD_S = "1.0f"
TAG = "VR camera probe (witcher-2-vr, 2026-10-01)"

START_ANCHOR = "\t\tm_isSpawned = true;\r\n"
START_INSERT = f"\t\tAddTimer( 'vrCamProbeTimer', {TIMER_PERIOD_S}, true );   // {TAG}\r\n"

TIMER_ANCHOR = "\ttimer function clearHudTextFieldTimer( timeDelta : float )\r\n"
TIMER_INSERT = "".join(line + "\r\n" for line in [
    f"\t// {TAG}: once a second, what the scripts see of the camera.",
    "\ttimer function vrCamProbeTimer( timeDelta : float )",
    "\t{",
    "\t\tvar m : Matrix;",
    "\t\tvar line : string;",
    "\t\tm = theCamera.GetCameraMatrixWorldSpace();",
    "\t\tline = \"VRCAM pos \" + VecToString( m.W ) + \" fwd \" + VecToString( m.Y ) + \" fov \" + "
    "FloatToString( theCamera.GetFov() );",
    "\t\tLog( line );",
    "\t\ttheHud.m_hud.setCSText( \"\", line );",
    "\t}",
    "",
])


def patch(text):
    for anchor in (START_ANCHOR, TIMER_ANCHOR):
        n = text.count(anchor)
        if n != 1:
            raise SystemExit(f"anchor found {n} times, expected once: {anchor.strip()!r} - nothing built")
    text = text.replace(START_ANCHOR, START_ANCHOR + START_INSERT)
    return text.replace(TIMER_ANCHOR, TIMER_INSERT + TIMER_ANCHOR)


def main():
    cooked, out = Path(sys.argv[1]), Path(sys.argv[2])
    data = (cooked / "base_scripts.dzip").read_bytes()
    _version, entries = rd.read_entries(data)
    hit = [e for e in entries if e[0].lower() == SCRIPT.lower()]
    if len(hit) != 1:
        raise SystemExit(f"{SCRIPT} not found once in base_scripts.dzip")
    name, size, off, _packed = hit[0]
    original = rd.extract(data, size, off).decode("latin-1")
    patched = patch(original)
    stage = out / "stage"
    dest = stage / name.replace("\\", "/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(patched.encode("latin-1"))
    blob, files = wr.build(stage)
    (out / ARCHIVE_NAME).write_bytes(blob)
    added = len(patched.splitlines()) - len(original.splitlines())
    print(f"built {out / ARCHIVE_NAME}: {name}, {added} lines added, {len(files)} file in the archive")


if __name__ == "__main__":
    main()
