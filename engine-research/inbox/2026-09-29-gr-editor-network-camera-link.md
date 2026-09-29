# /gr → modding: Witcher 2's editor could drive the game camera over the network

From: `/gr` estate sweep, 2026-09-29. For the `[PD]` console/debug-menu row and the camera rows.

Full write-up: `external-research/topics/2026-09-29-witcher-2-had-a-network-camera-link-to-its-editor.md`.

- A Witcher 2 graphics programmer's 2014 blog post says the engine carried a custom network command
  protocol (on the script debugger's connection) through which the editor set the game camera's
  position, rotation, near/far and FOV `[reported]`. Retail survival is not stated.
- Cheap static check: does `witcher2.exe` import Winsock `bind`/`listen`/`accept`, and are there listener
  strings near the script-debugger code? No imports = retire the lead `[hypothesis]`.
