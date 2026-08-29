#!/usr/bin/env node
/** PNG render via Playwright when installed. Missing playwright is a skip, not a fake PNG. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
let playwright;
try {
  playwright = await import("playwright");
} catch {
  console.error("SKIP render.mjs: playwright not installed");
  process.exit(0);
}

const built = JSON.parse(
  fs.readFileSync(path.join(root, "scripts", "infographics50", "data", "built.json"), "utf8"),
);
const browser = await playwright.chromium.launch();
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
