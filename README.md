# THE WORLD IN ONE DAY — TUESDAY 24 NOVEMBER 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Iyannn11/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Iyannn11/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page summing up the world's news of Tuesday 24 November 2026:
34 stories, 7 regions, one day — every story first reported 24 November 2026 (UTC).

## What the page shows

- **Lead:** Asia's markets roar back — Kospi +6.3% to 5,006, Nikkei +3.9%, Taiex +9.0%.
- **World map** with numbered pins 1–34 (tiny country flags beside each pin).
- **THE DAY IN UTC** strip: one real UTC time per story, in chronological order.
- **CONFLICT WATCH** panel: the 11 conflict/security stories (#6–16) under a single muted red accent.
- **34 story cards** grouped by region, each with its source; a green REPORTED pill on every verified story, an amber CLAIMED pill only on #14 (single-source claim), a blue TONIGHT pill on the Champions League (#28) with all five final scores.
- **DATE CHECK** footer naming the famous wrong-date stories deliberately left out (Puigdemont amnesty 23 Nov, Peru quake 20 Nov, CrowdStrike–Zscaler deal 23 Nov).

## How to run

```sh
python3 main.py
# writes output/entry.png (1024x1024 PNG, under 1 MiB)
```

`main.py` renders the page with `render.py` (Pillow only, no network) and writes
it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `./output/entry.png`). Running it
twice produces byte-identical output.
