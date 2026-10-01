# Blender background crash on this macOS host

## Symptom

Direct Blender `--background` test runs on this host can exit with status 139 and
print `ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` from
`Arch_ValidateAssumptions`.

## Response

Do not repeat the same headless launch, switch Blender builds, or download another
runtime to work around it. Use an already-running Blender through its MCP/Python
execution channel. If that channel is unavailable, report the failed check and wait
until an interactive Blender runtime is available.
