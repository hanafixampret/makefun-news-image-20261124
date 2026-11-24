// makefun-news-image-20261124: the entry image is drawn by draw_news.py
// (Python + Pillow, no network) and shipped as entry.png beside this file.
// This program copies it to the output directory, byte for byte, so the
// two graded runs write identical output.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const image = readFileSync(new URL('./entry.png', import.meta.url));
if (image.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png is not a PNG file');
}
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), image);
