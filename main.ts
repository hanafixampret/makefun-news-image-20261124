// makefun news-image-20261124 — entrypoint (Node 22, standard library only).
//
// The front page itself is drawn at build time by draw_news.py and ships
// in this repository as entry.png. All this program does is check that
// image against the competition's limits, then place a copy of those
// bytes at $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png), so the
// two graded runs write identical output without any network.
//
// Run it with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const ONE_MIB = 1048576;

function loadEntryImage(): Buffer {
  const bytes = readFileSync(new URL("./entry.png", import.meta.url));
  if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error("entry.png is not a whole PNG file");
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width !== 1024 || height !== 1024) {
    throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
  }
  if (bytes.length > ONE_MIB) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  }
  return bytes;
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
const image = loadEntryImage();
writeFileSync(target, image);
console.log(`wrote ${image.length} bytes to ${target}`);
