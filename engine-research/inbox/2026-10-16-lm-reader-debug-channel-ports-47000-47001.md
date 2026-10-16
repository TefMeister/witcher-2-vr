# The engine listens on TCP 47000 and 47001 for its debug channel (console commands, script debugger)

From: `/lm` static reader, 2026-10-16, on the Steamless-unpacked copy. Answers the board's `[FLAT]` row on
the editor network lead (the `netstat` check can now confirm a specific prediction).

- `witcher2.exe` reaches `bind`/`listen`/`accept` from two places `[inferred-static]`:
  1. **The engine's debug-channel server.** `0x00B0CA6A` makes a TCP socket bound to INADDR_ANY (all
     interfaces) on a given port, `listen` backlog 1. Its only callers (`0x00B19D84`, `0x00B19D9E`) pass the
     hard-coded ports **47000 (`0xB798`) and 47001 (`0xB799`)**. `0x00B19BFA` accepts and services them each
     tick. The server is a lazily created singleton (`0x004094C2`), created the first time an
     `IDebugChannelReciever` registers — and `CDebugConsole` registers at start-up, so the ports should
     open on every normal launch `[hypothesis]`. Receivers include `CDebugConsole` (packet `ConsoleCommand`
     runs a console command) and `CScriptDebugger`.
  2. **Havok's `hkBsdSocket::listen`** (`0x00553D60`, vtable `0x00CD5240`) — the Havok Visual Debugger
     path; the `-vdb` switch that might enable it is dead in retail, so it probably never listens
     `[hypothesis]`. FMOD's `fmod_event_net.dll` is a separate DLL, not part of this count.
- **Live check (FLAT):** with the game at the menu, `netstat -ano | findstr 4700` — expect LISTENING on
  `0.0.0.0:47000` and `0.0.0.0:47001` owned by witcher2.exe. If so, sending a `ConsoleCommand` packet is a
  remote console with no exe patch; the packet framing is the next static job (`0x00B0CB41` receive path,
  `0x00AA353D` reads the string with `0x00B0C82A`).
- ⚠️ Listening on all interfaces means other machines on the LAN could reach it while the game runs.
