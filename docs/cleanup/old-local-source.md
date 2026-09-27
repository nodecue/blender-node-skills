# Cleanup manifest: old local checkout

Non-destructive. This document does not authorize deletion, rename, move, or
modification of the old local development checkout.

Public GitHub `main` is now the product and development source. The old
checkout remains a preserved archive candidate. It contains historical,
private, and development-only material. It is not a second authority.

## What may be archived later

After a later explicit authorization:

- Inventory ignored and untracked material in the old checkout before any zip
  or archive.
- Uniquely needed private evidence, manual corpora, and development
  verification tools may be preserved in an appropriate private location.
- Credentials, API keys, tokens, and transient machine artifacts must be
  excluded from the archive and handled securely. Do not keep them in the
  zip.
- The remaining working tree may then be zipped or otherwise archived
  offline.
- Historical process notes that described a second local product tree may go
  with that archive.

Do not copy changes from that checkout back into public `main`
automatically. Do not treat it as a source to reconcile.

## What must be retained (separately, as appropriate)

Preserve outside public git, in an appropriate private location as needed:

- Uniquely needed private historical evidence and session records that must
  not be published.
- Manual corpora and unpublished manuals.
- Development verification tools that were never part of the public
  maintenance path.

Public git already owns the shipped skill, plugin packaging, node dumps, TSV
generator, pytest suite, and governance docs. Those stay on public `main`.

## What this document does not do

- It does not delete, empty, or relocate the old checkout.
- It does not instruct an agent to modify that checkout.
- It does not restore a second product source.
- It does not close Issue #10; merge and issue close are separate later
  actions.

A later issue may authorize an actual archive or removal. Until then, leave
the old checkout in place.
