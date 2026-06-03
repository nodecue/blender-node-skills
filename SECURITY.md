# Security Policy

This package contains agent skill text and a small installer that copies bundled skills into a local skills directory. It does not require model provider API keys and should not read Blender files by itself.

## Installer Scope

The installer writes to:

```text
~/.codex/skills/<skill-name>
```

or to the directory passed with `--target`.

Use `--force` carefully because it replaces the destination skill directory. Review the target path before running the command.

## Do Not Share Secrets

When opening issues, do not include:

- API keys;
- private asset-library paths;
- unreleasable `.blend` files;
- private prompts or readback JSON containing studio/project data.

Redact sensitive details before sharing screenshots, readback snippets, or agent traces.

## Reporting Security Issues

If you find a security issue in the installer or package contents, open a GitHub issue with minimal public detail and say that you have a private security report available.

Useful safe details:

- package version or commit;
- operating system;
- install command used;
- target directory shape without private path details;
- short non-sensitive summary.
