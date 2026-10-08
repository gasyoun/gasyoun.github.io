#!/usr/bin/env node
/** H5744 b6 PNG render via Playwright. Uses the epic-infographics skill's
 *  node_modules when the repo has none, and Chrome channel when no bundled
 *  chromium exists (H5744). Missing playwright/chrome is a skip, not a fake PNG. */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const require_ = createRequire(import.meta.url);

function loadPlaywright() {
  const tries = ["playwright"];
  const skill = path.join(
    process.env.HOME ?? "", ".agents", "skills", "epic-infographics", "node_modules",
  );
  if (fs.existsSync(skill)) tries.push(path.join(skill, "playwright"));
  for (const t of tries) {
    try { return require_(t); } catch { /* next */ }
  }
  return null;
}

const playwright = loadPlaywright();
if (!playwright) {
  console.error("SKIP render_h5744.mjs: playwright not installed");
  process.exit(0);
}

const built = JSON.parse(
  fs.readFileSync(
    path.join(root, "scripts", "infographics50", "data", "h5744_built.json"), "utf8",
  ),
);
const browser = await playwright.chromium.launch({ channel: "chrome" });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
for (const row of built) {
  const htmlPath = path.join(root, "infographics", row.slug, "index.html");
  const pngPath = path.join(root, "infographics", row.slug, "infographic.png");
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle", timeout: 60000 });
  const el = await page.$(".canvas");
  if (!el) {
    console.error("NO .canvas", row.slug);
    continue;
  }
  await el.screenshot({ path: pngPath });
  console.log("png", row.slug);
}
await browser.close();
