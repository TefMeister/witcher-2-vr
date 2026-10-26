# A 2012 3D Vision fix for The Witcher 2 says what breaks when its renderer is drawn twice

*For the `[PD]` row "where the renderer turns the camera bone into the D3D9 view and projection" (the place a
per-eye offset and projection would go), and for whoever plans the two-eye picture after it.*

## What was found

Helix Mod's blog has a post **"Witcher 2: Enhanced Edition"** (eqzitara, 20 April 2012), a shader-override package
for NVIDIA 3D Vision with a transparent HUD by **Artox**, installed into the game's `bin` folder (the same folder our
`d3d9` proxy uses). Its 27 comments, read online on 2026-10-26, say `[reported]`:

- In 3D Vision's automatic stereo the game's **shadows were drawn flat (2D)**; the fix's shader edits made them 3D
  (a 2014 comment).
- After alt-tab the shadows could go wrong again; nudging the depth one step (Ctrl+F3/F4) put them right (2018).
- The **HUD** stuck to the screen; a depth-placed HUD was tried and dropped (it looked bad in cut-scenes and clashed
  with other things), leaving only a see-through HUD, which made dialogue text and quick-time prompts harder to read.
- Convergence could not be changed in the game.
- With the fix installed, the **Steam version's launcher looped**, and a GOG user saw the logo flash and vanish
  (2015); the fix's original download link is dead, and bo3b pointed to a replacement copy on Helix Mod's storage.

## Why it matters here

- It is public evidence that this renderer runs as a two-eye picture once each eye gets its own shift, and it names
  the two places that went wrong: **shadows** (their maths assumed one camera, so they need the per-eye change too)
  and the **HUD** (screen-locked). Both are worth checking on our first two-eye image. Whether shadows will still need
  care when our per-eye change goes into the view and projection, rather than into shaders, is open `[hypothesis]`.
- The launcher loop is a warning for any DLL we put in `bin`: test the Steam launch path with our proxy installed
  (our first live session already ran with the proxy, so this is a watch item, not a blocker).
- Nothing here names the shader constants for view or projection; the package's files were not downloaded (we never
  download others' work to study it).

## Sources

- eqzitara and Artox, "Witcher 2: Enhanced Edition", Helix Mod blog, 2012-04-20, and its comments (bo3b among them) —
  https://helixmod.blogspot.com/2012/04/witcher-2-enhanced-edition.html
