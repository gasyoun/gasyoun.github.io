/* H8458 mechanical DoD gate — exit 0 iff all four facts hold on the working tree. */
const fs = require("fs");
const report = fs.readFileSync("console-popup-watch/report.html", "utf8");
const guide = fs.readFileSync("console-popup-watch/index.html", "utf8");
const fails = [];

// (1) dependency-free + MIT header
const body = report.replace(/<!--[\s\S]*?-->/g, "");
if (!/^<!DOCTYPE html>\s*<!--\s*\n?\s*MIT License/i.test(report)) fails.push("1a MIT header comment missing");
const ext = [];
// loaded-resource classes only; <a href> navigation anchors are exempt by contract
for (const m of body.matchAll(/<(script|img|iframe|embed|source|video|audio)[^>]*\ssrc=["']([^"']+)/gi)) {
  if (/^(https?:)?\/\/[^/]/i.test(m[2])) ext.push(`${m[1]} src: ${m[2]}`);
}
for (const m of body.matchAll(/<link[^>]*\shref=["']([^"']+)["'][^>]*>/gi)) {
  const tag = m[0];
  if (/^(https?:)?\/\/[^/]/i.test(m[1]) && !/rel=["'](nofollow|license|canonical)/i.test(tag) && !/href=["']data:/i.test(tag))
    ext.push("link href: " + m[1]);
}
for (const m of body.matchAll(/url\(\s*["']?([^"')]+)/gi)) {
  if (/^(https?:)?\/\/[^/]/i.test(m[1])) ext.push("css url(): " + m[1]);
}
for (const m of body.matchAll(/fetch\(\s*["'`]([^"'`]+)/g)) {
  if (/^https?:\/\//i.test(m[1])) ext.push("fetch:" + m[1]);
}
if (ext.length) fails.push("1b external resource refs: " + ext.join(","));
if (!/<link rel="icon" href="data:,">/.test(report)) fails.push("1c favicon suppressor missing");

// (2) Download-section link
const filesDiv = guide.match(/<div class="files">([\s\S]*?)<\/div>/);
if (!filesDiv || !/<a href="report.html">/.test(filesDiv[1])) fails.push("2 report.html link missing from .files div");
if (!/console_watch_cal\.py/.test(filesDiv ? filesDiv[1] : "")) fails.push("2b script links missing");

// (3) honesty gate: 0/0 -> inconclusive; PASS only under blind===true; count-driven warning
if (!/else if \(blind === true\) \{[\s\S]*?badge pass[\s\S]*?PASS — watcher not blind/.test(report))
  fails.push("3a PASS badge not guarded by blind===true");
if (!/else if \(bad === 0 && good === 0\) \{[\s\S]*?badge inconcl[\s\S]*?0\/0 — INCONCLUSIVE, never clean/.test(report))
  fails.push("3b 0/0 inconclusive branch missing");
if (!/0\/0 canary — inconclusive, never clean/.test(report)) fails.push("3c 0/0 blind-watch warning missing");

// (4) no-heartbeat warning
if (!/No heartbeat records in this watch — silence is not auditable/.test(report))
  fails.push("4 no-heartbeat warning missing");

if (fails.length) {
  console.error("H8458 DoD gate FAIL:\n- " + fails.join("\n- "));
  process.exit(1);
}
console.log("H8458 DoD gate: all 4 facts hold — exit 0");
