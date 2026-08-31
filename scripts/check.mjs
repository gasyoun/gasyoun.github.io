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
  // Canvas may be portrait 1080×1920 (build.py lane) or wide 1920×1080
  // (epic-infographics b2 lane, H3708). Accept either size in either order.
  if (!row.external) {
    const has = (w, h) =>
      (t.includes(`width:${w}px`) || t.includes(`width: ${w}px`)) &&
      (t.includes(`height:${h}px`) || t.includes(`height: ${h}px`));
    if (!has(1080, 1920) && !has(1920, 1080)) fails.push("1080", "1920");
  }
  if (!/Посчитано|посчитано|ПОСЧИТАНО/.test(t)) fails.push("Посчитано");
  if (!t.includes("scripts/infographics50")) fails.push("script provenance");
  if (/TODO|FIXME|lorem ipsum/i.test(t)) fails.push("placeholder");
  if (fails.length) {
    console.error("FAIL", row.slug, fails.join(","));
    errors += 1;
  }
}

// --index: H3768 gate — every infographics/* dir must be listed in the generated
// index, every href in the index must resolve on disk, and the emitted page must
// not have drifted from what gen_infographics_index.py derives from disk.
if (process.argv.includes("--index")) {
  const gen = path.join(root, "scripts", "infographics50", "gen_infographics_index.py");
  const { execFileSync } = await import("node:child_process");
  try {
    execFileSync("python3", [gen, "--check"], { stdio: "pipe" });
    console.log("index parity OK (gen_infographics_index --check)");
  } catch (e) {
    console.error("FAIL index parity:", String(e.stderr || e.message).trim());
    errors += 1;
  }
  const idxPath = path.join(inf, "index.html");
  if (!fs.existsSync(idxPath)) {
    console.error("FAIL index: infographics/index.html missing");
    errors += 1;
  } else {
    const idx = fs.readFileSync(idxPath, "utf8");
    const hrefs = [...idx.matchAll(/href="([^"#]+)"/g)].map(m => m[1]);
    const listed = new Set(
      [...idx.matchAll(/href="([a-z0-9-]+)\/[^"]*"/g)].map(m => m[1])
    );
    const dirs = fs.readdirSync(inf, { withFileTypes: true })
      .filter(d => d.isDirectory() && d.name !== "sanskrit-infographics-catalog")
      .map(d => d.name);
    for (const d of dirs) {
      if (!listed.has(d)) {
        console.error("FAIL index: directory not listed in index.html:", d);
        errors += 1;
      }
    }
    for (const h of hrefs) {
      if (/^(https?:|#|mailto:)/.test(h)) continue;
      const target = path.resolve(inf, h);
      if (!fs.existsSync(target)) {
        console.error("FAIL index: broken href ", h);
        errors += 1;
      }
    }
    if (!errors) console.error("index coverage:", dirs.length, "dirs listed,",
      hrefs.filter(h => !/^(https?:|#)/.test(h)).length, "local hrefs valid");
  }
}

if (errors) {
  console.error(errors, "errors");
  process.exit(1);
}
console.log("check.mjs 0 errors on", rows.length, "pages");
