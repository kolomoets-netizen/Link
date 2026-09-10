#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { readFile, mkdir, rm, copyFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "../..");
const screensDir = path.join(root, "docs/promo/screens");
const outDir = path.join(root, "docs/promo/screenshots");
const artifactDir = "/opt/cursor/artifacts/screens";
const chromePath = process.env.CHROME_PATH || "/usr/local/bin/google-chrome";

const SCREENS = [
  "01-needs",
  "02-purchase-requests",
  "03-approval-flow",
  "04-requests",
  "05-compare-offers",
  "06-products",
  "07-counterparties",
  "08-qualification",
  "09-evaluation",
  "10-receiving",
  "11-tenders-board",
  "12-tenders-feed",
];

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
};

async function startServer(dir) {
  const server = createServer(async (req, res) => {
    try {
      const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
      const filePath = path.join(dir, urlPath === "/" ? "index.html" : urlPath);
      if (!filePath.startsWith(dir)) {
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
  // Ensure HTML is built
  await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(__dirname, "build-screens.mjs")], { stdio: "inherit" });
    child.on("close", (c) => (c === 0 ? resolve() : reject(new Error("build failed"))));
  });

  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });
  await mkdir(artifactDir, { recursive: true });

  const { server, port } = await startServer(screensDir);
  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: "shell",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
    defaultViewport: { width: 1440, height: 900, deviceScaleFactor: 2 },
  });

  const page = await browser.newPage();
  for (const name of SCREENS) {
    const url = `http://127.0.0.1:${port}/${name}.html`;
    console.log("Capture", name);
    await page.goto(url, { waitUntil: "networkidle0", timeout: 60000 });
    await new Promise((r) => setTimeout(r, 200));
    const file = path.join(outDir, `${name}.png`);
    await page.screenshot({ path: file, type: "png", captureBeyondViewport: false });
    await copyFile(file, path.join(artifactDir, `${name}.png`));
  }

  await browser.close();
  server.close();
  console.log("Screenshots:", outDir);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
