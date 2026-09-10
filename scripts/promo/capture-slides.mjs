#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { readFile, mkdir, rm, copyFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "../..");
const slidesDir = path.join(root, "docs/promo/slides");
const pngDir = path.join(slidesDir, "png");
const artDir = "/opt/cursor/artifacts/slides";
const chromePath = process.env.CHROME_PATH || "/usr/local/bin/google-chrome";

const SLIDES = [
  "00-teaser-chaos",
  "01-teaser-demand",
  "02-teaser-cycle",
  "03-phrase-needs",
  "04-ui-needs",
  "05-phrase-approval",
  "06-ui-approval",
  "07-phrase-requests",
  "08-ui-compare",
  "09-phrase-products",
  "10-ui-products",
  "11-phrase-suppliers",
  "12-ui-suppliers",
  "13-phrase-warehouse",
  "14-ui-receiving",
  "15-phrase-tenders",
  "16-ui-tenders",
  "17-outro",
];

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
};

function runNode(script) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [script], { stdio: "inherit" });
    child.on("close", (c) => (c === 0 ? resolve() : reject(new Error("build failed"))));
  });
}

async function startServer() {
  // Serve docs/promo so slides + screenshots resolve
  const base = path.join(root, "docs/promo");
  const server = createServer(async (req, res) => {
    try {
      const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
      const filePath = path.join(base, urlPath === "/" ? "slides/index.html" : urlPath);
      if (!filePath.startsWith(base)) {
        res.writeHead(403);
        return res.end("Forbidden");
      }
      const data = await readFile(filePath);
      res.writeHead(200, { "Content-Type": MIME[path.extname(filePath)] || "application/octet-stream" });
      res.end(data);
    } catch {
      res.writeHead(404);
      res.end("Not found");
    }
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  return { server, port: server.address().port };
}

async function main() {
  await runNode(path.join(__dirname, "build-slides.mjs"));
  await rm(pngDir, { recursive: true, force: true });
  await mkdir(pngDir, { recursive: true });
  await mkdir(artDir, { recursive: true });

  const { server, port } = await startServer();
  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: "shell",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 },
  });
  const page = await browser.newPage();

  for (const name of SLIDES) {
    const url = `http://127.0.0.1:${port}/slides/${name}.html`;
    console.log("Capture", name);
    await page.goto(url, { waitUntil: "networkidle0", timeout: 60000 });
    await page.evaluateHandle("document.fonts.ready");
    await new Promise((r) => setTimeout(r, 150));
    const file = path.join(pngDir, `${name}.png`);
    await page.screenshot({ path: file, type: "png", captureBeyondViewport: false });
    await copyFile(file, path.join(artDir, `${name}.png`));
  }

  await browser.close();
  server.close();
  console.log("PNG →", pngDir);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
