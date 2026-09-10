#!/usr/bin/env node
/**
 * Records docs/promo/product-tour.html into an MP4 via Chrome screenshots + ffmpeg.
 * Uses realtime playback so CSS scene transitions animate correctly.
 */
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { readFile, mkdir, rm, writeFile, copyFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "../..");
const htmlPath = path.join(root, "docs/promo/product-tour.html");
const framesDir = path.join(root, "docs/promo/.frames");
const outMp4 = path.join(root, "docs/assets/videos/istocklink-product-tour.mp4");
const artifactMp4 = "/opt/cursor/artifacts/istocklink-product-tour.mp4";
const chromePath = process.env.CHROME_PATH || "/usr/local/bin/google-chrome";
const fps = Number(process.env.PROMO_FPS || 24);

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".woff2": "font/woff2",
};

function run(cmd, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: "inherit" });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`${cmd} exited with ${code}`));
    });
  });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function startStaticServer(dir) {
  const server = createServer(async (req, res) => {
    try {
      const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
      const filePath = path.join(dir, urlPath === "/" ? "index.html" : urlPath);
      if (!filePath.startsWith(dir)) {
        res.writeHead(403);
        res.end("Forbidden");
        return;
      }
      const data = await readFile(filePath);
      res.writeHead(200, {
        "Content-Type": MIME[path.extname(filePath)] || "application/octet-stream",
      });
      res.end(data);
    } catch {
      res.writeHead(404);
      res.end("Not found");
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  return { server, port: server.address().port };
}

async function main() {
  await mkdir(path.dirname(outMp4), { recursive: true });
  await mkdir(path.dirname(artifactMp4), { recursive: true });
  await rm(framesDir, { recursive: true, force: true });
  await mkdir(framesDir, { recursive: true });

  const promoDir = path.dirname(htmlPath);
  await writeFile(path.join(promoDir, "index.html"), await readFile(htmlPath));

  const { server, port } = await startStaticServer(promoDir);
  const url = `http://127.0.0.1:${port}/product-tour.html?play=1`;
  console.log("Serving", url);

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: "shell",
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--font-render-hinting=none",
      "--hide-scrollbars",
    ],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 },
  });

  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluateHandle("document.fonts.ready");
  await sleep(600);

  const total = await page.evaluate(() => window.__PROMO__.total);
  const frameCount = Math.ceil(total * fps);
  console.log(`Recording ${frameCount} frames @ ${fps}fps (${total.toFixed(1)}s wall-clock)`);

  const start = Date.now();
  for (let i = 0; i < frameCount; i++) {
    const targetMs = (i / fps) * 1000;
    const wait = targetMs - (Date.now() - start);
    if (wait > 1) await sleep(wait);

    const file = path.join(framesDir, `frame_${String(i).padStart(5, "0")}.png`);
    await page.screenshot({ path: file, type: "png", captureBeyondViewport: false });
    if (i % fps === 0) console.log(`  ${i}/${frameCount} (~${(i / fps).toFixed(1)}s)`);
  }

  await browser.close();
  server.close();

  console.log("Encoding MP4…");
  await run("ffmpeg", [
    "-y",
    "-framerate",
    String(fps),
    "-i",
    path.join(framesDir, "frame_%05d.png"),
    "-c:v",
    "libx264",
    "-pix_fmt",
    "yuv420p",
    "-crf",
    "18",
    "-preset",
    "medium",
    "-movflags",
    "+faststart",
    outMp4,
  ]);

  await copyFile(outMp4, artifactMp4);
  console.log("Wrote", outMp4);

  const previewDir = path.join(root, "docs/promo/stills");
  await mkdir(previewDir, { recursive: true });
  for (const sec of [0, 5, 15, 26, 38]) {
    const idx = Math.min(frameCount - 1, Math.floor(sec * fps));
    await copyFile(
      path.join(framesDir, `frame_${String(idx).padStart(5, "0")}.png`),
      path.join(previewDir, `still-${sec}s.png`)
    );
  }

  await rm(framesDir, { recursive: true, force: true });
  console.log("Done.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
