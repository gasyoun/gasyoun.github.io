# ALLOW_PUBLISH_PUSH pre-push gate REMOVED — MG ruling 26-09-2026

_Created: 26-09-2026 · Last updated: 26-09-2026_

## Fact (destroy-work-if-missed class)

MG ruling, 26-09-2026, verbatim: «remove the allow push algo for all handoffs, it disturbs my work».

The `.githooks/pre-push` publish gate installed by H5181 (20-09-2026) — which blocked every
plain `git push` to this Pages repo behind `ALLOW_PUBLISH_PUSH=1` — is **DELETED**. It blocked
at least three legitimate publish flows in one week (H5507 hub sheets, H5509 eli5 page, and
MG's own manual pushes). Publishes to this repo are **no longer gate-blocked** for any
handoff or lane.

## What still applies (policy, not hook)

- The publish-safety-check contract (visibility, rights, secrets, personal data) remains the
  advisory standard — rights uncertainty is not a stop (standing policy 2026), confirmed
  prohibition / privacy / platform policy still block a publication on their own.
- Supersedes the gate half of H5181's guard-fuse wave; the memory note
  `automode-classifier-blocks-guard-narrowing-and-site-pushes` (claude-config org store)
  keeps its guard-narrowing half, loses the site-push half.

_Гасунс_
