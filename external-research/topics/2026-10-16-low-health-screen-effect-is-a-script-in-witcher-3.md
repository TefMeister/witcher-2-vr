# The low-health screen effect is driven by a script in The Witcher 3: look for the same in The Witcher 2

**Found:** 2026-10-16 (`/gr`, estate sweep, check-in). **Status:** lead, not checked against The Witcher 2.

## What it is

No mod that removes The Witcher 2's low-health tint or screen blood turned up in one web search. The sequel's
mods show where such an effect can live, though: a Witcher 3 Nexus mod removes the flashing blood at the screen
edges at low health **by editing a game script, `lowHealth.ws`** `[reported]`, and a Witcher 3 "screen cleaning"
mod removes the on-screen blood spatter and red low-health corners as separate optional files `[reported]`.

## Why it matters here

The board's `[PD]` row asks what draws the low-health tint, damage flash and screen blood, since the `[Rendering]`
keys do not cover them. The Witcher 2's scripts are readable and our own `base_scripts.dzip` already loads
(2026-10-16), so if the Witcher 2 engine follows the same pattern, the effect is a script call that our archive can
switch off for VR only. This is an inference from the sequel `[hypothesis]`: REDengine 2 and 3 differ, and the
names will not match one to one.

## Next step

Search the unpacked Witcher 2 scripts for health-threshold and screen-effect calls (words like `lowHealth`,
`blood`, `ScreenEffect`, `Fullscreen`, `Vignette`, `damage`), then disable the one found in our archive and look.

## Sources

- Witcher 3 mod that removes the low-health blood edge effect by editing `lowHealth.ws`:
  <https://www.nexusmods.com/witcher3/mods/406>
- Witcher 3 next-gen screen-cleaning mod (blood spatter, low-health corners as optional files):
  <https://nexusmods.com/witcher3/mods/7233>
