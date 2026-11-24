# makefun-news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hanafixampret/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hanafixampret/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single image summing up the world news of Tuesday 24 November 2026,
drawn as a one-page newspaper front page: Jensen Huang returns as
Nvidia's chief executive and shares jump; the COP31 climate talks end
with no deal; a factory fire kills 24 in Indonesia; NATO sends
early-warning aircraft to Poland; fourteen are dead across the Kyiv
region and the war spills as far as Libya; and Gukesh opens his world
chess title defence in Geneva.

`draw_news.py` renders the page (Python + Pillow, no network, fully
deterministic) to `entry.png`. `main.ts` validates that image — whole
PNG, 1024×1024, under 1 MiB — and writes a copy to the output
directory, so both graded runs produce the same bytes.

## Run it

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
