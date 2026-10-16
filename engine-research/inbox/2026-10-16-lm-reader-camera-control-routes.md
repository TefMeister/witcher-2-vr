# Camera control routes: what script can set each frame, what is stubbed, and the native hook point

From: `/lm` static reader, 2026-10-16, on the Steamless-unpacked copy plus the unpacked `base_scripts.dzip`.
Natives were found through their registration (`mov [ebp-0x14], <impl>` beside the name string). The
method was checked on `IsCheatEnabled`, which resolved to the `0x00AA75D3` found earlier.
Helper: staging `witcher-2-vr/unpacked-exe-2026-10-16/native_of.py`.

## (a) Free camera is dead in retail

- **`theGame.EnableFreeCamera(flag)` → native `0x00AA7816` is a stub**: it reads the bool and returns
  `[inferred-static]`. That fits both live misses today (`-script "FreeCamera()"` and `FreeCamera()` over
  the console, n=1 each). `IsFreeCameraEnabled` (`0x00AA7838`) is real; it checks for a free-camera object
  (`0x00AA748F`), which nothing creates.
- **Whether `-script` fired is unknown**, because the command it ran is a no-op. The gate at `0x00B1FF61` needs:
  - the console object;
  - the armed flag;
  - a non-empty string;
  - a byte at `[[0x0160C6B0]+0x44]`;
  - a byte at `[[0x01404950]+0x4C]`, where `0x01404950` is the game object;
  - a non-zero result from that object's virtual `+0xB8`.

  The meaning of those three fields was not traced. Cheap live test: `-script "cameraSetFOV(40)"`.
- Also stubbed: script `Log()` (`0x0092F9F9`) and `IsCheatEnabled` (`0x00AA75D3`, always false).

## (b) Script routes that SET the camera, all natives real `[inferred-static]` unless marked

The gameplay camera `theCamera` (class `CCamera extends CEntity`) is an animated entity. Its view is a bone
of its own skeleton, driven by a behaviour graph. Yaw and pitch reach that graph as float variables.

| script call (exact signature) | native | what it really does |
|---|---|---|
| `theCamera.ResetRotationTo( smoothly : bool, horizontalAngle : float, optional verticalAngle : float, optional duration : float )` | `0x00A8F3FF` → `0x00A8EFE4` | ⭐ **absolute** yaw/pitch. Sets graph vars `cameraResetDuration`, `cameraLeftRightRotReset` = horizontalAngle minus a yaw read from the camera (`0x00423FD6` on `+0x70`), and `cameraUpDownRotReset` = verticalAngle. Raises a reset event per axis, choosing smooth or instant events by `smoothly`. Degrees `[hypothesis]` |
| `theCamera.Rotate( leftRightDelta, upDownDelta : float )` | `0x00A8F5B2` → `0x00A8F1B6` | sets `cameraLeftRightRot` / `cameraUpDownRot` = delta × a factor at `CCamera+0x138`. **Not added up**: these are per-frame rate inputs, like stick input. Does nothing while that factor is ≤ 0 |
| `theCamera.SetBehaviorVariable( varName : string, varValue : float ) : bool` | `0x00A87528` | writes any graph float directly: `cameraLeftRightRot`, `cameraUpDownRot`, `cameraLeftRightRotReset`, `cameraUpDownRotReset`, `cameraResetDuration`, `cameraFurther` (distance), `cameraUpDownMul`, `followHorizontal`, `cameraShakeStrength`, `cameraOffsetsSuppres` |
| `theCamera.SetBehaviorVectorVariable( varName : string, varValue : Vector ) : bool` | (entity) | vector graph variables; no camera names found in the scripts |
| `theCamera.RaiseEvent( eventName : name ) : bool` / `RaiseForceEvent` | `0x00A86801` / `0x00A867A8` | graph events, e.g. `'Camera_Interior'` |
| `theCamera.LookAtStatic( staticTarget : Vector, optional duration : float, optional activatingTime : float )` | `0x00A90A69` | aims at a world point; `LookAtDeactivation()` ends it |
| `theCamera.LookAt(...)`, `FocusOnStatic(...)`, `FocusOn(...)` | real | target-based aiming, not raw angles |
| `theCamera.SetFov( fov : float )` | `0x00A8F576` | **verified-live today** (`cameraSetFOV(40)`, n=1) |
| `theCamera.SetZoom( value : float )` | `0x00A8F53A` | zoom |
| `theCamera.TeleportWithRotation( position : Vector, rotation : EulerAngles )` / `Teleport( position : Vector )` | `0x00A857DC` / `0x00A8588B` | moves the camera ENTITY; the follow graph probably moves it back next frame `[hypothesis]` |
| `theCamera.Follow( dest : CEntity )`, `FollowWithRotation( dest : CEntity )` | `0x00A90C24` / `0x00A90BAC` | what the camera entity follows |
| `CComponent.SetRotation( rotation : EulerAngles )` / `SetPosition( position : Vector )` (local space) | `0x00A4E855` / `0x00A4E8AE` | via `theCamera.GetComponentByClassName('CCameraComponent')`: a local offset of the camera component. **Best head-tracking candidate** if the render view takes the component's transform rather than the bone `[hypothesis]` |
| `CStaticCamera.Run( flag : bool ) : bool`, `RunAndWait(...)` | not resolved | only for static cameras placed in levels |
| `exec camResetRotationTo( angle : float, dur : float )` | script | wraps ResetRotationTo |

**Suggested order for the yaw/pitch override test** (FLAT, over `w2console.py`, then in a script timer):

1. `camResetRotationTo(90, 0)`, or a timer calling `theCamera.ResetRotationTo(false, yaw, pitch, 0)` every
   frame. The smooth/instant semantics and the units are the open questions.
2. `theCamera.GetComponentByClassName('CCameraComponent').SetRotation(EulerAngles(pitch, yaw, roll))`
   as an offset on top of the gameplay camera.
3. Per-frame `SetBehaviorVariable("cameraLeftRightRot", rate)` as a rate drive (the mouse path).

## (c) Where the view comes from natively `[inferred-static]`

- `GetCameraMatrixWorldSpace` (`0x00A8EB47` → `0x00A8E9C2`) returns the **world matrix of one bone** of the
  camera's animated component. The bone index is at `CCamera+0x158`; the pose is read through the
  component's skeleton (`[comp+0xE0]`, virtual `+0x18`). The component comes from virtual `+0x18C`.
- The bone's rotation is written by **`CBehaviorGraphCameraControllerNode`** (vtable `0x00EABF34`):
  - Its sample routine **`0x00A13CED`** reads ONE float angle from the graph instance (offset at node
    `+0xC8`). It turns it to radians (× π/180, so the angle is in DEGREES), builds a quaternion about an
    axis (`0x00549FC0`), and multiplies it into the bone (index at node `+0xD0`).
  - Its update routine **`0x00A142E4`** integrates the inputs, calling `0x00423FD6` and `0x00A8F8CE`.
  - One node per axis is likely `[hypothesis]`.
- **Native fallback:** hook `0x00A13CED` and replace or add the angle (degrees) before the quaternion is
  built, or post-multiply the bone afterwards. A later hook on the render side (where `CCameraComponent`'s
  world matrix becomes the D3D9 view) was not located in this pass.
