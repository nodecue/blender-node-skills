# A node group with no user is dropped on save

## Symptom

An agent builds a Geometry Nodes group, verifies it on a temporary object, removes
that object, and saves. Live readback and a grader that inspects the running
Blender both pass. Reopening the saved `.blend` shows no node group at all.

Observed on Blender 5.2.2 in the 2026-10-01 distance-to-silhouette paired pilot
(without-skill arm): the saved file contained only the camera.

## Cause

Removing the last modifier that referenced the group leaves it with zero users.
Blender does not write zero-user datablocks unless they carry a fake user.

## Response

- Before saving, keep a real user or set `use_fake_user = True` on the group.
- Confirm with `scripts/verify_result.py`: `persistence.survives_save` must be true,
  and `GROUP_NOT_SAVED` must be absent.
- Graders and acceptance checks must reopen the saved file, not inspect the live
  session, or this failure passes as success.
