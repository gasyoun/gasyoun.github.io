# ADR 0001 — Publish the console-popup watcher as a self-contained page on gasyoun.github.io

_Created: 18-11-2026 · Status: accepted · Decided by: MG (grill round 18-11-2026), executed by GLM 5.3_

## Context

Eliminating a tooling-wide console-flash surface (1-second black windows on Windows, caused by console-subsystem children spawned from GUI/console-less parents) produced a reusable method and two small stdlib-only instruments: a window watcher with an A/B canary that proves it is not blind, and a three-place CRLF-normalized byte-match that proves a fix did not revert. Other Windows users have the same symptom and no cheap way to verify a repair. The estate already publishes public artifacts on the `gasyoun.github.io` static site (root-served from `master`, PR + auto-merge); a prior-art scan found no existing console-flash asset there.

## Decision

1. **Shape:** the kit plus a fix guide — not the toolkit alone and not the full estate incident report. The guide covers the confirmed patterns (Node `windowsHide`, Python `creationflags` / `STARTUPINFO`, PowerShell hidden launches / session-0 tasks, the `pythonw` probe rule) and the verification protocol (canary → ≥15-min interception with heartbeats → pre/post byte-match).
2. **Home:** a self-contained folder on `gasyoun.github.io` (`console-popup-watch/`), per the standing workspace rule that a one-off public deliverable is a site page, never a new repo. Org links point to the site, never to blob URLs.
3. **Licence:** MIT for the page and both scripts (code reuse is the point).
4. **Language:** English (the audience is “other Windows users” globally).
5. **Slug:** `console-popup-watch` — the wider name (console popups, not only “flashes”).
6. **Delivery:** the folder carries the runnable `.py` files (direct download links) beside the inline copy-paste blocks in `index.html`, plus a short `README.md`.

## Consequences

- The page and scripts become a public surface: fixes to the scripts must keep their receipts honest (the guide states the measurement discipline; the tooling stays dependency-free and read-only).
- The estate incident itself (handoff IDs, internal repo names, the S1–S7 verdict table) stays in the private hub; only the generic symptom → cure → verify chain is published.
- No personal data, secrets, or estate-private paths cross into the public folder (checked before PR under `/publish-safety-check`).

## Alternatives rejected

- **Separate repo** — violates the one-off-document rule and adds maintenance for two files.
- **Gist** — no page, no discoverability from org docs, and blob-style links are barred.
- **Toolkit without the fix guide** — a detector without the cure leaves the reader with a list of flashes and no next step.
- **Full sanitized incident report** — estate-specific (IDs, repos, dates) with low reuse value for an outside reader.
