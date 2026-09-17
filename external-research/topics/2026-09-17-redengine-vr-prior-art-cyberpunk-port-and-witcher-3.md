# REDengine VR prior art: the "impossible" Cyberpunk 2077 mod is the open-source CyberpunkVR Port

**Status:** 🆕 new · **Priority:** high — it answers the user's own research wish from the project's
first day, and it separates the ideas that can carry back to The Witcher 2 from those that cannot.

## Which mod the user meant

Three Cyberpunk 2077 VR efforts are public. The one that matches "all sorts of impossible things" is
the **CyberpunkVR Port** by **dariulone** (MIT licence, on GitHub and Nexus Mods) `[reported]`:
6DoF OpenXR head tracking, real stereo, full-body IK with motion-controlled hands, physical reload,
motion melee, holsters, and driving with your own hands on the wheel `[reported]`.

The other two, for context:
- **Luke Ross's R.E.A.L. VR** (alternate-eye rendering, no motion controls). CD PROJEKT sent a
  takedown over it, and Road to VR (2026-03-11) reports that the objection was the **paywall**
  (a Patreon subscription), not VR modding itself; his re-released free suite leaves Cyberpunk out
  `[reported]`. Useful for our own policy: CD PROJEKT's stated line is "no paywall", which free
  releases already meet.
- **Cyberpunk2077-VR-OpenSource** by **pinducoding** (RED4ext + OpenXR), with controllers mapped to
  gamepad buttons and no motion aiming yet `[reported]`.

## How the CyberpunkVR Port does it, from its public README

- **True two-view stereo, not alternate-eye:** the second eye is a real engine view, a
  render-to-texture camera on the player entity that runs the frame graph for its own eye, from its
  own position, with its own projection `[reported]`.
- **Hooks through RED4ext**, the native plugin loader for REDengine 4. Views are identified by the
  virtual camera's name hash, and the submitted frustum matches the engine-rendered geometry on both
  axes, including off-axis lens correction for headsets like Quest 3 `[reported]`.
- **Per-frame state shared between the eyes:** sun shadow cascades, the shader clock, foliage wind
  and the reflection march are computed once and reused, which is what stops shadows blinking and
  foliage jittering between eyes `[reported]`.
- Full-body IK with arm-length calibration; hand poses for reloading, driving and melee `[reported]`.

## What carries to The Witcher 2, and what does not

- ❌ **Engine-specific, does not carry:** RED4ext and redscript exist only for REDengine 4. The
  Witcher 2 is REDengine 1, 32-bit, Direct3D 9 (dossier §2–4), with no equivalent loader.
- ✅ **Method, likely carries** `[hypothesis]`: (1) drive the second eye as a *second engine camera*
  rather than duplicating draw calls, if the static pass can find how `CCamera` / `CCameraComponent`
  register a view; (2) whatever gets stereo, compute per-frame effects once and share them between
  eyes (shadows, time, wind), or they will flicker; (3) identify views by a stable name or ID, not by
  guessing from draw order.
- **The Witcher 3 is the closer sibling** (REDengine 3). **witcher3-vr** by **tig3rmast3r** (MIT)
  takes the other route: it hooks Direct3D 12 with MinHook and offers alternate-eye, full stereo and
  mono modes, with a design it says was informed by REFramework and UEVR `[reported]`. **vorpX** has a
  Witcher 3 profile with its own connection mod; its geometry 3D has shadow problems and its
  depth-based 3D works `[reported]`.
- No Witcher 2 VR prior art turned up in this pass. That was an automated search only, so it is not a
  negative `[hypothesis]`.

## Next step it unlocks

Read the CyberpunkVR Port's architecture notes online when designing the stereo approach, and credit
it. Nothing is downloaded or copied: study the explanation, write our own code.

## Sources

- https://github.com/dariulone/cyberpunk-vr-port
- https://github.com/pinducoding/Cyberpunk2077-VR-OpenSource
- https://roadtovr.com/luke-ross-vr-mods-free-cyberpunk-2077/
- https://github.com/tig3rmast3r/witcher3-vr
- https://www.vorpx.com/forums/topic/witcher-3-got-a-brand-new-first-person-mod-this-time-for-real/
