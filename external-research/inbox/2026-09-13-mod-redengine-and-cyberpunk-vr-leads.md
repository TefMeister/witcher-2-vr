# Leads for the first `/gr` pass: public REDengine research and the Cyberpunk 2077 VR work

From: modding session, home PC, 2026-09-13, at project start. No research has been done yet; this is
a hand-off of what the user wants studied, so the first `/gr` run on this project starts from it.

## What the user asked for

Tefa, verbatim: *"This one, as tough as it is, there is plenty of info about redengine out there,
and hopefully we can study the latest Cyberpunk 2077 mod that has all sorts of "impossible" things
done."*

## Leads

1. **Public REDengine research, Witcher 2 generation first.** The game ships its scripts
   (`CookedPC\base_scripts.dzip`, `compiledscripts.w2scripts`) and uses `.dzip` archives. How the
   camera, the projection and the render loop are driven, and whether a developer console exists
   (the exe contains the string `DebugConsole` `[inferred-static 2026-09-13]`), are the questions
   that matter for VR. CD Projekt Red's own official mod tools for this game are `[reported]` to
   exist; confirm, and whether they document the camera.
2. **The Cyberpunk 2077 VR work the user calls "impossible".** Identify which mod or mods that
   means (the user said "the latest"), who made them, and what they publicly explain about how
   stereo, head tracking, and first-person bodies and hands were achieved. Cyberpunk is a much later
   REDengine generation `[reported]`, so record which ideas are about the method (likely to carry
   over) and which are engine-specific (likely not) `[hypothesis]`.
3. **Any Witcher 2 or Witcher 3 VR prior art**, including generic drivers' profiles for either game,
   and whether their authors describe what the engine allowed.

## Reminder that applies here

Study is **online only**. Several VR mods in this space are closed or paid, and nothing gets
downloaded to look inside it. Take the publicly explained idea and credit it; the implementation
stays theirs. See the repo's `CONTRIBUTING.md`.

## Where the answers go

`external-research/INDEX.md` and `topics/` (the `/gr` lane creates both). Anything that answers a
question in `engine-research/ENGINE-DOSSIER.md` travels back as a file in
`engine-research/inbox/`.
