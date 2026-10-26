# Research index

**Last `/gr` pass: 2026-10-26 — CHECK-IN.** Inbox empty; board unchanged since 10-16. One search for the view/projection row: a 2012 Helix Mod 3D Vision fix shows this renderer runs as a two-eye picture, and names what broke (flat shadows, a screen-locked HUD, a Steam launcher loop with its files in `bin`); one topic.

_Previous: **Last `/gr` pass: 2026-10-16 (estate sweep) — CHECK-IN.** Inbox empty. One search on the screen-blood `[PD]` row: no Witcher 2 mod found, but the sequel drives the effect from a script; topic written and pointed at the dossier._

_Previous: **Last `/gr` pass: 2026-10-04 (estate sweep) — CHECK-IN.** Inbox empty. Cross-project hand-off: the Steam wrapper can be removed from a copy without running the game (Alice's project did it), which would make the debug-console search desk work; pointer sent to the dossier._

_Previous: **Last `/gr` pass: 2026-09-29 (estate sweep) — CHECK-IN.** A Witcher 2 developer's blog says the engine had a network link through which the editor set the game camera (pose, near/far, FOV); retail survival unknown, one static check proposed; pointer sent to `engine-research/inbox/`._

_Previous: **Last `/gr` pass: 2026-09-23 (estate sweep) — CHECK-IN.** Checked phunkaeg's *VR Modding Playbook*: witcher3-vr and the Cyberpunk port are already tracked; nothing for REDengine 2._

_Previous: **Last `/gr` pass: 2026-09-17 (estate sweep) — FULL.** First pass on this project: folder bootstrapped, the modding lane's project-start hand-off drained, two topics written (REDengine VR prior art; the Witcher 2 script, console and camera routes), and a pointer to both sent to `engine-research/inbox/`._

Every research topic gathered for this project, newest first. Each row links to a self-contained
write-up in `topics/`. Status tags:

- 🆕 **new** — found, not yet acted on by the modding side.
- 👀 **looked at** — the modding side has read it; no verdict yet.
- ✅ **used / confirmed** — acted on, and it held.
- ❌ **dead end** — tried, and it did not work (kept so it is not re-proposed).

| Date | Topic | Status | Why it matters |
| --- | --- | --- | --- |
| 2026-10-26 | [A 2012 3D Vision fix says what breaks when the renderer is drawn twice](topics/2026-10-26-a-2012-3d-vision-fix-says-shadows-and-hud-break-in-stereo.md) | 🆕 | Shadows went flat and the HUD stuck to the screen under 3D Vision; both are checks for our first two-eye image. |
| 2026-10-16 | [The low-health screen effect is a script in The Witcher 3: look for the same in The Witcher 2](topics/2026-10-16-low-health-screen-effect-is-a-script-in-witcher-3.md) | 🆕 | The `[PD]` screen-blood row: points at the scripts our archive already replaces. |
| 2026-09-29 | [The Witcher 2 engine had a network link that let its editor drive the game camera](topics/2026-09-29-witcher-2-had-a-network-camera-link-to-its-editor.md) | ✅ | A second, engine-native camera route beside the scripts; one cheap static check (Winsock imports) keeps or retires it |
| 2026-09-17 | [The Witcher 2: readable scripts, official REDkit, camera mods, an unconfirmed console route](topics/2026-09-17-witcher-2-scripts-redkit-console-and-camera-mods.md) | 🆕 | Both `[PD]` board rows: Gibbed RED Tools opens `base_scripts.dzip`, and camera mods show the camera is script-reachable |
| 2026-09-17 | [REDengine VR prior art: the "impossible" Cyberpunk mod is the open-source CyberpunkVR Port](topics/2026-09-17-redengine-vr-prior-art-cyberpunk-port-and-witcher-3.md) | 🆕 | Answers the user's research wish: true two-view stereo via a second engine camera, with per-frame state shared between eyes |
