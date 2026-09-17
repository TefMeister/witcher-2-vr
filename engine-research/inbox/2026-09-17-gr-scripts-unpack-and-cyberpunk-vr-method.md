# From /gr: routes for both [PD] rows, and what the Cyberpunk VR mod teaches

**From:** `/gr` estate sweep, 2026-09-17. Full write-ups in `external-research/topics/`.

1. **Board row "open `CookedPC\base_scripts.dzip`":** Gibbed RED Tools unpack and repack `.dzip`, and
   CD PROJEKT RED's official REDkit for this game includes a script IDE and an uncook tool `[reported]`.
   Existing camera mods (Enhanced Camera, First Person Camera) work by editing that archive
   `[reported]`, so camera placement is likely script-reachable `[hypothesis]`.
   → `external-research/topics/2026-09-17-witcher-2-scripts-redkit-console-and-camera-mods.md`
2. **Board row "find how `CDebugConsole` opens":** no Witcher 2 method is public. The Witcher 3 uses
   `DBGConsoleOn=true` in `general.ini` `[reported]`; trying a similar key here is cheap but unproven
   `[hypothesis]`. Suggested dossier §4 note: "The Witcher 3's ini key is a candidate to try, not a
   known route."
3. **Stereo design (dossier §6/§7, when reached):** the CyberpunkVR Port (MIT) renders the second eye
   as a real second engine camera, and shares per-frame effects (shadow cascades, shader clock, wind)
   between eyes to avoid flicker `[reported]`. Its loader (RED4ext) does not exist for REDengine 1,
   but the method may carry `[hypothesis]`.
   → `external-research/topics/2026-09-17-redengine-vr-prior-art-cyberpunk-port-and-witcher-3.md`
