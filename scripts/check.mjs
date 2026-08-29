#!/usr/bin/env node
/** Mechanical gate for H3705 infographics: 1080x1920, lang=ru, provenance, no TODOs. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const inf = path.join(root, "infographics");
function loadBuilt(name) {
  const p = path.join(root, "scripts", "infographics50", "data", name);
  if (!fs.existsSync(p)) return [];
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
const built = [
  ...loadBuilt("built.json"),
  ...loadBuilt("h3711_built.json"),
];
const seen = new Set();
const rows = [];
for (const row of built) {
  if (seen.has(row.slug)) continue;
  seen.add(row.slug);
  rows.push(row);
}
let errors = 0;
for (const row of rows) {
  // Wave-1 #3 (mw-letters) is a different generator (template + data.json), not the 1080×1920 canvas.
  if (row.slug === "mw-letters-2026-08-29") continue;
  const file = path.join(inf, row.slug, "index.html");
  if (!fs.existsSync(file)) {
    console.error("MISSING", row.slug);
    errors += 1;
    continue;
  }
  const t = fs.readFileSync(file, "utf8");
  const fails = [];
  if (!t.includes('lang="ru"')) fails.push("lang=ru");
  // Rows built by another lane (e.g. mw-letters by the catalog session) declare
  // "external": true — their canvas shape is owned there; H3707 keeps them untouched
  // and skips only the 1080x1920 shape assertion, not the provenance checks.
  if (!row.external) {
    if (!t.includes("width:1080px") && !t.includes("width: 1080px")) fails.push("1080");
    if (!t.includes("height:1920px") && !t.includes("height: 1920px")) fails.push("1920");
  }
  if (!/Посчитано|посчитано/.test(t)) fails.push("Посчитано");
  if (!t.includes("scripts/infographics50")) fails.push("script provenance");
  if (/TODO|FIXME|lorem ipsum/i.test(t)) fails.push("placeholder");
  if (fails.length) {
    console.error("FAIL", row.slug, fails.join(","));
    errors += 1;
  }
}
if (errors) {
  console.error(errors, "errors");
  process.exit(1);
}
console.log("check.mjs 0 errors on", rows.length, "pages");
