// Rendert docs/og.html nach docs/og.png (1200x630). Braucht Playwright + Chromium.
// Wird von scripts/build_de_page.py aufgerufen; manuell: node scripts/render_og.js
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const docs = path.resolve(__dirname, "..", "docs");
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto("file://" + path.join(docs, "og.html"));
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(docs, "og.png") });
  await b.close();
  console.log("docs/og.png gerendert");
})().catch((e) => { console.error("og.png nicht gerendert:", e.message); process.exit(1); });
