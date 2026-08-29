#!/usr/bin/env node
/** Mechanical gate for H3705 infographics: 1080x1920, lang=ru, provenance, no TODOs. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const inf = path.join(root, "infographics");
const built = JSON.parse(
  fs.readFileSync(path.join(root, "scripts", "infographics50", "data", "built.json"), "utf8"),
);
let errors = 0;
for (const row of built) {
  const file = path.join(inf, row.slug, "index.html");
  if (!fs.existsSync(file)) {
    console.error("MISSING", row.slug);
    errors += 1;
    continue;
  }
  const t = fs.readFileSync(file, "utf8");
  const fails = [];
  if (!t.includes('lang="ru"')) fails.push("lang=ru");
  if (!t.includes("width:1080px") && !t.includes("width: 1080px")) fails.push("1080");
  if (!t.includes("height:1920px") && !t.includes("height: 1920px")) fails.push("1920");
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
console.log("check.mjs 0 errors on", built.length, "pages");
