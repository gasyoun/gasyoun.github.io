/** PNG render for a slug subset: node scripts/render_slugs.mjs slug1 slug2 ...
 * Same pipeline as render.mjs (1080x1920 .canvas shot via Playwright).
 * Playwright resolves from NODE_PATH; missing playwright is a skip, not a fake PNG. */
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(""), process.cwd());
let playwright;
try {
  playwright = await import("playwright");
} catch {
  console.error("SKIP render_slugs.mjs: playwright not installed (set NODE_PATH)");
  process.exit(0);
}
const slugs = process.argv.slice(2);
if (!slugs.length) {
  console.error("usage: node scripts/render_slugs.mjs <slug-2026-08-29> ...");
  process.exit(1);
}
const browser = await playwright.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
for (const slug of slugs) {
  const dir = path.join(root, "infographics", slug);
  const htmlPath = path.join(dir, "index.html");
  if (!fs.existsSync(htmlPath)) {
    console.error("MISSING", slug);
    continue;
  }
  const pngPath = path.join(dir, "infographic.png");
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle", timeout: 60000 });
  const el = await page.$(".canvas");
  if (!el) { console.error("NO .canvas", slug); continue; }
  await el.screenshot({ path: pngPath });
  console.log("png", slug);
}
await browser.close();
